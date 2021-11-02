import disnake
import textwrap
import time


from disnake.ext import commands

def cleanup_code(content):
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    return content.strip('` \n')


def get_syntax_error(e):
    if e.text is None:
        return '```py\n{0.__class__.__name__}: {0}\n```'.format(e)

    return '```py\n{0.text}{1:>{0.offset}}\n{2}: {0}```'.format(e, '^', type(e).__name__)


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.env = {}
        self.before = None
        self.after = None

    @commands.command(hidden=True, name='eval')
    @commands.is_owner()
    async def _eval(self, ctx, *, code: str):
        """ Evaluate Python code """
        if code == 'exit()':
            self.env.clear()
            return await ctx.send('Environment cleared')

        self.env.update({
            'self': self,
            'bot': self.bot,
            'ctx': ctx,
            'message': ctx.message,
            'channel': ctx.message.channel,
            'guild': ctx.message.guild,
            'author': ctx.message.author,
        })

        code = code.replace('```py\n', '').replace('```', '').replace('`', '').strip()

        _code = 'async def func():\n  try:\n{}\n  finally:\n    self.env.update(locals())'\
            .format(textwrap.indent(code, '    '))

        try:
            self.before = time.monotonic()
            exec(_code, self.env)

            func = self.env['func']
            output = await func()

            output = repr(output) if output else str(output)
        except Exception as e:
            output = '{}: {}'.format(type(e).__name__, e)

        code = code.split('\n')
        s = ''
        for i, line in enumerate(code):
            s += '>>> ' if i == 0 else '... '
            s += line + '\n'
        self.after = time.monotonic()
        message = f'```py\n{s}\n{output}\n#Time of execution {(self.after - self.before)}\n```'

        try:
            await ctx.send(message)
        except disnake.HTTPException:
            await ctx.send('Output too large!')

    @commands.is_owner()
    @commands.command()
    async def reload(self, ctx, cog: str):
        """Reloads a cog"""
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(f"Reloaded cog **{cog}** successfully")
        except ModuleNotFoundError as e:  # noqa: F841
            await ctx.send(f"The cog **{cog}** wasn't found")
        except Exception as e:
            await ctx.send(f"Syntax error in cog {cog}: \n```py\n{e}```")

    @commands.is_owner()
    @commands.command()
    async def load(self, ctx, cog: str):
        """Loads a cog"""
        try:
            self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(f"Loaded cog **{cog}** successfully")
        except ModuleNotFoundError as e:  # noqa: F841
            await ctx.send(f"The cog **{cog}** wasn't found")
        except Exception as e:
            await ctx.send(f"Syntax error in cog {cog}: \n```py\n{e}```")

    @commands.is_owner()
    @commands.command()
    async def unload(self, ctx, cog: str):
        """Unloads a cog"""
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            await ctx.send(f"Unloaded cog **{cog}** successfully")
        except ModuleNotFoundError as e:  # noqa: F841
            await ctx.send(f"The cog **{cog}** wasn't found")
        except Exception as e:
            await ctx.send(f"Syntax error in cog {cog}: \n```py\n{e}```")


    @commands.command()
    @commands.is_owner()
    async def reload_translations(self, ctx):
        self.bot.translations.load_translations()
        await ctx.send("I've reloaded translations")

def setup(bot):
    bot.add_cog(Admin(bot))
