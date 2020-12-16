import asyncio
import itertools
import random
import sys  # only needed for debugging, see seed-code immediately below
from typing import Tuple

import discord
from redbot.core.bot import Red
from redbot.core import commands

SAND_COLOR = 0xC2B280


class DuneCard:
    def __init__(self, faction, strength, name):
        self.faction = faction
        self.strength = strength
        self.name = name


class DuneTraitorDealer:
    def __init__(self, bot: Red):
        # print what seed was used for debugging, unnecessary for final bot
        self.bot = bot
        seed = random.randrange(sys.maxsize)
        rng = random.Random(seed)
        print("Seed was:", seed)

        # Names of factions for IO
        self.factions = {
            # possible traitors by faction
            "Guild": [
                DuneCard("Guild", 5, "Staban Tuek"),
                DuneCard("Guild", 3, "Master Bewt"),
                DuneCard("Guild", 3, "Esmar Tuek"),
                DuneCard("Guild", 2, "Soo-Soo Sook"),
                DuneCard("Guild", 1, "Guild Rep."),
            ],
            "Atreides": [
                DuneCard("Atreides", 5, "Thufir Hawat"),
                DuneCard("Atreides", 5, "Lady Jessica"),
                DuneCard("Atreides", 4, "Gurney Halleck"),
                DuneCard("Atreides", 2, "Duncan Idaho"),
                DuneCard("Atreides", 1, "Dr.Wellington Yueh"),
            ],
            "Fremen": [
                DuneCard("Fremen", 7, "Stilgar"),
                DuneCard("Fremen", 6, "Chani"),
                DuneCard("Fremen", 5, "Otheym"),
                DuneCard("Fremen", 3, "Shadout Mapes"),
                DuneCard("Fremen", 2, "Jamis"),
            ],
            "Emperor": [
                DuneCard("Emperor", 6, "Hasimir Fenring"),
                DuneCard("Emperor", 5, "Captain Aramsham"),
                DuneCard("Emperor", 3, "Caid"),
                DuneCard("Emperor", 3, "Burseg"),
                DuneCard("Emperor", 2, "Bashar"),
            ],
            "Harkonnen": [
                DuneCard("Harkonnen", 6, "Feyd-Rautha"),
                DuneCard("Harkonnen", 4, "Beast Raban"),
                DuneCard("Harkonnen", 3, "Piter De Vries"),
                DuneCard("Harkonnen", 2, "Captain Iakin Nefud"),
                DuneCard("Harkonnen", 1, "Umman Kudu"),
            ],
            "BeneGesserit": [
                DuneCard("Bene Gesserit", 5, "Alia"),
                DuneCard("Bene Gesserit", 5, "Margot Lady Fenrig"),
                DuneCard("Bene Gesserit", 5, "Mother Ramallo"),
                DuneCard("Bene Gesserit", 5, "Princess Irulan"),
                DuneCard("Bene Gesserit", 5, "Wanna Yueh"),
            ],
        }

        # shuffle turn order (indexes to factions)
        self.turnOrder = [faction_name for faction_name in self.factions.keys()]
        random.shuffle(self.turnOrder)

    async def deal_the_traitors(self, ctx: commands.Context, *players: Tuple[discord.Member]):
        # Produces a list of (faction, player) pairs, where player is None if not enough players
        faction_player = list(itertools.zip_longest(self.turnOrder, players, fillvalue=None))

        embed = discord.Embed(
            title=f"Factions have been assigned",
            color=SAND_COLOR,
        )
        for fact, player in faction_player:
            embed.add_field(name=fact, value=str(player), inline=False)

        # Get the traitors for the factions that are in the game
        master_pool = [
            traitor
            for f_p in faction_player
            for traitor in self.factions[f_p[1]]
            if f_p[1] is not None
        ]

        # Announce the players and their factions
        await ctx.send(embed=embed)

        for current_faction, player in faction_player:
            print(f"Faction: {current_faction} - Player: {player}")
            player: discord.Member
            if player is None:
                # There's no more players to deal cards to, end.
                print("No more players")
                return
            # sending/receiving messages from this player
            embed = discord.Embed(
                title=f"Dealing cards to {player}",
                color=SAND_COLOR,
            )

            await ctx.send(embed=embed)

            # create a new pool for the individual player
            unselected_pool = [
                traitor for traitor in master_pool if traitor.faction != current_faction
            ]

            # # add only *other* factions leaders to it
            # for factionIdx in turnOrder:
            #     if factionIdx != playerIdx:
            #         pool += factions[masterpool[factionIdx]]

            # randomly draw 4 from personal pool
            # this might need different implementation depending on random library availablity
            random.shuffle(unselected_pool)
            pool = [unselected_pool.pop() for _ in range(4)]

            # Unselected_pool is now missing the chosen traitors
            # Merging unselected_pool with the traitors left in master_pool that *are* the current faction
            #   rebuilds the appropriate remaining traitors
            master_pool = [
                traitor for traitor in master_pool if traitor.faction == current_faction
            ] + unselected_pool

            # Harkonnens keep all cards
            if current_faction == "Harkonnen":
                embed = discord.Embed(
                    title=f"Your Traitors",
                    description=f"Harkonnen keep all their traitor cards.\n"
                    f"Take their cards out of the traitor deck in front of your zone and put them in your hand.",
                    color=SAND_COLOR,
                )
                # for each of the 4 traitors
                for i in range(4):
                    embed.add_field(
                        name=f"The {pool[i].faction} leader, {pool[i].name}",
                        value=f"Strength: {pool[i].strength}",
                        inline=False,
                    )
                    # print("the", pool[i][0], "leader,", pool[i][2])

                # Send them the results
                await player.send(embed=embed)

            # other factions must choose 1 of the 4
            else:
                embed = discord.Embed(
                    title=f"Your Traitors choices",
                    description=f"Choose one by responding with the letter (a, b, c, d):\n",
                    color=SAND_COLOR,
                )
                for i, letter in enumerate("abcd"):
                    # notify player
                    embed.add_field(
                        name=f"{letter}: The {pool[i].faction} leader, {pool[i].name}",
                        value=f"Strength: {pool[i].strength}",
                        inline=False,
                    )

                await player.send(embed=embed)

                letter = None

                def check(m: discord.Message):
                    return (
                        m.author == player
                        and m.channel == player.dm_channel
                        and m.content in "abcd"
                    )

                try:
                    answer = await self.bot.wait_for("message", timeout=None, check=check)
                except asyncio.TimeoutError:
                    await ctx.send("Timed out, canceling")
                    return

                # Expect response of A B C D
                letter = answer.content

                # convert to index and pop from pool
                choice = "abcd".index(letter)
                choice = pool.pop(choice)

                embed = discord.Embed(
                    title=f"You have chosen the {choice.faction} leader, {choice.name}",
                    description=f"Take their card out of the traitor deck in front of your zone and put it in your hand.",
                    color=SAND_COLOR,
                )
                # Confirm response
                await player.send(embed=embed)

                # unchosen cards are sent back
                master_pool = master_pool + pool
