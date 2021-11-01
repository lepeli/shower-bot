from disnake.ext import commands
from datetime import datetime

import disnake
import timeago

class Config(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def set_reminder_channel(self, ctx, channel: disnake.TextChannel = None):
        """Définir le salon de rappel des douches"""

        config = await self.bot.db.get_config(ctx.guild.id)

        if not channel:
            channel = ctx.channel

        config["shower"]["reminder_channel"] = channel.id
        await self.bot.db.update_config(ctx.guild.id, config)
        await ctx.send(f"Les rappels seront désormais envoyés dans le salon: {channel.mention}")

    @commands.command()
    async def config(self, ctx):
        config = await self.bot.db.get_config(ctx.guild.id)
        await ctx.send(f"```json\n{config}```")

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
        

def setup(bot):
    bot.add_cog(Config(bot))