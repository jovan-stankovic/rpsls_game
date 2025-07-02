# Rock Paper Scissors Lizard Spock Game

## Overview

This project integrates both the backend and frontend for the Rock Paper Scissors Lizard Spock game using FastAPI, PostgreSQL, and React. It provides a cohesive service that allows users to play against the computer, manage choices, view a scoreboard, and enjoy a streamlined web interface.

## Features

- **Interactive Gameplay**: Choose from Rock, Paper, Scissors, Lizard, or Spock to challenge the computer.
- **Random Choice Generation**: Utilizes an external API to generate random selections for the computer.
- **Scoreboard Display**: Keeps track of the last 10 game results and offers a reset option.
- **Integrated Experience**: The frontend and backend function together to deliver a smooth user experience.

## Setup & Installation

1. **Clone the Repository**:
```bash
git clone https://github.com/jovan-stankovic/rpsls_game.git
cd rpsls_game
mv .env.example .env
docker-compose up
```
## Access the Game:
Navigate to http://localhost:5000 in your browser to start playing the game.

## Playing the Game
- Select a move (Rock, Paper, Scissors, Lizard, or Spock) and play against the computer.
- View instant results on the interface.
- Viewing the Scoreboard
- Access the scoreboard to review the results of the latest 10 games.
- Resetting the Scoreboard
- Clear game history effortlessly through the reset option provided.

## Technologies Used
- **FastAPI**
- **PostgreSQL**
- **React**
- **Docker Compose**

## Contact
For further inquiries or support, please contact [jovan.stankovic993@example.com](mailto:jovan.stankovic993@example.com).
