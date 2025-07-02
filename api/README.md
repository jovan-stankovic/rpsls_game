# Rock Paper Scissors Lizard Spock Game Backend

## Overview

This project implements a game service for Rock Paper Scissors Lizard Spock using FastAPI and PostgreSQL. The service provides endpoints to play against a computer, manage choices, and maintain a scoreboard.

## Endpoints

### GET /choices
- Returns all possible choices.

### GET /choice
- Returns a random choice using an external random number API.

### POST /play
- Submit your choice to play against the computer. Returns the result.

### GET /scoreboard
- Fetch the latest 10 results.

### POST /scoreboard/reset
- Reset the scoreboard.
