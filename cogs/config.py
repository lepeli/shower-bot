from disnake.ext import commands

import disnake

class Config(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def set_reminder_channel(self, ctx, channel: disnake.TextChannel = None):
        """Define shower reminder"""

        config = await self.bot.db.get_config(ctx.guild.id)

        if not channel:
            channel = ctx.channel

        config["shower"]["enabled"] = True
        config["shower"]["reminder_channel"] = channel.id
        await self.bot.db.update_config(ctx.guild.id, config)
        await ctx.send(f"Les rappels seront désormais envoyés dans le salon: {channel.mention}")

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def disable_reminders(self, ctx):
        """Disable shower reminders"""
        config = await self.bot.db.get_config(ctx.guild.id)

        config["shower"]["enabled"] = False

        await self.bot.db.update_config(ctx.guild.id, config)

        await ctx.send(f"Les rappels sont désormais désactivés, pour les réactiver utilisez la commande `{ctx.prefix}set_reminder_channel")

    @commands.command()
    async def config(self, ctx):
        config = await self.bot.db.get_config(ctx.guild.id)

        em = disnake.Embed(title="Configuration du serveur")
        if config["shower"]["reminder_channel"]:
            em.add_field(name="Salon des rappels", value=f"{config['shower']['reminder_channel']}")
        else:
            em.add_field(name="Salon des rappels", value="Le salon n'a pas été défini")
        em.add_field(name="Rappels activés ?", value="Oui" if config["shower"]["enabled"] else "Non")
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Config(bot))