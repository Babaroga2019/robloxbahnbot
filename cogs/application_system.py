import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button, Select
import sqlite3
import json
from datetime import datetime, timedelta

BEWERBUNG_CHANNEL_ID = 1381561768530149436
ADMIN_APPLICATION_CHANNEL_ID = 1381561845428654181

# --- DB-Funktionen ---

def init_db():
    conn = sqlite3.connect("application_data.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            user_id INTEGER PRIMARY KEY,
            data_json TEXT DEFAULT '{}',
            posten TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS blocked_users (
            user_id INTEGER PRIMARY KEY,
            blocked_until TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_application(user_id, data, posten):
    conn = sqlite3.connect("application_data.db")
    c = conn.cursor()
    data_str = json.dumps(data)
    c.execute("""
        INSERT OR REPLACE INTO applications (user_id, data_json, posten)
        VALUES (?, ?, ?)
    """, (user_id, data_str, posten))
    conn.commit()
    conn.close()

def delete_application(user_id):
    conn = sqlite3.connect("application_data.db")
    c = conn.cursor()
    c.execute("DELETE FROM applications WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

def is_user_blocked(user_id):
    conn = sqlite3.connect("application_data.db")
    c = conn.cursor()
    c.execute("SELECT blocked_until FROM blocked_users WHERE user_id=?", (user_id,))
    result = c.fetchone()
    conn.close()
    if result:
        blocked_until = datetime.fromisoformat(result[0])
        if blocked_until > datetime.utcnow():
            return True, blocked_until
        else:
            remove_block(user_id)
            return False, None
    return False, None

def block_user(user_id, weeks=6):
    blocked_until = datetime.utcnow() + timedelta(weeks=weeks)
    conn = sqlite3.connect("application_data.db")
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO blocked_users (user_id, blocked_until)
        VALUES (?, ?)
    """, (user_id, blocked_until.isoformat()))
    conn.commit()
    conn.close()

def remove_block(user_id):
    conn = sqlite3.connect("application_data.db")
    c = conn.cursor()
    c.execute("DELETE FROM blocked_users WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

init_db()

# --- Bewerbung Cog ---

class ApplicationView(View):
    def __init__(self, user):
        super().__init__(timeout=180)  # 3 Minuten Timeout
        self.user = user
        self.result = None

    @discord.ui.select(
        placeholder="Wähle deinen gewünschten Posten",
        options=[
            discord.SelectOption(label="Developer"),
            discord.SelectOption(label="Builder"),
            discord.SelectOption(label="Designer"),
            discord.SelectOption(label="Moderator"),
        ],
    )
    async def posten_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        if interaction.user != self.user:
            await interaction.response.send_message("Das ist nicht für dich.", ephemeral=True)
            return
        self.result = select.values[0].lower()
        self.stop()

        gewaehlter_posten = select.values[0]
        await interaction.response.send_message(f"Du hast {gewaehlter_posten} ausgewählt!", ephemeral=True)

    async def on_timeout(self):
        try:
            await self.user.send("⏰ Deine Bewerbung wurde abgebrochen, weil du nicht reagiert hast.")
        except:
            pass

class ConfirmationView(View):
    def __init__(self, user):
        super().__init__(timeout=120)
        self.user = user
        self.confirmed = None

    @discord.ui.button(label="Ja, abschicken", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("Nicht für dich.", ephemeral=True)
            return
        self.confirmed = True
        self.stop()
        await interaction.response.edit_message(content="✅ Bewerbung wird abgeschickt...", view=None)

    @discord.ui.button(label="Nein, abbrechen", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            return await interaction.response.send_message("Nicht für dich.", ephemeral=True)
        self.confirmed = False
        self.stop()
        await interaction.response.edit_message(content="❌ Bewerbung wurde abgebrochen.", view=None)

    async def on_timeout(self):
        try:
            await self.user.send("⏰ Zeitüberschreitung: Bewerbung wurde abgebrochen.")
        except:
            pass

class Bewerbung(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bewerben", description="Starte eine neue Bewerbung per DM")
    async def bewerben(self, interaction: discord.Interaction):
        # Check block
        blocked, until = is_user_blocked(interaction.user.id)
        if blocked:
            return await interaction.response.send_message(
                f"⛔ Du bist bis {until.strftime('%d.%m.%Y')} gesperrt.", ephemeral=True)

        # Check open application
        conn = sqlite3.connect("application_data.db")
        c = conn.cursor()
        c.execute("SELECT * FROM applications WHERE user_id=?", (interaction.user.id,))
        if c.fetchone():
            conn.close()
            return await interaction.response.send_message("❌ Du hast bereits eine offene Bewerbung.", ephemeral=True)
        conn.close()

        await interaction.response.send_message("Ich starte deine Bewerbung per DM.", ephemeral=True)

        try:
            dm = await interaction.user.create_dm()
        except:
            return await interaction.followup.send("❌ Ich konnte dir keine DM schicken. Bitte aktiviere DMs vom Server.", ephemeral=True)

        # 1. Posten wählen
        view = ApplicationView(interaction.user)
        posten_msg = await dm.send("Willkommen zu deiner Bewerbung! Bitte wähle deinen gewünschten Posten aus:", view=view)
        await view.wait()
        if view.result is None:
            return  # Timeout, schon informiert

        posten = view.result

        # Fragen
        fragen = [
            ("Vorname", "Wie ist dein Vorname?"),
            ("Alter", "Wie alt bist du?"),
            ("Praktische Erfahrung", "Beschreibe deine praktische Erfahrung."),
            ("Roblox Erfahrung", "Welche Roblox-Erfahrung hast du?"),
            ("Fähigkeiten", "Welche Fähigkeiten bringst du mit?"),
            ("Stärken und Schwächen", "Was sind deine Stärken und Schwächen?"),
            ("Teamerfahrung", "Hast du Teamerfahrung?"),
            ("Andere Projekte", "Nenne andere Projekte, an denen du mitgewirkt hast."),
            ("Letzte Worte", "Möchtest du noch etwas hinzufügen? (optional)"),
        ]

        answers = {}
        def check(m):
            return m.author == interaction.user and m.channel == dm

        for key, frage in fragen:
            await dm.send(frage)
            try:
                antwort = await self.bot.wait_for('message', check=check, timeout=300)
                answers[key] = antwort.content if antwort.content.strip() != "" else "Keine Angabe"
            except:
                await dm.send("⏰ Du hast zu lange nicht geantwortet. Bewerbung abgebrochen.")
                return

        # Zusammenfassung
        embed = discord.Embed(title=f"Bewerbung für {posten.capitalize()}",
                              description=f"Hier sind deine Antworten:\n\n",
                              color=discord.Color.green())
        for key in answers:
            embed.add_field(name=key, value=answers[key], inline=False)

        embed.set_footer(text="Bitte bestätige unten, ob du die Bewerbung abschicken möchtest.")

        confirm_view = ConfirmationView(interaction.user)
        await dm.send(embed=embed, view=confirm_view)
        await confirm_view.wait()

        if confirm_view.confirmed:
            # Speichern
            save_application(interaction.user.id, answers, posten)
            # Bewerbung an Admin-Channel senden
            channel = self.bot.get_channel(ADMIN_APPLICATION_CHANNEL_ID)
            if channel:
                admin_embed = discord.Embed(
                    title=f"Neue Bewerbung: {posten.capitalize()}",
                    description=f"Von {interaction.user.mention} ({interaction.user.id})",
                    color=discord.Color.blue(),
                    timestamp=datetime.utcnow()
                )
                for key, val in answers.items():
                    admin_embed.add_field(name=key, value=val, inline=False)

                view = AdminApplicationView(self.bot, interaction.user.id)
                await channel.send(embed=admin_embed, view=view)

            await dm.send("✅ Deine Bewerbung wurde erfolgreich abgeschickt. Viel Erfolg!")
        else:
            await dm.send("❌ Bewerbung wurde nicht abgeschickt.")

        # Bewerbungsdaten löschen (je nach Wunsch hier oder später)
        # delete_application(interaction.user.id)

class AdminApplicationView(View):
    def __init__(self, bot, user_id):
        super().__init__(timeout=None)  # Kein Timeout
        self.bot = bot
        self.user_id = user_id

    @discord.ui.button(label="Annehmen", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Nur Admins dürfen
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("Keine Berechtigung.", ephemeral=True)

        # Bewerbung löschen und User informieren
        delete_application(self.user_id)
        try:
            user = await self.bot.fetch_user(self.user_id)
            await user.send("✅ Deine Bewerbung wurde angenommen. Willkommen im Team!")
        except:
            pass

        await interaction.response.edit_message(content="✅ Bewerbung wurde angenommen.", embed=None, view=None)

    @discord.ui.button(label="Ablehnen", style=discord.ButtonStyle.red)
    async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("Keine Berechtigung.", ephemeral=True)

        # User blockieren für 6 Wochen
        block_user(self.user_id, weeks=6)
        delete_application(self.user_id)

        try:
            user = await self.bot.fetch_user(self.user_id)
            await user.send("❌ Deine Bewerbung wurde leider abgelehnt. Du kannst dich in 6 Wochen erneut bewerben.")
        except:
            pass

        await interaction.response.edit_message(content="❌ Bewerbung wurde abgelehnt und Nutzer blockiert.", embed=None, view=None)

    @app_commands.command(name="blockieren", description="Blockiere einen Benutzer manuell für Bewerbungen")
    @app_commands.checks.has_role(1383490085630246952)
    async def blockieren(self, interaction: discord.Interaction, user: discord.User, wochen: int = 6):

        # Blockiere den Benutzer
        block_user(user.id, weeks=wochen)

        await interaction.response.send_message(
            f"✅ {user.mention} wurde für {wochen} Wochen blockiert.", ephemeral=True)

        try:
            await user.send(f"⛔ Du wurdest von der Bewerbung ausgeschlossen. Du kannst dich erst wieder in {wochen} Wochen bewerben.")
        except:
            pass

    @blockieren.error
    async def announcement_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message("Du hast keine Berechtigung für diesen Befehl.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Bewerbung(bot))
