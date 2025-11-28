# bot.py — FIXED, CLEANED, AND NOT CRYING ANYMORE

import discord
from discord import app_commands
from discord.ext import commands, tasks
from flask import Flask
from threading import Thread
import os
import random
import datetime

# ------------------ OWNER ID ------------------
OWNER_ID = 1382858887786528803  

# ------------------ Flask Keep-Alive ------------------
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run_flask, daemon=True).start()

# ------------------ Bot Setup ------------------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

# ------------------ Slash Commands ------------------

@bot.tree.command(name="ytlink", description="Get the link to the YouTube channel")
async def ytlink(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Here’s the official YouTube channel: https://youtube.com/@YOUR_CHANNEL"
    )

@bot.tree.command(name="about", description="About the YouTuber")
async def about(interaction: discord.Interaction):
    embed = discord.Embed(
        title="About the Creator",
        description=(
            "This bot was made for **YOUR YOUTUBER’S NAME**.\n\n"
            "They make videos about **whatever they actually do**. "
            "Stylish, chaotic, talented and powered by caffeine.\n\n"
            "If you're here, you're already part of the chaos."
        ),
        color=0x00ffcc,
    )
    embed.set_footer(text="Powered by a bot that barely survived development.")

    await interaction.response.send_message(embed=embed)

# ------------------ Status Rotator ------------------

status_list = [
    "Editing a banger video...",
    "Reading your DMs but pretending not to...",
    "Cooking up content...",
]

@tasks.loop(seconds=20)
async def update_status():
    await bot.change_presence(
        activity=discord.Game(random.choice(status_list))
    )

# ------------------ Events ------------------

@bot.event
async def on_ready():
    if not update_status.is_running():
        update_status.start()

    await bot.tree.sync()
    print(f"Logged in as {bot.user} — Slash commands synced!")

# ------------------ Run Bot ------------------
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable missing!")

bot.run(TOKEN)
