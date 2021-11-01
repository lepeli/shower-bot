from disnake.ext import commands
from datetime import datetime, timedelta
import disnake


class InscriptionView(disnake.ui.View):
    def __init__(self, bot, user):
        self.timeout = 30
        self.bot = bot
        self.user = user
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

    @disnake.ui.button(label="Accepter", style=disnake.ButtonStyle.green)
    async def first_button_callback(self, button, interaction):
        await self.disable_buttons(interaction)
        user = await self.bot.db.get_user(interaction.guild_id, interaction.user.id)

        user["joined"] = True

        await self.bot.db.update_user(interaction.guild_id, interaction.user.id, user)
        await interaction.channel.send(f"Bienvenue {interaction.user.mention} parmis les fous, n'oublies pas de signaler quand tu prends ta douche.")

    @disnake.ui.button(label="Refuser", style=disnake.ButtonStyle.danger)
    async def second_button_callback(self, button, interaction):
        await self.disable_buttons(interaction)
        await interaction.channel.send("Vous avez bien refusé de rejoindre le channel, on espère quand même que vous prenez des douches.")

class Douche(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def inscription(self, ctx):
        """S'inscrire sur le bot, pour pouvoir être mentionner quand il faut prendre votre douche"""

        user = await self.bot.db.get_user(ctx.guild.id, ctx.author.id)

        if user["joined"]:
            return await ctx.send(f"Vous êtes déjà inscrit ! Si vous voulez vous désinscrire utilisez la commande `{ctx.prefix}desinscription`")
        
        view = InscriptionView(self.bot, ctx.author.id)

        view.message = await ctx.send("Voulez-vous vous inscrire au programme avancé de douche ? ", view=view)


    @commands.command()
    async def desinscription(self, ctx):
        """Se désincrire du bot"""
        user = await self.bot.db.get_user(ctx.guild.id, ctx.author.id)

        if user["joined"]: 
            user["joined"] = False
            await self.bot.db.update_user(ctx.guild.id, ctx.author.id)
            return await ctx.send("Vous avez bien été désinscrit ! Nous espérons que vous avez du déo 72h.")
        
        return await ctx.send("Vous n'êtes pas inscrit !")

    @commands.command(aliases=['jaiprisunedouche', 'douche', 'jesuispropre'])
    async def pointeuse(self, ctx):
        user = await self.bot.db.get_user(ctx.guild.id, ctx.author.id)
        if user['last_shower']:
            # Vérification du temps entre deux douches

            next_shower_allowed = user['last_shower'] + timedelta(hours=11)
            if datetime.now() < next_shower_allowed:
                return await ctx.send("Vous avez déjà pris une douche il y a moins de 11h, veuillez repasser bientôt")

        await self.bot.db.add_shower(ctx.guild.id, ctx.author.id)
        return await ctx.send("Bravo, vous avez pris une douche !")


def setup(bot):
    bot.add_cog(Douche(bot))