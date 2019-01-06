import discord
from discord.ext import commands

from lib import dmm
# discord cog
class DMMSaleCommands:
    """
    ユーティリティーコマンド
    """
    def __init__(self, bot):
        self.bot = bot

    # command
    @commands.command()
    async def dmm_sale(self, ctx):
        """
        """
        em = self._make_dmm_embed(0)

        msg = await ctx.send(embed=em)
        await msg.add_reaction("👈")
        await msg.add_reaction("👉")
        self.bot.loop.create_task(self.reaction_dmm_sale(msg))
    
    #####################
    # dmm_sale function #
    #####################
    async def reaction_dmm_sale(self, message):
        idx = 0
        num_sale = dmm.get_num_DMM_sale()
        while True:
            def check(reaction, user):
                reactionlist = "👈👉"
                if user == self.bot.user:
                    return False
                return reaction.emoji in reactionlist

            reaction, user = await self.bot.wait_for("reaction_add", check=check)
            emoji = reaction.emoji
            
            if emoji == "👈":
                idx -= 1
                if 0 > idx:
                    idx = num_sale - 1
            elif emoji == "👉":
                idx += 1
                if num_sale <= idx:
                    idx = 0

            em = self._make_dmm_embed(idx)

            await message.edit(embed=em)
            await message.remove_reaction(emoji, user)

    def _make_dmm_embed(self, idx):
        sale = dmm.getDMMCampaigns(idx)
        
        em = discord.Embed(
            title=str(idx) + ". " + sale[2],
            url=sale[3]
        )
        em.add_field(name="Price Down", value=sale[0])
        em.add_field(name="sale term", value=sale[1])
        em.add_field(name="campaign", value=sale[2])
        em.add_field(name="top eroge title", value=sale[4][1] if sale[4][1] is not None else "None")
        em.add_field(name="top eroge url", value=sale[4][2] if sale[4][2] is not None else "None")
        if sale[4][0] is not None:
            em.set_image(url=sale[4][0])

        return em
        
# Bot本体側からCogを読み込む際に呼び出される関数./
def setup(bot):
    bot.add_cog(DMMSaleCommands(bot))