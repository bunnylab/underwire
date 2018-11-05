import discord
from discord.ext import commands

prefix = ''
bot = commands.Bot(command_prefix=prefix, self_bot=True)

@bot.event
async def on_ready():
    print("selfbot is ready")

bot.run('MjM1OTU1MTUxNTUzMjk4NDMy.CuCF-w.uJdfCsrglxNxoEeaM1jtFwZBbgA', bot=False)
#client.run('MjM1OTU1MTUxNTUzMjk4NDMy.CuCF-w.uJdfCsrglxNxoEeaM1jtFwZBbgA')

#client.login("MjM1OTU1MTUxNTUzMjk4NDMy.CuCF-w.uJdfCsrglxNxoEeaM1jtFwZBbgA")
#client.connect()
#client.close()
