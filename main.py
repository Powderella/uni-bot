import discord
from discord.ext import commands # Bot Commands Frameworkをインポート
import settings

import traceback

import os

cogs_path = ".\\lib\\cogs\\"
cogs = os.listdir(cogs_path)

# 読み込むCogの名前を格納しておく.
INITIAL_COGS = ["lib.cogs." + cog.strip(".py")
                for cog in cogs
                if cog.endswith(".py")]


# クラスの定義。ClientのサブクラスであるBotクラスを継承。
class MyBot(commands.Bot):

    def __init__(self, command_prefix):
        super().__init__(command_prefix)

        for cog in INITIAL_COGS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    # Botの準備完了時に呼び出されるイベント
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        print("opus lib is loaded :", discord.opus.is_loaded())

    # メッセージを受信した際に呼び出されるイベント
    async def on_message(self, message):
        if message.author.bot: # メッセージの送信者がBotなら、処理を終了する。
            return
        
        await self.process_commands(message)


# MyBotのインスタンス化及び起動処理。
if __name__ == '__main__':
    bot = MyBot(command_prefix='.') # command_prefixはコマンドの最初の文字として使うもの。 e.g. !ping
    bot.run(settings.DISCORD_TOKEN) # Botのトークン