from disnake.ext import commands
import disnake

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
    async def user(self, ctx):
        user = await self.bot.db.get_user(ctx.guild.id, ctx.author.id)
        
        await ctx.send(f"```json\n{user}```")
        

def setup(bot):
    bot.add_cog(Config(bot))