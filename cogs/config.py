from disnake.ext import commands

import disnake

class Config(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def set_reminders_channel(self, ctx, channel: disnake.TextChannel):
        """Define shower reminder"""

        config = await self.bot.db.get_config(ctx.guild.id)

        if not channel:
            channel = ctx.channel

        config["shower"]["enabled"] = True
        config["shower"]["reminder_channel"] = channel.id
        await self.bot.db.update_config(ctx.guild.id, config)
        await ctx.send(ctx.t("config.reminders_channel_set", channel=channel.mention))

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def disable_reminders(self, ctx):
        """Disable shower reminders"""
        config = await self.bot.db.get_config(ctx.guild.id)

        config["shower"]["enabled"] = False

        await self.bot.db.update_config(ctx.guild.id, config)

        await ctx.send(ctx.t("config.reminders_disabled", prefix=ctx.prefix))

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def config(self, ctx):
        config = await self.bot.db.get_config(ctx.guild.id)

        em = disnake.Embed(title=ctx.t("config.guild_config"))
        if config["shower"]["reminder_channel"]:
            em.add_field(name=ctx.t("config.reminders_channel"), value=f"<#{config['shower']['reminder_channel']}>")
        else:
            em.add_field(name=ctx.t("config.reminders_channel"), value=ctx.t("config.reminders_channel_not_set"))
        em.add_field(name=ctx.t("config.are_reminders_enabled"), value=ctx.t("words.yes" if config["shower"]["enabled"] else "words.no"))
        await ctx.send(embed=em)

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def locale(self, ctx, locale: str = None):
        config = await self.bot.db.get_config(ctx.guild.id)

        if not locale or locale not in self.bot.translations.locales:
            return await ctx.send(ctx.t('config.available_locales', locales=", ".join(self.bot.translations.locales)))            

        config['locale'] = locale

        await self.bot.db.update_config(ctx.guild.id, config)
        await ctx.send(ctx.t('config.locale_updated', locale=locale, new_locale=locale))
        

def setup(bot):
    bot.add_cog(Config(bot))