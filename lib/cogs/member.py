import discord
from discord.ext import commands

# discord cog
class MemberCommands:

    def __init__(self, bot):
        self.bot = bot
    
    #commands
    @commands.command(aliases=["info"])
    async def userinfo(self, ctx):
        profile = ctx.message.mentions[0]
        roles = [role.name for role in profile.roles
                 if role.name != "@everyone"]
        
        em = discord.Embed(title = "profile")
        em.add_field(name="name", value=profile.display_name)
        em.add_field(name="bot", value=str(profile.bot))
        em.add_field(name="joined at", value=str(profile.joined_at))
        em.add_field(name="roles", value="\n".join(roles))
        em.set_image(url=profile.avatar_url_as(static_format="jpg"))

        await ctx.send(embed=em)
# Bot本体側からCogを読み込む際に呼び出される関数.
def setup(bot):
    bot.add_cog(MemberCommands(bot))