# Bots-Game
A programming game about bots competing against each other

This repository is an improved version of the original project
[Bots Game](https://github.com/Cogno-Marco/Bots-Game) made by
[Cogno-Marco](https://github.com/Cogno-Marco)

Instead of playing using CMD and `.txt` files, you are going to play using a GUI
made in [Dear PyGui](https://github.com/hoffstadt/DearPyGui) and Python

![](images/main_game.png)


### Objective

The objective of this game is to code your bot and fight against another bot.


### Game Rules

To win the game, you have to do one of this:
- Have more resource than the enemy after 1000 turns;
- Destroy the enemy.

The resources are always 10, they have 3 HP. When you destroy a resource, you get 6 points.
You can spend points:
- creating new troops => it costs 5 points;
- power-up your troops => it costs 3 points.

On your troop, you can power-up health, movement speed or damage (+1).

A single troop, can move, attack or power-up, you can attack enemies or resources.


### Syntax Rule

- If you want to play the game, you have to put your code in the same folder as the `main.py` file (outside of `src/`).

- Your file have to start with `bot_` (Examples: `bot_test.py`, `bot_my_first_bot.py`, `bot_resource_collector.py`, etc.).

- Use the snake case convention to name your file.

### Installing

To install and play the game, simply execute the command `pip install -r requirements.txt`

### TODO

- At the end of the game, show bots' statistics like:
  - Trend of resources (graph)
  - Eliminated troops and resources
  - Top troops (kills, resources obtained, etc.)
- Tooltip of the troops and resources, showing its stats
- General graphic improvement
