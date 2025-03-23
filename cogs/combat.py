import discord
from discord.ext import commands
from main import ids
from datetime import datetime,timedelta
from sqlalchemy import create_engine, Column, Integer, String,func
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import User,Bank,Inventory,Stocks,Server,CommunityMarket

engine = create_engine('sqlite:///UserInfo.db')
Session = sessionmaker(bind=engine)
session = Session()
class StilBorbe(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Štemerski Stil", style=discord.ButtonStyle.primary, emoji="🥊",
                       custom_id="Štemerski Stil")
    async def stemarski_stil(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Vas stil borbe je od sada Štemerski Stil")

    @discord.ui.button(label="Kavalirski Stil", style=discord.ButtonStyle.primary, emoji="🎩",
                       custom_id="Kavalirski Stil")
    async def kavalirski_stil(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Vas stil borbe je od sada Kavalirski Stil")

    @discord.ui.button(label="Konobarski Stil", style=discord.ButtonStyle.primary, emoji="🍺",
                       custom_id="Konobarski Stil")
    async def konobarski_stil(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Vas stil borbe je od sada Konobarski Stil")

    @discord.ui.button(label="Purger Stil", style=discord.ButtonStyle.primary, emoji="🏙️", custom_id="Purger Stil")
    async def purger_stil(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Vas stil borbe je od sada Purger Stil")

    @discord.ui.button(label="Trgovački Stil", style=discord.ButtonStyle.primary, emoji="💰",
                       custom_id="Trgovački Stil")
    async def trgovacki_stil(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Vas stil borbe je od sada Trgovački Stil")


class Stil():
    def __init__(self, name, attack, defence, stamina, health, crit_chance, crit_damage, miss_chance):
        self.name = name
        self.attack = attack
        self.defence = defence
        self.health = health
        self.stamina = stamina
        self.crit_chance = crit_chance
        self.crit_damage = crit_damage
        self.miss_chance = miss_chance
stilovi = {
        "Štemerski Stil": Stil("Štemerski Stil", 15, 5, 70, 100, 0.3, 2, 0.1),
        "Kavalirski Stil": Stil("Kavalirski Stil", 8, 20, 100, 120, 0.1, 1.5, 0.4),
        "Konobarski Stil": Stil("Konobarski Stil", 7, 20, 100, 150, 0.1, 1.5, 0.2),
        "Purger Stil": Stil("Purger Stil", 10, 10, 100, 100, 0.1, 1.5, 0.2),
        "Trgovački Stil": Stil("Trgovački Stil", 5, 5, 80, 80, 0.1, 1.3, 0.15)

    }

class Combat(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    @commands.command(aliases=['stilovi'])
    async def stilovi_borbe(self,ctx):
        stilovi = discord.Embed(title="Stilovi borbe", color=discord.Color.dark_blue())
        stilovi.add_field(name="Štemerski Stil 🥊💥",
                          value="✅Prednosti: Brzi i snazni udarci, velika sansa za kriticne pogotke.\n❌Nedostaci: Slaba obrana, veća potrošnja energije/stamine.",
                          inline=False)
        stilovi.add_field(name="Kavalirski Stil 🎩🛡️",
                          value="✅Prednosti: Dobra obrana, veća šansa za izbjegavanje napada.\n❌Nedostatci: Manja šteta po udarcu, sporiji napadi.",
                          inline=False)
        stilovi.add_field(name="Konobarski Stil 🍺🪑",
                          value="✅Prednosti: Visok nivo zdravlja, može preživjeti duge borbe.\n❌Nedostaci: Nema jake i brze napade.",
                          inline=False)
        stilovi.add_field(name="Purger Stil 🏙️⚖️",
                          value="✅Prednosti: Dobro izbalansiran napad i obrana.\n❌Nedostaci: Nema ekstremne prednosti u nekom segmentu.",
                          inline=False)
        stilovi.add_field(name="Trgovački Stil 💰📜",
                          value="✅Prednosti: Može koristiti novac ili resurse za jačanje napada.\n❌Nedostaci: Ovisi o resursima, slabiji u svakom ostalom segmentu.",
                          inline=False)
        await ctx.send(embed=stilovi)

    @commands.command(aliases=['stil'])
    async def stil_borbe(self,ctx):
        if str(ctx.author.id) in ids():
            user = session.query(User).filter_by(id=str(ctx.author.id)).first()
            fight_style = session.query(User).filter_by(id=str(ctx.author.id)).first().fight_style
            last_selection_fight_style_date = datetime.strptime(user.last_fight_style_selection,
                                                                "%M-%H-%d-%m-%Y") + timedelta(minutes=15)
            if last_selection_fight_style_date < datetime.now():
                await ctx.send(f"Vas stil borbe je {fight_style}", view=StilBorbe())

                @self.bot.listen()
                async def on_interaction(interaction: discord.Interaction):
                    if interaction.type == discord.InteractionType.component:
                        stil = interaction.data.get("custom_id")
                        now = datetime.now()
                        user.last_fight_style_selection = now.strftime("%M-%H-%d-%m-%Y")
                        user.fight_style = str(stil)
                        session.commit()
            else:
                await ctx.send("Morate pricekati 15 minuta nakon biranja stila borbe kako bi ste opet birali stil")

        else:
            await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")
async def setup(bot):
    await bot.add_cog(Combat(bot))