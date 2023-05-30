########################################################################################################
###                                                                                                    #
##                              Bot für die Organisation der Geschenke einer Feier.                    ##
#                              Ihr könnt in die Datenbank eintragen, welche Person was gegeben hat,    ###
#                               ob sie ein Geschenk oder Geld gegeben haben und ob ihr eine Rückmeldung###
##                              geschickt habt.                                                        ##
###                                                                                                    #
########################################################################################################

####################################################################################
# Copyrigth 2023 by @K.A.R.#6886                                                   #
#Hiermit ist es erlaubt,diesen Code zu nutzen.                                     #
#Dieser Code ist für den eigenen Gebrauch gedacht,                                 #
#weshalb kein Name etc. angegeben werden muss.                                     #
#Es ist nicht erlaubt, diesen Code zu verkaufen.                                   #
#Es ist nicht erlaubt, diesen Code als eigenen auszugeben.                         #
#Dieser Code wurde von @K.A.R.#6886 geschrieben, ohne Hilfsmittel wie z.B. Chatgpt #
####################################################################################

##############
# Installs:  #
# py-cord    #
# aiosqlite  #
##############

### Importe ###
import discord
from discord.ext import commands
from discord.commands import slash_command, Option, SlashCommandGroup
import aiosqlite


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = "test.db"

        #konfi.db = Datenbank in der die Daten gespeichert werden - kann durch andere Datenbank ersetzt werden#


    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect(self.db) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS konfi (
                person TEXT PRIMARY KEY,
                geschenk TEXT,
                geld TEXT,
                rueckmeldung TEXT)
                """)
            ###
            # konfi = Tabelle in der Datenbank - kann durch anderes Fest z.B. Geburtstag ersetzt werden
            # person = Name der Person/Familie
            # geschenk = Geschenk der Person/Familie
            # geld = Geldgeschenk der Person/Familie
            # rueckmeldung = Rückmeldung/Dankeskarte an die Person/Familie - Ja- Gesendet / Nein - Nicht gesendet
            # ###

    konfi = SlashCommandGroup("konfi", "Alle Befehle für die Konfigeschenke")
    #SlashCommandGroup Konfi wird erstellt - Konfi kann durch anderes Fest z.B. Geburtstag ersetzt werden#


    @konfi.command(description="Trage die Personen in die DB ein")
    async def eintragen(self, ctx, person: Option(str, "Die Person die eingetragen wird"), geschenk: Option(str, "Das Geschenk das die Person geschenkt hat"), geld: Option(str, "Das Geld das die Person geschenkt hat")):
        async with aiosqlite.connect(self.db) as db:
            await db.execute("INSERT OR IGNORE INTO konfi (person, geschenk, geld) VALUES (?,?,?)",
                             (person, geschenk, geld))
            await db.commit()
        await ctx.respond(f"Die Person {person} wurde eingetragen! Ihr Geschenk: {geschenk}. Geldgeschenk: {geld}", ephemeral=True)

    #@konfi.command - Befehl wird erstellt - Daten werden in DB eingetragen - aufpassen, dass die Tabelle gleich heißt wie in der on_ready Funktion#

    @konfi.command(description="Lösche eine Person aus der DB")
    async def loeschen(self, ctx, person: Option(str, "Die Person die gelöscht wird")):
        async with aiosqlite.connect(self.db) as db:
            await db.execute("DELETE FROM konfi WHERE person = ?", (person,))
            await db.commit()
        await ctx.respond(f"Die Person {person} wurde gelöscht!", ephemeral=True)

    #@konfi.command - Befehl wird erstellt - Daten einer Person werden aus DB gelöscht - aufpassen, dass die Tabelle gleich heißt wie in der on_ready Funktion#

    @konfi.command(description="Zeige alle Infos aus der DB an!")
    async def anzeigen(self, ctx, person: Option(str, "Die Person die angezeigt wird", required=True)):
        async with aiosqlite.connect(self.db) as db:
            async with db.execute("SELECT geschenk, geld FROM konfi WHERE person = ?", (person,)) as cursor:
                geschenk, geld = await cursor.fetchone()
        embed = discord.Embed(
            title=f"**Alle Infos über {person}**",
            description=f"Geschenk: {geschenk}\nGeld: {geld}",
        )
        await ctx.respond(embed=embed)

    #@konfi.command - Befehl wird erstellt - Daten einer Person werden aus DB angezeigt - aufpassen, dass die Tabelle gleich heißt wie in der on_ready Funktion#

    @konfi.command(description="Änder etwas!")
    async def aendern(self, ctx, person: Option(str, "Die Person die geändert wird", required=True), geschenk: Option(str, "Das Geschenk das die Person geschenkt hat",required=False), geld: Option(str, "Das Geld das die Person geschenkt hat",required=False), rueckmeldung: Option(str, choices = ["Ja","Nein"],required=False)):
        if geschenk is not None:
            async with aiosqlite.connect(self.db) as db:
                await db.execute("UPDATE konfi SET geschenk = (?) WHERE person = ?", (geschenk, person))
                await db.commit()
            await ctx.channel.send(f"Das Geschenk von {person} wurde geändert!")
        if geld is not None:
            async with aiosqlite.connect(self.db) as db:
                await db.execute("UPDATE konfi SET geld = (?) WHERE person = ?", (geld, person))
                await db.commit()
            await ctx.channel.send(f"Das Geld von {person} wurde geändert!")
        if rueckmeldung is not None:
            async with aiosqlite.connect(self.db) as db:
                await db.execute("UPDATE konfi SET rueckmeldung = (?) WHERE person = ?", (rueckmeldung, person))
                await db.commit()
            await ctx.channel.send(f"Die Rückmeldung von {person} wurde geändert!")

        await ctx.respond(f"Die Person {person} wurde geändert!", ephemeral=True)

    #@konfi.command - Befehl wird erstellt - Daten einer Person werden aus DB geändert - aufpassen, dass die Tabelle gleich heißt wie in der on_ready Funktion#

    @konfi.command(description="Zeige alle Daten!")
    async def daten(self, ctx):

        async with aiosqlite.connect(self.db) as db:
            async with db.execute("SELECT person, geschenk, geld, rueckmeldung FROM konfi") as cursor:
                data = await cursor.fetchall()

        embed = discord.Embed(
            title="**Alle Daten aus der DB**",
            description=f"Hier siehst du die Daten aus der DB:",
            colour=discord.Colour.blue()
        )
        persons = []
        geschenke = []
        gelder = []
        rueckmeldungen = []
        for row in data:
            persons.append(row[0])
            geschenke.append(row[1])
            gelder.append(row[2])
            rueckmeldungen.append(row[3])
            print(rueckmeldungen)
            print(persons)
            print(geschenke)
            print(gelder)
            if rueckmeldungen is None:
                rueckmeldungen.append("Nichts")
        embed.add_field(name="Personen", value="\n".join(persons), inline=True)
        embed.add_field(name="Geschenke", value="\n".join(geschenke), inline=True)
        embed.add_field(name="Gelder", value="\n".join(gelder), inline=True)
        embed.add_field(name="Rückmeldungen", value="\n".join(rueckmeldungen), inline=True)
        await ctx.respond(embed=embed)

        #@konfi.command - Befehl wird erstellt - Daten einer Person werden aus DB angezeigt - aufpassen, dass die Tabelle gleich heißt wie in der on_ready Funktion#





def setup(bot):
    bot.add_cog(Base(bot))

    #Base wird als Cog hinzugefügt#