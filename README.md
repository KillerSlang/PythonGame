# PythonGame

## Overview

PythonGame is an interactive game built using Python and Pygame. The game involves character selection, navigating through a grid-based world, encountering enemies, and engaging in battles. Players can collect items, use strategies, and progress through increasingly challenging levels.

## Features

- **Character Selection**: Choose from three unique characters: Gunner, Swordman, or Warlock, each with distinct stats and abilities.
- **Grid-Based Exploration**: Navigate through a procedurally generated grid world with random shapes and challenges.
- **Enemy Encounters**: Engage in battles with enemies of varying difficulty based on progression.
- **Item Collection**: Collect items like Health Potions, Damage Boosts, and more to aid in battles.
- **Dynamic Battles**: Use character-specific attacks and strategies to defeat enemies or escape.
- **Tutorial**: A step-by-step tutorial introduces players to the game's mechanics.

## Prerequisites

Before running the game, ensure you have the following installed on your system:

1. **Python 3.x**: Download and install Python from [python.org](https://www.python.org/downloads/).
2. **Pygame**: Install Pygame using pip.
3. **Tkinter**: Tkinter is usually included with Python, but if not, you can install it using your package manager.

## Installation

To install the required packages, run the following commands:

```bash
pip install pygame
pip install python-tk
```

## Running the Game

1. **Start the Game**: Run the `Main.py` file to start the game.
   ```bash
   python Main.py
   ```
2. **Character Selection**: Choose your character by clicking on one of the character buttons.
3. **Navigate the World**: Use the arrow keys to navigate through the grid-based world and encounter enemies.
4. **Battle Enemies**: Engage in battles using character-specific attacks and strategies.
5. **Collect Items**: Collect items to enhance your abilities and improve your chances of winning battles.

## Game Mechanics

### Characters

Each character has unique stats:

- **Gunner**: Health: 100, Attack: 55, Defense: 35
- **Swordman**: Health: 120, Attack: 40, Defense: 40
- **Warlock**: Health: 80, Attack: 70, Defense: 20

### Items

Items can be collected during exploration and used in battles:

- **Health Potion**: Restores health.
- **Damage Boost**: Increases attack damage.
- **Weaken Potion**: Reduces enemy attack damage.
- **Speed Potion**: Skips enemy's turn.
- **Accuracy Potion**: Increases attack accuracy.

### Battles

- Battles are turn-based and involve selecting attacks with varying damage and accuracy.
- Enemies have their own attacks and can block or recover health.
- Players can attempt to escape battles, but success is not guaranteed.

### Grid Exploration

- The world is procedurally generated with random shapes and challenges.
- Cells can contain enemies, items, or special objectives.
- Winning battles clears cells, while escaping marks them as "Runaway."

### Tutorial

The game includes a tutorial to guide players through the mechanics:

- **TAB Key**: Displays attack stats during battles.
- **Health Bar**: Shows enemy health during battles.
- **Escape Button**: Explains how to exit battles.

## File Descriptions

- **Main.py**: The main entry point of the game. Displays the start screen and launches the character selection screen.
- **CharacterSelect.py**: Handles character selection and displays character stats.
- **Game.py**: Manages the world map, player navigation, and procedural grid generation.
- **EnemyEncounter.py**: Handles enemy encounters, battles, and item usage.
- **Tutorial.py**: Provides a step-by-step tutorial for new players.

## Notes

- Ensure all image files are in the correct directory as referenced in the code.
- The game uses command-line arguments to pass character names, enemy counters, and inventory between scripts.
- The game is designed for single-player mode.

## Enjoy the Game!

Explore, battle, and strategize your way to victory in PythonGame!
