import discord, sqlite3, asyncio, random
from discord.ext import commands, tasks

# Initialize bot
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix='rona ', intents=intents)

# Open database
conn = sqlite3.connect("ronatutoring.sqlite")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Constants
tellTutorToReact = '''
            
React to this message with an emoji of your choice if you're interested in taking this request. Our discord bot will reach out to those interested with more details.'''

# Send tutor requests to tutor-request channel every 2 hours
async def send_requests():
    await client.wait_until_ready()
    while True:
        # Delete all requests
        while True:
            deleted = await client.get_guild(671509704157167646).get_channel(787592274119884843).purge(limit=100)
            if len(deleted) == 0:
                break

        # From pending_requests database, get discordMessage
        cur.execute("SELECT * FROM pending_requests")
        rows = cur.fetchall()
        discordMessages = [row['discordMessage'] for row in rows]
        for message in discordMessages:
            # Send pending request message
            await client.get_guild(671509704157167646).get_channel(787592274119884843).send(f"{client.get_guild(671509704157167646).default_role} {message}")

        # Wait 2 hours for reactions from tutors
        #                   vv
        await asyncio.sleep(120) # HEY SOHAM SOHAM SOHAM YOU GOTTA CHANGE THIS TO 2 ACTUAL HOURS AFTER YOU'RE DONE OKAY???
        #                   ^^

        cur.execute("SELECT * FROM confirmation_message_counters")
        counters = cur.fetchall()
        tutorIds = [counter['tutorId'] for counter in counters]
        # Go through all pending requests from this 2 hour period
        async for message in client.get_guild(671509704157167646).get_channel(787592274119884843).history():
            if len(message.reactions) >= 1:
                # Send confirmation messages to all people who reacted
                # Some people might have reacted twice or more with different emojis; we want to send a confirmation message to them only ONCE
                ids = []
                for reaction in message.reactions:
                    async for user in reaction.users():
                        if user.id not in ids:
                            # If this is the first time a tutor reacted to a request, initialize the confirmationMessageCount to 1 in the confirmation_message_counters table
                            if user.id not in tutorIds:
                                newConfirmationMessageCount = 1
                                cur.execute('INSERT INTO confirmation_message_counters (tutorId, confirmationMessageCount) VALUES (?, ?)', (user.id, newConfirmationMessageCount))
                            # If this is not the first time a tutor reacted to a request, increment the confirmationMessageCount by 1 in the confirmation_message_counters table
                            else:
                                newConfirmationMessageCount = counter = list(filter(lambda counter: counter['tutorId']==user.id, counters))[0]['confirmationMessageCount'] + 1
                                cur.execute('UPDATE confirmation_message_counters SET confirmationMessageCount = ? WHERE tutorId = ?;', (newConfirmationMessageCount, user.id))
                            conn.commit()
                            
                            # Send confirmation message
                            # message.content[:(-1)*len(tellTutorToReact)] ==> the tutor-requests message, without the "React to this message..." part
                            await user.send(f"{message.content[:(-1)*len(tellTutorToReact)]}\n\nAre you sure you want this student? Text either \"yes {newConfirmationMessageCount}\" or \"no {newConfirmationMessageCount}\" (all undercase, without the quotes)")
                        ids.append(user.id)
                ids.clear()


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

#TESTING
@client.command()
async def foo(ctx, member: discord.Member):
    await ctx.send(f"{member.name}#{member.id}")


# Run bot
client.loop.create_task(send_requests())
client.run('Nzg1OTc2MzE5NDg5OTk4ODk4.X8_rfQ.cQe6lKkS2mXNzgnpFgO7bKubLBM')