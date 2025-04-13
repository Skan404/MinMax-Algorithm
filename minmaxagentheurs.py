import copy
import random


class MinMaxAgentHeurs:
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

    def heuristic_evaluate(self, connect4):
        my_advantage = 0.0
        opponent_advantage = 0.0

        center_column = connect4.width // 2

        for row in range(connect4.height):
            for col in range(connect4.width):
                column_advantage = 0.05 - (0.01 * abs(center_column - col))
                if connect4.board[row][col] == self.my_token:
                    my_advantage += column_advantage
                elif connect4.board[row][col] == self.opponent_token:
                    opponent_advantage += column_advantage

        my_advantage += self.count_three_in_a_row(connect4, self.my_token) * 0.1
        opponent_advantage += self.count_three_in_a_row(connect4, self.opponent_token) * 0.1

        block_opportunity_score = self.evaluate_block_opportunities(connect4, self.opponent_token)
        my_advantage += block_opportunity_score * 0.1

        return my_advantage - opponent_advantage

    def evaluate_block_opportunities(self, connect4, token):
        block_count = 0
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        for row in range(connect4.height):
            for col in range(connect4.width):
                for dx, dy in directions:
                    if self.check_line_for_block(connect4, row, col, dx, dy, token) >= 2:
                        block_count += 1
        return block_count

    def check_line_for_block(self, connect4, row, col, dx, dy, token):
        sequence_length = 0
        for i in range(1, 3):
            new_row, new_col = row + i * dy, col + i * dx
            if 0 <= new_row < connect4.height and 0 <= new_col < connect4.width:
                if connect4.board[new_row][new_col] == token:
                    sequence_length += 1
                else:
                    break
        return sequence_length

    def count_three_in_a_row(self, connect4, token):
        count = 0
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        for row in range(connect4.height):
            for col in range(connect4.width):
                for dx, dy in directions:
                    if self.check_line(connect4, row, col, dx, dy, token) == 3:
                        count += 1
        return count

    def check_line(self, connect4, row, col, dx, dy, token):
        count = 0
        for i in range(3):
            new_row, new_col = row + i * dy, col + i * dx
            if 0 <= new_row < connect4.height and 0 <= new_col < connect4.width and connect4.board[new_row][
                new_col] == token:
                count += 1
            else:
                break
        return count

    def minmax(self, connect4, depth, is_maximizing):
        score = self.evaluate_board(connect4)
        if score == 1 or score == -1 or depth == 0:
            if depth == 0:
                return self.heuristic_evaluate(connect4)
            return score

        if not connect4.possible_drops():
            return 0

        if is_maximizing:
            max_eval = -float('inf')
            for col in connect4.possible_drops():
                new_game = copy.deepcopy(connect4)
                new_game.drop_token(col)
                score = self.minmax(new_game, depth - 1, False)
                max_eval = max(max_eval, score)
            return max_eval
        else:
            min_eval = float('inf')
            for col in connect4.possible_drops():
                new_game = copy.deepcopy(connect4)
                new_game.drop_token(col)
                score = self.minmax(new_game, depth - 1, True)
                min_eval = min(min_eval, score)
            return min_eval

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
