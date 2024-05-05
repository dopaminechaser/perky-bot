import os
import discord
from discord.ext import commands
import datetime
import time

intents = discord.Intents.all()
intents.messages = True  # Enable the message content intent

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def counts(ctx, start_date_str: str, end_date_str: str):
    # Validate date format
    startTime = time.perf_counter()
    try:
        start_date = datetime.datetime.strptime(start_date_str, '%m/%d/%Y')
        end_date = datetime.datetime.strptime(end_date_str, '%m/%d/%Y') + datetime.timedelta(days=1)
    except ValueError:
        await ctx.send("I can't believe this... an incorrectly formatted date? This simply won't do. How can one expect to maintain any sort of order with such carelessness? Please ensure that you adhere to the proper date of MM/DD/YYYY. We must all do our part to uphold the standards of proper documentation!")
        return

    user_counts = {}

    # Iterate through messages in the specified channel and time range
    channel = discord.utils.get(ctx.guild.channels, name="join-notifications")  # Replace "general" with your specific channel name
    total_messages = 0
    
    startingMessage = "grata nuntiis computare. This spell is slow but its working...."
    await ctx.send(startingMessage)
    checkmark_emoji = '✅'
    async for message in channel.history(limit=None, after=start_date, before=end_date):
        total_messages += 1
        for reaction in message.reactions:
            if str(reaction.emoji) == checkmark_emoji:
                async for user in reaction.users():
                    user_display_name = user.display_name
                    user_counts[user_display_name] = user_counts.get(user_display_name, 0) + 1
    if not user_counts:
        counts_message = f"No Welcome Messages Sent from {start_date_str} to {end_date_str}"
 
    else:
        # Prepare the counts message
        counts_message = "Welcome Counts:\n"
        for user_id, count in user_counts.items():

            counts_message += f"{user_id}: {count} \n"

    # Send the counts message
    endTime = time.perf_counter()
    await ctx.send(counts_message)
    await ctx.send("I looked at {} messages".format(total_messages) )


# Retrieve bot token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")




# Run the bot with the retrieved token
bot.run(BOT_TOKEN)


