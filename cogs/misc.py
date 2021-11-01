from disnake.ext import commands
import disnake

class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        """Get bot's invite link"""
        await ctx.send(f"Lien d'invitation du bot: https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=0&scope=bot")

    @commands.command()
    async def stats(self, ctx):
        """Show the bot's stats"""
        # online_time = _time.time_string(datetime.now() - self.bot.startup)
        em = disnake.Embed()

        em.add_field(name="Servers", value=str(len(self.bot.guilds)))
        em.add_field(name="Users", value=str(len(self.bot.users)))
        em.add_field(name="Emojis", value=str(len(self.bot.emojis)))

        # em.add_field(name="Uptime", value=online_time)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Misc(bot))