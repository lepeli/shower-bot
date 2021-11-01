from disnake.ext import commands
from datetime import datetime

import timeago
import disnake

class Stats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def user(self, ctx, user: disnake.Member = None): 
        if not user:
            user = ctx.author # Si pas d'utilisateur précisé on passe au suivant

        last_showers = await self.bot.db.get_last_showers_by_user(ctx.guild.id, user.id)

        user_profile = await self.bot.db.get_user(ctx.guild.id, user.id)
        em = disnake.Embed(title=f"Profile de {user.display_name}")
        em.add_field(name="Total de douches", value=user_profile["showers_taken"])
        em.add_field(name="Streak", value=user_profile["showers_streak"])
        if len(last_showers):
           em.add_field(name="Dernière douche", value=timeago.format(user_profile["last_shower"], datetime.now(), locale="fr"))
        else:
           em.add_field(name="Dernière douche", value="Aucune douche n'a été enregistrée")

        em.set_thumbnail(url=user.display_avatar.url)

        em.description = "**Liste des dernières douches prises**\n```yaml\n"

        if len(last_showers):
            for shower in last_showers:
                em.description += f"· Douche: {timeago.format(shower['date'], datetime.now(), locale='fr')}\n"
        else:
            em.description += "Aucune douche enregistrée\n"
        em.description += "```"
        await ctx.send(embed=em)

    @commands.command(disable=True)
    async def server_stats(self, ctx):
        """Show the server's statistics""" #WIP: users, last showers by which user, ect, shower count...
        em = disnake.Embed(title="Statistiques du serveur")
        em.add_field(name="Nombre de douches totales", value=await self.bot.db.count_showers_guild(ctx.guild.id))
        em.add_field(name="Nombres d'inscrits", value=await self.bot.db.count_active_users_guild(ctx.guild.id))
        
        desc = "**Dernières douches prises**\n```yaml\n"

        last_showers = await self.bot.db.get_last_showers_by_guild(ctx.guild.id)
        for shower in last_showers:
            user = await self.bot.getch_user(int(shower["user_id"]))
            desc += f"· Douche: {timeago.format(shower['date'], datetime.now(), locale='fr')} par {user.name}"

        desc += "\n```"
        em.description = desc
        await ctx.send(embed=em)
        


def setup(bot):
    bot.add_cog(Stats(bot))