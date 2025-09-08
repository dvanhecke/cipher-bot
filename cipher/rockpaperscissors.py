import random
from discord.ext import commands


RULES = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock"
}


class RockPaperScissors(commands.Converter):
    async def convert(self, ctx, argument):
        if argument.lower() not in list(RULES.keys()):
            return "**invalid option**, please choose a valid option"
        choice = random.choice(list(RULES.keys()))
        if argument.lower() == RULES[choice]:
            return f"I win because **{choice}** beats **{argument.lower()}**"
        if choice == RULES[argument.lower()]:
            return f"{ctx.author} wins because **{argument.lower()}** beats **{choice}**"
        return "It's a draw"
