import socket
import threading
import time
from game_logic import ShapeFactory, PlayerState

class GameServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('127.0.0.1', 8000))
        self.server.listen(2)
        self.clients = []
        self.player_states = {}
        self.is_running = True
        self.game_duration = 60
        self.start_time = time.time()
        self.last_stamina_recovery = time.time()
        self.last_stress = time.time()

    def broadcast(self, message):
        # sending messeages such as SPAWN NEW , ... for different actions
        for client in self.clients:
            try:
                client.send(str.encode(message))
            except:
                pass

    def send_specific_update(self, conn, player_id):
        # sending specific updates for each player seperately
        p = self.player_states[player_id]
        time_left = max(0, int(self.game_duration - (time.time() - self.start_time)))
        frozen_status = 1 if time.time() < p.frozen_until else 0
        msg = f"UPDATE:{p.score}|{p.stamina}|{p.stress}|{time_left}|{frozen_status}|{player_id}"
        try:
            conn.send(str.encode(msg))
        except:
            pass

    def handle_client(self, conn, player_id):
        self.player_states[player_id] = PlayerState()
        conn.send(str.encode(f"ID:{player_id}"))
        
        while self.is_running:
            try:
                data = conn.recv(1024).decode()
                if not data:
                    break
                
                p = self.player_states[player_id]

                now_for_stress = time.time()

                # ignore click if player is frozen or stamina is below 10
                if time.time() < p.frozen_until or p.stamina <= 10:
                    continue

                if data.startswith("CLICK"):
                    # data structure --> CLICK:score:shape_name
                    parts = data.split(":")
                    score = int(parts[1])
                    shape_name = parts[2]

                    if shape_name == "Shield":
                        p.shield_until = time.time() + 5

                    is_shielded = time.time() < p.shield_until

                    p.stamina -= 10            # stamina decreases with every click
                    
                    final_score = score

                    if score < 0:
                        if is_shielded:
                            final_score = 0
                            print(f"Player {player_id} protected by Shield! No penalty.")
                        else:
                            final_score = score 
                    if p.stamina >= 90:
                        final_score = score * 2
                        if score < 0:
                            if is_shielded:
                                final_score = 0
                                print(f"Player {player_id} protected by Shield! No penalty.")
                            else: 
                                final_score = score // 2
                        if now_for_stress - self.last_stress >= 2:
                            p.stress = max(0, p.stress - 5)

                    self.last_stress = now_for_stress
                    p.score += final_score

                    if shape_name == "Empty":
                        p.stress += 5
                    elif score < 0:
                        p.stress += 30
                    elif score > 0 and score < 3: 
                        p.stress += 10
                    elif score == 6:
                        p.stress += 5
                    if score > 0: 
                        p.stress = max(0, p.stress - 5)

                    if shape_name == "Ice":
                        opponent_id = 1 - player_id
                        if opponent_id in self.player_states:
                            self.player_states[opponent_id].frozen_until = time.time() + 3
                            print(f"Player {player_id} is FROZEN !")

                    self.send_specific_update(conn, player_id)
                    self.broadcast("SPAWN_NEW")
                
                else:
                    p.stress += 5
            
            except Exception as e:
                print(f"Error handling client {player_id}: {e}")
                break
        conn.close()

    def start(self):
        print("Server started... Waiting for 2 players")
        while len(self.clients) < 2:
            conn, addr = self.server.accept()
            player_id = len(self.clients)
            self.clients.append(conn)
            threading.Thread(target=self.handle_client, args = (conn, player_id), daemon = True).start()
            print(f"Player {player_id} joined!")

        while self.is_running:
            time.sleep(3) 
        
            now = time.time()
            for pid, p in self.player_states.items():
                # increase stamina (10 percrnt every 2 seconds)
                if now - self.last_stamina_recovery >= 2:
                    if p.stamina < 100:
                        p.stamina = min(100, p.stamina + 10)
                        p.stress = max(0, p.stress - 5)
                
            self.broadcast("SPAWN_NEW")
            
            # check for game over
            if now - self.start_time > self.game_duration:
                self.is_running = False
                p0 = self.player_states[0].score
                p1 = self.player_states[1].score
                winner = "Player 0 Wins!" if p0 > p1 else "Player 1 Wins!"
                print(winner)
                self.broadcast(f"GAME_OVER,{winner}")
                conn.close()
        self.last_stamina_recovery = now

if __name__ == "__main__":
    server = GameServer()
    server.start()
