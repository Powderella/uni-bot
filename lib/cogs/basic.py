from discord.ext import commands

# discord cog
class BasicCommands:

    def __init__(self, bot):
        self.bot = bot
    
    #commands
    @commands.command()
    async def hello(self, ctx):
        """
        あいさつします！
        """
        reply = "Hello, {0}".format(ctx.author)
        await ctx.send(reply)

    @commands.command()
    async def shutdown(self, ctx):
        """
        さよならします！(プログラムを終了する)
        """
        reply = "byebye!!"
        await ctx.send(reply)
        exit()
    
    @commands.command()
    async def reboot(self, ctx):
        """
        再起動する！
        """
        import subprocess
        reply = "再起動します。"
        await ctx.send(reply)
        subprocess.Popen("py main.py")
        exit()

    @commands.command(name="eval")
    async def eval_(self, ctx, message):
        """
        計算する.
        """
        reply = str(eval(message))
        await ctx.send(reply)

# Bot本体側からCogを読み込む際に呼び出される関数.
def setup(bot):
    bot.add_cog(BasicCommands(bot))