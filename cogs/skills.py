import discord
from discord.ext import commands
from sqlalchemy import create_engine, Column, Integer, String,func
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import User,Bank,Inventory,Stocks,Server,CommunityMarket
from main import ids,prvi_sektor_poslovi,drugi_sektor_poslovi,treci_sektor_poslovi,level_xp
from datetime import datetime,timedelta

engine = create_engine('sqlite:///UserInfo.db')
Session = sessionmaker(bind=engine)
session = Session()

class Skills(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def posao(self,ctx):
        if str(ctx.author.id) in ids():
            user = session.query(User).filter_by(id=str(ctx.author.id)).first()
            raw_message = ctx.message.content
            raw_message = raw_message.split(" ")
            if len(raw_message) == 1 or len(raw_message) > 2:
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

    @commands.command()
    async def radi(self,ctx):
        '''

        Ova komanda ne radi uopce!!

        '''
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
                await ctx.send(
                    "Vec ste radili, morate pricekati 4 sata od zadnjeg puta kada ste radili da bi mogli opet raditi.")
        else:
            await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")

    @commands.command()
    async def drva(self,ctx):
        if str(ctx.author.id) in ids():
            user = session.query(User).filter_by(id=str(ctx.author.id)).first()
            last_chop_time = str(user.last_chop_time)
            if datetime.strptime(last_chop_time, "%M-%H-%d-%m-%Y") + timedelta(hours=2) < datetime.now():
                user.chop_xp += 100
                user.last_chop_time = datetime.now().strftime("%M-%H-%d-%m-%Y")
                session.commit()
                await ctx.send(f"Dobili ste 100 xp za drva i trenutni xp je {user.chop_xp}")
            else:
                await ctx.send(
                    "Vec ste cijepali drva, morate pricekati 2 sata od zadnjeg puta kada ste cjepali da bi mogli opet cjepati.")
        else:
            await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")

    @commands.command()
    async def rude(self,ctx):
        if str(ctx.author.id) in ids():
            user = session.query(User).filter_by(id=str(ctx.author.id)).first()
            last_mine_time = str(user.last_mine_time)
            if datetime.strptime(last_mine_time, "%M-%H-%d-%m-%Y") + timedelta(hours=2) < datetime.now():
                user.mine_xp += 100
                user.last_mine_time = datetime.now().strftime("%M-%H-%d-%m-%Y")
                session.commit()
                await ctx.send(f"Dobili ste 100 xp za rude i trenutni xp je {user.mine_xp}")
            else:
                await ctx.send(
                    "Vec ste rudarili, morate pricekati 2 sata od zadnjeg puta kada ste rudarili da bi mogli opet rudariti.")
        else:
            await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")

    @commands.command()
    async def ribarenje(self,ctx):
        if str(ctx.author.id) in ids():
            user = session.query(User).filter_by(id=str(ctx.author.id)).first()
            last_fishing_time = str(user.last_fishing_time)
            if datetime.strptime(last_fishing_time, "%M-%H-%d-%m-%Y") + timedelta(hours=2) < datetime.now():
                user.fishing_xp += 100
                user.last_fishing_time = datetime.now().strftime("%M-%H-%d-%m-%Y")
                session.commit()
                await ctx.send(f"Dobili ste 100 xp za ribarenje i trenutni xp je {user.fishing_xp}")
            else:
                await ctx.send(
                    "Vec ste ribarili, morate pricekati 2 sata od zadnjeg puta kada ste ribarili da bi mogli opet ribariti.")
        else:
            await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")

async def setup(bot):
    await bot.add_cog(Skills(bot))