from disnake.ext import commands
from disnake.ext.commands import errors

import disnake

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"================\n{self.bot.user}\nOn {len(self.bot.guilds)} guilds\n================")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, (errors.MissingRequiredArgument, errors.BadArgument)):
            helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)
            await ctx.send_help(helper)

        elif isinstance(err, errors.CommandInvokeError):
            if 'forbidden' in str(err).lower() or 'not found' in str(err).lower():
                return
            await ctx.send('An unexpected error occurred while processing the command :/')

        elif isinstance(err, errors.MissingPermissions):
            permissions = '\n'.join([f'- {p.title()}' for p in err.missing_perms])
            await ctx.send(f'You\'re missing some permissions...\n{permissions}')

        elif isinstance(err, errors.BotMissingPermissions):
            permissions = '\n'.join([f'- {p.title()}' for p in err.missing_perms])
            await ctx.send(f'I\'m missing some permissions...\n{permissions}')

        elif isinstance(err, errors.CommandOnCooldown):
            await ctx.send('This command is on cooldown, you can use it again in '
                           f'{err.retry_after:.0f} seconds.')

        elif isinstance(err, errors.CommandError) and not isinstance(err, errors.CommandNotFound):
            await ctx.send(str(err))

        else:
            pass

def setup(bot):
    bot.add_cog(Events(bot))