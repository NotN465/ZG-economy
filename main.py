import random
import time
from datetime import datetime,timedelta
import discord
from discord.ext import commands
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import User,Bank,Inventory,Stocks,Server
import os
import json
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!",intents=intents)

engine = create_engine('sqlite:///UserInfo.db')
Session = sessionmaker(bind=engine)
session = Session()
developer_status = ["411797205020704768"]
def level_xp(user_id):
    xp = session.query(User).filter_by(id=str(user_id)).first().xp
    xp_needed = 500
    level = 1
    while xp > xp_needed:
        level += 1
        xp -= xp_needed
        xp_needed = xp_needed +100
    remaining_xp = xp
    next_level_xp = xp_needed-remaining_xp
    #Prvo returna level onda koliko je ostalo xp za sledeci level i onda koliko jos treba xpa do sljedeceg levela
    return level, remaining_xp,next_level_xp

def ids():
    user = discord.User
    users = []
    user_info = session.query(User.id).all()
    if user_info == []:
        return ()
    for x in user_info:
        users.append(str(x[0]))
    return users
#Ovo su neke komande koje samo ja mogu koristiti
@bot.command()
async def daj_pare(ctx):
    if str(ctx.author.id) in developer_status:
        message = ctx.message.content
        message = message.split(" ")
        user_name = session.query(User).filter_by(id=str(message[1][2:-1])).first()
        if len(message) == 3:
            user_message = message[1][2:-1]
            user = session.query(Bank).filter_by(user_id=str(user_message)).first()
            user.money += int(message[2])
            session.commit()
            await ctx.send(f"{user_name.name} dobija {message[2]}kn od strane {ctx.author.mention}")
@bot.command()
async def oduzmi_pare(ctx):
    if str(ctx.author.id) in developer_status:
        message = ctx.message.content
        message = message.split(" ")
        user_name = session.query(User).filter_by(id=str(message[1][2:-1])).first()
        if len(message) == 3:
            user_message = message[1][2:-1]
            user = session.query(Bank).filter_by(user_id=str(user_message)).first()
            user.money -= int(message[2])
            session.commit()
            await ctx.send(f"{user_name.name} gubi {message[2]}kn od strane {ctx.author.mention}")
@bot.command()
async def daj_xp(ctx):
    if str(ctx.author.id) in developer_status:
        message = ctx.message.content
        message = message.split(" ")
        if len(message) == 4:
            user_message = message[1][2:-1]
            vrsta_xp = message[2]
            kolicina = message[3]
            user = session.query(User).filter_by(id=str(user_message)).first()
            if vrsta_xp == "xp":
                user.xp += int(kolicina)
            elif vrsta_xp == "chop_xp":
                user.chop_xp += int(kolicina)
            elif vrsta_xp == "mine_xp":
                user.mine_xp += int(kolicina)
            elif vrsta_xp == "fishing_xp":
                user.fishing_xp += int(kolicina)
            session.commit()
        else:
            await ctx.send("Pogresan format komande! Upisi !daj_xp <@korisnik> <vrsta_xp> <kolicina>\nVrste xp su: xp, chop_xp, mine_xp, fishing_xp")
@bot.command()
async def daj_dionice(ctx):
    if str(ctx.author.id) in developer_status:
        with open("stocks.json") as f:
            data = json.load(f)
        message = ctx.message.content
        message = message.split(" ")
        if len(message) == 4:
            user_message = message[1][2:-1]
            vrsta_dionica = str(message[2]).upper()
            kolicina = message[3]
            user = session.query(Stocks).filter_by(user_id=str(user_message)).first()
            user_name = session.query(User).filter_by(id=str(user_message)).first()
            price= data[vrsta_dionica]
            if vrsta_dionica == "MEME":
                user.MEME += int(kolicina)/price
            elif vrsta_dionica == "TROLL":
                user.TROLL += int(kolicina)/price
            elif vrsta_dionica == "FOMO":
                user.FOMO += int(kolicina)/price
            elif vrsta_dionica == "YOLO":
                user.YOLO += int(kolicina)/price
            elif vrsta_dionica == "LOL":
                user.LOL += int(kolicina)/price
            await ctx.send(f"{user_name.name} dobija {kolicina} {vrsta_dionica} od strane {ctx.author.mention}")
            session.commit()

@bot.command()
async def daj_stvar(ctx):
    if str(ctx.author.id) in developer_status:
        message = ctx.message.content
        message = message.split(" ")
        if len(message) == 4:
            user_message = message[1][2:-1]
            stvar = message[2]
            kolicina = message[3]
            inv_user = session.query(Inventory).filter_by(user_id=str(user_message)).first()
    else:
        await ctx.send("Nemate ovlaste da koristite ovu komandu!")
@bot.command()
async def ocisti_poruke(ctx):
    if str(ctx.author.id) in developer_status:
        message = ctx.message.content
        message = message.split(" ")
        if len(message) == 2:
            amount = int(message[1])+1
            await ctx.channel.purge(limit=amount)
            await ctx.send(f"{amount} poruke su obrisane!")
@bot.command()
async def developer_pomoc(ctx):
    if str(ctx.author.id) in developer_status:
        embed = discord.Embed(
            title="Developer pomoc",
            description="Pomoc za developera. Ove komande samo developer i ljudi koji su ovlasteni mogu koristiti.",
        )
        embed.add_field(name="!daj_pare", value="Daje pare od strane developer-a.", inline=False)
        embed.add_field(name="!oduzmi_pare", value="Oduzima pare od strane developer-a.", inline=False)
        embed.add_field(name="!daj_xp", value="Daje xp od strane developer-a.", inline=False)
        embed.add_field(name="!oduzmi_xp", value="Oduzima xp od strane developer-a.", inline=False)
        embed.add_field(name="!daj_dionice", value="Daje dionice od strane developer-a.", inline=False)
        embed.add_field(name="!daj_stvar", value="Daje stvar od strane developer-a.", inline=False)
        embed.add_field(name="!ocisti_pourke", value="Ocisti poruke od strane developer-a.", inline=False)
        await ctx.send(embed=embed)
@bot.command()
async def oduzmi_xp(ctx):
    if str(ctx.author.id) in developer_status:
        message = ctx.message.content
        message = message.split(" ")
        if len(message) == 4:
            user_message = message[1][2:-1]
            vrsta_xp = message[2]
            kolicina = message[3]
            user = session.query(User).filter_by(id=str(user_message)).first()
            if vrsta_xp == "xp":
                user.xp -= int(kolicina)
            elif vrsta_xp == "chop_xp":
                user.chop_xp -= int(kolicina)
            elif vrsta_xp == "mine_xp":
                user.mine_xp -= int(kolicina)
            elif vrsta_xp == "fishing_xp":
                user.fishing_xp -= int(kolicina)
            session.commit()
        else:
            await ctx.send("Pogresan format komande! Upisi !oduzmi_xp <@korisnik> <vrsta_xp> <kolicina>\nVrste xp su: xp, chop_xp, mine_xp, fishing_xp")
@bot.command()
async def provjeri_level(ctx):
    if str(ctx.author.id) in ids():
        user = session.query(User).filter_by(id=str(ctx.author.id)).first()
        level = level_xp(ctx.author.id)[0]
        await ctx.send(f"Tvoj level je {level}")
    else:
        await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")
@bot.command()
async def pomoc(ctx):
    embed_pomoc = discord.Embed(
        title="Pomoc",
        description="Pomoc za sve komande dostupne koristeci bota.",
        color=discord.Color.blue()
    )

    embed_pomoc.add_field(name="!NapraviProfil", value="Napravi novi profil na serveru.", inline=False)
    embed_pomoc.add_field(name="!stanje", value="Prikazuje stanje racuna.", inline=False)
    embed_pomoc.add_field(name="!posao", value="Prikazuje poslove i njihovu zaradu i omogućava zapošljavanje. Poslovi su:\nPrvi sektor: Farmer, Ribar, Rudar, Drvosječa, Lovac, Pčelar, Vinogradar, Voćar, Cvjećar, Stožar"
                                               "\nDrugi sektor: Radnik u tvornici, Zidar, Bravar, Električar, Stolar, Automehaničar, Kovač, Vodoinstalater, Tekstilni radnik, Keramičar"
                                               "\nTreci sektor: Liječnik, Pravni savjetnik, Inženjer, Profesor, Arhitekt, Farmaceut, Psiholog, Računalni programer, Ekonomist, Financijski analitičar", inline=False)
    embed_pomoc.add_field(name="!radi", value="Omogućuje zarađivanje i dobivanje plače koja je prikazana u !posao.", inline=False)
    embed_pomoc.add_field(name="!stvari", value="Prikazuje sve stvari koje imas u racunu.", inline=False)
    embed_pomoc.add_field(name="!drva", value="Omogućava sijecanje drva i dobivanje xp-a za drvo.", inline=False)
    embed_pomoc.add_field(name="!rude", value="Omogućava rudarenje ruda i dobivanje xp-a za rude.", inline=False)
    embed_pomoc.add_field(name="!ribarenje", value="Omogućava ribarenje i dobivanje xp-a za ribarenje.", inline=False)
    embed_pomoc.add_field(name="!trade", value="Upisi !trade <@korisnik> <proizvod koji primas> <kolicina> <proizvod koji dajes> <kolicina>.", inline=False)
    embed_pomoc.add_field(name="!pokloni", value="Pokloni neku stvar korisniku", inline=False)
    embed_pomoc.add_field(name="!plati", value="Daj pare korisniku", inline=False)
    embed_pomoc.add_field(name="!provjeri_level", value="Provjerava level korisnika", inline=False)
    embed_pomoc.add_field(name="!rulet", value="Pokrece rulet.", inline=False)
    embed_pomoc.add_field(name="!blackjack", value="Pokrece blackjack.", inline=False)
    embed_pomoc.add_field(name="!najbogatiji", value="Prikazuje 10 najbogatijih korisnika", inline=False)
    embed_pomoc.add_field(name="!dionice_pomoc", value="Pomoc za dionice", inline=False)

    embed_pomoc.set_footer(text="Bot created by NotN465")

    await ctx.send(embed=embed_pomoc)
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
@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')
    #os.system('python "stock market.py"')
    for guild in bot.guilds:
        asyncio.create_task(update_dionice(int(guild.id)))
@bot.command()
async def NapraviProfil(ctx):
    check_ids = ids()
    if str(ctx.author.id) in check_ids:
        await ctx.send("Vec imas racun!")
    else:
        now = (datetime.now() - timedelta(hours=4)).strftime("%M-%H-%d-%m-%Y")
        user = User(name=str(ctx.author.name), id=str(ctx.author.id),posao="Nema",xp=0,chop_xp=0,mine_xp=0,fishing_xp=0,last_fishing_time=now,last_mine_time=now,last_chop_time=now)
        money = Bank(money=50, savings=0, user_id=str(ctx.author.id), last_work_time=now)
        invetory = Inventory(items={}, user_id=str(ctx.author.id))
        stocks = Stocks(stocks={},user_id=str(ctx.author.id))
        session.add(money)
        session.add(user)
        session.add(invetory)
        session.add(stocks)
        session.commit()
        await ctx.send("Racun je napravljen!")
@bot.command()
async def stanje(ctx,alias=['bal']):
    check_ids = ids()
    if str(ctx.author.id) in check_ids:
        await ctx.send(f"Tvoje stanje je: {str(session.query(Bank).filter_by(user_id=str(ctx.author.id)).first().money)}kn")
    else:
        await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")

@bot.command()
async def stvari(ctx,alias=['inv']):
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
prvi_sektor_poslovi = {"Farmer": 900, "Ribar": 900, "Rudar": 950 , "Drvosječa": 1000, "Lovac": 1000, "Pčelar": 800, "Vinogradar": 1200, "Voćar": 950, "Cvjećar": 850, "Stožar": 900}
drugi_sektor_poslovi = {"Radnik u tvornici": 1200, "Zidar":1100, "Bravar":1050, "Električar":1700, "Stolar":1300, "Automehaničar": 1500, "Kovač": 1200, "Vodoinstalater": 1700, "Tekstilni radnik": 1050, "Keramičar": 1800}
treci_sektor_poslovi = {"Liječnik": 2500, "Pravni savjetnik": 2000, "Inženjer": 2000, "Profesor": 1500, "Arhitekt": 1700, "Farmaceut": 1200, "Psiholog": 2000, "Računalni programer": 2200, "Ekonomist": 1800, "Financijski analitičar": 2000}
@bot.command()
async def posao(ctx):
    if str(ctx.author.id) in ids():
        user = session.query(User).filter_by(id=str(ctx.author.id)).first()
        raw_message = ctx.message.content
        raw_message = raw_message.split(" ")
        if len(raw_message) == 1 or len(raw_message) >2:
            await ctx.send("Pogresan format komande! Upisi !Posao <posao>")
        else:
            raw_message = str(raw_message[1]).lower().capitalize()
            if raw_message in prvi_sektor_poslovi.keys():
                user.posao = raw_message
                session.commit()
                await ctx.send(f"Za {raw_message} zarada je {prvi_sektor_poslovi[raw_message]}kn")
            elif raw_message in drugi_sektor_poslovi.keys():
                if level_xp(ctx.author.id)[0] >= 10:
                    user.posao = raw_message
                    session.commit()
                    await ctx.send(f"Za {raw_message} zarada je {drugi_sektor_poslovi[raw_message]}kn")
                else:
                    await ctx.send("Za drugi sektor moras biti level 10 ili visi!")
            elif raw_message in treci_sektor_poslovi.keys():
                if level_xp(ctx.author.id)[0] >= 20:
                    user.posao = raw_message
                    session.commit()
                    await ctx.send(f"Za {raw_message} zarada je {treci_sektor_poslovi[raw_message]}kn")
                else:
                    await ctx.send("Za treci sektor moras biti level 20 ili visi!")
            else:
                await ctx.send("Posao nije pronadjen!")

    else:
        await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")
@bot.command()
async def radi(ctx):
    if str(ctx.author.id) in ids():
        user = session.query(User).filter_by(id=str(ctx.author.id)).first()
        last_work_time = session.query(Bank).filter_by(user_id=str(ctx.author.id)).first().last_work_time
        last_work_time = datetime.strptime(last_work_time, "%M-%H-%d-%m-%Y") + timedelta(hours=4)
        datetime_now = datetime.now()
        datetime_now = datetime_now.strftime("%M-%H-%d-%m-%Y")
        datetime_now = datetime.strptime(datetime_now, "%M-%H-%d-%m-%Y")
        sektor = ''
        if user.posao != "Nema" and last_work_time < datetime_now:
            if user.posao in prvi_sektor_poslovi.keys():
                sektor = prvi_sektor_poslovi
            elif user.posao in drugi_sektor_poslovi.keys():
                sektor = drugi_sektor_poslovi
            elif user.posao in treci_sektor_poslovi.keys():
                sektor = treci_sektor_poslovi
            user_bank = session.query(Bank).filter_by(user_id=str(ctx.author.id)).first()
            await ctx.send(f"Radili ste kao {user.posao} i zaradili je {sektor[user.posao]}")
            user_bank.money += int(sektor[user.posao])
            user_bank.last_work_time = datetime_now.strftime("%M-%H-%d-%m-%Y")
            user.xp += 100
            session.commit()
        elif user.posao == "Nema":
            await ctx.send("Vi niste zaposleni!")
        else:
            await ctx.send("Vec ste radili, morate pricekati 4 sata od zadnjeg puta kada ste radili da bi mogli opet raditi.")
    else:
        await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")
@bot.command()
async def drva(ctx):
    if str(ctx.author.id) in ids():
        user = session.query(User).filter_by(id=str(ctx.author.id)).first()
        last_chop_time = str(user.last_chop_time)
        if datetime.strptime(last_chop_time, "%M-%H-%d-%m-%Y") + timedelta(hours=2) < datetime.now():
            user.chop_xp += 100
            user.last_chop_time = datetime.now().strftime("%M-%H-%d-%m-%Y")
            session.commit()
            await ctx.send(f"Dobili ste 100 xp za drva i trenutni xp je {user.chop_xp}")
        else:
            await ctx.send("Vec ste cijepali drva, morate pricekati 2 sata od zadnjeg puta kada ste cjepali da bi mogli opet cjepati.")
    else:
        await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")
@bot.command()
async def rude(ctx):
    if str(ctx.author.id) in ids():
        user = session.query(User).filter_by(id=str(ctx.author.id)).first()
        last_mine_time = str(user.last_mine_time)
        if datetime.strptime(last_mine_time, "%M-%H-%d-%m-%Y") + timedelta(hours=2) < datetime.now():
            user.mine_xp += 100
            user.last_mine_time = datetime.now().strftime("%M-%H-%d-%m-%Y")
            session.commit()
            await ctx.send(f"Dobili ste 100 xp za rude i trenutni xp je {user.mine_xp}")
        else:
            await ctx.send("Vec ste rudarili, morate pricekati 2 sata od zadnjeg puta kada ste rudarili da bi mogli opet rudariti.")
    else:
        await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")
@bot.command()
async def ribarenje(ctx):
    if str(ctx.author.id) in ids():
        user = session.query(User).filter_by(id=str(ctx.author.id)).first()
        last_fishing_time = str(user.last_fishing_time)
        if datetime.strptime(last_fishing_time, "%M-%H-%d-%m-%Y") + timedelta(hours=2) < datetime.now():
            user.fishing_xp += 100
            user.last_fishing_time = datetime.now().strftime("%M-%H-%d-%m-%Y")
            session.commit()
            await ctx.send(f"Dobili ste 100 xp za ribarenje i trenutni xp je {user.fishing_xp}")
        else:
            await ctx.send("Vec ste ribarili, morate pricekati 2 sata od zadnjeg puta kada ste ribarili da bi mogli opet ribariti.")
    else:
        await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")
proizvodi = {"Hrana": {"Pica":80,"Burek":30,"Ćevapi":70,"Cokolino":20,"Sarma":50},
             "Pica":{"Coca-cola":20,"Cedevita":15,"Rakija":50,"Piva":12,"Kava":15,"Voda":5},
             "Ostalo":{"Spin":300}}
@bot.command()
async def ducan(ctx):
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



@bot.command()
async def kupi(ctx):

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
@bot.command(aliases=['ds'])
async def Spin(ctx):
    def temp_multiple(object,n,item):
        for i in range(n):
            object.append(item)
    def randomize_emojis(emojis, n):
        randomized = dict()
        for i in range(len(emojis)):
            randomized[emojis[i]] = random.randint(1, n/2)
        while sum(randomized.values()) < n:
            randomized[random.choice(emojis)] += 1
        while sum(randomized.values()) > n:
            emojis_random = random.choice(emojis)
            if randomized[emojis_random] != 0:
                randomized[emojis_random] -= 1
        return randomized
    if str(ctx.author.id) in ids():
        inv = session.query(Inventory).filter_by(user_id=str(ctx.author.id)).first()
        if "Spin" in inv.items:
           if inv.items["Spin"] > 0:
            inv.items["Spin"] -= 1
            emojis = ["💰","💲","🍕","🍞","✨","⬜"]
            randomize = randomize_emojis(emojis,20)
            spinwheel = ""
            for i in range(20):
                random_item = random.choice(emojis)
                while randomize[random_item] == 0:
                    random_item = random.choice(emojis)
                spinwheel = spinwheel + random_item
            start = spinwheel[0:3]
            tick = 0.2
            msg = await ctx.send(f"{start}\n"
                           f"               👆   ",ephemeral=True)
            for i in range(3,18):
                if i >= 13:
                    tick += 0.1
                await asyncio.sleep(tick)
                start = spinwheel[i-3:i]
                await msg.delete()
                msg = await ctx.send(f"{start}\n"
                               f"               👆   ",ephemeral=True)

            msg = await ctx.send(f"{start}\n"
                                 f"             👆   ",ephemeral=True)
            time.sleep(2)
            item = start[1]
            await msg.delete()
            await ctx.send(f"Kraj spinanja! Dobili ste {item}")
            user = session.query(User).filter_by(id=str(ctx.author.id)).first()
            user_bank = session.query(Bank).filter_by(user_id=str(ctx.author.id)).first()
            user_inv = session.query(Inventory).filter_by(user_id=str(ctx.author.id)).first()
            if item == "💰":
                user_bank.money += 2000
            elif item == "💲":
                user_bank.money += 500
            elif item == "🍕":
                if item in user_inv.items:
                    user_inv.items["Pica"] += 1
                else:
                    user_inv.items["Pica"] = 1
            elif item == "🍞":
                if item in user_inv.items:
                    user_inv.items["Burek"] += 1
                else:
                    user_inv.items["Burek"] = 1
            elif item == "✨":
                user.xp += 1000
            flag_modified(user_inv, "items")
            session.commit()
           else:
               await ctx.send("Nemate dovoljno spinova!")
        else:
            await ctx.send("Nemate dovoljno spinova!")

    else:
        await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")

class TestMenuButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="✔",style=discord.ButtonStyle.green,custom_id="positive")
    async def button_func_green(selfself,interaction:discord.Interaction,button:discord.ui.Button):
        pass
    @discord.ui.button(label="❌",style=discord.ButtonStyle.red,custom_id="negative")
    async def button_func_red(selfself,interaction:discord.Interaction,button:discord.ui.Button):
        pass
@bot.command()
async def trade(ctx):
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
                user_to_send = await bot.fetch_user(user)
                await user_to_send.send(poruka_primatelju, view=TestMenuButton())

                @bot.listen()
                async def on_interaction(interaction: discord.Interaction):
                    user = message[1][2:-1]
                    user2 = session.query(User).filter_by(id=str(user)).first()
                    if interaction.type == discord.InteractionType.component:
                        custom_id = interaction.data.get("custom_id")
                        if custom_id == "positive":
                            await interaction.response.send_message("Korisnik je prihvatio", ephemeral=True)
                            inv_user = session.query(Inventory).filter_by(user_id=str(ctx.author.id)).first()
                            inv_user2 = session.query(Inventory).filter_by(user_id=str(user)).first()
                            if proizvod_za_dati in inv_user.items and int(kolicina_za_dati) <= int(inv_user.items[proizvod_za_dati]):
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
                            user_to_send = await bot.fetch_user(other_user)
                            await user_to_send.send(f"Korisnik {user2.name} je prihvatio trade, dobili ste {kolicina_za_primati} {proizvod_za_primati} i  izgubili ste {kolicina_za_dati} {proizvod_za_dati}")
                        elif custom_id == "negative":
                            await interaction.response.send_message("Odbili ste trade i nece biti izvrsen", ephemeral=True)
                            other_user = ctx.author.id
                            user_to_send = await bot.fetch_user(other_user)
                            await user_to_send.send(f"Korisnik {user2.name} je odbio trade")

            else:
                await ctx.send("Korisnik nije pronaden, upisite postojeceg korisnika!")
        else:
            await ctx.send("Pogresan format komande! Upisi !trade <@korisnik> <proizvod koji primas> <kolicina> <proizvod koji dajes> <kolicina>")

    else:
        await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")
@bot.command()
async def pokloni(ctx):
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
                        await ctx.send(f"Korisnik {ctx.author.mention} je poklonio {kolicina} {stvar} korisniku {user_name.name}")
        else:
            await ctx.send("Pogresan format komande! Upisi !pokloni <@korisnik> <stvar> <kolicina>")
    else:
        await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")
@bot.command()
async def plati(ctx):
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
                        await ctx.send(f"Korisnik {ctx.author.mention} je platio {kolicina}kn korisniku {user_name.name}")
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
@bot.command()
async def dionice_pomoc(ctx):
    embed_dionice = discord.Embed(
        title="Pomoc za dionice",
        description="Pomoc za sve komande dostupne koristeci bota u vezi dionica.",
        color=discord.Color.blue()
    )

    embed_dionice.add_field(name="!dionice", value="Prikazuje dostupne dionice", inline=False)
    embed_dionice.add_field(name="!moje_dionice", value="Prikazuje dionice koje imas i jel tradeas long ili short", inline=False)
    embed_dionice.add_field(name="!kupi_dionice", value="Upisi !dionice_kupi <dionica> <kolicina za kupnju>", inline=False)
    embed_dionice.add_field(name="!prodaj_dionice", value="Upisi !dionice_prodaj <dionica> <kolicina za prodaju izrazena u dionicama(ne u kunama)>", inline=False)
    embed_dionice.add_field(name="!prikazuj_dionice", value="Setup za prikazivanje dionica u odredenom kanalu.", inline=False)
    embed_dionice.set_footer(text="Pomoc za komande dionica")

    await ctx.send(embed=embed_dionice)
@bot.command()
async def dionice(ctx):
    dionice_embed = discord.Embed(
        title="Dionice",
        description="Pogledaj dostupne dionice",
        color=discord.Color.dark_blue()
    )
    server = session.query(Server).filter_by(server_id=ctx.guild.id).first()
    data = server.stocks
    for stock, price in data.items():
        dionice_embed.add_field(name=stock, value=f"Cijena: {round(price,2)}", inline=False)

    await ctx.send(embed=dionice_embed)
@bot.command()
async def moje_dionice(ctx):
    if str(ctx.author.id) in ids():
        server = session.query(Server).filter_by(server_id=ctx.guild.id).first()
        user_stocks = session.query(Stocks).filter_by(user_id=int(ctx.author.id)).first()
        data = server.stocks
        dionice_embed = discord.Embed(
            title="Moje dionice",
            description="Pogledaj dostupne dionice",
            color=discord.Color.dark_blue()
        )
        for stock_key,stock_value in data.items():
            if stock_key not in user_stocks.stocks.keys():
                user_stocks.stocks[stock_key] = 0
                flag_modified(user_stocks, "stocks")
                session.commit()
            dionice_embed.add_field(name=f"{stock_key}",value=f"Kolicina dionice: {user_stocks.stocks[stock_key]}",inline=False)
        await ctx.send(embed=dionice_embed)

@bot.command()
async def rulet(ctx):

    if str(ctx.author.id) in ids():
        rewards = {
    '0': 35, '00': 35, '1': 35, '2': 35, '3': 35, '4': 35, '5': 35, '6': 35,
    '7': 35, '8': 35, '9': 35, '10': 35, '11': 35, '12': 35, '13': 35, '14': 35,
    '15': 35, '16': 35, '17': 35, '18': 35, '19': 35, '20': 35, '21': 35, '22': 35,
    '23': 35, '24': 35, '25': 35, '26': 35, '27': 35, '28': 35, '29': 35, '30': 35,
    '31': 35, '32': 35, '33': 35, '34': 35, 'zelena': 35, 'crvena': 2, 'crna': 2,"1-18":2, "19-36":2, "par":2, "nepar":2,"1-12":3, "13-24":3, "25-36":3
}
        message = ctx.message.content
        message_content = message.split(" ")
        if 'pomoc' in message or len(message_content) <= 2 or len(message_content) >= 4:
            embed_rulet_pomoc = discord.Embed(title="Pomoc za !rulet", description="Upisi !rulet <odabir broja ili boje> <kolicina>\nDostupne brojevi i boje su:")
            embed_rulet_pomoc.add_field(name="Brojevi", value="0, 00, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34", inline=False)
            embed_rulet_pomoc.add_field(name="Boje", value="zelena, crvena, crna", inline=False)
            embed_rulet_pomoc.add_field(name="Ostalo", value="1-12, 13-24, 25-36, 1-18, 19-36, par, nepar", inline=False)
            await ctx.send(embed=embed_rulet_pomoc)
        elif len(message_content) == 3:
            odabir = message_content[1]
            kolicina = message_content[2]
            user_bank = session.query(Bank).filter_by(user_id=str(ctx.author.id)).first()
            if odabir in rewards:
                if kolicina == "sve":
                    kolicina = int(user_bank.money)
                if int(kolicina) > 0 and user_bank.money >= int(kolicina):
                    random_list = [[random.choice(["🟥", "⚫"]) for x in range(36)] for x in range(3)]
                    msg = await ctx.send('1')
                    i = 0
                    for x in range(10):
                        msg_to_send = f'{"".join(random_list[0][i:i + 5])}\n{"".join(random_list[1][i:i + 5])}\n{"".join(random_list[2][i:i + 5])}'
                        await msg.edit(content=msg_to_send)
                        await asyncio.sleep(1)
                        i = i + 1
                    user_bank.money -= int(kolicina)
                    random_rulet_num = random.randint(0, 35)
                    random_rulet_color = random.randint(0, 35)
                    if random_rulet_color == 0:
                        random_rulet_color = "zelena"
                    elif random_rulet_num %2==0:
                        random_rulet_color = "crvena"
                    else:
                        random_rulet_color = "crna"
                    nums = [str(i) for i in range(36)] + ["00", "0"]
                    if odabir == random_rulet_color:
                        user_bank.money += int(kolicina) * rewards[odabir]+ int(kolicina)
                        await ctx.send(f"Odabrali ste {odabir} i rulet je bila {random_rulet_color}, dobili ste {int(kolicina) * rewards[odabir]} kuna!")
                    elif odabir in ["1-18", "19-36","1-12", "13-24", "25-36"] and random_rulet_num in range(int(odabir.split("-")[0]), int(odabir.split("-")[1])+1):
                        user_bank.money += int(kolicina) * rewards[odabir]+ int(kolicina)
                        await ctx.send(f"Odabrali ste {odabir} i rulet je bila {random_rulet_num}, dobili ste {int(kolicina) * rewards[odabir]} kuna!")
                    elif odabir == "par" and random_rulet_num % 2 == 0:
                        user_bank.money += int(kolicina) * rewards[odabir]+ int(kolicina)
                        await ctx.send(f"Odabrali ste {odabir} i rulet je bila {random_rulet_num}, dobili ste {int(kolicina) * rewards[odabir]} kuna!")
                    elif odabir == "nepar" and random_rulet_num % 2 == 1:
                        user_bank.money += int(kolicina) * rewards[odabir]+ int(kolicina)
                        await ctx.send(f"Odabrali ste {odabir} i rulet je bila {random_rulet_num}, dobili ste {int(kolicina) * rewards[odabir]} kuna!")
                    elif odabir in nums and random_rulet_num == int(odabir):
                        user_bank.money += int(kolicina) * rewards[odabir]+ int(kolicina)
                        await ctx.send(f"Odabrali ste {odabir} i rulet je bila {random_rulet_num}, dobili ste {int(kolicina) * rewards[odabir]} kuna!")
                    else:
                        await ctx.send(f"Nazalost niste nista osvojili, rulet je bila {random_rulet_num} i {random_rulet_color}")

                else:
                    await ctx.send("Nemate dovoljno novca za igru!")
            else:
                await ctx.send("Pogresan format komande! Upisi !rulet <odabir broja ili boje> <kolicina>")
    else:
        await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")
@bot.command()
async def blackjack(ctx):
    if str(ctx.author.id) in ids():
        guild = ctx.guild
        user = ctx.author
        ctx_message = ctx.message.content
        ctx_message = ctx_message.split(" ")
        if len(ctx_message) == 2:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                user: discord.PermissionOverwrite(view_channel=True, send_messages=True)
            }
            channel = await guild.create_text_channel(name=f"blackjack - {user.name}", overwrites=overwrites)


            def check(msg):
                return msg.author == ctx.author
            await channel.send("Usao su u igru blackjack-a!")
            try:
                black_jack_pos = {"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"kralj":10,"kraljica":10,"decko":10}
                igrac_karta1,igrac_karta2 = random.choice(list(black_jack_pos.keys())),random.choice(list(black_jack_pos.keys()))
                diler_karta1,diler_karta2 = random.choice(list(black_jack_pos.keys())),random.choice(list(black_jack_pos.keys()))
                igrac_karte = [igrac_karta1,igrac_karta2]
                diler_karte = [diler_karta1,diler_karta2]

                igrac = black_jack_pos[igrac_karta1] + black_jack_pos[igrac_karta2]
                diler = black_jack_pos[diler_karta1] + black_jack_pos[diler_karta2]
                embed_igrac = discord.Embed(title="Igrac", color=0x00ff00)
                embed_diler = discord.Embed(title="Diler", color=0x00ff00)
                embed_igrac.add_field(name="Karta 1", value=igrac_karta1, inline=True)
                embed_igrac.add_field(name="Karta 2", value=igrac_karta2, inline=True)
                embed_igrac.add_field(name="Ukupno", value=igrac, inline=True)
                embed_diler.add_field(name="Karta 1", value=diler_karta1, inline=True)
                embed_diler.add_field(name="Karta 2", value=diler_karta2, inline=True)
                embed_diler.add_field(name="Ukupno", value=diler, inline=True)
                igrac_message = await channel.send(embed=embed_igrac)
                diler_message = await channel.send(embed=embed_diler)
                await channel.send("Odaberi hit da bi vukao novu kartu ili stand da bi drzao poziciju")
                while igrac < 21 and diler < 21:
                    message_in_channel = await bot.wait_for("message", check=check, timeout=30)
                    message_content = message_in_channel.content
                    await message_in_channel.delete()
                    if diler < 17:
                        diler_karta3 = random.choice(list(black_jack_pos.keys()))
                        diler_karte.append(diler_karta3)
                        diler += black_jack_pos[diler_karta3]
                        embed_diler = discord.Embed(title="Diler", color=0x00ff00)
                        for i in range(len(diler_karte)):
                            embed_diler.add_field(name=f"Karta {i+1}", value=diler_karte[i], inline=True)
                        embed_diler.add_field(name=f"Ukupno", value=diler, inline=True)
                        await diler_message.edit(embed=embed_diler)
                    if message_content == "hit":
                        igrac_karta3 = random.choice(list(black_jack_pos.keys()))
                        igrac_karte.append(igrac_karta3)
                        igrac += black_jack_pos[igrac_karta3]
                        embed_igrac = discord.Embed(title="Igrac", color=0x00ff00)
                        for i in range(len(igrac_karte)):
                            embed_igrac.add_field(name=f"Karta {i+1}", value=igrac_karte[i], inline=True)
                        embed_igrac.add_field(name=f"Ukupno", value=igrac, inline=True)
                        await igrac_message.edit(embed=embed_igrac)
                        await channel.send("Odabrali ste hit", delete_after=2)
                    elif message_content == "stand":
                        await channel.send("Odabrali ste stand", delete_after=2)
                    if igrac > diler and igrac < 21 and diler < 21 and diler > 17:
                        break
                    if igrac == 17 and diler == 17:
                        break
                user = str(ctx.author.id)
                user_bank = session.query(Bank).filter_by(user_id=user).first()
                if igrac > 21 or (diler > igrac and diler < 21):
                    gubitak = int(ctx_message[1])
                    user_bank.money -= gubitak
                    await channel.send(f"Igrac je proglasio kraj igre! Vas gubitak je {gubitak}")
                elif igrac == 21:
                    dobitak = int(ctx_message[1])*1.5+int(ctx_message[1])
                    user_bank.money += dobitak
                    await channel.send(f"Igrac je dobio black jack! Vas dobitak je {dobitak}")
                elif diler > 21:
                    dobitak = int(ctx_message[1])*2
                    user_bank.money += dobitak
                    await channel.send(f"Diler je proglasio kraj igre i igrac je pobijedio! Vas dobitak je {dobitak}")
                elif igrac > diler:
                    dobitak = int(ctx_message[1])*2
                    user_bank.money += dobitak
                    await channel.send(f"Igrac je pobijedio! Vas dobitak je {dobitak}")
                elif igrac == diler:
                    await channel.send("Ne rijeseno! Niste nista dobili niti izgubili")
                session.commit()

                await asyncio.sleep(10)
                await channel.delete()
            except TimeoutError:
                await user.send("Kanal za blackjack ti se izbrisao jer nisi dovoljno brzo odgovorio!")
                await channel.delete()
        else:
            await ctx.send("Pogresan format komande! Upisi !blackjack <kolicina>")
    else:
        await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")
@bot.command()
async def najbogatiji(ctx):
    najbogatiji_embed = discord.Embed(title="Najbogatiji", color=0x00ff00)
    najbogatiji = session.query(Bank).order_by(Bank.money.desc()).limit(10).all()
    for person in najbogatiji:
        najbogatiji_embed.add_field(name=person.user.name, value=person.money, inline=False)
    await ctx.send(embed=najbogatiji_embed)
@bot.command()
async def prikazuj_dionice(ctx):
    if ctx.author.guild_permissions.administrator:
        message = ctx.message.content
        message = message.split(" ")
        if len(message) == 2:
            server_id = ctx.guild.id
            if str(message[1]).isdigit():
                server = session.query(Server).all()
                server = map(lambda x: x.server_id, server)
                if int(server_id) in list(server):
                    existing_server = session.query(Server).filter_by(server_id=int(server_id)).first()
                    channel = bot.get_channel(int(existing_server.stock_market_channel_id))
                    message_to_delete = await ctx.channel.fetch_message(int(existing_server.message_stock_market_id))
                    await message_to_delete.delete()
                    session.delete(existing_server)
                    session.commit()
                channel = bot.get_channel(int(message[1]))
                stocks = await channel.send("temp message")
                server_setup = Server(server_id=int(server_id), stock_market_channel_id=int(message[1]),
                                          message_stock_market_id=stocks.id, stocks={})
                session.add(server_setup)
                session.commit()
                for guild in bot.guilds:
                    asyncio.create_task(update_dionice(int(guild.id)))
        else:
            await ctx.send("Pogresan format komande! Upisi !prikazuj_dionice <id od kanala>")
    else:
        await ctx.send("Nemate prava za ovu komandu!")
@bot.command()
async def napravi_coin(ctx):
    if ctx.author.guild_permissions.administrator:
        server_id = ctx.guild.id
        server = session.query(Server).all()
        server = map(lambda x: x.server_id, server)
        if int(server_id) not in list(server):
            await ctx.send("Niste postavili kanal za dionice!")
        else:
            existing_server = session.query(Server).filter_by(server_id=int(server_id)).first()
            message = ctx.message.content
            message = message.split(" ")
            if len(message) == 3:
                if str(message[2]).isdigit():
                    existing_server.stocks[message[1]] = int(message[2])
                    flag_modified(existing_server, "stocks")
                    session.commit()
                    await ctx.send(f"Uspjesno napravljen novi coin {message[1]} sa vrijednosti {message[2]}kn po coinu!")
            else:
                await ctx.send("Pogresan format komande! Upisi !napravi_coin <ime_coina> <vrijednost u kn>")

with open('token.txt', 'r') as f:
    token = f.read()
bot.run(str(token))