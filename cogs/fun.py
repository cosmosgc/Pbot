""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""

import random

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import logging
    


class Choice(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.value = None

    @discord.ui.button(label="Heads", style=discord.ButtonStyle.blurple)
    async def confirm(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ) -> None:
        self.value = "heads"
        self.stop()

    @discord.ui.button(label="Tails", style=discord.ButtonStyle.blurple)
    async def cancel(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ) -> None:
        self.value = "tails"
        self.stop()


class RockPaperScissors(discord.ui.Select):
    def __init__(self) -> None:
        options = [
            discord.SelectOption(
                label="Scissors", description="You choose scissors.", emoji="✂"
            ),
            discord.SelectOption(
                label="Rock", description="You choose rock.", emoji="🪨"
            ),
            discord.SelectOption(
                label="Paper", description="You choose paper.", emoji="🧻"
            ),
        ]
        super().__init__(
            placeholder="Choose...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        choices = {
            "rock": 0,
            "paper": 1,
            "scissors": 2,
        }
        user_choice = self.values[0].lower()
        user_choice_index = choices[user_choice]

        bot_choice = random.choice(list(choices.keys()))
        bot_choice_index = choices[bot_choice]

        result_embed = discord.Embed(color=0xBEBEFE)
        result_embed.set_author(
            name=interaction.user.name, icon_url=interaction.user.display_avatar.url
        )

        winner = (3 + user_choice_index - bot_choice_index) % 3
        if winner == 0:
            result_embed.description = f"**That's a draw!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0xF59E42
        elif winner == 1:
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0x57F287
        else:
            result_embed.description = f"**You lost!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0xE02B2B

        await interaction.response.edit_message(
            embed=result_embed, content=None, view=None
        )


class RockPaperScissorsView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.add_item(RockPaperScissors())


class Fun(commands.Cog, name="fun"):
    def __init__(self, bot) -> None:
        self.bot = bot

    logger = logging.getLogger("discord_bot")
    logger.setLevel(logging.INFO)

    @commands.hybrid_command(name="randomfact", description="Get a random fact.")
    async def randomfact(self, context: Context) -> None:
        """
        Get a random fact.

        :param context: The hybrid command context.
        """
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://uselessfacts.jsph.pl/random.json?language=en"
            ) as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(description=data["text"], color=0xD75BF4)
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B,
                    )
                await context.send(embed=embed)

    @commands.hybrid_command(
        name="coinflip", description="Make a coin flip, but give your bet before."
    )
    async def coinflip(self, context: Context) -> None:
        """
        Make a coin flip, but give your bet before.

        :param context: The hybrid command context.
        """
        buttons = Choice()
        embed = discord.Embed(description="What is your bet?", color=0xBEBEFE)
        message = await context.send(embed=embed, view=buttons)
        await buttons.wait()  # We wait for the user to click a button.
        result = random.choice(["heads", "tails"])
        if buttons.value == result:
            embed = discord.Embed(
                description=f"Correct! You guessed `{buttons.value}` and I flipped the coin to `{result}`.",
                color=0xBEBEFE,
            )
        else:
            embed = discord.Embed(
                description=f"Woops! You guessed `{buttons.value}` and I flipped the coin to `{result}`, better luck next time!",
                color=0xE02B2B,
            )
        await message.edit(embed=embed, view=None, content=None)

    @commands.hybrid_command(
        name="rps", description="Play the rock paper scissors game against the bot."
    )
    async def rock_paper_scissors(self, context: Context) -> None:
        """
        Play the rock paper scissors game against the bot.

        :param context: The hybrid command context.
        """
        view = RockPaperScissorsView()
        await context.send("Please make your choice", view=view)
    
    
    @commands.hybrid_command(
        name="destiny", description="Generate a Destiny text."
    )
    @app_commands.guilds(discord.Object(id=481659634701303838))
    async def generate_destiny_text(self, context: Context) -> None:
        """
        Generate a Destiny text.

        :param context: The hybrid command context.
        """
        names = self.read_words('destiny/names.txt')
        titles = self.read_words('destiny/titles.txt')
        aspects = self.read_words('destiny/aspect.txt')
        Classes = self.read_words('destiny/class.txt')
        destinies = self.read_words('destiny/destinies.txt')
        destinations = self.read_words('destiny/destinations.txt')

        name = random.choice(names)
        title = random.choice(titles)
        aspect = random.choice(aspects)
        Class = random.choice(Classes)
        destiny = random.choice(destinies)
        destination = random.choice(destinations)

        text = f"Você é {title} {name}, O {Class} {aspect}, destinado a {destiny} {destination}!"
        await context.send(text)
        
    logger.warning(f"Destiny")
    def get_random_user(self):
        return random.choice(self.participants)
    
    def remove_user(self, user):
        self.participants.remove(user)
        
    
        
    async def run_battle_royale(self, ctx, participants):
        await ctx.send("O Battle Royale começou!")
        waysToDie = self.read_words('text/waystodie.txt')
        events = []
        while len(participants) > 1:
            user1 = self.get_random_user()
            user2 = self.get_random_user()

            while user1 == user2:
                user2 = self.get_random_user()

            winner = random.choice([user1, user2])
            loser = user1 if winner == user2 else user2
            howItDied = random.choice(waysToDie)
            events.append(f"{loser.mention} {howItDied} kill de {winner.mention}!")

            self.remove_user(loser)

        final_winner = participants[0]
        events.append(f"A ultima pessoa a sobreviver foi {final_winner.mention}! O vencedor(a)!")
        embed = discord.Embed(title="Battle Royale Results", color=discord.Color.green())
        for event in events:
            embed.add_field(name="Evento", value=event, inline=False)
        # Send the Discord embed
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="start_battle_royale", description="Começa um battle royale com as utlimas 10 pessoas do chat.")
    async def start_battle_royale(self, ctx: Context):
        # Get the last 10 users in the chat
        #self.participants = ctx.channel.members[-10:]
        self.participants = [member for member in ctx.channel.members if not member.bot and member != ctx.bot.user]
        # Shuffle the participants randomly
        #random.shuffle(self.participants)
        # Limit the participants to the last 10 users
        self.participants = self.participants[-10:]
        if len(self.participants) < 2:
            await ctx.send("There are not enough users to start a battle royale.")
            return

        # Shuffle the participants randomly
        random.shuffle(self.participants)

        # Run the battle royale
        await self.run_battle_royale(ctx, self.participants)

    def read_words(self, filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return [word.strip() for word in f]
        
async def setup(bot) -> None:
    await bot.add_cog(Fun(bot))
