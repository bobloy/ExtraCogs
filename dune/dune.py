import logging

import discord
from redbot.core import Config, commands
from redbot.core.bot import Red

from dune.traitordealer import DuneTraitorDealer

log = logging.getLogger("red.fox_v3.dune")


class Dune(commands.Cog):
    """
    Deal traitor cogs for the Dune board game.

    This is not designed for public use.
    """

    def __init__(self, bot: Red):
        super().__init__()
        self.bot = bot
        self.config = Config.get_conf(self, identifier=68117110101, force_registration=True)

        default_guild = {}

        self.config.register_guild(**default_guild)

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    @commands.command(require_var_positional=True)
    async def dune(self, ctx: commands.Context, *playerlist: discord.Member):
        """Deal traitor cards to the provided list of players"""
        dealer = DuneTraitorDealer(self.bot)
        await ctx.send(
            f"Dealing cards to these players:\n{' '.join(p.mention for p in playerlist)}"
        )
        await dealer.deal_the_traitors(ctx, *playerlist)

        await ctx.send("Traitors have been dealt!")
