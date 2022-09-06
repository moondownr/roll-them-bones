# roll-them-bones
A Discord bot for rolling dice, written in Python. Has optional sound effect support. Supports specific rules of several RPG systems (currently World of Darkness, Call of Cthulhu, Shadowrun and Mutants: Year Zero).

## Running requirements

- [discord.py](https://github.com/Rapptz/discord.py)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

  Optional:
- [FFmpeg](https://github.com/FFmpeg/FFmpeg) (only for sound effects).

You need to provide an .env file with following variables:

    DISCORD_TOKEN="YOUR_DISCORD_BOT_TOKEN"
    DICE_SOUND_PATH="PATH_TO_SOUND_FILE"

## Commands

### Dicerolls

**!roll**/**!r** - make a basic/World of Darkness dice roll. Examples:
- "!roll 2d20" - roll two D20 dice.
- "!r d4+2d3-1 - roll one D4 die, two D3 dice, add the results and substract 1.
- "!r d9999" - roll a "D9999" die (get a random number between 1 and 9999).
- "!r 5wod7" - roll 5 World of Darkness d10 dice, set threshold to 7.
- "!r 6wodx8" - roll 6 World of Darkness d10 dice, set threshold to 8, make 10s explode.

**!sr** - make a Shadowrun dice roll. Example:
- "!sr 12" - roll 12 Shadowrun D6 dice.

**!srx** - same, but with exploding 6s.

**!mut** - make a Mutants:Year Zero dice roll. Example:
- "!mut 5b+4g+1s+3n" - roll 5 Basic dice, 4 Gear dice, 1 Skill die and 3 Negative dice. 

**!adv** - roll a D100 with advantage according to Call of Cthulhu 7th ed. rules (3d10).

**!dis** - roll a D100 with disadvantage according to Call of Cthulhu 7th ed. rules (3d10).

### Deleting messages
**!delete**/**!del** - delete a given number of messages from the channel chat history, starting from the latest one before this command. The **!delete** command itself will also be deleted from history, but is not counted. Example:
- "!del 10" - deletes 10 previous messages from the text channel, as well as the "!del 10" message. 

### Configuration

**!unsort** - display individual dice in multiple-die rolls in the order they were rolled, as opposed to sorting them from highest to lowest.

**!sort** - sort individual dice from the highest value down when displaying roll results (default behaviour).

**!silent** - stop playing a sound effect after rolling dice.

**!loud** - try to play a sound effect after each roll (default).

### Voice channels

**!join**/**!j**: join the issuer of the command in a voice channel.

**!leave**/**!l**: leave the voice channel.


### Acknowledgements

Partially inspired by https://github.com/Chaithi/Discord-Dice-Roller-Bot
