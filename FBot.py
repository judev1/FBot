import discord, sys

sys.path.insert(0, "FBot_Libs")
try:
    from Triggers import trigger_response as tr
    from Functions import Functions as fn
    from Database import Database as db
    from Functions import Time as ftime
    from discord.ext import commands
    from BookProgram import book
except:
    input(" > Unable to install some of the dependencies, shutting down ")
    sys.exit()

# 1 for FBot, 2 for Jude, 3 for Chris
token = fn.Get_Token(1)

# Setup
ftime.Set_Start()
sessionstart = ftime.Get_Start()
print(f" > Session started at {sessionstart}")
tr.trigger_load()
db.Setup()
bot = commands.Bot(command_prefix=fn.Get_Prefix, owner_ids=[671791003065384987, 216260005827969024, 634454757645221908])

# When the Bot connects to the server
@bot.event
async def on_connect():
    print(f"\n > Began signing into Discord as {bot.user}")

# When the Server connection is ready
@bot.event
async def on_ready():
    print(f" > Finished signing into Discord as {bot.user}\n")

    db.Check_Guilds(bot.guilds)
    bot.remove_command("help")
    initial_extensions = ["Commands", "DBL", "DMs", "Error_Handler", "Help",
        "Events", "FBotdev", "Infomation", "Join_Leave", "Links", "Modtoggle",
        "Notices", "PatchNotes", "Ping", "Prefix", "Priority", "Quote", "Say",
        "Session", "Status", "Trigger_Responses", "Version", "Snipe", "Bonk",
        "Bigpp"]
    dev = ["FBotdev"]

    for extension in initial_extensions:
        bot.load_extension("FBot_Cogs." + extension)
    print(" > Loaded all cogs\n")
        
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="'FBot help'"))

bot.run(token)
