import discord
from discord.ext import commands
from lib import onsenradio
from lib import short_url

# discord cog
class OnsenRadio:

    def __init__(self, bot):
        self.bot = bot
        self.onsen = onsenradio.OnsenRadio()
        self.radio_path = ".\\sources\\onsen\\"
    
    #######################
    #   utility function  #
    #######################
    async def add_reactions(self, message, emojis):
        for emoji in emojis:
            await message.add_reaction(emoji)

    def make_program_info_embed(self, program_name, is_music_embed=False):
        from datetime import datetime, timedelta, timezone

        contents = self.onsen.show_program_contents(program_name)
        JST = timezone(timedelta(hours=+9), 'JST')

        em = discord.Embed(
            title=contents["title"],
            url=contents["program_url"],
            timestamp=datetime.now(tz=JST),
        )
        em.set_image(url="https://www.onsen.ag"+contents["banner_image"])
        
        if not is_music_embed:
            em.add_field(name="actor",value=contents["actor_tag"])
            em.add_field(name="schedule",value=contents["schedule"])
            em.add_field(name="episode",value=contents["count"])
            em.add_field(name="guests", value=contents["guest"] if contents["guest"] != "" else "None")
            em.add_field(name="download",value=short_url.get_shortenURL(contents["android_url"]))
            em.set_footer(text="powerd by 音泉", icon_url="http://www.onsen.ag/blog/wp-content/uploads/2009/03/onsen.jpg")
        return em

    #################
    #   commands    #
    #################
    @commands.group(aliases=["radio", "onsen"])
    async def onsenradio(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("サブコマンドを入力してください.")
    
    @onsenradio.command()
    async def search(self, ctx, program_name):
        em = self.make_program_info_embed(program_name)
        await ctx.send(embed=em)

    @onsenradio.command(name="list")
    async def listup(self, ctx):
        reply = self._make_message_listup(idx=0)
        
        msg = await ctx.send(reply)

        await self.add_reactions(msg, "👈👉")

        self.bot.loop.create_task(self.reaction_programs(msg))
    
    @onsenradio.command(name="play")
    async def playradio(self, ctx, program_name):
        if ctx.guild.voice_client in self.bot.voice_clients:
            import os

            try:
                contents = self.onsen.show_program_contents(program_name)
            except KeyError:
                await ctx.send("その名前の番組はありません。")
                return

            filename = contents["movie_url"].split("/")[-1]
            self.np = ctx.guild.voice_client
            if not os.path.exists(self.radio_path+filename):
                msg = await ctx.send("download中")
                self.onsen.download_mp3(contents["movie_url"])
                while not os.path.exists(self.radio_path + filename):
                    pass
                await msg.delete()

            ctx.guild.voice_client.play(
                discord.FFmpegPCMAudio(self.radio_path + filename))

            em = self.make_program_info_embed(program_name,
                                              is_music_embed=True)
            np_message = await ctx.send(embed=em)

            await self.add_reactions(np_message, "▶⏸⏏⏮⏭")
            self.bot.loop.create_task(self.reaction_radio(np_message, filename, program_name))

    #############################
    # programs play function    #
    #############################

    async def reaction_radio(self, musicplayer_message, filename, program_name):
        while True:
            def check(reaction, user):
                reactionlist = "▶⏸⏏⏮⏭"
                if user == self.bot.user:
                    return False
                return reaction.emoji in reactionlist

            reaction, user = await self.bot.wait_for("reaction_add", check=check)
            emoji = reaction.emoji

            await self._event_reaction_play(filename, emoji, musicplayer_message, program_name)

            try:
                await musicplayer_message.remove_reaction(emoji, user)
            except discord.errors.NotFound:
                break

    async def _event_reaction_play(self, filename, emoji, musicplayer_message, program_name):
        program_files = self.onsen.search_mp3_from_folder(program_name)
        num_program_files = len(program_files)
        tracknumber_np = program_files.index(filename)

        
        def clac_tracknumber(tracknumber_np ,emoji, change_track_emojis="⏮⏭"):
            if emoji == change_track_emojis[0]:
                if num_program_files-1 <= tracknumber_np:
                    tracknumber_np = 0
                else:
                    tracknumber_np += 1
            elif emoji == change_track_emojis[1]:
                if 0 >= tracknumber_np:
                    tracknumber_np = num_program_files-1
                else:
                    tracknumber_np -= 1
            
            return tracknumber_np
                
        if emoji == "▶":
            if self.np.is_pause():
                self.np.resume()
        elif emoji == "⏸":
            if not self.np.is_pause():
                self.np.pause()
        elif emoji == "⏏":
            self.np.stop()
            await musicplayer_message.delete()
        elif emoji in "⏮⏭":
            self.np.stop()
            tracknumber_np = clac_tracknumber(tracknumber_np, emoji)
            self.np.play(
                discord.FFmpegPCMAudio(self.radio_path+program_files[tracknumber_np]))
        else :
            pass


    #############################
    # programs listup function  #
    #############################

    def _make_message_listup(self, idx):        
        self.programs_list = list(self.onsen.listup_all_programs())
        self.num_programs = len(self.programs_list)

        gen = ("{0:03}. ".format(i) + program for i, program in enumerate(self.programs_list[idx:idx+7], idx+1))
        

        reply = "\n\n".join(gen)
        reply = "`" + reply + "`" + "\n{0:2.0f}/{1}".format(idx//7+1, self.num_programs//7)

        return reply

    async def reaction_programs(self, message):
        idx = 0
        while True:
            def check(reaction, user):
                reactionlist = "👈👉"
                if user == self.bot.user:
                    return False
                return reaction.emoji in reactionlist

            reaction, user = await self.bot.wait_for("reaction_add", check=check)

            emoji = reaction.emoji

            idx = self._event_reaction_listup(idx, emoji)
            
            await message.edit(content=self._make_message_listup(idx))
            
            await message.remove_reaction(emoji, user)
    
    def _event_reaction_listup(self, idx, emoji):
        if emoji == "👈":
            idx -= 7
            if not idx / 7 + 1:
                idx = 7 * (self.num_programs // 7 - 1)
        elif emoji == "👉":
            idx += 7
            if (idx / 7 + 1) > self.num_programs // 7:
                idx = 0
        else :
            pass
        
        return idx

# Bot本体側からCogを読み込む際に呼び出される関数.
def setup(bot):
    bot.add_cog(OnsenRadio(bot))