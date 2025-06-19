import discord
from discord import app_commands
from discord.ext import commands
import json
import os

class InfoSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_embed(self, name: str):
        """Gibt das richtige Embed zurück"""
        if name == "regeln":
            embed = discord.Embed(
                title="📜 Server-Regeln",
                description="Willkommen auf unserem Discord-Server! Lies dir die Regeln sorgfältig durch.",
                color=discord.Color.blue()
            )

            embed.add_field(
                name="1. Allgemeines Verhalten",
                value="Sei respektvoll gegenüber anderen Mitgliedern. Beleidigungen, Diskriminierung oder Schikanen sind nicht erlaubt.",
                inline=False
            )

            embed.add_field(
                name="2. Kein Spam & Werbung",
                value="Vermeide unnötige Nachrichten, Emojis oder Links. Unverlangte Werbung ist untersagt.",
                inline=False
            )

            embed.add_field(
                name="3. NSFW-Inhalte verboten",
                value="Sexuell explizite, gewalttätige oder unangemessene Inhalte (auch Bilder, Videos, Links) sind strikt untersagt – auch in Profilen oder Statusnachrichten.",
                inline=False
            )

            embed.add_field(
                name="4. Sprache & Rechtschreibung",
                value="Schreibe in klarer, verständlicher Sprache. Groß- und Kleinschreibung beachten. Spam von Zeichen wie 'xddd' oder 'brooooo' ist nicht erwünscht.",
                inline=False
            )

            embed.add_field(
                name="5. Respektiere die Moderation",
                value="Die Moderatoren vertreten die Regeln. Folge ihren Anweisungen. Widerspruch oder Provokation gegenüber Mods/Admins wird bestraft.",
                inline=False
            )

            embed.add_field(
                name="6. Nickname & Profil",
                value="Dein Name und Profilbild sollten angemessen sein. Keine beleidigenden, NSFW oder unklaren Namen/Bilder.",
                inline=False
            )

            embed.add_field(
                name="7. Voice-Chats",
                value="Sprich deutlich und laut genug, damit dich alle verstehen können. Nutze keine störenden Töne oder Mikrofon-Test-Sounds.",
                inline=False
            )

            embed.add_field(
                name="8. Spoiler & Sensitives Material",
                value="Spoiler müssen markiert werden. Sensitives Material (z. B. Horrorbilder, politisch heikle Themen) nur mit Zustimmung der Moderation.",
                inline=False
            )

            embed.set_footer(
                text="⚠️ Verstöße gegen diese Regeln führen zu Verwarnungen, Mutes, Kicks oder einem Bann.",
                icon_url="https://cdn.discordapp.com/attachments/1359491782483644577/1385288205405782036/logoneu.png?ex=685585ad&is=6854342d&hm=fe3d8e34eb208ba736d8e9fe2b03b85e390169978d88ce3bd981497cc24df5be&"
            )

            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1359491782483644577/1381557068346949683/ChatGPT_Image_9._Juni_2025_10_02_10.png?ex=6847f2c9&is=6846a149&hm=b1c7720691e7c81cc52a982b2ff34d885f4f4779383749460a7e6f30791236cc&")
            
            return embed
        elif name == "text-support":
            embed = discord.Embed(
                title="💬 Text-Support",
                description="Willkommen im Text-Support-Bereich! Hier bekommst du Hilfe zu deinen Fragen.",
                color=discord.Color.green()
            )

            embed.add_field(
                name="🛠️ Wofür ist dieser Support?",
                value="Melde dich hier, wenn du Fragen zum Server, zu Regeln oder technischen Themen hast.",
                inline=False
            )

            embed.add_field(
                name="🧑‍🔧 Unser Team",
                value="Unsere Supporter helfen dir gerne weiter. Sei höflich und stelle deine Frage klar – dann können wir dir am schnellsten helfen!",
                inline=False
            )

            embed.add_field(
                name="📝 Wie melde ich mich an?",
                value="Wenn du Unterstützung brauchst, schreibe einfach:\n`@[🛡️]` + deine Frage.\nEin Supporter meldet sich baldmöglichst bei dir.",
                inline=False
            )

            embed.add_field(
                name="💡 Tipps für deine Anfrage",
                value="• Gib so viele Details wie möglich\n• Schreibe in ganzen Sätzen\n• Sei geduldig – wir sind ehrenamtlich hier",
                inline=False
            )

            embed.set_footer(
                text="Hinweis: Keine dringenden oder Notfall-Anfragen hier – dafür gibt es den Voice-Support.",
                icon_url="https://cdn.discordapp.com/emojis/123456789012345678.png?size=64"
            )

            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1359491782483644577/1385288205405782036/logoneu.png?ex=685585ad&is=6854342d&hm=fe3d8e34eb208ba736d8e9fe2b03b85e390169978d88ce3bd981497cc24df5be&") 

            return embed
        elif name == "roblox-bahn":
            embed = discord.Embed(
                title="🚆 Was ist Roblox Bahn?",
                description="Roblox Bahn ist ein realistischer Simulator auf Roblox, der echte deutsche Züge und maßstabsgetreue Strecken nachbildet.",
                color=discord.Color.orange()
            )

            embed.add_field(
                name="🚄 Realismus pur",
                value="Der Simulator verwendet originalgetreu nachgebaute Züge wie den BR 622 oder BR 648, inklusive korrekter Steuerung und Fahrphysik.",
                inline=False
            )

            embed.add_field(
                name="📏 Maßstabsgetreue Strecken",
                value="Die Gleisführungen sind exakt nach realen Vorbildern gebaut – mit richtigen Entfernungen, Haltestellen und Signaltechnik.",
                inline=False
            )

            embed.add_field(
                name="🚦 Wie im echten Leben",
                value="Du musst dich an Fahrpläne halten, Signale beachten und korrekt beschleunigen/abbremsen – ideal für alle Eisenbahn-Fans!",
                inline=False
            )

            embed.add_field(
                name="👥 Community & Multiplayer",
                value="Fahre gemeinsam mit Freunden oder anderen Spielern. Es gibt auch aktive Communities, die Server hosten und Events organisieren.",
                inline=False
            )

            embed.set_footer(
                text="💡 Tipp: Melde dich im Text-Support, wenn du Hilfe beim Einstieg brauchst!",
                icon_url="https://cdn.discordapp.com/emojis/123456789012345678.png?size=64"
            )

            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1359491782483644577/1385288205405782036/logoneu.png?ex=685585ad&is=6854342d&hm=fe3d8e34eb208ba736d8e9fe2b03b85e390169978d88ce3bd981497cc24df5be&") 

            return embed
        elif name == "bewerben":
            embed = discord.Embed(
                title="📨 Bewirb dich jetzt!",
                description="Du möchtest Teil unseres Teams werden? Hier erfährst du, wie du dich ganz einfach bewerben kannst.",
                color=discord.Color.purple()
            )

            embed.add_field(
                name="🔍 Voraussetzungen",
                value="• Mindestalter: 14 Jahre\n• Freundlicher und respektvoller Umgang\n• Bereitschaft zur Zusammenarbeit im Team\n• Aktivität auf dem Server",
                inline=False
            )

            embed.add_field(
                name="📝 So funktioniert die Bewerbung",
                value="Gib einfach den Befehl `/bewerben` ein. Es öffnet sich ein Formular, in dem du deine Bewerbung ausfüllen kannst.",
                inline=False
            )

            embed.add_field(
                name="📌 Hinweis",
                value="Stelle sicher, dass du deine Angaben sorgfältig und vollständig machst. Unvollständige Bewerbungen werden nicht berücksichtigt.",
                inline=False
            )

            embed.set_footer(
                text="Viel Erfolg bei deiner Bewerbung! Dein Team von Roblox Bahn",
                icon_url="https://cdn.discordapp.com/emojis/123456789012345678.png?size=64"
            )

            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1359491782483644577/1385288205405782036/logoneu.png?ex=685585ad&is=6854342d&hm=fe3d8e34eb208ba736d8e9fe2b03b85e390169978d88ce3bd981497cc24df5be&")

            return embed
        else:
            return None

    @app_commands.command(name="setupinfo", description="Sendet ein vordefiniertes Embed und speichert es.")
    @app_commands.checks.has_role(1383490085630246952)
    async def setupinfo(self, interaction: discord.Interaction, name: str):
        embed = self.get_embed(name.lower())
        if not embed:
            await interaction.response.send_message(f"❌ Es gibt kein Embed mit dem Namen `{name}`.", ephemeral=True)
            return

        channel = interaction.channel
        message = await channel.send(embed=embed)

        # Speichere in JSON
        data_file = "data/info_messages.json"
        if not os.path.exists(data_file):
            data = {}
        else:
            with open(data_file, "r") as f:
                data = json.load(f)

        data[name.lower()] = {
            "channel_id": str(channel.id),
            "message_id": str(message.id)
        }

        with open(data_file, "w") as f:
            json.dump(data, f, indent=4)

        await interaction.response.send_message(f"✅ `{name}` wurde gesendet und gespeichert.", ephemeral=True)

    @setupinfo.error
    async def announcement_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message("Du hast keine Berechtigung für diesen Befehl.", ephemeral=True)

# Füge das Cog hinzu
async def setup(bot):
    await bot.add_cog(InfoSystem(bot))
