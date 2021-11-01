from datetime import datetime, timedelta
from disnake.ext import tasks, commands

class Watcher(commands.Cog): 

    def __init__(self, bot) -> None:
        self.bot = bot
        self.douche_watch.start()
    
    def cog_unload(self) -> None:
        self.douche_watch.cancel()
    

    @tasks.loop(minutes=5)
    async def douche_watch(self): # Faire une boucle de rappel qui va parcourir les utilisateurs et les mentionner s'ils ont pas pris de douche depuis 48 heures.
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