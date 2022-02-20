"""
Bot available commands definition.
"""
from io import BytesIO
import json
import requests
from base64 import b64encode, b64decode
import discord
from discord.ext import commands
from discord import ActionRow, Button, ButtonStyle
from redis import Redis
from ast import literal_eval as evl
from quentin.settings import (__version__, IMG_URL, REDIS_HOST,
                              REDIS_PORT, MYSQL_CONFIG)
from core.api_call import get_trending
from core.util import paginate
from core.db_handler import Database


client = commands.Bot(command_prefix='/')
cache = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)


@client.event
async def on_ready():
    """
    Prints a "log message" on the shell informing the bot (system) was
    initialized and running.
    """
    print(f'Running Quentin version {__version__}')
    await client.change_presence(activity=discord.Game(name=f'/help'))
    print(f'Bot has successfully logged in as: {client.user}')
    print(f'Bot ID: {client.user.id}')
    global responses


@client.on_click()
async def section_up(i: discord.Interaction, button):
    global responses
    section[0] += 1
    # index looping
    if section[0] > section[1] - 1:
        section[0] = 0

    trends = evl(cache.get(page_key))
    sections = list(paginate(trends['results']))
    page, total_pages = trends['page'], trends['total_pages']
    current, last = section
    payloads = []

    await i.defer()
    for movie in sections[current]:
        embed = discord.Embed(color=0x1E1E1E, type='rich')
        embed.add_field(name='Title:', value=movie['original_title'], inline=False)
        embed.add_field(name='Overview:', value=movie['overview'], inline=False)
        embed.add_field(name='Average :chart_with_upwards_trend: :', value=movie['vote_average'], inline=False)
        embed.add_field(name='Popularity :family:  :', value=movie['popularity'], inline=True)
        embed.add_field(name='Release :calendar_spiral: :', value=movie['release_date'], inline=True)

        avatar = f'{IMG_URL}{movie["backdrop_path"]}'
        embed.set_thumbnail(url=avatar)

        payloads.append({
            'content': f'Movie ID: {movie["id"]} - Section {current+1}/{last} - Page: {page}/{total_pages}',
            'embed': embed,
        })

    for message, payload in zip(responses, payloads):
        await message.edit(content=payload['content'], embed=payload['embed'])


@client.on_click()
async def section_down(i: discord.Interaction, button):
    global responses
    section[0] -= 1

    # index looping
    if section[0] < 0:
        section[0] = section[1] - 1

    trends = evl(cache.get(page_key))
    sections = list(paginate(trends['results']))
    page, total_pages = trends['page'], trends['total_pages']
    current, last = section
    payloads = []

    await i.defer()
    for movie in sections[current]:
        embed = discord.Embed(color=0x1E1E1E, type='rich')
        embed.add_field(name='Title:', value=movie['original_title'], inline=False)
        embed.add_field(name='Overview:', value=movie['overview'], inline=False)
        embed.add_field(name='Average :chart_with_upwards_trend: :', value=movie['vote_average'], inline=False)
        embed.add_field(name='Popularity :family:  :', value=movie['popularity'], inline=True)
        embed.add_field(name='Release :calendar_spiral: :', value=movie['release_date'], inline=True)

        avatar = f'{IMG_URL}{movie["backdrop_path"]}'
        embed.set_thumbnail(url=avatar)

        payloads.append({
            'content': f'Movie ID: {movie["id"]} - Section {current+1}/{last} - Page: {page}/{total_pages}',
            'embed': embed
        })

    for message, payload in zip(responses, payloads):
        await message.edit(content=payload['content'], embed=payload['embed'])


@client.on_click()
async def next_page(i: discord.Interaction, button):
    page = page_key.split('_')[1]
    page = f'page:{int(page)+1}'
    await i.defer()
    for msg in responses:
        await msg.delete()
    await get_trends(ctxn, page)


@client.on_click()
async def previous_page(i: discord.Interaction, button):
    page = page_key.split('_')[1]
    if int(page) < 1:
        page = 1
    page = f'page:{int(page)-1}'
    await i.defer()
    for msg in responses:
        await msg.delete()
    await get_trends(ctxn, page)


@client.command(aliases=['get_movies', 'trends', 'list_movies'])
async def get_trends(ctx, *args):
    """
    List five trending movies information.
    The list are splitted in sections, use the up/down arrow buttons to scroll
    between sections of a current page.
    Use next/previous buttons to switch between pages.

    Params: <name>:<value>
    Valid params and values:
        - page: integers from 1 to max available pages;
        - media_type: [movie, person, tv, all];
        - time_window: [day, week];

    Usage examples:
        /get_trends page:15
        /get_trends time_window:week page:5
    """
    global responses
    global section
    global page_key
    global ctxn
    ctxn = ctx

    if not args:  # default search
        args = ('page:1', 'media_type:movie', 'time_window:day')

    # preprocess query arguments
    media_type = next(iter([(i+':').split(':')[1] for i in args if 'media' in i]), 'movie')
    time_window = next(iter([(i+':').split(':')[1] for i in args if 'time' in i]), 'day')
    page = next(iter([(i+':').split(':')[1] for i in args if 'page' in i]), 1)

    # Validate media type
    if media_type not in ('movie', 'tv', 'person', 'all'):
        return await ctx.send(f'Invalid media type param `{media_type}`')

    # Validate time window
    if time_window not in ('day', 'week'):
        return await ctx.send(f'Invalid time window param `{time_window}`')

    # caches request if not cached, else get cached data instead of request it
    page_key = f'page_{page}'
    if not cache.get(page_key):
        trends = get_trending(media_type, time_window, page)
        cache.set(page_key, str(trends))
    else:
        trends = evl(cache.get(page_key))

    # Paginate response into sections
    sections = list(paginate(trends['results']))
    total_pages = trends['total_pages']
    section = [0, len(sections)]

    # button availability
    # Button is disabled if value is True
    prev_btn = not (trends['page'] >= 2)
    next_btn = not (trends['page'] < total_pages)

    # Button definition
    components=[
        ActionRow(
            Button(
                style=ButtonStyle.gray,
                custom_id='section_up',
                emoji='🔺',
                label='▲'  # U+25B2
            ),
            Button(
                style=ButtonStyle.gray,
                custom_id='section_down',
                emoji='🔻',
                label='▼'  # U+25BC
            ),
        ),
        ActionRow(
            Button(
                style=ButtonStyle.blurple,
                custom_id='previous_page',
                emoji='⬅️',
                label='Previous page',
                disabled=prev_btn
            ),
            Button(
                style=ButtonStyle.blurple,
                custom_id='next_page',
                emoji='➡️',
                label='Next page',
                disabled=next_btn
            ),
        ),
    ]

    # build message structure and send to chat
    responses = []
    current, last = section
    for movie in sections[current]:
        embed = discord.Embed(color=0x1E1E1E, type='rich')
        embed.add_field(name='Title:', value=movie['original_title'], inline=False)
        embed.add_field(name='Overview:', value=movie['overview'], inline=False)
        embed.add_field(name='Average :chart_with_upwards_trend: :', value=movie['vote_average'], inline=False)
        embed.add_field(name='Popularity :family:  :', value=movie['popularity'], inline=True)
        embed.add_field(name='Release :calendar_spiral: :', value=movie['release_date'], inline=True)

        avatar = f'{IMG_URL}{movie["backdrop_path"]}'
        embed.set_thumbnail(url=avatar)

        if movie['id'] != sections[current][-1]['id']:
            response = await ctx.send(
                f'Movie ID: {movie["id"]} - Section {current+1}/{last} - Page: {page}/{total_pages}',
                embed=embed
            )
        else:
            response = await ctx.send(
                f'Movie ID: {movie["id"]} - Section {current+1}/{last} - Page: {page}/{total_pages}',
                embed=embed,
                components=components
            )
        # Store sent messages for later edition if button clicked
        responses.append(response)


@client.command(aliases=['send_file'])
async def upload(ctx):
    files = ctx.message.attachments
    user_id = ctx.message.author.id
    if not files:
        return await ctx.send('You must upload a file.')

    # validate files extension
    valid_extensions = ('image/png', 'video/mp4')
    for file in files:
        if file.content_type not in valid_extensions:
            return await ctx.send(f'Invalid file extension {file.content_type}')

    db = Database(MYSQL_CONFIG['database'])
    for file in files:
        extension = file.content_type.split('/')[1]
        file_request = requests.get(file.url)
        dumped = json.dumps(b64encode(file_request.content).decode('utf-8'))
        item_id = db.insert(user_id, dumped, json.dumps(file.url), json.dumps(extension))
        await ctx.send(f'Inserted file on database with ID: {item_id}')
    db.close()


@client.command(aliases=['get_file'])
async def download(ctx, item_id=None):
    if not item_id:
        return await ctx.send('Must inform item ID.')

    db = Database()
    results = db.select(item_id)

    if not results:
        return await ctx.send(f'No file found for ID: {item_id}')

    record = results[0]
    id, user_id, dump, url, extension, date = record
    file = b64decode(dump)

    embed = discord.Embed(color=0x1E1E1E, type='rich')
    embed.add_field(name='Stored by:', value=user_id, inline=False)
    embed.add_field(name='File URL:', value=f'`{url}`', inline=True)
    embed.add_field(name='Stored at:', value=str(date), inline=True)
    db.close()

    await ctx.send(
        f'Item ID: {id}',
        embed=embed,
        file=discord.File(BytesIO(file), filename=f'file.{extension}')
    )
