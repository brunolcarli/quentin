"""
Bot valid commands definition.
"""
import discord
from discord.ext import commands

from quentin.settings.common import __version__, IMG_URL
from core.api_call import get_trending

client = commands.Bot(command_prefix='/')


@client.event
async def on_ready():
    """
    Prints a "log message" on the shell informing the bot (system) was
    initialized and running.
    """
    print(f'Running Quentin version {__version__}')



@client.command()
async def get_movies(ctx):
    trends = get_trending('movie', 'day')

    movie = trends['results'][1]

    embed = discord.Embed(color=0x1E1E1E, type='rich')
    embed.add_field(name='Title:', value=movie['original_title'], inline=False)
    embed.add_field(name='Overview:', value=movie['overview'], inline=False)
    embed.add_field(name='Average :chart_with_upwards_trend: :', value=movie['vote_average'], inline=False)
    embed.add_field(name='Popularity :family:  :', value=movie['popularity'], inline=True)
    embed.add_field(name='Release :calendar_spiral: :', value=movie['release_date'], inline=True)

    avatar = f'{IMG_URL}{movie["backdrop_path"]}'
    embed.set_thumbnail(url=avatar)

    await ctx.send(f'Movie ID: {movie["id"]}', embed=embed)
