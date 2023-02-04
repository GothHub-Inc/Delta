# from discord.ext import commands
import random
X = "x"
Y = "o"

clearBoard = [["-", "-", "-"],
              ["-", "-", "-"],
              ["-", "-", "-"]]


class TTT ():
    def __init__(self):
        self.board = clearBoard
        pass

    def __select_tile(self, x, y, board, player):
        if x < 3 and y < 3 and x >= 0 and y >= 0 and board[y][x] == "-":
            board[y][x] = player
            return True
        return False

    def __adjective_win(self, board, player):
        for i in range(3):
            rowWin = True
            columnWin = True
            for j in range(3):
                # rows
                if board[i][j] != player:
                    rowWin = False
                if board[j][i] != player:
                    columnWin = False
            if rowWin or columnWin:
                return True
        return False

    def __diagonal_win(self, board):
        for i in range(2):
            if board[i*2][i*2] == board[1][1] and board[1][1] == board[2-(i*2)][2-(i*2)] and board[1][1] != "-":
                return True
        return False

    def __check_tie(self, board):
        for i in range(3):
            for tile in board[i]:
                if tile == "-":
                    return False
        return True

    def __check_win(self, board, player):
        # check vertical:
        if self.__adjective_win(board, player):
            print("Adjective win")
            return True

        # check diagonal;
        if self.__diagonal_win(board):
            print("diagonal win")
            return True

        print("No winner found")
        return False

    def print_board(self, board):
        for i in range(3):
            row = ""
            for char in board[i]:
                row += char + ", "
            print(row)

    def run(self):
        player = X
        if random.randint(0, 1) == 1:
            player = Y
        while True:
            print("It is player "+player+"'s turn")

            self.print_board(self.board)
            print("current board:")

            row, col = list(map(int, input("Enter x and y coordinates: ").split()))
            print()

            if self.__select_tile(row-1, col-1, self.board, player):
                if self.__check_win(self.board, player):
                    print("player "+player+" wins \nFinal board:")
                    self.print_board(self.board)
                    break

                if self.__check_tie(self.board):
                    print("Tie, no winners \nFinal board:")
                    self.print_board(self.board)
                    break

                player = X if player == Y else Y
            else:
                print("Invalid coordinate")


def setup(bot):
    bot.add_cog(TTT(bot))


TestTTT = TTT()
TestTTT.run()
# TestTTT.test_run(charBoardTest)
# TestTTT.print_board(charBoardTest)
# print(list(zip(testBoard)))
