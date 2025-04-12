import random
import time
from datetime import datetime,timedelta
import discord
from discord.ext import commands
from sqlalchemy import create_engine, Column, Integer, String,func
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import User,Bank,Inventory,Stocks,Server,CommunityMarket,Combat
import os
import json
import asyncio
import math
from cogs.Functions import level_xp,floor_decimal

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="zg ",intents=intents)

engine = create_engine('sqlite:///UserInfo.db')
Session = sessionmaker(bind=engine)
session = Session()

proizvodi = {"Hrana": {"Pica": 80, "Burek": 30, "Ćevapi": 70, "Cokolino": 20, "Sarma": 50},
             "Pica": {"Coca-cola": 20, "Cedevita": 15, "Rakija": 50, "Piva": 12, "Kava": 15, "Voda": 5},
             "Ostalo": {"Spin": 300}}


def ids():
    user = discord.User
    users = []
    user_info = session.query(User.id).all()
    if user_info == []:
        return ()
    for x in user_info:
        users.append(str(x[0]))
    return users
@bot.command()
async def provjeri_level(ctx):
    if str(ctx.author.id) in ids():
        user = session.query(User).filter_by(id=str(ctx.author.id)).first()
        level = level_xp(ctx.author.id)[0]
        await ctx.send(f"Tvoj level je {level}")
    else:
        await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")
'''
async def update_dionice(server_id):
    await bot.wait_until_ready()
    server = session.query(Server).filter_by(server_id=server_id).first()
    while not bot.is_closed():
        dionice_embed = discord.Embed(
            title="Dionice",
            description="Pogledaj dostupne dionice",
            color=discord.Color.dark_blue()
        )
        with open("stocks.json") as f:
            data = json.load(f)
        with open("prev_stocks.json") as f:
            prev_data = json.load(f)
        prev_dionice = dict()
        round_num = 3
        for stock, price in data.items():
            if prev_data[stock] > price:
                dionice_embed.add_field(name=f"📉 **{stock}**", value=f"Cijena: {round(price, round_num)} (-{round(prev_data[stock] - price,round_num)})", inline=False)
            else:
                dionice_embed.add_field(name=f"📈 **{stock}**", value=f"Cijena: {round(price,round_num)} (+{round(price - prev_data[stock],round_num)})", inline=False)
            prev_dionice[stock] = price
        with open("prev_stocks.json", "w") as f:
            json.dump(prev_dionice, f)
        try:
            chanel = bot.get_channel(int(server.stock_market_channel_id))
            message = await chanel.fetch_message(int(server.message_stock_market_id))
            await message.edit(embed=dionice_embed)
        except:
            pass
        await asyncio.sleep(15)
'''
async def update_dionice(server_id):
    await bot.wait_until_ready()
    while not bot.is_closed():
        session.expire_all()
        server = session.query(Server).all()
        if len(list(server)) == 0:
            first_server =Server(server_id=914183541103919215,stock_market_channel_id=1340120438491189349,message_stock_market_id=1340478597290397760,stocks={"Temp":10})
            session.add(first_server)
            session.commit()
        server = session.query(Server).filter_by(server_id=server_id).first()
        dionice_embed = discord.Embed(
            title="Dionice",
            description="Pogledaj dostupne dionice",
            color=discord.Color.dark_blue()
        )
        for stock,price in server.stocks.items():
            dionice_embed.add_field(name=stock, value=f"Cijena: {round(price,2)}kn", inline=False)
        try:
            chanel = bot.get_channel(server.stock_market_channel_id)
            message = await chanel.fetch_message(int(server.message_stock_market_id))
            await message.edit(embed=dionice_embed)
        except:
            pass
        await asyncio.sleep(15)
async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != 'Functions.py':
            await bot.load_extension(f'cogs.{filename[:-3]}')
async def main():
    async with bot:
        await load()
        with open('token.txt', 'r') as f:
            token = f.read()
        await bot.start(token)
@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')
    for guild in bot.guilds:
        asyncio.create_task(update_dionice(int(guild.id)))
@bot.command()
async def NapraviProfil(ctx):
    check_ids = ids()
    if str(ctx.author.id) in check_ids:
        await ctx.send("Vec imas racun!")
    else:
        now = (datetime.now() - timedelta(hours=4)).strftime("%M-%H-%d-%m-%Y")
        user = User(name=str(ctx.author.name), id=str(ctx.author.id),posao="Nema"
                    ,xp=0,chop_xp=0,mine_xp=0,fishing_xp=0
                    ,last_fishing_time=now,last_mine_time=now,last_chop_time=now
                    ,fight_style="Nema",last_fight_style_selection=now,last_fight_time=now,lokacija="Park Maksimir")

        money = Bank(money=50, savings=0, user_id=str(ctx.author.id), last_work_time=now)
        invetory = Inventory(items={}, user_id=str(ctx.author.id))
        stocks = Stocks(stocks={},user_id=str(ctx.author.id))
        combat = Combat(health=100,last_hunt_time=now,equipment={},user_id=str(ctx.author.id),attack=10,defence=0,remaining_health=100)
        session.add(money)
        session.add(user)
        session.add(invetory)
        session.add(stocks)
        session.add(combat)
        session.commit()
        await ctx.send("Racun je napravljen!")
@bot.command(aliases=['p'])
async def profil(ctx):
    if str(ctx.author.id) in ids():
        profile_embed = discord.Embed(
            title="Profil od: " + str(ctx.author.name),
            color=discord.Color.dark_blue(),
        )
        user = session.query(User).filter_by(id=str(ctx.author.id)).first()
        money = session.query(Bank).filter_by(user_id=str(ctx.author.id)).first()
        combat = session.query(Combat).filter_by(user_id=str(ctx.author.id)).first()

        profile_embed.set_thumbnail(url=ctx.author.avatar.url)
        profile_embed.add_field(name="XP/Level", value=f"Level: {level_xp(ctx.author.id)[0]}\nXP: {level_xp(ctx.author.id)[1]}/{level_xp(ctx.author.id)[2]}", inline=False)
        profile_embed.add_field(name="Stats",value=f":heart: Zdravlje: {combat.remaining_health}/{combat.health}\n:crossed_swords:Napad: {combat.attack}\n🛡Obrana: {combat.defence}", inline=False)
        profile_embed.add_field(name="Naoruzanje",value=f"Oprema: {combat.equipment}", inline=False)
        profile_embed.add_field(name="Posao",value=f":hammer_pick: Posao: {user.posao}", inline=False)
        profile_embed.add_field(name="Lokacija",value=f":map: Lokacija: {user.lokacija}", inline=False)
        profile_embed.add_field(name="Pare",value=f"💵Pare: {money.money}", inline=False)

        await ctx.send(embed=profile_embed)
    else:
        await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")
@bot.event
async def on_command_error(ctx, error):
    raise error
prvi_sektor_poslovi = {"Farmer": 900, "Ribar": 900, "Rudar": 950 , "Drvosječa": 1000, "Lovac": 1000, "Pčelar": 800, "Vinogradar": 1200, "Voćar": 950, "Cvjećar": 850, "Stožar": 900}
drugi_sektor_poslovi = {"Radnik u tvornici": 1200, "Zidar":1100, "Bravar":1050, "Električar":1700, "Stolar":1300, "Automehaničar": 1500, "Kovač": 1200, "Vodoinstalater": 1700, "Tekstilni radnik": 1050, "Keramičar": 1800}
treci_sektor_poslovi = {"Liječnik": 2500, "Pravni savjetnik": 2000, "Inženjer": 2000, "Profesor": 1500, "Arhitekt": 1700, "Farmaceut": 1200, "Psiholog": 2000, "Računalni programer": 2200, "Ekonomist": 1800, "Financijski analitičar": 2000}
if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # No event loop is running
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(main())