from exceptions import GameplayException
from connect4 import Connect4
from randomagent import RandomAgent
from alphabetaagent import AlphaBetaAgent
from minmaxagentheurs import MinMaxAgentHeurs
from minmaxagent import MinMaxAgent

connect4 = Connect4(width=7, height=6)
agent1 = MinMaxAgentHeurs('o')
agent2 = MinMaxAgent('x')
while not connect4.game_over:
    connect4.draw()
    try:
        if connect4.who_moves == agent1.my_token:
            n_column = agent1.decide(connect4)
        else:
            n_column = agent2.decide(connect4)
        connect4.drop_token(n_column)
    except (ValueError, GameplayException):
        print('invalid move')

connect4.draw()
