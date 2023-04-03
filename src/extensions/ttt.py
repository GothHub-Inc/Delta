from discord.ext import commands
import discord

from enum import Enum
import random

players = [":x:", ":o:"]
wordboard = [":one:", ":two:", ":three:",
             ":four:", ":five:", ":six:",
             ":seven:", ":eight:", ":nine:"]


class State (Enum):
    WIN = 1
    TIE = 2
    CONTINUE = 3
    INVALID = 4


class tictactoe(commands.Cog):
    def __init__(self, bot):
        self.client = bot
        self.gamestate = State.TIE

    def __print_board(self):
        line = ""
        for i in range(3):
            for j in range(3):
                if str.isnumeric(self.board[i*3 + j]):
                    line += wordboard[i*3 + j]
                else:
                    line += self.board[i*3 + j]
            line += "\n"
        return line

    def __reset_board(self):
        self.board = [str(i+1) for i in range(9)]
        self.currentplayer = random.choice(players)
        self.gamestate = State.CONTINUE

    def __check_win(self):
        board = self.board
        # diagonal:
        if ((board[0] == board[4] == board[8]) or (board[2] == board[4] == board[6])) and not str.isnumeric(board[4]):
            self.gamestate = State.WIN
            return
        # check columns:
        for i in range(3):
            if board[i] == board[i+3] == board[i+6] and not str.isnumeric(board[i]):
                self.gamestate = State.WIN
                return 
        # check rows:
        for i in range(3):
            if board[i*3] == board[i*3 + 1] == board[i*3 + 2] and not str.isnumeric(board[i*3]):
                self.gamestate = State.WIN
                return

    def __check_tie(self):
        for tile in self.board:
            if str.isnumeric(tile):
                return
        self.gamestate = State.TIE

    def __select_tile(self, tile: int):
        if tile >= 1 and tile <= 9 and str.isnumeric(self.board[tile-1]):
            self.board[tile-1] = self.currentplayer
            self.gamestate = State.CONTINUE
            return
        self.gamestate = State.INVALID

    def __switch_players(self):
        self.currentplayer = players[1] if self.currentplayer == players[0] else players[0]

    @commands.slash_command(
        guild_ids=[1033025456242434089],
        description="Play tic tac toe"
    )
    @discord.option(
        "tile",
        description="play the selected tile",
        min_value=1,
        max_value=9
    )
    @discord.option(
        "reset",
        description="reset the game board",
        default=False
        )
    async def ttt(
        self,
        ctx: discord.ApplicationContext,
        tile: int = discord.Option(
            int, autocomplete=discord.utils.basic_autocomplete(
            [i for i in range(9)])),
        reset: bool = False,
    ):
        if reset or self.gamestate == State.WIN or self.gamestate == State.TIE:
            self.__reset_board()
            self.message = await ctx.respond(embed=self.__create_embed(f"Starting new game. \nIt's {self.currentplayer}'s turn", True))
        self.__select_tile(tile)
        self.__check_tie()
        self.__check_win()
        match self.gamestate:
            case State.WIN:
                await self.message.edit_original_response(embed=self.__create_embed(f"{self.currentplayer} Wins.", True))
            case State.TIE:
                await self.message.edit_original_response(embed=self.__create_embed("It's a tie, no winners.", True))
            case State.CONTINUE:
                self.__switch_players()
                await self.message.edit_original_response(embed=self.__create_embed(f"It's {self.currentplayer}'s turn", True))
            case State.INVALID:
                await self.message.edit_original_response(embed=self.__create_embed(f"Invalid coord.\nIt's {self.currentplayer}'s turn", True))
        await ctx.respond(embed=self.__played_embed(), delete_after=0)

    def __played_embed(self):
        embed = discord.Embed(
            title="Tic tac toe",
            description="An action has been taken",
            color=discord.Colour.green()
        )
        return embed

    def __create_embed(self, message: str, showboard: bool):
        embed = discord.Embed(
            title="Tic tac toe",
            description=f"A simple game of tic tac toe\n\n{message}",
            color=discord.Colour.green()
        )
        if showboard:
            embed.add_field(
                name="Board:",
                value=self.__print_board(),
                inline=False
            )
        return embed


def setup(bot):
    bot.add_cog(tictactoe(bot))
