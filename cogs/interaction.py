import discord
from discord.ext import commands
from main import ids
from sqlalchemy import create_engine, Column, Integer, String,func
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import User,Bank,Inventory,Stocks,Server,CommunityMarket

engine = create_engine('sqlite:///UserInfo.db')
Session = sessionmaker(bind=engine)
session = Session()


class TestMenuButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="✔",style=discord.ButtonStyle.green,custom_id="positive")
    async def button_func_green(selfself,interaction:discord.Interaction,button:discord.ui.Button):
        pass
    @discord.ui.button(label="❌",style=discord.ButtonStyle.red,custom_id="negative")
    async def button_func_red(selfself,interaction:discord.Interaction,button:discord.ui.Button):
        pass


class Interaction(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def trade(self,ctx):
        if str(ctx.author.id) in ids():
            message = ctx.message.content
            message = message.split(" ")
            if len(message) == 2:
                user = message[1][2:-1]
                if str(user) in ids():
                    inv_user2 = session.query(Inventory).filter_by(user_id=str(user)).first()
                    user2 = session.query(User).filter_by(id=str(user)).first()
                    embed = discord.Embed(
                        title=f"{user2.name} stvari",
                        color=discord.Color.blue()
                    )
                    for i in inv_user2.items:
                        embed.add_field(name=i, value=inv_user2.items[i], inline=True)
                    await ctx.send(embed=embed)
            if len(message) == 6:
                user = message[1][2:-1]
                proizvod_za_dati = message[2]
                kolicina_za_dati = message[3]
                proizvod_za_primati = message[4]
                kolicina_za_primati = message[5]
                if str(user) in ids():
                    inv_user2 = session.query(Inventory).filter_by(user_id=str(user)).first()
                    poruka_primatelju = f"{ctx.author.name} ti je poslao {kolicina_za_dati} {proizvod_za_dati} za {kolicina_za_primati} {proizvod_za_primati}, ako prihvacas pritisni tipku ✔ ako odbijas pritisni tipku ❌"
                    user_to_send = await self.bot.fetch_user(user)
                    await user_to_send.send(poruka_primatelju, view=TestMenuButton())

                    @self.bot.listen()
                    async def on_interaction(interaction: discord.Interaction):
                        user = message[1][2:-1]
                        user2 = session.query(User).filter_by(id=str(user)).first()
                        if interaction.type == discord.InteractionType.component:
                            custom_id = interaction.data.get("custom_id")
                            if custom_id == "positive":
                                await interaction.response.send_message("Korisnik je prihvatio", ephemeral=True)
                                inv_user = session.query(Inventory).filter_by(user_id=str(ctx.author.id)).first()
                                inv_user2 = session.query(Inventory).filter_by(user_id=str(user)).first()
                                if proizvod_za_dati in inv_user.items and int(kolicina_za_dati) <= int(
                                        inv_user.items[proizvod_za_dati]):
                                    inv_user.items[proizvod_za_dati] -= int(kolicina_za_dati)
                                    inv_user2.items[proizvod_za_primati] -= int(kolicina_za_primati)
                                    if proizvod_za_dati in inv_user2.items:
                                        inv_user2.items[proizvod_za_dati] += int(kolicina_za_dati)
                                    else:
                                        inv_user2.items[proizvod_za_dati] = int(kolicina_za_dati)
                                    if proizvod_za_primati in inv_user.items:
                                        inv_user.items[proizvod_za_primati] += int(kolicina_za_primati)
                                    else:
                                        inv_user.items[proizvod_za_primati] = int(kolicina_za_primati)
                                    flag_modified(inv_user, "items")
                                    flag_modified(inv_user2, "items")
                                    session.commit()
                                other_user = ctx.author.id
                                user_to_send = await self.bot.fetch_user(other_user)
                                await user_to_send.send(
                                    f"Korisnik {user2.name} je prihvatio trade, dobili ste {kolicina_za_primati} {proizvod_za_primati} i  izgubili ste {kolicina_za_dati} {proizvod_za_dati}")
                            elif custom_id == "negative":
                                await interaction.response.send_message("Odbili ste trade i nece biti izvrsen",
                                                                        ephemeral=True)
                                other_user = ctx.author.id
                                user_to_send = await self.bot.fetch_user(other_user)
                                await user_to_send.send(f"Korisnik {user2.name} je odbio trade")

                else:
                    await ctx.send("Korisnik nije pronaden, upisite postojeceg korisnika!")
            else:
                await ctx.send(
                    "Pogresan format komande! Upisi !trade <@korisnik> <proizvod koji primas> <kolicina> <proizvod koji dajes> <kolicina>")

        else:
            await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")

    @commands.command(aliases=['bal'])
    async def stanje(self,ctx):
        check_ids = ids()
        if str(ctx.author.id) in check_ids:
            await ctx.send(
                f"Tvoje stanje je: {str(session.query(Bank).filter_by(user_id=str(ctx.author.id)).first().money)}kn")
        else:
            await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")

    @commands.command(aliases=['inv'])
    async def stvari(self,ctx):
        check_ids = ids()
        stvari_embed = discord.Embed(
            title="Tvoje stvari",
            description="Ovo su tvoje stvari",
            color=discord.Color.blue()
        )
        if str(ctx.author.id) in check_ids:
            inventory = session.query(Inventory).filter_by(user_id=str(ctx.author.id)).first()
            for stvar, kolicina in inventory.items.items():
                stvari_embed.add_field(name=stvar, value=kolicina, inline=True)
            await ctx.send(embed=stvari_embed)
        else:
            await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")
    @commands.command()
    async def pokloni(self,ctx):
        if str(ctx.author.id) in ids():
            message = ctx.message.content
            message = message.split(" ")
            if len(message) == 4:
                user = message[1][2:-1]
                stvar = message[2]
                kolicina = message[3]
                if kolicina.isdigit() == False:
                    await ctx.send("Kolicina mora biti broj!")
                else:
                    if str(user) in ids():
                        user2_inv = session.query(Inventory).filter_by(user_id=str(user)).first()
                        inv_user = session.query(Inventory).filter_by(user_id=str(ctx.author.id)).first()
                        user_name = session.query(User).filter_by(id=str(user)).first()
                        if stvar in inv_user.items and int(kolicina) <= int(inv_user.items[stvar]):
                            inv_user.items[stvar] -= int(kolicina)
                            if stvar in user2_inv.items:
                                user2_inv.items[stvar] += int(kolicina)
                            else:
                                user2_inv.items[stvar] = int(kolicina)
                            flag_modified(inv_user, "items")
                            flag_modified(user2_inv, "items")
                            session.commit()
                            await ctx.send(
                                f"Korisnik {ctx.author.mention} je poklonio {kolicina} {stvar} korisniku {user_name.name}")
            else:
                await ctx.send("Pogresan format komande! Upisi !pokloni <@korisnik> <stvar> <kolicina>")
        else:
            await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")

    @commands.command()
    async def plati(self,ctx):
        if str(ctx.author.id) in ids():
            message = ctx.message.content
            message = message.split(" ")
            if len(message) == 3:
                user = message[1][2:-1]
                kolicina = message[2]
                if kolicina.isdigit() == False:
                    await ctx.send("Kolicina mora biti broj!")
                else:
                    if str(user) in ids():
                        user1_bank = session.query(Bank).filter_by(user_id=str(ctx.author.id)).first()
                        user2_bank = session.query(Bank).filter_by(user_id=str(user)).first()
                        user_name = session.query(User).filter_by(id=str(user)).first()
                        if user1_bank.money >= int(kolicina):
                            user1_bank.money -= int(kolicina)
                            user2_bank.money += int(kolicina)
                            session.commit()
                            await ctx.send(
                                f"Korisnik {ctx.author.mention} je platio {kolicina}kn korisniku {user_name.name}")
                        elif user1_bank.money < int(kolicina):
                            await ctx.send("Korisnik nema dovoljno novca!")
                        elif int(kolicina) < 0:
                            await ctx.send("Nemozete dati negativnu kolicinu!")
                        else:
                            await ctx.send("Nesto se spigalo.")
            else:
                await ctx.send("Pogresan format komande! Upisi !plati <@korisnik> <kolicina>")


        else:
            await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")
async def setup(bot):
    await bot.add_cog(Interaction(bot))