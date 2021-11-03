from disnake.ext import commands
from datetime import datetime, timedelta
import disnake


class InscriptionView(disnake.ui.View):
    def __init__(self, bot, user, t):
        self.timeout = 30
        self.bot = bot
        self.user = user
        self.t = t
        super().__init__(timeout=30)
    
    async def interaction_check(self, interaction):
        return interaction.user.id == self.user # On retourne si l'utilsateur a le droit ou non de réagir
        

    async def on_timeout(self):
        await self.disable_buttons()

    async def disable_buttons(self, interaction = None):
        for child in self.children:
            child.disabled = True
        if interaction:
            await interaction.response.edit_message(view=self)

        else:
            await self.message.edit(view=self)

    @disnake.ui.button(label="Confirmer", style=disnake.ButtonStyle.green)
    async def first_button_callback(self, button, interaction):
        await self.disable_buttons(interaction)
        user = await self.bot.db.get_user(interaction.guild_id, interaction.user.id)

        user["joined"] = True

        await self.bot.db.update_user(interaction.guild_id, interaction.user.id, user)
        await interaction.channel.send(self.t("shower.joining_confirmed", mention=interaction.user.mention))

    @disnake.ui.button(label="Rejeter", style=disnake.ButtonStyle.danger)
    async def second_button_callback(self, button, interaction):
        await self.disable_buttons(interaction)
        await interaction.channel.send(self.t("shower.joining_refused"))

class Shower(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["inscription"])
    async def join(self, ctx):
        """Be a part of people that takes shower"""

        user = await self.bot.db.get_user(ctx.guild.id, ctx.author.id)

        if user["joined"]:
            return await ctx.send(ctx.t("shower.already_joined", prefix=ctx.prefix))
        
        view = InscriptionView(self.bot, ctx.author.id, ctx.t)

        view.message = await ctx.send(ctx.t("shower.confirm_joining"), view=view)


    @commands.command(aliases=["desinscription"])
    async def leave(self, ctx):
        """Leave the group of clean people"""
        user = await self.bot.db.get_user(ctx.guild.id, ctx.author.id)

        if user["joined"]: 
            user["joined"] = False
            await self.bot.db.update_user(ctx.guild.id, ctx.author.id, user)
            return await ctx.send(ctx.t("shower.leaving_confirmed"))
        
        return await ctx.send(ctx.t("shower.havent_joined"))

    @commands.command(aliases=['jaiprisunedouche', 'douche', 'jesuispropre', 'itookashower'])
    async def shower(self, ctx):
        """Tell the bot when you take a shower"""
        user = await self.bot.db.get_user(ctx.guild.id, ctx.author.id)

        if not user['joined']:
            return await ctx.send(ctx.t("shower.you_need_to_join", prefix=ctx.prefix))
        if user['last_shower']:
            # Vérification du temps entre deux douches

            next_shower_allowed = user['last_shower'] + timedelta(hours=11)
            if datetime.now() < next_shower_allowed:
                return await ctx.send(ctx.t('shower.you_already_took_one', time_allowed=11))

        await self.bot.db.add_shower(ctx.guild.id, ctx.author.id)
        return await ctx.send(ctx.t('shower.shower_confirmed'))


def setup(bot):
    bot.add_cog(Shower(bot))