from discord.ext import commands
import discord

import random


players = [":x:", ":o:"]
wordboard = [":one:", ":two:", ":three:",
             ":four:", ":five:", ":six:",
             ":seven:", ":eight:", ":nine:"]


class tictactoe(commands.Cog):
    def __init__(self, bot):
        self.client = bot
        self.__reset_board()
        self.gameover = True

    def __print_board(self):
        line = ""
        for i in range(3):
            for j in range(3):
                if self.__is_number(self.board[i*3 + j]):
                    line += wordboard[i*3 + j]
                else:
                    line += self.board[i*3 + j]
            line += "\n"
        return line

    def __reset_board(self):
        self.board = [str(i+1) for i in range(9)]
        self.currentplayer = random.choice(players)
        self.gameover = False

    def __check_win(self):
        board = self.board
        # diagonal:
        if ((board[0] == board[4] == board[8]) or (board[2] == board[4] == board[6])) and not self.__is_number(board[4]):
            return True
        # check columns:
        for i in range(3):
            if board[i] == board[i+3] == board[i+6] and not self.__is_number(board[i]):
                return True
        # check rows:
        for i in range(3):
            if board[i*3] == board[i*3 + 1] == board[i*3 + 2] and not self.__is_number(board[i*3]):
                return True
        return False

    def __check_tie(self):
        for tile in self.board:
            if self.__is_number(tile):
                return False
        return True

    def __is_number(self, value):
        try:
            int(value)
            return True
        except Exception:
            return False

    def __select_tile(self, tile: int):
        if tile >= 1 and tile <= 9 and self.__is_number(self.board[tile-1]):
            self.board[tile-1] = self.currentplayer
            return True
        return False

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
        if reset or self.gameover:
            self.__reset_board()
            self.message = await ctx.respond(embed=self.__create_embed(f"Starting new game. \nIt's {self.currentplayer}'s turn", True))
        elif self.__select_tile(tile):
            if self.__check_win():
                self.gameover = True
                await self.message.edit_original_response(embed=self.__create_embed(f"{self.currentplayer} Wins.", True))
            elif self.__check_tie():
                self.gameover = True
                await self.message.edit_original_response(embed=self.__create_embed("It's a tie, no winners.", True))
            else:
                self.__switch_players()
                await self.message.edit_original_response(embed=self.__create_embed(f"It's {self.currentplayer}'s turn", True))
        else:
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
