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
                    if user["last_shower"] < datetime.now() - timedelta(hours=32) and (not user['last_notified'] or user["last_notified"] < datetime.now() - timedelta(hours=12)):
                        channel = guild.get_channel(int(guild_config["shower"]["reminder_channel"]))
                        diff = datetime.now() - user["last_shower"]
                        hours = int(diff.total_seconds() // 3600) # Convert to hours
                        try:
                            await channel.send(self.bot.t("reminder.reminder_text", locale=guild_config['locale'], mention=f"<@{user['user_id']}>", hours=hours))
                            user["last_notified"] = datetime.now()
                            user["showers_streak"] = 0 # Resets the streak to 0 because user didn't shower for more than 32 hours...
                            await self.bot.db.update_user(guild.id, int(user['user_id']), user)
                        except:
                            pass


def setup(bot):
    bot.add_cog(Watcher(bot))