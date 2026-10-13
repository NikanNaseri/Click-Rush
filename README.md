# 🎮 ClickRush — Multiplayer Reaction Game

ClickRush is a real-time, two-player reaction game developed in Python. Players compete to achieve the highest score by clicking randomly appearing shapes before the game timer runs out.

The game combines reaction speed, accuracy, and strategic decision-making with unique mechanics such as stamina, stress, shields, and freezing opponents.

## ✨ Features

- **Real-Time Multiplayer:** Two players compete in the same game session.
- **Client-Server Architecture:** Uses TCP sockets to communicate between the game server and clients.
- **Graphical User Interface:** Built with Python's Tkinter library.
- **Random Shape Generation:** Different shapes appear with varying scores and effects.
- **Scoring System:** Earn points from positive shapes and lose points by clicking negative ones.
- **Stamina System:** Players manage their stamina throughout the game.
- **Stress System:** Player actions affect stress levels, adding another layer of strategy.
- **Power-Ups:**
  - 🛡️ **Shield:** Temporarily protects players from negative scoring penalties.
  - ❄️ **Ice:** Freezes the opponent for a short period.
- **Timed Matches:** Each game runs for a limited duration.
- **Concurrent Processing:** Uses Python threading to handle client connections and server communication.

## 🛠️ Technologies Used

- **Python 3**
- **Tkinter** — Graphical user interface
- **Socket Programming** — TCP client-server communication
- **Threading** — Concurrent client handling
- **Object-Oriented Programming (OOP)** — Classes and game logic
- **Random** — Randomized shape generation

## 📂 Project Structure

```text
ClickRush/
├── client.py
├── server.py
├── game_logic.py
└── README.md
```

### File Descriptions

- `client.py` — Implements the game window, player interface, shape rendering, and communication with the server.
- `server.py` — Manages player connections, scores, stamina, stress, power-ups, and match timing.
- `game_logic.py` — Defines game objects, shape generation, and player state.

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Tkinter (usually included with standard Python installations)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/NikanNaseri/Click-Rush
   ```

2. Navigate to the project directory:

   ```bash
   cd ClickRush
   ```

### Running the Game

**Step 1 — Start the server**

Open a terminal and run:

```bash
python server.py
```

The server will wait for two players to connect.

**Step 2 — Start the first client**

Open another terminal and run:

```bash
python client.py
```

**Step 3 — Start the second client**

Open a third terminal and run:

```bash
python client.py
```

Both clients connect to the server, and the match begins.

> **Note:** The current implementation connects to `127.0.0.1` on port `8000`, so both clients and the server are intended to run on the same computer by default.

## 🎯 How to Play

1. Start the server and connect two players.
2. Watch for shapes that appear in the game window.
3. Click a shape to submit your action and update your score.
4. Avoid negative-score shapes and empty-space clicks.
5. Use power-ups strategically to protect yourself or disrupt your opponent.
6. Manage your stamina and stress while competing.
7. The player with the higher score at the end of the match wins.

## 🧠 Game Mechanics

### Scoring

- Positive shapes award points.
- Negative shapes reduce the player's score.
- Clicking empty space increases stress.
- Scoring and penalties can be affected by the player's stamina and shield status.

### Stamina

Stamina decreases when a player clicks and gradually recovers during the game. Low stamina can prevent a player from performing actions.

### Stress

Stress changes according to player actions and can influence gameplay, including the appearance of illusionary shapes.

### Power-Ups

- **Shield:** Protects against negative scoring penalties for a limited time.
- **Ice:** Temporarily freezes the opponent.

## 🏗️ Architecture

ClickRush follows a simple client-server architecture:

- **Server:** Maintains player states, processes actions, calculates scores, and manages the match.
- **Client:** Displays the game interface, renders shapes, receives player input, and communicates with the server.
- **Game Logic:** Defines reusable classes for shapes and player state.

## 🎓 Project Goals

This project was developed to practice:

- Object-Oriented Programming (OOP)
- TCP socket communication
- Multithreading and concurrent connections
- GUI development with Tkinter
- Real-time game state management
- Basic game mechanics and scoring systems

## 🔮 Future Improvements

- Support for remote players over a local network or the internet.
- Improved synchronization of game events between clients.
- A lobby system for creating and joining matches.
- Match replay and spectator modes.
- Enhanced graphics, animations, and sound effects.
- Improved network error handling and reconnection support.
- More robust validation of player actions.

## 📄 License

No license has been specified yet. Add a license file if you want to define how others may use, modify, and distribute this project.
