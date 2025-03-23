import discord
from discord.ext import commands
from main import ids
import asyncio
import random
from sqlalchemy import create_engine, Column, Integer, String,func
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import User,Bank,Inventory,Stocks,Server,CommunityMarket

engine = create_engine('sqlite:///UserInfo.db')
Session = sessionmaker(bind=engine)
session = Session()

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rulet(self,ctx):

        if str(ctx.author.id) in ids():
            rewards = {
                '0': 35, '00': 35, '1': 35, '2': 35, '3': 35, '4': 35, '5': 35, '6': 35,
                '7': 35, '8': 35, '9': 35, '10': 35, '11': 35, '12': 35, '13': 35, '14': 35,
                '15': 35, '16': 35, '17': 35, '18': 35, '19': 35, '20': 35, '21': 35, '22': 35,
                '23': 35, '24': 35, '25': 35, '26': 35, '27': 35, '28': 35, '29': 35, '30': 35,
                '31': 35, '32': 35, '33': 35, '34': 35, 'zelena': 35, 'crvena': 2, 'crna': 2, "1-18": 2, "19-36": 2,
                "par": 2, "nepar": 2, "1-12": 3, "13-24": 3, "25-36": 3
            }
            message = ctx.message.content
            message_content = message.split(" ")
            if 'pomoc' in message or len(message_content) <= 2 or len(message_content) >= 4:
                embed_rulet_pomoc = discord.Embed(title="Pomoc za !rulet",
                                                  description="Upisi !rulet <odabir broja ili boje> <kolicina>\nDostupne brojevi i boje su:")
                embed_rulet_pomoc.add_field(name="Brojevi",
                                            value="0, 00, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34",
                                            inline=False)
                embed_rulet_pomoc.add_field(name="Boje", value="zelena, crvena, crna", inline=False)
                embed_rulet_pomoc.add_field(name="Ostalo", value="1-12, 13-24, 25-36, 1-18, 19-36, par, nepar",
                                            inline=False)
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
                        elif random_rulet_num % 2 == 0:
                            random_rulet_color = "crvena"
                        else:
                            random_rulet_color = "crna"
                        nums = [str(i) for i in range(36)] + ["00", "0"]
                        if odabir == random_rulet_color:
                            user_bank.money += int(kolicina) * rewards[odabir] + int(kolicina)
                            await ctx.send(
                                f"Odabrali ste {odabir} i rulet je bila {random_rulet_color}, dobili ste {int(kolicina) * rewards[odabir]} kuna!")
                        elif odabir in ["1-18", "19-36", "1-12", "13-24", "25-36"] and random_rulet_num in range(
                                int(odabir.split("-")[0]), int(odabir.split("-")[1]) + 1):
                            user_bank.money += int(kolicina) * rewards[odabir] + int(kolicina)
                            await ctx.send(
                                f"Odabrali ste {odabir} i rulet je bila {random_rulet_num}, dobili ste {int(kolicina) * rewards[odabir]} kuna!")
                        elif odabir == "par" and random_rulet_num % 2 == 0:
                            user_bank.money += int(kolicina) * rewards[odabir] + int(kolicina)
                            await ctx.send(
                                f"Odabrali ste {odabir} i rulet je bila {random_rulet_num}, dobili ste {int(kolicina) * rewards[odabir]} kuna!")
                        elif odabir == "nepar" and random_rulet_num % 2 == 1:
                            user_bank.money += int(kolicina) * rewards[odabir] + int(kolicina)
                            await ctx.send(
                                f"Odabrali ste {odabir} i rulet je bila {random_rulet_num}, dobili ste {int(kolicina) * rewards[odabir]} kuna!")
                        elif odabir in nums and random_rulet_num == int(odabir):
                            user_bank.money += int(kolicina) * rewards[odabir] + int(kolicina)
                            await ctx.send(
                                f"Odabrali ste {odabir} i rulet je bila {random_rulet_num}, dobili ste {int(kolicina) * rewards[odabir]} kuna!")
                        else:
                            await ctx.send(
                                f"Nazalost niste nista osvojili, rulet je bila {random_rulet_num} i {random_rulet_color}")

                        session.commit()

                    else:
                        await ctx.send("Nemate dovoljno novca za igru!")
                else:
                    await ctx.send("Pogresan format komande! Upisi !rulet <odabir broja ili boje> <kolicina>")
        else:
            await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")

    @commands.command()
    async def blackjack(self,ctx):
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
                    black_jack_pos = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
                                      "kralj": 10, "kraljica": 10, "decko": 10}
                    igrac_karta1, igrac_karta2 = random.choice(list(black_jack_pos.keys())), random.choice(
                        list(black_jack_pos.keys()))
                    diler_karta1, diler_karta2 = random.choice(list(black_jack_pos.keys())), random.choice(
                        list(black_jack_pos.keys()))
                    igrac_karte = [igrac_karta1, igrac_karta2]
                    diler_karte = [diler_karta1, diler_karta2]

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
                    await channel.send("Odaberi hit da bi vukao novu kartu ili stand da bi drzao poziciju ili kraj ako oces zavrsiti igru svojom voljom")
                    while igrac < 21 and diler < 21:
                        message_in_channel = await self.bot.wait_for("message", check=check, timeout=30)
                        message_content = message_in_channel.content
                        await message_in_channel.delete()
                        if diler < 17:
                            diler_karta3 = random.choice(list(black_jack_pos.keys()))
                            diler_karte.append(diler_karta3)
                            diler += black_jack_pos[diler_karta3]
                            embed_diler = discord.Embed(title="Diler", color=0x00ff00)
                            for i in range(len(diler_karte)):
                                embed_diler.add_field(name=f"Karta {i + 1}", value=diler_karte[i], inline=True)
                            embed_diler.add_field(name=f"Ukupno", value=diler, inline=True)
                            await diler_message.edit(embed=embed_diler)
                        if message_content == "hit":
                            igrac_karta3 = random.choice(list(black_jack_pos.keys()))
                            igrac_karte.append(igrac_karta3)
                            igrac += black_jack_pos[igrac_karta3]
                            embed_igrac = discord.Embed(title="Igrac", color=0x00ff00)
                            for i in range(len(igrac_karte)):
                                embed_igrac.add_field(name=f"Karta {i + 1}", value=igrac_karte[i], inline=True)
                            embed_igrac.add_field(name=f"Ukupno", value=igrac, inline=True)
                            await igrac_message.edit(embed=embed_igrac)
                            await channel.send("Odabrali ste hit", delete_after=2)
                        elif message_content == "stand":
                            if diler == igrac:
                                break
                            if diler > 17:
                                break
                            await channel.send("Odabrali ste stand", delete_after=2)
                        elif message_content == "kraj":
                            break
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
                        dobitak = int(ctx_message[1]) * 1.5 + int(ctx_message[1])
                        user_bank.money += dobitak
                        await channel.send(f"Igrac je dobio black jack! Vas dobitak je {dobitak}")
                    elif diler > 21:
                        dobitak = int(ctx_message[1]) * 2
                        user_bank.money += dobitak
                        await channel.send(
                            f"Diler je proglasio kraj igre i igrac je pobijedio! Vas dobitak je {dobitak}")
                    elif igrac > diler:
                        dobitak = int(ctx_message[1]) * 2
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

    @commands.command(aliases=['ds'])
    async def Spin(self,ctx):
        def temp_multiple(object, n, item):
            for i in range(n):
                object.append(item)

        def randomize_emojis(emojis, n):
            randomized = dict()
            for i in range(len(emojis)):
                randomized[emojis[i]] = random.randint(1, n / 2)
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
                    emojis = ["💰", "💲", "🍕", "🍞", "✨", "⬜"]
                    randomize = randomize_emojis(emojis, 20)
                    spinwheel = ""
                    for i in range(20):
                        random_item = random.choice(emojis)
                        while randomize[random_item] == 0:
                            random_item = random.choice(emojis)
                        spinwheel = spinwheel + random_item
                    start = spinwheel[0:3]
                    tick = 0.2
                    msg = await ctx.send(f"{start}\n"
                                         f"               👆   ", ephemeral=True)
                    for i in range(3, 18):
                        if i >= 13:
                            tick += 0.1
                        await asyncio.sleep(tick)
                        start = spinwheel[i - 3:i]
                        await msg.delete()
                        msg = await ctx.send(f"{start}\n"
                                             f"               👆   ", ephemeral=True)

                    msg = await ctx.send(f"{start}\n"
                                         f"             👆   ", ephemeral=True)
                    await asyncio.sleep(2)
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
async def setup(bot):
    await bot.add_cog(Games(bot))