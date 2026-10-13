import socket
import threading
import tkinter as tk
import random
from game_logic import ShapeFactory, GameObject

class GameClient:
    def __init__(self, host = '127.0.0.1', port = 8000):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        
        self.player_id = None
        self.current_shape = None
        self.stamina = 100
        self.stress = 0
        
        self.root = tk.Tk()
        self.root.title(f"Game Client")
        
        self.canvas = tk.Canvas(self.root, width = 400, height = 400, bg = "white")
        self.canvas.pack()

        self.id_label = tk.Label(self.root, text = "player 0", font = ("Arial", 10))
        self.id_label.pack()
        
        self.score_label = tk.Label(self.root, text = "Score: 0", font = ("Arial", 12))
        self.score_label.pack()

        self.status_label = tk.Label(self.root, text = "Stamina: 100 | Stress: 0 | Time: 60", font = ("Arial", 10))
        self.status_label.pack()

        self.msg_label = tk.Label(self.root, text = "", fg = "red", font = ("Arial", 12, "bold"))
        self.msg_label.pack()

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        threading.Thread(target=self.listen_to_server, daemon = True).start()

    def listen_to_server(self):
        while True:
            try:
                data = self.client.recv(1024).decode()
                if not data:
                    break
                
                if data.startswith("ID:"):
                    self.player_id = int(data.split(":")[1])
                
                elif data == "SPAWN_NEW":
                    self.root.after(0, self.draw_new_shape)
                
                elif data.startswith("GAME_OVER"):
                    winner = data.split(",")[1]
                    self.root.after(0, lambda: self.msg_label.config(text = f"GAME OVER\n{winner}", fg = "red"))
                    self.client.close()
                    
                elif data.startswith("UPDATE:"):
                    parts = data.split(":")[1].split("|")
                    self.root.after(0, lambda p = parts: self.update_ui(p))
                    
            except Exception as e:
                print(f"Error: {e}")
                break

    def update_ui(self, parts):
        score, stamina, stress, time_left, frozen, id = parts
        self.score = int(score)
        self.stamina = int(stamina)
        self.stress = int(stress)

        self.id_label.config(text = f"Player {id}")
        self.score_label.config(text = f"Score: {score}")
        self.status_label.config(text = f"Stamina: {stamina} | Stress: {stress} | Time: {time_left}")
        if frozen == "1":
            self.msg_label.config(text = "FROZEN! ❄️", fg = "blue")
        else:
            self.msg_label.config(text = "")

    def draw_new_shape(self):
        self.canvas.delete("all")
        
        # now showing random objects when 10 < stamina < 40
        if 10 <= self.stamina <= 40:
            if random.random() < 0.5:
                self.current_shape = None
                return
            
        new_shape = ShapeFactory.create_shape()
    
        if self.stress >= 50 and self.stress < 70:
            if random.random() < 0.3:
                new_shape = GameObject("Illusion", 0, "pink", 3, is_illusion = True)
        elif self.stress >= 70:
            if random.random() < 0.6:
                new_shape = GameObject("Illusion", 0, "pink", 3, is_illusion = True)

        self.current_shape = new_shape
        s = self.current_shape
        
        fill_color = s.color
        if self.stress >= 70 and s.is_illusion:
             fill_color = "purple" 

        self.canvas.create_oval(s.x, s.y, s.x + 40, s.y + 40, fill = fill_color, outline = "black", width = 2)

    def on_canvas_click(self, event):
        if self.current_shape:
            s = self.current_shape
            if s.x <= event.x <= s.x + 40 and s.y <= event.y <= s.y + 40:
                msg = f"CLICK:{s.score}:{s.name}"
                self.client.send(str.encode(msg))
            else:
                self.client.send(str.encode("CLICK:0:Empty:0"))
        else:
            self.client.send(str.encode("CLICK:0:Empty:0"))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    client = GameClient()
    client.run()
