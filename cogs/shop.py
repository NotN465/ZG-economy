import discord
from discord.ext import commands
from main import proizvodi,ids
from sqlalchemy import create_engine, Column, Integer, String,func
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import User,Bank,Inventory,Stocks,Server,CommunityMarket

engine = create_engine('sqlite:///UserInfo.db')
Session = sessionmaker(bind=engine)
session = Session()
class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ducan(self,ctx):
        embed = discord.Embed(
            title="Ducan",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Proizvodi i njihove cijene")
        await ctx.send(embed=embed)
        for key, value in proizvodi.items():
            new_embed = discord.Embed(
                title=key,
                color=discord.Color.blue()
            )
            for keyX, valueX in value.items():
                new_embed.add_field(name=keyX, value=valueX, inline=True)
            await ctx.send(embed=new_embed)

    @commands.command()
    async def kupi(self,ctx):

        if str(ctx.author.id) in ids():
            raw_message = ctx.message.content
            raw_message = raw_message.split(" ")
            if len(raw_message) == 3 or len(raw_message) == 2:
                proizvod = str(raw_message[1]).lower().capitalize()
                kolicina = int(raw_message[2])
                for key in proizvodi.keys():
                    if proizvod in proizvodi[key]:
                        user_bank = session.query(Bank).filter_by(user_id=str(ctx.author.id)).first()
                        VrijednostProizvoda = kolicina * proizvodi[key][proizvod]
                        if user_bank.money >= VrijednostProizvoda:
                            user_bank.money -= VrijednostProizvoda
                            await ctx.send(f"Kupili ste {kolicina} {proizvod} za {VrijednostProizvoda}kn")
                            user_items = session.query(Inventory).filter_by(user_id=str(ctx.author.id)).first()
                            if not isinstance(user_items.items, dict):
                                user_items.items = {}
                            if proizvod in user_items.items:
                                user_items.items[proizvod] += kolicina
                            else:
                                user_items.items[proizvod] = kolicina
                            flag_modified(user_items, "items")
                            session.commit()
                        else:
                            await ctx.send("Nemate dovoljno novca!")
            else:
                await ctx.send("Pogresan format komande! Upisi !kupi <proizvod> <kolicina>")

        else:
            await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")
async def setup(bot):
    await bot.add_cog(Shop(bot))