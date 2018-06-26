# pip3 install python-chess


import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from ChessGame import ChessGame


import sys

#all the potential playesr
player1 = HumanPlayer()
player2 = RandomAI()
player3 = MinimaxAI(4)
player4 = AlphaBetaAI(3)

#starting the game with correct players
game = ChessGame(player1, player4)

#keeping the game going
while not game.is_game_over():
    print(game)
    game.make_move()

