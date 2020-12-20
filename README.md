# American Checkers - AI (WIP)

This repository hosts the American Checkers game built using Python.

  ![Checkers Board](https://github.com/nikeshsraj10/checkers-ai/blob/main/images/board.PNG)
## Rules:
Open [rules.md](./rules.md) to view the rules of the game


## Python Version 

3.8.6

## Setup
  Python version: 3.0+
  ### Libraries
  - [Numpy](https://numpy.org/install/)
  - [Torch](https://pytorch.org/)
  - [Matplotlib](https://matplotlib.org/3.3.3/users/installing.html)

  ### Sample Installation commands <Open the above link to find appropriate command depending on your OS & PackageManager
  Run: `pip install numpy` <br/>
  Run: `pip install matplotlib` <br/>
  Run: `pip install torch==1.7.1+cpu torchvision==0.8.2+cpu torchaudio===0.7.2 -f https://download.pytorch.org/whl/torch_stable.html`

## How to play?

Clone the repository by using the URL: `https://github.com/nikeshsraj10/checkers-ai.git`

CD into the game directory: `cd checkers-ai`

### To play against our AI:
Run: `python .\src\main.py`<br/>
You'll have the option to play against an AI or another Human or watch two AI play <br/>
Run the above command to know more <br/>

### Simulate MCTS AI vs Baseline AI
To Configure the board and number of games use the below command <br/>
Run: `python .\src\bot_simulate.py {board_config} {number_of_games}` <br/>
Valid values for board_config are 8 & 10 <br/> <br/>
The following command will run 8x8 board for 50 games <br/>
Run: `python .\src\bot_simulate.py 8 50` <br/>

### Simulate MCTS + NN AI vs MCTS AI
To Configure the board and number of games use the below command <br/>
Run: `python .\src\treenn_vs_tree.py {board_config} {number_of_games}` <br/>
Valid values for board_config are 8 & 10 <br/> <br/>
The following command will run 8x8 board for 50 games <br/>
Run: `python .\src\treenn_vs_tree.py 8 50` <br/>

### View data and performance

Run: `cd plots` to check out the plots and the saved data from our simulation <br/>
View Plots:  [Plots](/plots)


