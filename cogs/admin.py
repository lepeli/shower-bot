from disnake.ext import commands

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command()
    async def reload(self, ctx, cog: str):
        """Reloads a cog"""
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(f"Reloaded cog **{cog}** successfully")
        except ModuleNotFoundError as e:  # noqa: F841
            await ctx.send(f"The cog **{cog}** wasn't found")
        except Exception as e:
            await ctx.send(f"Syntax error in cog {cog}: \n```py\n{e}```")

    @commands.is_owner()
    @commands.command()
    async def load(self, ctx, cog: str):
        """Loads a cog"""
        try:
            self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(f"Loaded cog **{cog}** successfully")
        except ModuleNotFoundError as e:  # noqa: F841
            await ctx.send(f"The cog **{cog}** wasn't found")
        except Exception as e:
            await ctx.send(f"Syntax error in cog {cog}: \n```py\n{e}```")

    @commands.is_owner()
    @commands.command()
    async def unload(self, ctx, cog: str):
        """Unloads a cog"""
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            await ctx.send(f"Unloaded cog **{cog}** successfully")
        except ModuleNotFoundError as e:  # noqa: F841
            await ctx.send(f"The cog **{cog}** wasn't found")
        except Exception as e:
            await ctx.send(f"Syntax error in cog {cog}: \n```py\n{e}```")


def setup(bot):
    bot.add_cog(Admin(bot))