# Data

## Game Data
This folder contains all the saved game data and trained NN models <br/>
Game data files are named as follows: data_<board_config>_<num_of_pawns>_<num_of_games_trained>.pkl <br/>
i.e. File data_8_12_50.pkl contains game data for a 8x8 board with 12 pawns per player, trained for 50games. <br/>


## NN Models
NN Models files are names as follows: model<board_config>_<num_of_pawns>_<num_of_games_trained>_<version_num || ''>.pth <br/>
i.e. File model_8_12_50.pkl contains trained NN model using  data file for a 8x8 board with 12 pawns per player, trained for 50games using v1 NN architecture.<br/>

The NN architectures are defined in `checkers_net.py`

