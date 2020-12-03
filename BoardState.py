import chess
import numpy as np
class StateBoard():
    
    def __init__(self, board=None):
        
        if board is None:
            self.board = chess.Board()
        else:
            self.board = board
            
        self.BOARD_SIZE = 64
        
        self.serial_vals = {'P': 1, 'N': 2, 'B': 3, 'R': 4, 'Q': 5, 'K': 6,
                       'p': 11, 'n': 12, 'b': 13, 'r': 14, 'q': 16, 'k': 17}
        
    def serialize(self):
        
        assert self.board.is_valid() == True
        
        state = np.zeros(self.BOARD_SIZE,dtype=np.uint8)
        
        for i in range(self.BOARD_SIZE):
            
            aPiece = self.board.piece_at(i)
            
            if aPiece is not None:
                
                state[i] = self.serial_vals[aPiece.symbol()]
                
        if self.board.has_kingside_castling_rights(chess.WHITE):
            assert state[chess.H1] == self.serial_vals['R']
            state[chess.H1] = 28
        if self.board.has_queenside_castling_rights(chess.WHITE):
            assert state[chess.A1] == self.serial_vals['R']
            state[chess.A1] = 21
        if self.board.has_kingside_castling_rights(chess.BLACK):
            assert state[chess.H8] == self.serial_vals['r']
            state[chess.H8] = 38
        if self.board.has_queenside_castling_rights(chess.BLACK):
            assert state[chess.A8] == self.serial_vals['r']
            state[chess.H8] = 31
        
        if self.board.ep_square is not None:
            assert state[self.board.ep_square] == 0
            state[self.board.ep_square] = 41
        
        state = state.reshape(8,8)
        
        binary_state = np.zeros((5,8,8))
        
        binary_state[0] = (state>>3)&1
        binary_state[1] = (state>>2)&1
        binary_state[2] = (state>>1)&1
        binary_state[3] = (state>>0)&1
        binary_state[4] = (self.board.turn*1.0)
        
        return binary_state
    
    def moves(self):
        
        return list(self.board.legal_moves)
        
        
    def state_features(self):
        
        feature_list = [self.board.board_fen(),self.board.turn, self.board.castling_rights, self.board.ep_square]
    
        return info_list
print(StateBoard().serialize())
