from disnake.ext import commands
from disnake.ext.commands import errors


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
            print(str(err))
            await ctx.send(ctx.t("error.unexpected_error"))

        elif isinstance(err, errors.MissingPermissions):
            permissions = '\n'.join([f'- {p.title()}' for p in err.missing_perms])
            await ctx.send(ctx.t("error.missing_permissions", permissions=permissions))

        elif isinstance(err, errors.BotMissingPermissions):
            permissions = '\n'.join([f'- {p.title()}' for p in err.missing_perms])
            await ctx.send(ctx.t("error.bot_missing_permissions", permissions=permissions))

        elif isinstance(err, errors.CommandOnCooldown):
            await ctx.send(ctx.t("error.command_cooldown", seconds=f"{err.retry_after:.0f}"))

        elif isinstance(err, errors.CommandError) and not isinstance(err, errors.CommandNotFound):
            print(err)
            await ctx.send(ctx.t("error.unknown_error", error=err))

        else:
            pass


def setup(bot):
    bot.add_cog(Events(bot))