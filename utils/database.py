import motor.motor_asyncio
import utils.default_configs as default_configs
import pymongo

from datetime import datetime, timedelta

class Database:

    def __init__(self, bot):  # Init the database to be used globally in the bot
        self.bot = bot
        self.conf = self.bot.c['database']  # Get database config
        if self.conf['authentication']:
            self.connection = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{self.conf['username']}:{self.conf['password']}@{self.conf['ip']}:{self.conf['port']}/{self.conf['database']}")
        else:
            self.connection = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{self.conf['ip']}:{self.conf['port']}")
        self.db = self.connection[bot.c['database']['database']]

    #  =======================[CONFIG]=======================
    #  Part used for guild configurations
    #  ======================================================

    async def get_config(self, guild_id: int):
        config = await self.db['config'].find_one({"guild_id": str(guild_id)})
        default_config = dict(default_configs.server_conf)
        if not config:
            default_config.update({"guild_id": str(guild_id)})
            config = default_config
        else:
            default_config.update(config)
            config = default_config
        return config

    async def update_config(self, guild_id: int, new_conf: dict):
        new_conf.update({"guild_id": str(guild_id)})
        config = await self.db['config'].find_one({"guild_id": str(guild_id)})

        if config:
            await self.db['config'].replace_one({"_id": config['_id']}, new_conf)
        else:
            await self.db['config'].insert_one(new_conf)

    # async def get_prefix(self, guild_id: int):
    #     config = await self.db['config'].find_one({"guild_id": str(guild_id)})

    #     if config["prefix"]:
    #         return config["prefix"]
    #     return self.bot.c['prefix']


    #  ========================[USER]========================
    #  Part used to configure users, add them to the
    #  notifications or change their last shower date.
    #  ======================================================

    async def get_user(self, guild_id: int, user_id: int):
        """Get user config"""
        user_db = await self.db['users'].find_one({"guild_id": str(guild_id), "user_id": str(user_id)})
        default_user = dict(default_configs.user_conf)
        if not user_db:
            user = dict(default_configs.user_conf)
            user.update({"guild_id": str(guild_id), "user_id": str(user_id)})
        
        else:
            user = default_user
            user.update(user_db)

        return user
    
    async def update_user(self, guild_id: int, user_id: int, new_user: dict):
        """Update a user in the database"""
        new_user.update({"user_id": str(user_id), "guild_id": str(guild_id)})
        config = await self.db['users'].find_one({"guild_id": str(guild_id), "user_id": str(user_id)})
        if config:
            new_user.update({"_id": config['_id']})
            await self.db["users"].replace_one({"_id": config['_id']}, new_user)
        
        else:
            new_user["last_shower"] = datetime.now() - timedelta(hours=12) # On initialise la dernière 12h en arrière.
            await self.db["users"].insert_one(new_user)

    async def get_guild_users(self, guild_id: int):
        usr_cursor = self.db["users"].find({"guild_id": str(guild_id), "joined": True})
        users = await usr_cursor.to_list(length=None)
        return users

    #  =======================[SHOWERS]=======================
    #  Part used to count showers of users in a server
    #  will include shower streak (increases by days when you 
    #  take a shower)
    #  =======================================================

    async def add_shower(self, guild_id: int, user_id: int):
        """Ajouter une douche pour un utilisateur"""
        
        shower = {
            "guild_id": str(guild_id),
            "user_id": str(user_id),
            "date": datetime.now()
        } # Objet douche pour le stocker dans la bd

        user = await self.get_user(guild_id, user_id)

        user['showers_taken'] += 1 # On ajoute le compte de douches

        if not user["last_shower"]:
            user["showers_streak"] = 1
        elif user["last_notified"] and user["last_shower"].day != shower["date"].day:
            user["showers_streak"] += 1 # Ajout dans le streak si le jour est différent

        user['last_notified'] = None # On reset le compteur de notification
        user['last_shower'] = shower["date"]
        await self.update_user(guild_id, user_id, user)
    
        await self.db["showers"].insert_one(shower)

    async def count_active_users_guild(self, guild_id: int):
        return await self.db["users"].count_documents({"guild_id": str(guild_id), "joined": True})

    async def count_showers_guild(self, guild_id: int):
        """Count total shower by server"""
        return await self.db["showers"].count_documents({"guild_id": str(guild_id)})

    async def count_showers_all_guilds(self):
        """Return the total of showers taken across all the guilds"""
        return await self.db['showers'].count_documents({})

    async def count_showers_user_guild(self, guild_id: int, user_id: int):
        return await self.db["showers"].count_documents({"guild_id": str(guild_id), "user_id": str(user_id)})

    async def get_last_showers_by_user(self, guild_id: int, user_id: int):
        cursor = self.db["showers"].find({"guild_id": str(guild_id), "user_id": str(user_id)}, sort=[('date',pymongo.DESCENDING)])

        return await cursor.to_list(length=5)

    async def get_last_showers_by_guild(self, guild_id: int):
        cursor = self.db["showers"].find({"guild_id": str(guild_id)}, sort=[('date',pymongo.DESCENDING)])

        return await cursor.to_list(length=5)

    async def get_smelliest_by_guild(self, guild_id: int):
        cursor = self.db["showers"].find({"guild_id": str(guild_id)}, sort=[('date',pymongo.ASCENDING)])

        return await cursor.to_list(length=5)