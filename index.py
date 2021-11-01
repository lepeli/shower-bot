import os
import json

from disnake.ext import commands
from utils import database


if __name__ == "__main__":
    bot = commands.AutoShardedBot(".")

    with open("config.json") as c:
        bot.c = json.load(c)

    for cog in os.listdir("./cogs"):
        if not cog.endswith(".py"):
            continue
        print(f"Loading Cog: {cog[:-3]}")
        try:
            bot.load_extension(f"cogs.{cog[:-3]}")
            print(f"[OK] Loaded cog: {cog}")
        except SyntaxError as e:
            print(f"[Fail] Failed to load {cog}: Syntax error \n\t{e}")
        except ImportError as e:
            print(f"[Fail] Failed to import cog {cog}: \n\t{e}")

    bot.db = database.Database(bot) # Initialisation de la base de données

    bot.run(bot.c["token"])

    @bot.event
    async def on_message(message):
        if not bot.is_ready() or message.author.bot:
            return
        await bot.process_commands(message)


