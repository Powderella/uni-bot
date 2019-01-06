import discord
from discord.ext import commands

from lib import short_url
from lib import translate
# discord cog
class UtilityCommands:
    """
    ユーティリティーコマンド
    """
    def __init__(self, bot):
        self.bot = bot
    
    #commands
    @commands.command(aliases=["shorturl"])
    async def shorten_url(self, ctx, url):
        """
        bit.lyを使ってURLを短くして返すぞ！！！！！
        """
        reply = short_url.get_shortenURL(url)
        await ctx.send(reply)

    @commands.command()
    async def trans(self, ctx, target, *text):
        """
        GASを使って翻訳するぞ、翻訳。
        """
        reply = translate.translate(text, "", target)
        await ctx.send(reply)
    
    @commands.command()
    async def github(self, ctx):
        """
        uni-botのURLを返すぞ
        """
        em = discord.Embed(
            title="uni-bot",
            url="https://github.com/Powderella/uni-bot"
        )

        await ctx.send(embed=em)
# Bot本体側からCogを読み込む際に呼び出される関数.
def setup(bot):
    bot.add_cog(UtilityCommands(bot))