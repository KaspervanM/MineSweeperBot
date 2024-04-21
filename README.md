# MineSweeper Bot

This is a bot that plays the game of MineSweeper. It uses a simple algorithm to play the game. The bot is written in
Python and uses the PyAutoGUI, Pillow and Pynput libraries to interact with the game.

## How to use

1. Install the required libraries using the following command: `pip install numpy pyautogui pillow pynput`.
2. Open the game of MineSweeper and start a new game.
3. (Temporary for now) Change the values of field_width, field_height and num_mines in the main.py file to match the
   values of the game of MineSweeper that you are playing.
4. Run the bot using the following command: `python main.py`.
5. Click in the top left corner of the game of MineSweeper, just outside the minefield. Again, in the bottom right
   corner of the game of MineSweeper, just outside the minefield. This is to calibrate the area in which the bot will
   play the game.
6. The bot will start playing the game. To stop the bot, press the space bar. When pressing the space bar again, the bot
   will restart and resume playing the game.

## How it works

The bot uses a simple algorithm to play the game. It starts by initializing a 2D array of size field_width x 
field_height of unknown cells, each with the same probability of being a mine equal to the # of mines over the # of
cells. Then, it reads the state of the game on the screen and updates the cells that are known to contain the number of
cells around them that are mines. The bot then calculates the probability of each cell being a mine based on the
information it has and chooses the cell with the lowest probability to click on. If the bot is unsure of which cell to
click on, it will click on a random cell with the lowest probability.

### Probability calculation

The probability of an unknown cell being a mine is calculated as follows:

1. If the cell has no known cells around it, the probability is the number of mines to be found over the number of 
   unknown cells left.
2. If the cell already has probability 1, the probability remains 1.
3. If the cell has known cells around it, the probability is the number of mines around the cell minus the number of
   known mines around the cell over the number of unknown cells around the cell.
4. For each probability from each of the known cells around the cell, the probability is the highest of the calculated
   values. However, if any contain 0, the probability is 0.

Unknown cells with a probability of 1 are considered to be mines.

## Known Limitations

I as a person have one strategy that this bot doesn't yet have. When I get stuck, I try to find contradictions. With
that, I mean that I look for cells that I could place a flag on and walk through the implications of that flag. If I
find a contradiction, I know that the flag is wrong and I can safely reveal that cell. This bot doesn't yet have that
capability, and I am unsure of how I intend to implement it.
