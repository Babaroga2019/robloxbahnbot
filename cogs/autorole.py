import discord
from discord.ext import commands

class AutoRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        # Die ID deiner gewünschten Rolle
        role_id = 1359493702510444614
        role = member.guild.get_role(role_id)

        if role is None:
            print(f"⚠️ Rolle mit ID {role_id} nicht gefunden.")
            return

        try:
            await member.add_roles(role, reason="AutoRole beim Beitritt")
            print(f"✅ Rolle '{role.name}' an {member} vergeben.")
        except discord.Forbidden:
            print("❌ Bot hat keine Berechtigung, die Rolle zu vergeben.")
        except Exception as e:
            print(f"❌ Fehler beim Hinzufügen der Rolle: {e}")

async def setup(bot):
    await bot.add_cog(AutoRole(bot))
