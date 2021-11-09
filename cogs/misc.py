from disnake.ext import commands
import disnake

class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        """Get bot's invite link"""
        await ctx.send(ctx.t("misc.invite_link", invite=f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=0&scope=bot"))

    @commands.command()
    async def stats(self, ctx):
        """Show the bot's stats"""
        # online_time = _time.time_string(datetime.now() - self.bot.startup)
        em = disnake.Embed(title=ctx.t("misc.stats"))

        em.add_field(name=ctx.t("misc.stats_guilds"), value=str(len(self.bot.guilds)))
        em.add_field(name=ctx.t("misc.stats_users"), value=str(len(self.bot.users)))
        em.add_field(name=ctx.t("misc.stats_emotes"), value=str(len(self.bot.emojis)))
        em.add_field(name=ctx.t("stats.showers_total"), value=await self.bot.db.count_showers_all_guilds())
        em.add_field(name=ctx.t("stats.members_joined_count"), value= await self.bot.db.count_all_active_users())

        # em.add_field(name="Uptime", value=online_time)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Misc(bot))