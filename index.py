import os
import json

from utils import database
from disnake.ext import commands
from utils import translations


async def before_invoke(ctx):

    if ctx.guild:
        ctx.config = await ctx.bot.db.get_config(ctx.guild.id)
        ctx.lang = ctx.config["locale"]
    else:
        ctx.lang = ctx.bot.c["default_locale"]

    ctx.t = translations.Translate(lang=ctx.lang, translate_module=ctx.bot.translations).t

if __name__ == "__main__":

    with open("config.json") as conf:
        c = json.load(conf)

    bot = commands.AutoShardedBot(command_prefix=c["prefix"])
    bot.c = c

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

    bot.translations = translations.Translations("./translations/")
    bot.translations.load_translations()
    bot.t = bot.translations.t
    bot.before_invoke(before_invoke)

    bot.run(bot.c["token"])

    @bot.event
    async def on_message(message):
        if not bot.is_ready() or message.author.bot:
            return
        await bot.process_commands(message)

