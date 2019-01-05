import discord
from discord.ext import commands

# discord cog
class ChannelCommands:

    def __init__(self, bot):
        self.bot = bot

    def _get_channel_name(self, channels):
        for channel in channels:
            yield channel.name

    async def _create_channel(self, guild, name,channel_type):
        """
        """
        ct_lower = channel_type.lower()
        if ct_lower == "text":
            await guild.create_text_channel(name)
        elif ct_lower == "voice":
            await guild.create_voice_channel(name)
        elif ct_lower == "category":
            await guild.create_category_channel(name)

    #commands
    @commands.group(aliases=["ch"])
    async def channel(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("サブコマンドを入力してください.")
    
    @channel.command(name="create")
    async def create_channel(self, ctx, name, channel_type):
        reply = "{0} has created {1} {2} channel."
      
        self._create_channel(ctx.guild, name, channel_type)

        await ctx.send(reply.format(ctx.author, name, channel_type))

    @channel.group(name="get")
    async def get_channel(self, ctx):
        self._guild = ctx.message.guild
        if ctx.invoked_with == ctx.subcommand_passed:
            channels = self._guild.channels
            reply = "\n".join(self._get_channel_name(channels))

            await ctx.send(reply)

    @get_channel.command()
    async def text(self, ctx):
        channels = self._guild.text_channels
        reply = "\n".join(self._get_channel_name(channels))

        await ctx.send(reply)
    
    @get_channel.command()
    async def voice(self, ctx):
        channels = self._guild.voice_channels
        reply = "\n".join(self._get_channel_name(channels))

        await ctx.send(reply)
    
    @get_channel.command()
    async def category(self, ctx):
        category = self._guild.categories
        reply = "\n".join(self._get_channel_name(category))

        await ctx.send(reply)



# Bot本体側からCogを読み込む際に呼び出される関数.
def setup(bot):
    bot.add_cog(ChannelCommands(bot))