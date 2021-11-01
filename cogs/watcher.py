from datetime import datetime, timedelta
from disnake.ext import tasks, commands

class Watcher(commands.Cog): 

    def __init__(self, bot):
        self.bot = bot
        self.shower_watch.start()
    
    def cog_unload(self):
        self.shower_watch.cancel()
    

    @tasks.loop(minutes=5)
    async def shower_watch(self): # After 32h without a shower it will ping the person and then every 12 hours if they didn't answer to the first ping.
        for guild in self.bot.guilds:
            guild_config = await self.bot.db.get_config(guild.id)
            if guild_config["shower"]["enabled"] and guild_config["shower"]["reminder_channel"]:
                users = await self.bot.db.get_guild_users(guild.id)
                for user in users:
                    if user["last_shower"] < datetime.now() - timedelta(hours=30) and (not user['last_notified'] or user["last_notified"] < datetime.now() - timedelta(hours=12)):
                        channel = guild.get_channel(int(guild_config["shower"]["reminder_channel"]))
                        try:
                            await channel.send(f"Bonjour <@{user['user_id']}>, il faudrait prendre une douche là, ça fait 30h que tu n'en n'a pas pris une!")
                            user["last_notified"] = datetime.now()
                            await self.bot.db.update_user(guild.id, int(user['user_id']), user)
                        except:
                            pass


def setup(bot):
    bot.add_cog(Watcher(bot))