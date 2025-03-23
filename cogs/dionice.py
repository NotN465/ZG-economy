import discord
from discord.ext import commands
from sqlalchemy import create_engine, Column, Integer, String,func
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import User,Bank,Inventory,Stocks,Server,CommunityMarket
import json
import math
import asyncio
from cogs.Functions import floor_decimal
from main import ids


engine = create_engine('sqlite:///UserInfo.db')
Session = sessionmaker(bind=engine)
session = Session()

class Dionice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def update_dionice(self, server_id):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            session.expire_all()
            server = session.query(Server).all()
            if len(list(server)) == 0:
                first_server = Server(server_id=914183541103919215, stock_market_channel_id=1340120438491189349,
                                      message_stock_market_id=1340478597290397760, stocks={"Temp": 10})
                session.add(first_server)
                session.commit()
            server = session.query(Server).filter_by(server_id=server_id).first()
            dionice_embed = discord.Embed(
                title="Dionice",
                description="Pogledaj dostupne dionice",
                color=discord.Color.dark_blue()
            )
            for stock, price in server.stocks.items():
                dionice_embed.add_field(name=stock, value=f"Cijena: {round(price, 2)}kn", inline=False)
            try:
                chanel = await self.bot.get_channel(server.stock_market_channel_id)
                message = await chanel.fetch_message(int(server.message_stock_market_id))
                await message.edit(embed=dionice_embed)
            except:
                pass
            await asyncio.sleep(15)
    @commands.command()
    async def najbogatiji(self,ctx):
        najbogatiji_embed = discord.Embed(title="Najbogatiji", color=0x00ff00)
        najbogatiji = session.query(Bank).order_by(Bank.money.desc()).limit(10).all()
        for person in najbogatiji:
            najbogatiji_embed.add_field(name=person.user.name, value=person.money, inline=False)
        await ctx.send(embed=najbogatiji_embed)

    @commands.command()
    async def prikazuj_dionice(self,ctx):
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
                        channel = await self.bot.get_channel(int(existing_server.stock_market_channel_id))
                        message_to_delete = await ctx.channel.fetch_message(
                            int(existing_server.message_stock_market_id))
                        await message_to_delete.delete()
                        session.delete(existing_server)
                        session.commit()
                    channel = await self.bot.get_channel(int(message[1]))
                    stocks = await channel.send("temp message")
                    server_setup = Server(server_id=int(server_id), stock_market_channel_id=int(message[1]),
                                          message_stock_market_id=stocks.id, stocks={})
                    session.add(server_setup)
                    session.commit()
                    for guild in self.bot.guilds:
                        asyncio.create_task(self.update_dionice(int(guild.id)))
            else:
                await ctx.send("Pogresan format komande! Upisi !prikazuj_dionice <id od kanala>")
        else:
            await ctx.send("Nemate prava za ovu komandu!")

    @commands.command()
    async def napravi_coin(self,ctx):
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
                        await ctx.send(
                            f"Uspjesno napravljen novi coin {message[1]} sa vrijednosti {message[2]}kn po coinu!")
                else:
                    await ctx.send("Pogresan format komande! Upisi !napravi_coin <ime_coina> <vrijednost u kn>")

    @commands.command()
    async def izbrisi_coin(self,ctx):
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
                if len(message) == 2:
                    if message[1] in existing_server.stocks.keys():
                        users_money = session.query(Stocks).filter(Stocks.stocks.like(f"%{message[1]}%")).all()
                        for user in users_money:
                            user_money = session.query(Bank).filter_by(user_id=int(user.user_id)).first()
                            user_money.money += user.stocks[message[1]] * existing_server.stocks[message[1]]
                            del user.stocks[message[1]]
                            flag_modified(user, "stocks")
                            session.commit()
                        del existing_server.stocks[message[1]]
                        flag_modified(existing_server, "stocks")
                        session.commit()
                        await ctx.send(f"Uspjesno izbrisan coin {message[1]}!")
                else:
                    await ctx.send("Pogresan format komande! Upisi !izbrisi_coin <ime_coina>")

    @commands.command()
    async def dionice(self,ctx):
        dionice_embed = discord.Embed(
            title="Dionice",
            description="Pogledaj dostupne dionice",
            color=discord.Color.dark_blue()
        )
        server = session.query(Server).filter_by(server_id=ctx.guild.id).first()
        data = server.stocks
        for stock, price in data.items():
            dionice_embed.add_field(name=stock, value=f"Cijena: {round(price, 2)}", inline=False)

        await ctx.send(embed=dionice_embed)

    @commands.command()
    async def moje_dionice(self,ctx):
        if str(ctx.author.id) in ids():
            server = session.query(Server).filter_by(server_id=ctx.guild.id).first()
            user_stocks = session.query(Stocks).filter_by(user_id=int(ctx.author.id)).first()
            data = server.stocks
            dionice_embed = discord.Embed(
                title="Moje dionice",
                description="Pogledaj dostupne dionice",
                color=discord.Color.dark_blue()
            )
            for stock_key, stock_value in data.items():
                if stock_key not in user_stocks.stocks.keys():
                    user_stocks.stocks[stock_key] = 0
                    flag_modified(user_stocks, "stocks")
                    session.commit()
                dionice_embed.add_field(name=f"{stock_key}",
                                        value=f"Kolicina dionice: {round(user_stocks.stocks[stock_key], 2)}\nKolicina u kunama: {round(user_stocks.stocks[stock_key] * stock_value, 2)}kn",
                                        inline=False)
            await ctx.send(embed=dionice_embed)
        else:
            await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")

    @commands.command()
    async def kupi_dionice(self,ctx):
        if str(ctx.author.id) in ids():
            message = ctx.message.content
            message = message.split(" ")
            if len(message) == 3:
                user_stocks = session.query(Stocks).filter_by(user_id=int(ctx.author.id)).first()
                user_bank = session.query(Bank).filter_by(user_id=int(ctx.author.id)).first()
                server = session.query(Server).filter_by(server_id=ctx.guild.id).first()
                server_stocks_data = server.stocks
                if message[1] in server_stocks_data.keys():
                    if message[1] not in user_stocks.stocks.keys():
                        user_stocks.stocks[message[1]] = 0
                        flag_modified(user_stocks, "stocks")
                        session.commit()
                    if int(message[2]) > 0 and int(message[2]) < user_bank.money:
                        user_stocks.stocks[message[1]] += int(message[2]) / server_stocks_data[message[1]]
                        flag_modified(user_stocks, "stocks")
                        session.commit()
                        await ctx.send(
                            f"Uspesno kupljeno {math.floor(int(message[2]) / server_stocks_data[message[1]] * 1000) / 1000} dionica {message[1]}")
                    else:
                        await ctx.send("Nemate dovoljno novca na racunu")
                else:
                    await ctx.send(f"Ne postoji dionica sa imenom {message[1]}")
            else:
                await ctx.send("Pogresan format komande! Upisi !dionice_kupi <dionica> <kolicina za kupnju u kunama>")
        else:
            await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")

    @commands.command()
    async def prodaj_dionice(self,ctx):
        if str(ctx.author.id) in ids():
            message = ctx.message.content
            message = message.split(" ")
            if len(message) == 3:
                user_stocks = session.query(Stocks).filter_by(user_id=int(ctx.author.id)).first()
                user_bank = session.query(Bank).filter_by(user_id=int(ctx.author.id)).first()
                server = session.query(Server).filter_by(server_id=ctx.guild.id).first()
                servers_stocks = server.stocks
                if message[1] in list(servers_stocks.keys()):
                    if message[1] in list(user_stocks.stocks.keys()):
                        to_stock = int(message[2]) / servers_stocks[message[1]]
                        if user_stocks.stocks[message[1]] > to_stock:
                            print(to_stock)
                            user_stocks.stocks[message[1]] -= to_stock
                            flag_modified(user_stocks, "stocks")
                            session.commit()
                            user_bank.money += int(message[2])
                            flag_modified(user_bank, "money")
                            session.commit()
                            await ctx.send(
                                f"Uspjesno ste prodali {message[1]} kolicine {floor_decimal(int(message[2]) / servers_stocks[message[1]], 3)} na {message[2]}kn")
                    else:
                        await ctx.send(f"Ne mozes prodati ovu dionicu jer niste kupili nijednu!")
            else:
                await ctx.send(
                    "Pogresan format komande! Upisi !dionice_prodaj <dionica> <kolicina za prodaju u kunama>")
        else:
            await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")


async def setup(bot):
    await bot.add_cog(Dionice(bot))