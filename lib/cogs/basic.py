from discord.ext import commands

# discord cog
class BasicCommands:

    def __init__(self, bot):
        self.bot = bot
    
    #commands
    @commands.command()
    async def hello(self, ctx):
        reply = "Hello, {0}".format(ctx.author)
        await ctx.send(reply)

    @commands.command()
    async def shutdown(self, ctx):
        #if return
        reply = "byebye!!"
        await ctx.send(reply)
        exit()
    
    @commands.command()
    async def reboot(self, ctx):
        import subprocess
        reply = "再起動します。"
        await ctx.send(reply)
        subprocess.Popen("py main.py")
        exit()
    
    @commands.command()
    async def now(self, ctx):
        from datetime import datetime
        reply = str(datetime.now())
        await ctx.send(reply)

    @commands.command()
    async def eval(self, ctx, message):
        reply = str(eval(message))
        await ctx.send(reply)

# Bot本体側からCogを読み込む際に呼び出される関数.
def setup(bot):
    bot.add_cog(BasicCommands(bot))