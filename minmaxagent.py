from exceptions import AgentException
import copy
import random


class MinMaxAgent:
    def __init__(self, my_token='x'):
        self.my_token = my_token
        self.opponent_token = 'o' if my_token == 'x' else 'x'

    def evaluate_board(self, connect4):
        if connect4.check_winner() == self.my_token:
            return 1
        elif connect4.check_winner() == self.opponent_token:
            return -1
        else:
            return 0

    def minmax(self, connect4, depth, is_maximizing):
        score = self.evaluate_board(connect4)
        if score == 1 or score == -1 or not connect4.possible_drops() or depth == 0:
            return score

        if is_maximizing:
            best_score = -float('inf')
            for col in connect4.possible_drops():
                new_game = copy.deepcopy(connect4)
                original_who_moves = new_game.who_moves
                new_game.who_moves = self.my_token
                new_game.drop_token(col)
                new_game.who_moves = original_who_moves
                score = self.minmax(new_game, depth - 1, False)
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for col in connect4.possible_drops():
                new_game = copy.deepcopy(connect4)
                original_who_moves = new_game.who_moves
                new_game.who_moves = self.opponent_token
                new_game.drop_token(col)
                new_game.who_moves = original_who_moves
                score = self.minmax(new_game, depth - 1, True)
                best_score = min(best_score, score)
            return best_score

    def decide(self, connect4):
        best_score = -float('inf')
        best_moves = []

        for col in connect4.possible_drops():
            new_game = copy.deepcopy(connect4)
            new_game.drop_token(col)
            score = self.minmax(new_game, 4, True)
            if score > best_score:
                best_score = score
                best_moves = [col]
            elif score == best_score:
                best_moves.append(col)

        if best_moves:
            return random.choice(best_moves)
        else:
            return None

