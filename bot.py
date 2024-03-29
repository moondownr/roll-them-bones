#!/usr/bin/env python3

from operator import truediv
import os
import discord
import asyncio
import random
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# Provide token and guild ID in the .env file
token = os.getenv('DISCORD_TOKEN')
guildid = os.getenv('GUILD_ID')
# Requires FFMpeg to work. Change to False to turn off.
dice_sound_on = True
# Provide the path to the sound of rolling dice (or any other sound file you like). Takes mp3|wav|flac|ogg|most of other formats. Has no effect if "dice_sound_off = False". 
dice_sound_path = os.getenv('DICE_SOUND_PATH') 
# Arrange the dice from highest to lowest
sort_dice = True

#Next two lines are needed if you are using discord.py 2.* or later. Connected to the recent changes in the Discord API and intents. If your bot reaches 100 servers, this will need to be approved by Discord.
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="!",intents=intents)

@bot.event 
async def on_ready():
    guild = discord.Object(id=guildid)
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)

class MyHelpCommand(commands.DefaultHelpCommand):
	def get_ending_note(self):
		return 'Run "!help command" to see more info on a given command'

bot.help_command = MyHelpCommand(show_parameter_descriptions=False,no_category='Commands')

# Checks if a variable can be converted to int
def is_num(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# Checks if an expression can be parsed
def can_split(s, d):
	try:
		a, b = s.split(d)
		return True
	except ValueError:
		return False

# Calculates generic dicerolls, as well as World of Darkness with or without exploding dice
def diceroll(dice, eachroll):
	results = 0
	num_of_dice, dice_type, threshold = 0, 0, 0
	if (dice.find('wodx') != -1): # with exploding 10s
		if can_split(dice, 'wodx') is False:
			results = (f"Wrong expression: can't parse {dice}")
		else:
			num_of_dice, threshold = dice.split('wodx')
			if (is_num(num_of_dice) is False):
				results = (f"Wrong expression: {num_of_dice} is not a number")
			elif (is_num(threshold) is False):
				results = (f"Wrong expression: {threshold} is not a number")
			else:
				while int(num_of_dice)>0:
					roll = random.randint(1, 10)
					eachroll.append(roll)
					if roll == 10:
						results = results+1
						num_of_dice = int(num_of_dice)+1
					elif roll >= int(threshold):
						results = results+1
					elif roll == 1:
						results = results-1
					num_of_dice = int(num_of_dice)-1
				if results < 0:
					results = "Botch!"
	elif (dice.find('wod') != -1): # without exploding 10s
		if can_split(dice, 'wod') is False:
			results = (f"Wrong expression: can't parse {dice}")
		else:
			num_of_dice, threshold = dice.split('wod')
			if (is_num(num_of_dice) is False):
				results = (f"Wrong expression: {num_of_dice} is not a number")
			elif (is_num(threshold) is False):
				results = (f"Wrong expression: {threshold} is not a number")
			else:
				while int(num_of_dice)>0:
					roll = random.randint(1, 10)
					eachroll.append(roll)
					if roll >= int(threshold):
						results = results+1
					elif roll == 1:
						results = results-1
					num_of_dice = int(num_of_dice)-1
				if results < 0:
					results = "Botch!"
	elif (dice.find('d') != -1): # Generic dice rolls
		if can_split(dice, 'd') is False:
			results = (f"Wrong expression: can't parse {dice}")
		else:
			num_of_dice, dice_type = dice.split('d')
			if len(num_of_dice) == 0:
				num_of_dice = 1
			if (is_num(num_of_dice) is False):
				results = (f"Wrong expression: {num_of_dice} is not a number")
			elif (is_num(dice_type) is False):
				results = (f"Wrong expression: {dice_type} is not a number")
			else:
				while int(num_of_dice)>0:
					roll = random.randint(1, int(dice_type))
					results += roll
					eachroll.append(roll)
					num_of_dice = int(num_of_dice)-1
	else: # If given a number instead of a diceroll return that number as a result
		if (is_num(dice) is False):
			results = (f"Wrong expression: {dice} is not a number")
		else:
			roll = int(dice)
			results = roll
			eachroll.append(roll)
	return results

# Calculates Mutants:Year Zero dicerolls
def mutroll(num_of_dice, dicetype):
	results, sixresults, oneresults = 0, 0, 0
	everyroll = []
	if (is_num(num_of_dice) is False):
		results = (f"\nWrong expression: {num_of_dice} is not a number")
	else:
		while int(num_of_dice)>0:
			roll = random.randint(1, 6)
			everyroll.append(roll)
			if roll == 6:
				sixresults = sixresults+1
			elif roll == 1:
				oneresults = oneresults+1
			num_of_dice = int(num_of_dice)-1
		if sort_dice == True:
			everyroll.sort(reverse=True)
		results = (f"\n**{dicetype}** {everyroll}: sixes {sixresults}, ones {oneresults}")
	return results

# Calculates Shadowrun(5) dicerolls
def shadowrun(num_of_dice, xpld):
	results, hits, ones, explodes = 0, 0, 0, 0
	everyroll = []
	if (is_num(num_of_dice) is False):
		results = (f"\nWrong expression: {num_of_dice} is not a number")
	else:
		while int(num_of_dice)>0:
			roll = random.randint(1, 6)
			everyroll.append(roll)
			if roll == 6:
				hits = hits+1
				if xpld == 1:
					explodes = explodes+1
					num_of_dice = int(num_of_dice)+1
			elif roll == 5:
				hits = hits+1
			elif roll == 1:
				ones = ones+1
			num_of_dice = int(num_of_dice)-1
		if sort_dice == True:
			everyroll.sort(reverse=True)
		if ones*2>len(everyroll)-explodes:
			results = (f"**___GLITCH!___**\n**HITS**:{hits}\n**ONES**:{ones}\n{explodes} dice have exploded!\n{everyroll}")
		else:
			results = (f"**HITS**:{hits}\n**ONES**:{ones}\n{explodes} dice exploded!\n{everyroll}")
	return results

# Calculate Fate dicerolls
def fateroll():
	results, rollsum = 0, 0
	everyroll = []
	sides = ["-", "  ", "+"]
	for x in range(4):
		roll = random.choice(sides)
		if roll == "+":
			rollsum = int(rollsum)+1
		elif roll == "-":
			rollsum = int(rollsum)-1
		everyroll.append(roll)
	if rollsum > 0:
		rollsum = (f"+{rollsum}")
	results = (f" **{rollsum}** {everyroll}")
	return results

# Plays a sound effect after each roll
async def dicesound(ctx):
	if dice_sound_on == True:
		guild = ctx.guild
		voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
		audio_source = discord.FFmpegOpusAudio(dice_sound_path)
		while voice_client.is_playing():
			await asyncio.sleep(1)
		voice_client.play(audio_source)
	else:
		return

# Join a voice channel (only needed for sound effects)
@bot.hybrid_command(name='join', aliases=['j'], brief='Join voice channel', help='Joins the issuer\'s voice channel. Only needed to play sound effects.')
async def join(ctx):
	if not ctx.message.author.voice:
		await ctx.send("Join you where, **{}**?".format(ctx.message.author.name))
		return
	else:
		channel = ctx.message.author.voice.channel
		if ctx.message.guild.voice_client:
			if ctx.message.guild.voice_client.channel == channel:
				await ctx.send("I am already here.")
				return
			else:
				await ctx.message.guild.voice_client.disconnect()
		else:
			await channel.connect()
			await ctx.send("I have arrived.")

# Leave the voice channel
@bot.hybrid_command(name='leave', aliases=['l'], brief='Leave voice channel', help='Leave the voice channel.')
async def leave(ctx):
	voice_client = ctx.message.guild.voice_client
	if voice_client:
		await voice_client.disconnect()
		await ctx.send("I am leaving.")
	else:
		await ctx.send("I can't leave where I am not.")

# Mute the sound effect
@bot.hybrid_command(name='silent', brief='Stop making dice sounds', help='Stop playing a sound effect after rolling dice.')
async def silent(ctx):
	global dice_sound_on
	dice_sound_on = False
	await ctx.send("Dice are now silent.")

# Unmute the sound effect
@bot.hybrid_command(name='loud', brief='Start making dice sounds again', help='Try to play a sound effect after each roll.')
async def silent(ctx):
	global dice_sound_on
	dice_sound_on = True
	await ctx.send("Dice make sound now!")

# Change the setting to arrange dice from highest to lowest
@bot.hybrid_command(name='sort', brief='Sort dice from highest down', help='Sort individual dice from the highest value down when displaying roll results.')
async def silent(ctx):
	global sort_dice
	sort_dice = True
	await ctx.send("Dice are now arranged from highest to lowest.")

# Change the setting to stop arranging dice from highest to lowest
@bot.hybrid_command(name='unsort', brief='Stop sorting dice', help='Display individual dice in the order they were rolled')
async def silent(ctx):
	global sort_dice
	sort_dice = False
	await ctx.send("Dice are now unsorted.")

# Command to roll generic or WoD dice
@bot.hybrid_command(name='roll', aliases=['r'], brief='Make a basic/World of Darkness dice roll', help='"!roll 2d20" - roll two D20 dice.\n'\
	'"!r d4+2d3-1" - roll one D4 die, two D3 dice, add the results and substract 1.\n'\
	'"!r d9999" - roll a "D9999" die (get a random number between 1 and 9999).\n'\
	'"!r 5wod7" - roll 5 World of Darkness d10 dice, set threshold to 7.\n'\
	'"!r 6wodx8" - roll 6 World of Darkness d10 dice, set threshold to 8, make 10s explode.')
async def roll(ctx, roll: str):
	eachroll = []
	diceresult = 0
	rolls = roll.split('+')
	for x in rolls:
		if (x.find('-') != -1):
			sub = x.split('-')
			temp1 = diceroll(sub[0], eachroll)
			temp2 = diceroll(sub[1], eachroll)
			if (is_num(temp1) is False):
				diceresult = temp1
			elif (is_num(temp2) is False):
				diceresult = temp2
			else:
				diceresult += temp1-temp2
		else:
			temp1 = diceroll(x, eachroll)
			if (is_num(temp1) is False):
				diceresult = temp1
			else:
				diceresult += temp1
	if sort_dice == True:
		eachroll.sort(reverse=True)
	await ctx.send(f"**{diceresult}** ({ctx.author.mention} rolled {roll} and got:{eachroll})")
	await dicesound (ctx)

# Command to roll Shadowrun dice
@bot.hybrid_command(name='sr', brief='Make a Shadowrun dice roll', help='"!sr 12" - roll 12 Shadowrun D6 dice.')
async def srx(ctx, roll:str):
	result = shadowrun(roll, 0)
	await ctx.send(f"({ctx.author.mention} rolled {roll} dice and got:\n{result})")
	await dicesound (ctx)

# Command to roll Shadowrun dice with exploding 6s
@bot.hybrid_command(name='srx', brief='Make a Shadowrun dice roll and explode the 6s', help='"!srx 12" - roll 12 Shadowrun D6 dice with exploding sixes.')
async def srx(ctx, roll: str):
	result = shadowrun(roll, 1)
	await ctx.send(f"({ctx.author.mention} rolled {roll} dice and got:\n{result})")
	await dicesound (ctx)

# Command to roll Mutant: Year Zero dice
@bot.hybrid_command(name='mut', brief='Make a Mutants:Year Zero dice roll', help='"!mut 5b+4g+1s+3n" - roll 5 Basic dice, 4 Gear dice, 1 Skill die and 3 Negative dice.')
async def mut(ctx, roll: str):
	result = ""
	rolls = roll.split('+')
	for x in rolls:
		if (x.find('b') != -1):
			sub = x.split('b')
			result += mutroll(sub[0],"BASIC")
		elif (x.find('g') != -1):
			sub = x.split('g')
			result += mutroll(sub[0],"GEAR")
		elif (x.find('s') != -1):
			sub = x.split('s')
			result += mutroll(sub[0],"SKILL")
		elif (x.find('n') != -1):
			sub = x.split('n')
			result += mutroll(sub[0],"NEGATIVE")
	await ctx.send(f"{ctx.author.mention} rolled:\n{result}")
	await dicesound (ctx)

# Command to roll Fate dice
@bot.hybrid_command(name='fate', aliases=['f'], brief='Make a Fate dice roll', help='Roll 4 Fate/Fudge dice.')
async def fate(ctx):
	await ctx.send(f"{ctx.author.mention} rolled{fateroll()}")
	await dicesound (ctx)

# Command to roll Call of Cthulhu dice with advantage (lesser of two D00 and one D10)
@bot.hybrid_command(name='adv', brief='Make a Call of Cthulhu roll with advantage', help='Rolls 1D10 and 2D00s. Combines a D10 with each of the D00s'\
	' into 2D100. Keeps a lower result.')
async def adv(ctx):
	eachroll = []
	a, b, c, rollresult = 0, 0, 0, 0
	a = (diceroll('d10',eachroll)-1)*10
	b = (diceroll('d10',eachroll)-1)*10
	c = diceroll('d10',eachroll)-1
	if a <= b:
		rollresult = a+c
	else:
		rollresult = b+c
	await ctx.send(f"{ctx.author.mention} rolled **{a}**, **{b}**, and **{c}**. Their result is **{rollresult}**!")
	await dicesound (ctx)

# Command to roll Call of Cthulhu dice with disadvantage (higher of two D00 and one D10)
@bot.hybrid_command(name='dis', brief='Make a Call of Cthulhu roll with disadvantage', help='Rolls 1D10 and 2D00s. Combines a D10 with each of the D00s'\
	' into 2D100. Keeps a higher result.')
async def dis(ctx):
	eachroll = []
	a, b, c, rollresult = 0, 0, 0, 0
	a = (diceroll('d10',eachroll)-1)*10
	b = (diceroll('d10',eachroll)-1)*10
	c = diceroll('d10',eachroll)-1
	if a <= b:
		rollresult = b+c
	else:
		rollresult = a+c
	await ctx.send(f"{ctx.author.mention} rolled **{a}**, **{b}**, and **{c}**. Their result is **{rollresult}**!")
	await dicesound (ctx)

# Command to delete a given number of messages from the chat history
@bot.hybrid_command(name='delete', aliases=['del'], brief='Delete a given number of messages', help='Delete a given number of messages from history,'\
	' starting from the latest one before this command. The "!delete" command itself will also be deleted from history, but is not counted. Example:\n'\
	'"!del 10" - deletes 10 previous messages from the text channel, as well as the "!del 10" message.')
async def delete(ctx, number:int):
	if (is_num(number) is False):
		await ctx.send(f"Wrong expression: {number} is not a number")
	else:
		messages = []
		channel = ctx.message.channel
		async for message in channel.history(limit=number+1):
			messages.append(message)
		await channel.delete_messages(messages)
		await ctx.send(f"Deleted {number} message(s). This message will self-destruct in 5s",delete_after=5)
		
bot.run(token)
