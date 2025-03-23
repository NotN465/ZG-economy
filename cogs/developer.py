import discord
from discord.ext import commands
from sqlalchemy import create_engine
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import User,Bank,Inventory,Stocks,Server,CommunityMarket
import json


#event - @commands.Cog.Listener()
#command - @commands.command()
developer_status = ["411797205020704768"]
engine = create_engine('sqlite:///UserInfo.db')
Session = sessionmaker(bind=engine)
session = Session()

class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def daj_pare(self,ctx):
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

    @commands.command()
    async def oduzmi_pare(self,ctx):
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

    @commands.command()
    async def daj_xp(self,ctx):
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
                await ctx.send(
                    "Pogresan format komande! Upisi !daj_xp <@korisnik> <vrsta_xp> <kolicina>\nVrste xp su: xp, chop_xp, mine_xp, fishing_xp")

    @commands.command()
    async def daj_dionice(self,ctx):
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
                price = data[vrsta_dionica]
                if vrsta_dionica == "MEME":
                    user.MEME += int(kolicina) / price
                elif vrsta_dionica == "TROLL":
                    user.TROLL += int(kolicina) / price
                elif vrsta_dionica == "FOMO":
                    user.FOMO += int(kolicina) / price
                elif vrsta_dionica == "YOLO":
                    user.YOLO += int(kolicina) / price
                elif vrsta_dionica == "LOL":
                    user.LOL += int(kolicina) / price
                await ctx.send(f"{user_name.name} dobija {kolicina} {vrsta_dionica} od strane {ctx.author.mention}")
                session.commit()

    @commands.command()
    async def daj_stvar(self,ctx):
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

    @commands.command()
    async def ocisti_poruke(self,ctx):
        if str(ctx.author.id) in developer_status:
            message = ctx.message.content
            message = message.split(" ")
            if len(message) == 2:
                amount = int(message[1]) + 1
                await ctx.channel.purge(limit=amount)
                await ctx.send(f"{amount} poruke su obrisane!")

    @commands.command()
    async def oduzmi_xp(self,ctx):
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
                await ctx.send(
                    "Pogresan format komande! Upisi !oduzmi_xp <@korisnik> <vrsta_xp> <kolicina>\nVrste xp su: xp, chop_xp, mine_xp, fishing_xp")

async def setup(bot):
    await bot.add_cog(Developer(bot))