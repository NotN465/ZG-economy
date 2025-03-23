import discord
from discord.ext import commands

developer_status = ["411797205020704768"]


class Help(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def pomoc(self,ctx):
        embed_pomoc = discord.Embed(
            title="Pomoc",
            description="Pomoc za sve komande dostupne koristeci bota.",
            color=discord.Color.blue()
        )

        embed_pomoc.add_field(name="!NapraviProfil", value="Napravi novi profil na serveru.", inline=False)
        embed_pomoc.add_field(name="!stanje", value="Prikazuje stanje racuna.", inline=False)
        embed_pomoc.add_field(name="!posao",
                              value="Prikazuje poslove i njihovu zaradu i omogućava zapošljavanje. Poslovi su:\nPrvi sektor: Farmer, Ribar, Rudar, Drvosječa, Lovac, Pčelar, Vinogradar, Voćar, Cvjećar, Stožar"
                                    "\nDrugi sektor: Radnik u tvornici, Zidar, Bravar, Električar, Stolar, Automehaničar, Kovač, Vodoinstalater, Tekstilni radnik, Keramičar"
                                    "\nTreci sektor: Liječnik, Pravni savjetnik, Inženjer, Profesor, Arhitekt, Farmaceut, Psiholog, Računalni programer, Ekonomist, Financijski analitičar",
                              inline=False)
        embed_pomoc.add_field(name="!radi", value="Omogućuje zarađivanje i dobivanje plače koja je prikazana u !posao.",
                              inline=False)
        embed_pomoc.add_field(name="!stvari", value="Prikazuje sve stvari koje imas u racunu.", inline=False)
        embed_pomoc.add_field(name="!drva", value="Omogućava sijecanje drva i dobivanje xp-a za drvo.", inline=False)
        embed_pomoc.add_field(name="!rude", value="Omogućava rudarenje ruda i dobivanje xp-a za rude.", inline=False)
        embed_pomoc.add_field(name="!ribarenje", value="Omogućava ribarenje i dobivanje xp-a za ribarenje.",
                              inline=False)
        embed_pomoc.add_field(name="!trade",
                              value="Upisi !trade <@korisnik> <proizvod koji primas> <kolicina> <proizvod koji dajes> <kolicina>.",
                              inline=False)
        embed_pomoc.add_field(name="!pokloni", value="Pokloni neku stvar korisniku", inline=False)
        embed_pomoc.add_field(name="!plati", value="Daj pare korisniku", inline=False)
        embed_pomoc.add_field(name="!provjeri_level", value="Provjerava level korisnika", inline=False)
        embed_pomoc.add_field(name="!rulet", value="Pokrece rulet.", inline=False)
        embed_pomoc.add_field(name="!blackjack", value="Pokrece blackjack.", inline=False)
        embed_pomoc.add_field(name="!najbogatiji", value="Prikazuje 10 najbogatijih korisnika", inline=False)
        embed_pomoc.add_field(name="!dionice_pomoc", value="Pomoc za dionice", inline=False)

        embed_pomoc.set_footer(text="Bot created by NotN465")

        await ctx.send(embed=embed_pomoc)

    @commands.command()
    async def dionice_pomoc(self,ctx):
        embed_dionice = discord.Embed(
            title="Pomoc za dionice",
            description="Pomoc za sve komande dostupne koristeci bota u vezi dionica.",
            color=discord.Color.blue()
        )

        embed_dionice.add_field(name="!dionice", value="Prikazuje dostupne dionice", inline=False)
        embed_dionice.add_field(name="!moje_dionice", value="Prikazuje dionice koje imas i jel tradeas long ili short",
                                inline=False)
        embed_dionice.add_field(name="!kupi_dionice", value="Upisi !dionice_kupi <dionica> <kolicina za kupnju>",
                                inline=False)
        embed_dionice.add_field(name="!prodaj_dionice",
                                value="Upisi !dionice_prodaj <dionica> <kolicina za prodaju izrazena u dionicama(ne u kunama)>",
                                inline=False)
        embed_dionice.add_field(name="!prikazuj_dionice", value="Setup za prikazivanje dionica u odredenom kanalu.",
                                inline=False)
        embed_dionice.set_footer(text="Pomoc za komande dionica")

        await ctx.send(embed=embed_dionice)
    @commands.command()
    async def developer_pomoc(self,ctx):
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

async def setup(bot):
    await bot.add_cog(Help(bot))