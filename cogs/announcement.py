import discord
from discord import app_commands
from discord.ext import commands

class AnnouncementModal(discord.ui.Modal, title="Verfasse eine Ankündigung"):
    title_input = discord.ui.TextInput(
        label="Titel",
        placeholder="Gib hier den Titel deiner Ankündigung ein...",
        required=True,
        max_length=256
    )

    content = discord.ui.TextInput(
        label="Inhalt",
        style=discord.TextStyle.paragraph,
        placeholder="Schreibe hier deine Nachricht...",
        required=True,
        max_length=4000
    )

    color = discord.ui.TextInput(
        label="Farbe (Englisch oder Hex)",
        placeholder="Beispiele: blue, red, #FF5733",
        required=False,
        max_length=100
    )

    mention_everyone = discord.ui.TextInput(
        label="@everyone erwähnen? (ja/nein)",
        placeholder="Schreibe 'ja' oder 'nein'",
        required=True,
        max_length=3
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Farbe parsen
        color_input = self.color.value.strip().lower()
        color_map = {
            "red": discord.Color.red(),
            "green": discord.Color.green(),
            "blue": discord.Color.blue(),
            "orange": discord.Color.orange(),
            "purple": discord.Color.purple(),
            "gold": discord.Color.gold(),
            "teal": discord.Color.teal(),
            "gray": discord.Color.greyple(),
            "pink": discord.Color.magenta()
        }

        if color_input in color_map:
            embed_color = color_map[color_input]
        else:
            try:
                # Versuche Hex-Farbe zu parsen
                hex_value = int(color_input.replace("#", ""), 16)
                embed_color = discord.Color(hex_value)
            except:
                embed_color = discord.Color.default()

        # Embed erstellen
        embed = discord.Embed(
            title=self.title_input.value,
            description=self.content.value,
            color=embed_color
        )
        embed.set_footer(text=f"Angekündigt von {interaction.user.display_name}", icon_url=interaction.user.avatar.url)

        # @everyone prüfen
        mention = ""
        if self.mention_everyone.value.lower() == "ja":
            if interaction.channel.permissions_for(interaction.guild.me).mention_everyone:
                mention = "@everyone"
            else:
                await interaction.response.send_message(
                    "❌ Ich habe keine Berechtigung, `@everyone` zu erwähnen.", ephemeral=True
                )
                return

        elif self.mention_everyone.value.lower() != "nein":
            await interaction.response.send_message(
                "❌ Ungültige Eingabe für `@everyone`. Gib entweder `ja` oder `nein` ein.", ephemeral=True
            )
            return

        # Nachrichten senden
        await interaction.response.send_message("✅ Deine Ankündigung wird gesendet...", ephemeral=True)

        if mention:
            await interaction.channel.send(mention)  # Separate Nachricht für @everyone

        await interaction.channel.send(embed=embed)  # Zweite Nachricht mit dem Embed

        await interaction.followup.send("📢 Deine Ankündigung wurde erfolgreich gesendet!", ephemeral=True)


class Announcement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="announcement", description="Sende eine schöne Ankündigung per Modal.")
    @app_commands.checks.has_role(1383490085630246952)
    async def announcement(self, interaction: discord.Interaction):
        modal = AnnouncementModal()
        await interaction.response.send_modal(modal)

    @announcement.error
    async def announcement_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message("Du hast keine Berechtigung für diesen Befehl.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Announcement(bot))
