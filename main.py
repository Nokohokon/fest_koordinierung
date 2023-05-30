import discord
import os
from dotenv import load_dotenv
import ezcord

intents = discord.Intents.default()

bot = ezcord.Bot(
    intents=intents,
    debug_guilds=[1112744178577834116]  # hier server id einfügen
)


@bot.event
async def on_ready():
    print(f"{bot.user} ist online")


if __name__ == "__main__":
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

    load_dotenv()
    bot.run(os.getenv("TOKEN"))
    
    
    #Main.py Datei von CodingKeks
