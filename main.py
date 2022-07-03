import requests
import interactions
from interactions.ext.wait_for import wait_for,setup

Token = ""

bot = interactions.Client(token=Token, intents = interactions.Intents.ALL)
setup(bot)

@bot.command(
    name="chart",
    description="指定の仮想通貨のチャートを定期的に通知します",
    options= [
        interactions.Option(
            type=interactions.OptionType.STRING,
            name="coin", 
            description="仮想通貨", 
            required=True,
            choices=[
        interactions.Choice(name="btc", value="bitcoin"),
        interactions.Choice(name="ltc", value="litecoin"),
        interactions.Choice(name="eth", value="ethereum")
            ], 
        ),
    ],
)

async def chart(ctx: interactions.CommandContext, coin:str):
    jma_url = f"https://api.coinstats.app/public/v1/coins/{coin}?currency=JPY"
    jma_json = requests.get(jma_url).json()
    jma_name = jma_json["coin"]["symbol"]
    jma_price = jma_json["coin"]["price"]
    jma_volume = jma_json["coin"]["volume"]
    jma_marketcap = jma_json["coin"]["marketCap"]

    if coin == "bitcoin":
        jma_icon = "https://media.discordapp.net/attachments/991686407787659324/993066938035093524/unknown.png"
        jma_color = 0xed9023

    elif coin == "litecoin":
        jma_icon = "https://media.discordapp.net/attachments/991686407787659324/993092279088713738/unknown.png?width=641&height=641"
        jma_color = 0x3c5a9a

    elif coin == "ethereum":
        jma_icon = "https://media.discordapp.net/attachments/991686407787659324/993090976488902686/unknown.png?width=641&height=641"
        jma_color = 0x8c8c8c

    embed=interactions.Embed(title=f"{jma_name}'s chart", color=jma_color)
    embed.set_thumbnail(url=jma_icon)
    embed.add_field(name="価格", value=str(jma_price), inline=False)
    embed.add_field(name="ボリューム", value=str(jma_volume), inline=True)
    embed.add_field(name="マーケットキャップ", value=str(jma_marketcap), inline=True)
    embed.set_footer(text="Produced by mepuru210")
    await ctx.send(embeds=embed)

bot.start()
