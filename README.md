# roll-them-bones
A Discord bot for rolling dice, written in Python. Has optional sound effect support. Supports specific rules of several RPG systems (currently World of Darkness, Call of Cthulhu, Fate, Shadowrun and Mutants: Year Zero).

## Test the bot

You can try out roll-them-bones by adding it to your Discord server via this url:

https://discord.com/api/oauth2/authorize?client_id=971918847957434428&permissions=3353600&scope=bot

**PLEASE NOTE**

This instance is provided for testing purposes. 100% uptime is not guaranteed. Performance might suffer under load.

The way it currently is, this instance will stop working after reaching 100 servers. After that it will either need to be reviewed and whitelisted by Discord or rewritten to not use Message Content Intent. If and when it gets there, I'll figure something out.

If you tried it and liked it, please consider hosting your own instance (see below).

## Creating your own Discord bot

You can refer to any of the manuals online. [Here](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/) is a good one.

To make full use of this bot's functions, you will need to give it following permissions:

**Needed to roll and display dice (core)**
- Read messages/View channels
- Send messages
- Mention everyone

**Needed for !delete command**
- Manage messages
- Read message history

**Need for dice sounds/effects**
- Connect
- Speak

## Running requirements
- Python 3.8+
- [discord.py](https://github.com/Rapptz/discord.py)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

  Optional:
  Optional (only for sound):
- [PyNaCL](https://pypi.org/project/PyNaCl/)
- [FFmpeg](https://github.com/FFmpeg/FFmpeg)
 
You need to provide an .env file with following variables:

    DISCORD_TOKEN="YOUR_DISCORD_BOT_TOKEN"
    DICE_SOUND_PATH="PATH_TO_SOUND_FILE"
    GUILD_ID="YOUR SERVER ID"

## Commands

Since version 0.4 this bot utilizes Discord application commands (the ones starting with "/"), while retaining the old text command functionality.


### Dicerolls

**/roll**/**!roll**/**!r** - make a basic/World of Darkness dice roll. Examples:
- "/roll 2d20" - roll two D20 dice.
- "!roll d4+2d3-1" - roll one D4 die, two D3 dice, add the results and substract 1.
- "!r d9999" - roll a "D9999" die (get a random number between 1 and 9999).
- "!r 5wod7" - roll 5 World of Darkness d10 dice, set threshold to 7.
- "!r 6wodx8" - roll 6 World of Darkness d10 dice, set threshold to 8, make 10s explode.

**/sr**/**!sr** - make a Shadowrun dice roll. Example:
- "/sr 12" - roll 12 Shadowrun D6 dice.

**/srx**/**!srx** - same, but with exploding 6s.

**/mut**/**!mut** - make a Mutants:Year Zero dice roll. Example:
- "/mut 5b+4g+1s+3n" - roll 5 Basic dice, 4 Gear dice, 1 Skill die and 3 Negative dice. 

**/adv**/**!adv** - roll a D100 with advantage according to Call of Cthulhu 7th ed. rules (3d10).

**/dis**/**!dis** - roll a D100 with disadvantage according to Call of Cthulhu 7th ed. rules (3d10).

**/fate**/**!fate**/**!f** - roll 4 Fate/Fudge dice.

### Deleting messages
**/delete**/**!delete**/**!del** - delete a given number of messages from the channel's chat history, starting from the latest one before this command. The **!delete** command itself will also be deleted from history, but is not counted. Example:
- "!del 10" - deletes 10 previous messages from the text channel, as well as the "!del 10" message. 

### Configuration

**/unsort**/**!unsort** - display individual dice in multiple-die rolls in the order they were rolled, as opposed to sorting them from highest to lowest.

**/sort**/**!sort** - sort individual dice from the highest value down when displaying roll results (default behaviour).

**/silent**/**!silent** - stop playing a sound effect after rolling dice.

**/loud**/**!loud** - try to play a sound effect after each roll (default).

### Voice channels

**/join**/**!join**/**!j**: join the issuer of the command in a voice channel.

**/leave**/**!leave**/**!l**: leave the voice channel.


### Acknowledgements

Partially inspired by https://github.com/Chaithi/Discord-Dice-Roller-Bot
