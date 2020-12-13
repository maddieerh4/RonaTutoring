import discord, sqlite3, asyncio
from discord.ext import commands, tasks

# Initialize bot
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix='rona ', intents=intents)

# Open database
conn = sqlite3.connect("ronatutoring.sqlite")
cur = conn.cursor()


# Send tutor requests to tutor-request channel every 2 hours
async def send_requests():
    await client.wait_until_ready()
    while True:
        # Delete all requests
        while True:
            deleted = await client.get_guild(671509704157167646).get_channel(787592274119884843).purge(limit=100)
            if len(deleted) == 0:
                break

        # Send pending requests
        cur.execute("SELECT * FROM pending_requests")
        rows = cur.fetchall()
        for row in rows:
            location = row[4]
            subjects = f"{'Math, ' if row[11] else ''}{'Science, ' if row[12] else ''}{'English, ' if row[13] else ''}{'History, ' if row[14] else ''}{'Computer Science, ' if row[15] else ''}{row[16] if row[16] else ''}".strip()
            if subjects[-1] == ',': subjects = subjects[:-1]
            age = row[5]
            grade = row[6]
            availability = row[7]
            if row[18]:
                additional = f'''
-----------------
Additional Information: {row[18]}'''
            else:
                additional = ''
            msg = f'''{client.get_guild(671509704157167646).default_role} **Student from {location} needs help with {subjects}**
-----------------
Grade: {grade}, Age: {age}
-----------------
Availability: {availability} {additional}
            
React to this message with an emoji of your choice if you're interested in taking this request. Our operations team will reach out to those interested with more details.'''
            await client.get_guild(671509704157167646).get_channel(787592274119884843).send(msg)
        await asyncio.sleep(3600*2)
    

# Before doing anything *important* wait for bot to be ready
@client.event
async def on_ready():
    print("Bot is ready.")


# Welcome new users
@client.event
async def on_member_join(member):
    print(f'{member} has joined this server.')
    for channel in member.guild.channels:
        if str(channel) == "welcome":
            await channel.send(f"Hi {member.mention}! Welcome!")

# Track when users leave server
@client.event
async def on_member_remove(member):
    print(f'{member} has left this server.')


# Get ping
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


# Run bot
client.loop.create_task(send_requests())
client.run('Nzg1OTc2MzE5NDg5OTk4ODk4.X8_rfQ.Ac8uGR71gbQae4Z2M0e_wt0YSfo')