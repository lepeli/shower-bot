from disnake.ext import commands
from datetime import datetime

import timeago
import disnake

class Stats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["profile"])
    async def user(self, ctx, user: disnake.Member = None): 
        """Get showers stats for you or a mentionned user"""
        if not user:
            user = ctx.author # Si pas d'utilisateur précisé on passe au suivant

        last_showers = await self.bot.db.get_last_showers_by_user(ctx.guild.id, user.id)

        user_profile = await self.bot.db.get_user(ctx.guild.id, user.id)
        em = disnake.Embed(title=ctx.t("stats.profile_of", user=user.display_name))
        em.add_field(name=ctx.t("stats.showers_total"), value=user_profile["showers_taken"])
        em.add_field(name=ctx.t("stats.streak"), value=user_profile["showers_streak"])
        if len(last_showers):
           em.add_field(name=ctx.t("stats.last_shower"), value=timeago.format(user_profile["last_shower"], datetime.now(), locale=ctx.t("__lang_short")))
        else:
           em.add_field(name=ctx.t("last_shower"), value=ctx.t("stats.no_recorded_shower"))

        em.set_thumbnail(url=user.display_avatar.url)

        em.description = f"**{ctx.t('stats.last_showers_taken_list')}**\n```yaml\n"

        if len(last_showers):
            for shower in last_showers:
                em.description += f"· {ctx.t('words.shower')}: {timeago.format(shower['date'], datetime.now(), locale=ctx.t('__lang_short'))}\n"
        else:
            em.description += f"{ctx.t('stats.no_recorded_shower')}\n"
        em.description += "```"
        await ctx.send(embed=em)

    @commands.command(aliases=["server"])
    async def server_stats(self, ctx):
        """Show the server's statistics"""
        em = disnake.Embed(title=ctx.t('stats.guild_stats'))
        em.add_field(name=ctx.t("stats.showers_total"), value=await self.bot.db.count_showers_guild(ctx.guild.id))
        em.add_field(name=ctx.t("stats.members_joined_count"), value=await self.bot.db.count_active_users_guild(ctx.guild.id))
        
        desc = f"**{ctx.t('stats.last_showers_taken_list')}**\n```yaml\n"

        last_showers = await self.bot.db.get_last_showers_by_guild(ctx.guild.id)
        for shower in last_showers:
            user = await self.bot.getch_user(int(shower["user_id"]))
            desc += f"· {ctx.t('words.shower')}: {timeago.format(shower['date'], datetime.now(), locale=ctx.t('__lang_short'))} {ctx.t('words.by')} {user.name}\n"

        desc += "\n```"
        em.description = desc
        await ctx.send(embed=em)
        

def setup(bot):
    bot.add_cog(Stats(bot))