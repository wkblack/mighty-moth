########################################################################
# Mighty Moth 
# Tic-Tac-Toe solver 

########################################################################
# import statements 
import numpy as np

########################################################################
# helper functions 

def check_board(board,mark="x"):
    " given `board`, check whether `mark` has won. "
    bool_board = np.array(board) == mark
    report = False # default return
    rows = np.any(np.sum(bool_board,axis=0)==3)
    cols = np.any(np.sum(bool_board,axis=1)==3)
    diag1 = np.sum(np.diag(bool_board))==3
    diag2 = np.sum(np.diag(np.fliplr(bool_board)))==3
    return int(rows + cols + diag1 + diag2) # return ways to win


def test_move(board,x,y,mark='x'):
    " check whether marking a given (x,y) move on a board would win "
    test = np.copy(board)
    test[x,y] = mark
    return check_board(test,mark)


def can_move(x,y,board):
    " check whether a given space is available "
    return board[x][y] == 'empty'


def open_moves(board):
    " check which moves are currently available "
    options = []
    for x in range(3):
        for y in range(3):
            if can_move(x,y,board):
                options += [[x,y]]
    return np.array(options)


def test_options(board,mark='x'):
    " check various options "
    options = open_moves(board)
    results = np.array([test_move(board,t[0],t[1],mark) \
                        for t in options])
    return options, results


def check_turn(board):
    " check which symbol's turn it is, given a board "
    if np.sum(np.array(board) != 'empty') % 2 == 0:
        return 'x'
    else: 
        return 'o'


def opposite_symbol(symbol):
    if symbol == 'x':
        return 'o'
    elif symbol == 'o':
        return 'x'
    else:
        return symbol


########################################################################
# main body 

class TicTacToeBot:
    def __init__(self, config):
        # 👇 Get started by uncommenting this line
        print("Mighty Moth, making mischeif!", config)
        self.symbol = config['player']
    
    def move(self, board):
        if can_move(1,1,board): # try for center
            return {"x":1,"y":1}
        
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # check whether any moves could win me the game
        options,results = test_options(board,self.symbol)
        if np.any(results > 0): # there's a way to win; take it. 
            idx = np.flip(np.argsort(results))[0]
            return {"x":options[idx][0], "y":options[idx][1]}
        
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # check for and prevent potential enemy wins
        enemy = opposite_symbol(self.symbol)
        options,results = test_options(board,enemy)
        if np.any(results > 0): # prevent enemy win
            idx = np.flip(np.argsort(results))[0]
            return {"x":options[idx][0], "y":options[idx][1]}
        
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # try for corners 
        for ii in [0,2]:
            for jj in [0,2]:
                if can_move(ii,jj,board):
                    return {"x": ii, "y": jj}
        
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # catch-all ending clause: 
        # put in random left over legal spot
        for ii in range(3):
            for jj in range(3):
                if can_move(ii,jj,board):
                    return {"x": ii, "y": jj}

