import import_ipynb
from BoardState import StateBoard
import chess.pgn
import numpy as np
import os
import pandas as pd
def generate_training_dataset(num_games=None):
    
    df = pd.DataFrame(columns=["Bit Board", "Result"])
    index = 0
    
    game_num = 0
    result_vals = {'1/2-1/2':0, '0-1': -1, '1-0': 1}
    
    for file in os.listdir("GameData"):
        
        parsed_pgn = open(os.path.join("GameData", file))
        
        while True:
            
            game = chess.pgn.read_game(parsed_pgn)
            
            if game is None:
                break

            result = game.headers['Result']
            if result not in result_vals:
                continue
            aBoard = game.board()
            res_val = result_vals[result]

            for move in game.mainline_moves():
                aBoard.push(move)
                bitBoard = StateBoard(aBoard).serialize()

                df.loc[index] = [bitBoard, res_val]
                index += 1
                
            print("parsing game", game_num, "Examples", len(df.index))
            
            if num_games is not None and len(df.index) > num_games:
                return df

            game_num += 1
            
    return df
dataset_modern_10kExample = generate_training_dataset(num_games = 10000)
dataset_modern_10kExample.loc[0]
