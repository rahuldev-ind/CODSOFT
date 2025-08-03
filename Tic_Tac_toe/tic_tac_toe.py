import math

class TicTacToe:
    def __init__(self):
        #Initializes the Tic-Tac-Toe game board and the winner."""
        self.board = [' ' for _ in range(9)]  # A list to represent the 3x3 board
        self.current_winner = None  # Keep track of the winner

    def print_board(self):
        #Prints the current state of the board.
        print("")
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')
        print("")

    @staticmethod
    def print_board_nums():
        #Prints the board with numbers indicating the position to choose.
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        print("")
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')
        print("")

    def make_move(self, square, letter):
        """
        makes a move on the board if the square is available.
        Returns True if the move is successful, False otherwise.
        """
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.is_winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def is_winner(self, square, letter):
        # Checks if the recent move resulted in a win.
        # Check the row
        row_index = square // 3
        row = self.board[row_index*3 : (row_index + 1) * 3]
        if all([spot == letter for spot in row]):
            return True

        # Check the column
        col_index = square % 3
        column = [self.board[col_index + i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        # Check diagonals (only if the move is on an even-numbered square)
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]  # Top-left to bottom-right
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]  # Top-right to bottom-left
            if all([spot == letter for spot in diagonal2]):
                return True

        return False

    def empty_squares(self):
        #Returns a list of indices of the empty squares.
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def num_empty_squares(self):
        #Returns the number of empty squares.....
        return len(self.empty_squares())

class Player:
    #A base class for a player…
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass

class HumanPlayer(Player):
    #A class for a human player…
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-8): ')
            try:
                val = int(square)
                if val not in game.empty_squares():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Please try again.')
        return val

class AIPlayer(Player):
    #An unbeatable AI player using Minimax with Alpha-Beta Pruning.....
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        #Gets the best possible move for the AI…
        if len(game.empty_squares()) == 9:
            # For the first move, choose a random square for variety.
            return 4 # Start in the center for optimal play
        else:
            # Get the best move using the minimax algorithm
            return self.minimax(game, self.letter)['position']

    def minimax(self, state, player, alpha=-math.inf, beta=math.inf):

        max_player = self.letter  # The AI
        other_player = 'O' if player == 'X' else 'X'

        # Base cases: check for a terminal state (win, lose, tie)
        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)}
        elif state.num_empty_squares() == 0:
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}  # Maximize score
        else:
            best = {'position': None, 'score': math.inf}   # Minimize score

        for possible_move in state.empty_squares():
            # Make a move and recurse
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player, alpha, beta)

            # Undo the move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
                alpha = max(alpha, best['score'])
                if beta <= alpha:
                    break # Prune the branch
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
                beta = min(beta, best['score'])
                if beta <= alpha:
                    break # Prune the branch

        return best

def play_game(game, x_player, o_player, print_game=True):
    #Function to run the game loop…
    if print_game:
        game.print_board_nums()

    letter = 'X'  # Starting letter
    while game.empty_squares():
        if letter == 'O':
            move = o_player.get_move(game)
        else:
            move = x_player.get_move(game)

        if game.make_move(move, letter):
            if print_game:
                print(f"{letter} makes a move to square {move}")
                game.print_board()

            if game.current_winner:
                if print_game:
                    print(f"{letter} wins!")
                return letter  # End the game

            letter = 'O' if letter == 'X' else 'X'  # Switch players

    if print_game:
        print("It's a tie!")

if __name__ == '__main__':
    human = HumanPlayer('O')
    ai = AIPlayer('X')
    tic_tac_toe_game = TicTacToe()
    play_game(tic_tac_toe_game, ai, human)