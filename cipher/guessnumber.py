import random
from discord.ext import commands


number = None
guess_count = 0


class GuessNumber(commands.Converter):
    async def convert(self, ctx, argument):
        global number
        global guess_count
        try:
            guess = int(argument)
            if not (0 <= guess <= 100):
                return "Please guess a number between *0* and *100*, (otherwise I get headaches :<)"
        except ValueError:
            return "Please guess a number between *0* and *100*, (otherwise I get headaches :<)"
        guess_count = guess_count + 1
        if number is None:
            guess_count = 1
            number = random.randint(0, 100)
        if guess == number:
            number = None
            return f"You guessed it!! *In {guess_count} tries"
        if guess < number:
            return f"The number is **higher** than {guess}"
        if guess > number:
            return f"The number is **lower** than {guess}"
