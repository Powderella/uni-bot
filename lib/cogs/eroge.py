import discord
from discord.ext import commands

import datetime
from dateutil.relativedelta import relativedelta
import asyncio

from lib import dmm
from lib import shinsaku_eroge
# discord cog
class ErogeCommands:
    """
    えっちなげーむようのこまんど
    """
    def __init__(self, bot):
        self.bot = bot

    #group
    @commands.group()
    async def eroge(self, ctx):
        """
        サブコマンド sale, shinsaku
        """
        if ctx.invoked_subcommand is None:
            await ctx.send("サブコマンドを入力してください.")

    # eroge command
    @eroge.command()
    async def sale(self, ctx):
        """
        """
        em = self._make_dmm_embed(0)

        msg = await ctx.send(embed=em)
        await msg.add_reaction("👈")
        await msg.add_reaction("👉")
        self.bot.loop.create_task(self.reaction_eroge(msg, dmm.get_num_DMM_sale(), True))
    
    @eroge.command()
    async def shinsaku(self, ctx, months=0):
        """
        monthsは今月から比較した月を入れる
        """
        self.months = months
        em = self._make_shinsaku_eroge_embed(self.months, 0)

        msg = await ctx.send(embed=em)
        await msg.add_reaction("👈")
        await msg.add_reaction("👉")
        self.bot.loop.create_task(self.reaction_eroge(msg, shinsaku_eroge.num_shinsaku_eroges(self.months), False))

    ###################
    # eroge function  #
    ###################
    async def reaction_eroge(self, message, limit, isSale):
        idx = 0
        while True:
            await asyncio.sleep(1)
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
                    idx = limit - 1
            elif emoji == "👉":
                idx += 1
                if limit <= idx:
                    idx = 0

            if isSale:
                em = self._make_dmm_embed(idx)
            else:
                em = self._make_shinsaku_eroge_embed(self.months, idx)
            await message.edit(embed=em)
            await message.remove_reaction(emoji, user)


    ###################
    # embed functions #
    ###################
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
    
    def _make_shinsaku_eroge_embed(self, months, idx):
        eroge = shinsaku_eroge.shinsaku_eroges(months=months, idx=idx)
        
        today = datetime.date.today()
        view_month = today + relativedelta(months=months)
        current_month = view_month.strftime("%Y-%m")

        em = discord.Embed(
            title=current_month + "発売のエロゲ - " + str(idx),
            url=eroge[2]
        )
        em.add_field(name="title", value=eroge[0])
        em.add_field(name="release date", value=eroge[1][-10:])
        em.add_field(name="maker", value=eroge[1][:-10])
        em.set_image(url=eroge[3])

        return em
# Bot本体側からCogを読み込む際に呼び出される関数./
def setup(bot):
    bot.add_cog(ErogeCommands(bot))