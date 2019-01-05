import discord
from discord.ext import commands

# discord cog
class VoiceCommand:

    def __init__(self, bot):
        self.bot = bot

    #commands
    @commands.command()
    async def connect(self, ctx):
        # authorの接続しているボイスチャンネルに接続する
        if ctx.author.voice is None:
            await ctx.send("ボイスチャンネルに参加してください.")
        else:
            self._voice = await ctx.author.voice.channel.connect()
    
    @commands.command()
    async def disconnect(self, ctx):
        if ctx.guild.voice_client in self.bot.voice_clients:
            await self._voice.disconnect()
        else:
            reply = "{0}はボイスチャンネルに接続していません."
            await ctx.send(reply.format(self.bot.user.display_name))



# Bot本体側からCogを読み込む際に呼び出される関数.
def setup(bot):
    bot.add_cog(VoiceCommand(bot))