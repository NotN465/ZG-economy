import discord
from discord.ext import commands
from sqlalchemy import create_engine, Column, Integer, String,func
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import User,Bank,Inventory,Stocks,Server,CommunityMarket
from discord.ui import  View,Button
from main import ids
"""


Treba popraviti market - ne zeli se pokazati embed


"""


engine = create_engine('sqlite:///UserInfo.db')
Session = sessionmaker(bind=engine)
session = Session()


class MarketEmbeds(View):
    def __init__(self, embeds):
        super().__init__()
        self.page = 0
        self.embeds = embeds

    @discord.ui.button(label="◀", style=discord.ButtonStyle.gray)
    async def previous_page(self, interaction: discord.Interaction, button: Button):
        if self.page > 0:
            self.page -= 1
            if self.page == 0:
                button.disabled = True
                self.children[1].disabled = False
            else:
                button.disabled = False
                self.children[1].disabled = False
            await interaction.response.edit_message(embed=self.embeds[self.page], view=self)
        else:
            button.disabled = False
            self.children[1].disabled = False
            await interaction.response.edit_message(embed=self.embeds[self.page], view=self)

    @discord.ui.button(label="▶", style=discord.ButtonStyle.gray)
    async def next_page(self, interaction: discord.Interaction, button: Button):
        print(self.page, len(self.embeds) - 1)
        if self.page < len(self.embeds) - 1:
            self.page += 1
            if self.page == len(self.embeds) - 1:
                button.disabled = True
                self.children[0].disabled = False
            else:
                button.disabled = False
                self.children[0].disabled = False
            await interaction.response.edit_message(embed=self.embeds[self.page], view=self)

        else:
            button.disabled = False
            self.children[0].disabled = False
            await interaction.response.edit_message(embed=self.embeds[self.page], view=self)

class Market(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def market(self,ctx):
        embeds = []
        market_dict = {}
        market_items = session.query(CommunityMarket).all()
        guild = self.bot.get_guild(ctx.guild.id)
        for user_items in market_items:
            for item, value in user_items.items.items():
                print(item,value)
                user = await self.bot.fetch_user(int(user_items.user_id))
                print(user.name)
            for item_name, item_value in user_items.items.items():
                user = await self.bot.fetch_user(int(user_items.user_id))
                item_name = item_name + f' : {user.name}'
                market_dict[item_name] = item_value
                print(item_name,item_value,user.name)
        broj_stranica = int(len(market_dict) / 5) + 1
        market_embed = discord.Embed(title="Market", color=discord.Color.dark_blue())
        market_embed.set_footer(text=f"Stranica 1/{broj_stranica}")
        for i in range(len(market_dict)):
            if i % 5 == 0 and i != 0:
                embeds.append(market_embed)
                market_embed = discord.Embed(title="Market",
                                             color=discord.Color.dark_blue())
                market_embed.set_footer(text=f"Stranica {int(i / 5) + 1}/{broj_stranica}")
            if (i == len(market_dict) - 1 and i % 5 != 0) or (i == len(market_dict) - 1 and len(market_dict) < 5):
                market_embed.add_field(name=list(market_dict.keys())[i],
                                       value=f'Kolicina: {list(market_dict.values())[i][1]}\nCijena jednog:{list(market_dict.values())[i][0]}',
                                       inline=False)
                embeds.append(market_embed)
            else:
                market_embed.add_field(name=list(market_dict.keys())[i],
                                       value=f'Kolicina: {list(market_dict.values())[i][1]}\nCijena jednog: {list(market_dict.values())[i][0]}kn',
                                       inline=False)
        view = MarketEmbeds(embeds)
        view.children[0].disabled = True
        if len(embeds) == 1:
            view.children[1].disabled = True

        await ctx.send(embed=embeds[0], view=view)

    @commands.command()
    async def prodaj(self,ctx):
        if str(ctx.author.id) in ids():
            message = ctx.message.content
            message = message.split(" ")
            if len(message) == 4:
                market = session.query(CommunityMarket).all()
                market_ids = map(lambda x: int(x.user_id), market)
                inventory = session.query(Inventory).filter_by(user_id=str(ctx.author.id)).first()
                if message[1] in inventory.items.keys() and int(message[3]) <= inventory.items[message[1]]:
                    inventory.items[message[1]] -= int(message[3])
                    flag_modified(inventory, "items")
                    session.commit()
                    if int(ctx.author.id) not in list(market_ids):
                        market = CommunityMarket(user_id=str(ctx.author.id), items={})
                        session.add(market)
                        session.commit()
                    user_market = session.query(CommunityMarket).filter_by(user_id=str(ctx.author.id)).first()
                    if message[1] in user_market.items.keys():
                        user_market.items[message[1]] = [int(message[2]),
                                                         int(message[3]) + user_market.items[message[1]][1]]
                        flag_modified(user_market, "items")
                        session.commit()
                        await ctx.send(
                            f"Cijena {message[1]} je promjenjena na {message[2]}kn za jedan i dodano ih je jos {message[3]} za prodaju")
                        return
                    cijena = int(message[2])
                    kolicina = int(message[3])
                    user_market.items[str(message[1])] = [cijena, kolicina]
                    flag_modified(user_market, "items")
                    session.commit()
                    await ctx.send(
                        f"Uspjesno ste {message[3]} {message[1]} stavili na prodaju za {message[2]}kn za jedan")
                else:
                    await ctx.send("Nemate tu kolicinu tog proizvoda.")
            else:
                await ctx.send("Pogresan format komande! Upisi !prodaj <ime_proizvoda> <cijena_u_kn> <kolicina>")
        else:
            await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")

    @commands.command()
    async def market_kupi(self,ctx):
        print(ctx.author.id)
        if str(ctx.author.id) in ids():
            message = ctx.message.content
            message = message.split(' ')
            if len(message) == 3:
                market_list = []
                market_items = session.query(CommunityMarket).all()
                for user_items in market_items:
                    for item_name in user_items.items.keys():
                        if item_name not in market_list:
                            market_list.append(str(item_name))
                smallest_user = 0
                smallest_price = 0
                if str(message[1]) in market_list:
                    for user_items in market_items:
                        for item_name, item_value in user_items.items.items():
                            if item_value < smallest_price:
                                smallest_price = int(item_value)
                                smallest_user = str(user_items.user_id)
                    smallest_user_market = session.query(CommunityMarket).filter_by(user_id=smallest_user).first()
                    smallest_user_market_bank = session.query(Bank).filter_by(user_id=smallest_user).first()
                    user_market = session.query(Inventory).filter_by(user_id=str(ctx.author.id)).first()
                    user_market_bank = session.query(Bank).filter_by(user_id=str(ctx.author.id)).first()
                    if int(message[2]) * smallest_price <= user_market.money:
                        user_market_bank.money -= int(message[2]) * smallest_price
                        user_market.items[str(message[1])] += int(message[2])
                        flag_modified(user_market, "items")
                        session.commit()
                        smallest_user_market_bank.money += int(message[2]) * smallest_price
                        smallest_user_market.items[str(message[1])] -= int(message[2])
                        flag_modified(smallest_user_market, "items")
                        session.commit()
                        await ctx.send(
                            f"Uspjesno ste kupili {message[2]} {message[1]} za {int(message[2]) * smallest_price}kn")
                    else:
                        await ctx.send("Nemate dovoljno novca!")
                    # Provjerio si jel postoji na marketu, sad moras napraviti to da mozes kupiti najjeftiniji proizvod od onih koji trazi
                else:
                    await ctx.send("Tog proizvoda nema na marketu")
            else:
                await ctx.send("Pogresan format komande, tocan format glasi ovako: !market_kupi <proizvod> <kolicina>")
        else:
            await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")

    @commands.command()
    async def na_prodaji(self,ctx):
        if str(ctx.author.id) in ids():
            item_embed = discord.Embed(title="Proizvodi", color=discord.Color.dark_blue())
            item_embed.set_footer(text=f"Proizvodi od {ctx.author.name} koji su na prodaji")
            user_market_items = session.query(CommunityMarket).filter_by(user_id=int(ctx.author.id)).first()
            for item_name, item_value in user_market_items.items.items():
                item_embed.add_field(name=item_name, value=f"Kolicina: {item_value[1]}\nCijena jednog: {item_value[0]}")
            await ctx.send(embed=item_embed)
        else:
            await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")

    @commands.command()
    async def makni_proizvod(self,ctx):
        if str(ctx.author.id) in ids():
            message = ctx.message.content
            message = message.split(' ')
            proizvod = str(message[1])
            kolicina = int(message[2])
            user_market_inv = session.query(CommunityMarket).filter_by(user_id=str(ctx.author.id)).first()
            user_inv = session.query(Inventory).filter_by(user_id=str(ctx.author.id)).first()
            print(user_market_inv.items, user_inv.items, user_market_inv.items[proizvod])
            if len(message) == 3:
                if proizvod in user_market_inv.items.keys() and user_market_inv.items[proizvod][1] >= kolicina:
                    if kolicina == user_market_inv.items[proizvod][1]:
                        user_market_inv.items.pop(proizvod)
                    else:
                        user_market_inv.items[proizvod][1] -= kolicina
                    flag_modified(user_market_inv, "items")
                    if proizvod in user_inv.items:
                        user_inv.items[proizvod] += kolicina
                    else:
                        user_inv.items[proizvod] = kolicina
                    flag_modified(user_inv, "items")
                    session.commit()
                    await ctx.send(f"Uspjesno ste maknuli {kolicina} {proizvod}")
                else:
                    await ctx.send(
                        "Taj proizvod ne postoji na vasoj prodaji ili ste stavili preveliku kolicinu tog proizvoda.")
        else:
            await ctx.send("Korisnik nije pronadjen, !NapraviProfil za napraviti racun!")
async def setup(bot):
    await bot.add_cog(Market(bot))