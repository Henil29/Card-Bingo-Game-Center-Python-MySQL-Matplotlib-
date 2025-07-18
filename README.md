# Card & Bingo Game Center 🎮

This is a terminal-based multiplayer game application built in Python that includes two games: a Card Game and Bingo. It uses MySQL for data persistence and Matplotlib for visualizing game stats.

## 🚀 Features

- Multiplayer support (up to 4 players)
- Two game modes: Card Game and Bingo
- Smart suggestions during gameplay (e.g., which card to keep)
- Game history tracking in MySQL
- Visual analytics with Matplotlib (bar, line, pie, scatter charts)
- CLI-based interactive game center

## 🛠️ Tech Stack

- **Language:** Python  
- **Database:** MySQL  
- **Libraries:** `mysql-connector-python`, `matplotlib`, `numpy`

## 🧾 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
````

### `requirements.txt`

```
mysql-connector-python
matplotlib
numpy
```

## 🧱 Database Schema

Import the following into your MySQL database:

```sql
CREATE DATABASE IF NOT EXISTS game;

USE game;

CREATE TABLE IF NOT EXISTS card_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    winner VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS card_winning_count (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player VARCHAR(50),
    count INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS bingo_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    winner VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS bingo_winning_count (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player VARCHAR(50),
    count INT DEFAULT 0
);
```

## ▶️ How to Run

```bash
python game.py
```

Follow on-screen instructions to select and play games.

## 📊 Graphs Included

* Bar Chart
* Scatter Plot
* Line Graph
* Pie Chart
* Combined Multi-Chart View

## 🧑‍💻 Author

Henil Patel
GitHub: [Henil29](https://github.com/Henil29)

---

Enjoy the game and feel free to contribute!

```

---

### 🔧 Fixes Applied:
- Removed extra closing triple-backtick at the end (`\`\`\``).
- Fixed malformed code blocks and `<details>` that were accidentally left in.
- Made bullet formatting consistent.

---

You're now good to go! Let me know if you want:
- `requirements.txt` file
- `schema.sql` file  
I'll give them in ready-to-copy or downloadable format.
```
