import discord
from discord.ext import commands, tasks
from itertools import cycle

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionary to store the number of cookies for each user
cookies_count = {8}

# Channel ID where the bot will steal cookies
target_channel_id = 1234567890  # Replace with your desired channel ID

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')
    # Start the task to periodically check for active users in the target channel
    check_activity.start()

@tasks.loop(minutes=1)
async def check_activity():
    target_channel = bot.get_channel(target_channel_id)
    if target_channel:
        # Iterate through all members in the target channel
        for member in target_channel.members:
            user_id = member.id
            # Initialize user's cookie count if not present
            if user_id not in cookies_count:
                cookies_count[user_id] = 8

            # Steal a cookie if the user has more than 3 cookies
            if cookies_count[user_id] > 3:
                cookies_count[user_id] -= 1
                print(f'Stole a cookie from {member.display_name}!')

@bot.command(name='give_cookie', help='Give a cookie to a user')
async def give_cookie(ctx, user: discord.Member):
    # Check if the user is the bot itself
    if user == bot.user:
        await ctx.send("I can't eat cookies!")
        return

    # Initialize user's cookie count if not present
    if user.id not in cookies_count:
        cookies_count[user.id] = 0

    # Increment the user's cookie count
    cookies_count[user.id] += 1

    await ctx.send(f'{ctx.author.mention} gave a cookie to {user.mention}! 🍪')

@bot.command(name='check_cookies', help='Check your current number of cookies')
async def check_cookies(ctx):
    user_id = ctx.author.id

    # Check if the user has cookies in the dictionary
    if user_id in cookies_count:
        cookies = cookies_count[user_id]
        await ctx.send(f'{ctx.author.mention}, you have {cookies} cookies! 🍪')
    else:
        await ctx.send(f'{ctx.author.mention}, you have no cookies. 😢')

# Run the bot with your token
bot.run('YOUR_BOT_TOKEN')
