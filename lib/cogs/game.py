import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone

from lib import riotapi

# discord cog
class GameCommands:

    def __init__(self, bot):
        self.bot = bot

    #commands    
    @commands.group(name="lol")
    async def riot_lol(self, ctx):
        """
        サブコマンドが必要
        """
        if ctx.invoked_subcommand is None:
            await ctx.send("サブコマンドを入力してください.")
    
    #riot_lol commands
    @riot_lol.command(aliases=["summoner"])
    async def summoner_info(self, ctx, summoner_name):
        lol = riotapi.RiotAPI()
        contents = lol.get_summoner(summoner_name)
        JST = timezone(timedelta(hours=+9), 'JST')
        
        summoner_rank = contents["tier"]+contents["rank"]
        winrate =  100 * round(contents["wins"] / (contents["wins"] + contents["losses"]), 2)
        rank_content = "win:{0}, lose:{1}, winrate:{2}%".format(contents["wins"],
                                                                contents["losses"],
                                                                winrate)

        em = discord.Embed(
            title=contents["summonerName"],
            timestamp=datetime.now(tz=JST),
        )
        em.set_image(url=contents["icon_url"])
        
        em.add_field(name="Rank",value=summoner_rank)
        em.add_field(name="Level",value=contents["summonerLevel"])
        em.add_field(name="winrate",value=rank_content)
        em.add_field(name="LP",value=contents["leaguePoints"])
        em.add_field(name="League Name",value=contents["leagueName"])

        await ctx.send(embed=em)
    
    @riot_lol.command()
    async def spectate(self, ctx, summoner_name):
        lol = riotapi.RiotAPI()
        team_blueside = ""
        team_redside = ""
        try:
            summoners = lol._get_spectate_summoner_info(summoner_name)
        except TypeError as err:
            print(err)
            ctx.send(summoner_name + "は見つかりませんでした")

        for summoner in summoners:
            if summoner["teamId"] == "100":
                team_blueside += summoner[0]
            else:
                team_redside += summoner[0]
        
        ctx.send(team_blueside+"\nvs\n"+team_redside)


# Bot本体側からCogを読み込む際に呼び出される関数.
def setup(bot):
    bot.add_cog(GameCommands(bot))