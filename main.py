import discord
from discord.ext import commands
import os
import json
from dotenv import load_dotenv
import threading
from fastapi import FastAPI
import uvicorn

load_dotenv()  # Lädt Umgebungsvariablen aus .env

# FastAPI-Webserver starten
app = FastAPI()

@app.get("/")
async def root():
    return {"status": "Bot is alive!"}

def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Lade die gespeicherten Infos
def load_info_data():
    if not os.path.exists("data/info_messages.json"):
        return {}
    with open("data/info_messages.json", "r") as f:
        return json.load(f)

# Speichere die Infos
def save_info_data(data):
    with open("data/info_messages.json", "w") as f:
        json.dump(data, f, indent=4)

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(command_prefix="!", intents=intents, help_command=None)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.guild is None:
            await interaction.response.send_message(
                "⚠️ Slash-Commands können nicht in DMs benutzt werden.", ephemeral=True)
            return False
        return True

    async def on_ready(self):
        print(f"{self.user} ist online!")
        await self.tree.sync()

        info_data = load_info_data()
        for name, entry in info_data.items():
            channel = self.get_channel(int(entry["channel_id"]))
            message_id = int(entry["message_id"])
            try:
                await channel.fetch_message(message_id)
                print(f"[INFO] Nachricht '{name}' gefunden.")
            except (discord.NotFound, AttributeError):
                print(f"[INFO] Nachricht '{name}' wurde gelöscht. Wird neu gesendet...")
                cog = self.get_cog("InfoSystem")
                if cog:
                    embed = cog.get_embed(name)
                    if embed:
                        message = await channel.send(embed=embed)
                        info_data[name]["message_id"] = str(message.id)
                        save_info_data(info_data)

    async def setup_hook(self):
        await self.load_extension("cogs.info_system")
        await self.load_extension("cogs.announcement")
        await self.load_extension("cogs.application_system")

bot = MyBot()

# Starte den FastAPI-Webserver in einem separaten Thread
threading.Thread(target=run_api, daemon=True).start()

bot.run(os.getenv("DISCORD_TOKEN"))
