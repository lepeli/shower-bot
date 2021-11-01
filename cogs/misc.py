from disnake.ext import commands

class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        """Avoir le lien d'invitation du bot"""
        await ctx.send("Lien d'invitation du bot: https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=0&scope=bot")