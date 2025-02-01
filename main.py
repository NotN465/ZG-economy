import random
import time
from datetime import datetime,timedelta
import discord
from discord.ext import commands
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import User,Bank,Inventory,Stocks
import os
import json

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!",intents=intents)

engine = create_engine('sqlite:///UserInfo.db')
Session = sessionmaker(bind=engine)
session = Session()
developer_status = ["411797205020704768","621724403364921354"]
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
        pass
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
    embed_pomoc.add_field(name="!dionice_pomoc", value="Pomoc za dionice", inline=False)

    embed_pomoc.set_footer(text="Bot created by NotN465")

    await ctx.send(embed=embed_pomoc)
@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')
    #os.system('python "stock market.py"')
    await bot.tree.sync()
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
        stocks = Stocks(MEME=0,TROLL=0,FOMO=0,YOLO=0,LOL=0,user_id=str(ctx.author.id))
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
                time.sleep(tick)
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
    embed_dionice.add_field(name="!dionice_prodaj", value="Upisi !dionice_prodaj <dionica> <kolicina za prodaju>", inline=False)
    embed_dionice.set_footer(text="Pomoc za komande dionica")

    await ctx.send(embed=embed_dionice)
@bot.command()
async def dionice(ctx):
    dionice_embed = discord.Embed(
        title="Dionice",
        description="Pogledaj dostupne dionice",
        color=discord.Color.dark_blue()
    )
    with open("stocks.json") as f:
        data = json.load(f)
    for stock, price in data.items():
        dionice_embed.add_field(name=stock, value=f"Cijena: {price}", inline=False)

    await ctx.send(embed=dionice_embed)
@bot.command()
async def moje_dionice(ctx):
    if str(ctx.author.id) in ids():
        with open("stocks.json") as f:
            data = json.load(f)
        stocks = session.query(Stocks).filter_by(user_id=str(ctx.author.id)).first()
        print(stocks)
        dionice_embed = discord.Embed(
            title="Moje dionice",
            description="Pogledaj svoje dionice",
            color=discord.Color.dark_blue()
        )
        dionice_vrijednost = dict()
        for stock, price in data.items():
            dionice_vrijednost[stock] = price
        print(dionice_vrijednost)
        round_num = 3
        dionice_embed.add_field(name="Meme", value=f'{round(stocks.MEME,round_num)} MEME dionica, ukupna cijena: {round(stocks.MEME*dionice_vrijednost["MEME"],round_num)}kn', inline=False)
        dionice_embed.add_field(name="Troll", value=f'{round(stocks.TROLL,round_num)} TROLL dionica, ukupna cijena: {round(stocks.TROLL*dionice_vrijednost["TROLL"],round_num)}kn', inline=False)
        dionice_embed.add_field(name="FOMO", value=f'{round(stocks.FOMO,round_num)} FOMO dionica, ukupna cijena: {round(stocks.FOMO*dionice_vrijednost["FOMO"],round_num)}kn', inline=False)
        dionice_embed.add_field(name="YOLO", value=f'{round(stocks.YOLO,round_num)} YOLO dionica, ukupna cijena: {round(stocks.YOLO*dionice_vrijednost["YOLO"],round_num)}kn', inline=False)
        dionice_embed.add_field(name="LOL", value=f'{round(stocks.LOL,round_num)} LOL dionica, ukupna cijena: {round(stocks.LOL*dionice_vrijednost["LOL"],round_num)}kn', inline=False)
        await ctx.send(embed=dionice_embed)
    else:
        await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")
@bot.command()
async def kupi_dionice(ctx):
    if str(ctx.author.id) in ids():
        user_bank = session.query(Bank).filter_by(user_id=str(ctx.author.id)).first()
        user_stocks = session.query(Stocks).filter_by(user_id=str(ctx.author.id)).first()
        message = ctx.message.content
        message = message.split(" ")
        if len(message) == 3:
            stock = message[1].upper()
            kolicina_u_kn = message[2]
            if kolicina_u_kn.isdigit() == False:
                await ctx.send("Kolicina mora biti ispravna!")
            elif stock not in ["MEME", "TROLL", "FOMO", "YOLO", "LOL"]:
                await ctx.send("Nepostojeca dionica!")
            else:
                with open("stocks.json") as f:
                    data = json.load(f)
                if user_bank.money >= int(kolicina_u_kn):
                    user_bank.money -= int(kolicina_u_kn)
                    price = data[stock]
                    if stock == "MEME":
                        user_stocks.MEME += int(kolicina_u_kn)/price
                    elif stock == "TROLL":
                        user_stocks.TROLL += int(kolicina_u_kn)/price
                    elif stock == "FOMO":
                        user_stocks.FOMO += int(kolicina_u_kn)/price
                    elif stock == "YOLO":
                        user_stocks.YOLO += int(kolicina_u_kn)/price
                    elif stock == "LOL":
                        user_stocks.LOL += int(kolicina_u_kn)/price
                    session.commit()
                    await ctx.send(f"Korisnik {ctx.author.mention} je kupio {kolicina_u_kn}kn dionice {stock}")
        else:
            await ctx.send("Pogresan format komande! Upisi !kupi_dionice <dionica> <kolicina u kunama>")
    else:
        await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")
@bot.command()
async def prodaj_dionice(ctx):
    if str(ctx.author.id) in ids():
        user_bank = session.query(Bank).filter_by(user_id=str(ctx.author.id)).first()
        user_stocks = session.query(Stocks).filter_by(user_id=str(ctx.author.id)).first()
        message = ctx.message.content
        message = message.split(" ")
        if len(message) == 3:
            stock = message[1].upper()
            kolicina_u_kn = message[2]
            if kolicina_u_kn.isdigit() == False:
                await ctx.send("Kolicina mora biti ispravna!")
            elif stock not in ["MEME", "TROLL", "FOMO", "YOLO", "LOL"]:
                await ctx.send("Nepostojeca dionica!")
            else:
                with open("stocks.json") as f:
                    data = json.load(f)
                    user_bank.money += int(kolicina_u_kn)
                    price = data[stock]
                    if stock == "MEME" and user_stocks.MEME >= int(kolicina_u_kn)/price:
                        user_stocks.MEME -= int(kolicina_u_kn)/price
                        await ctx.send(f"Korisnik {ctx.author.mention} je prodao {kolicina_u_kn}kn dionice {stock}")
                    elif stock == "TROLL" and user_stocks.TROLL >= int(kolicina_u_kn)/price:
                        user_stocks.TROLL -= int(kolicina_u_kn)/price
                        await ctx.send(f"Korisnik {ctx.author.mention} je prodao {kolicina_u_kn}kn dionice {stock}")
                    elif stock == "FOMO" and user_stocks.FOMO >= int(kolicina_u_kn)/price:
                        user_stocks.FOMO -= int(kolicina_u_kn)/price
                        await ctx.send(f"Korisnik {ctx.author.mention} je prodao {kolicina_u_kn}kn dionice {stock}")
                    elif stock == "YOLO" and user_stocks.YOLO >= int(kolicina_u_kn)/price:
                        user_stocks.YOLO -= int(kolicina_u_kn)/price
                        await ctx.send(f"Korisnik {ctx.author.mention} je prodao {kolicina_u_kn}kn dionice {stock}")
                    elif stock == "LOL" and user_stocks.LOL >= int(kolicina_u_kn)/price:
                        user_stocks.LOL -= int(kolicina_u_kn)/price
                        await ctx.send(f"Korisnik {ctx.author.mention} je prodao {kolicina_u_kn}kn dionice {stock}")
                    else:
                        await ctx.send("Nemate dovoljno dionica za prodaju!")
                    session.commit()
        else:
            await ctx.send("Pogresan format komande! Upisi !prodaj_dionice <dionica> <kolicina u kunama>")
    else:
        await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")
with open('token.txt', 'r') as f:
    token = f.read()
bot.run(str(token))