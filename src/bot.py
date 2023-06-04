import platform
import asyncio
from typing import List
import discord
from discord.ext import commands
import botdb
from botutils import *

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

bot_token = 0
path_token = 0

isTest = True

def Setup():
    global bot_token
    global path_token

    file = "discord-token.txt"
    if isTest:
        file="discord-token-test.txt"

    if(platform.system() == "Linux"):
        path_token = f"/var/www/{file}"
    elif(platform.system() =="Windows"):
        path_token = f"./{file}"
     
    with open(path_token) as f:
        bot_token = f.readlines()[0]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name="about")
async def ctx_about(ctx):
    embed = discord.Embed(title="About ED-FCO", description="I am ED-FCO, a bot written to help fleet carrier owners communicate activities and movements of their carrier to servers that are subscribed to said carriers.\nUse `!man` to get a list of commands you can use with me", color=0x9b59b6)
    embed.set_footer(text="Made with <3 by Sebastian.#0083", icon_url=None)
    embed.set_image(url="https://i.imgur.com/uGxxo6b.png")
    message = await ctx.send(embed=embed)
    await asyncio.sleep(60)
    await message.delete()

    await ctx.message.delete()

@bot.command(name="man")
async def ctx_man(ctx):
    newEmbed = discord.Embed(title="Manual for ED-FCO", color=0x9b59b6)
    newEmbed.add_field(name = "`!register CARRIER-ID \"CARRIER-NAME\" \"CMDR-NAME\"`", value="Example: `!register JZH-6XY \"The Bad Dragon\" \"Ultraviol3nt\"`\nUse this to register a new carrier using your Discord ID and CMDR name.\nYou must DM me in order to perform this action.", inline=False)
    newEmbed.add_field(name = "`!unregister CARRIER-ID`", value="Example: `!unregister JZH-6XY`\nUse this to unregister a carrier that is associated with your Discord ID.\nYou must DM me in order to perform this action.", inline=False)
    newEmbed.add_field(name = "`!jump`", value="Broadcast to all subscribers that your carrier will be jumping soon.\nYou must DM me in order to perform this action.", inline=False)
    newEmbed.add_field(name = "`!subscribe CARRIER-ID`", value="Example: `!subscribe JZH-6XY`\nUse this to subscribe a channel to carrier updates.\nThis cannot be performed via DMs.", inline=False)
    newEmbed.add_field(name = "`!sublist`", value="Get a list of all carriers this channel is subscribed to\nThis cannot be performed via DMs.", inline=False)
    newEmbed.add_field(name = "`!unsubscribe CARRIER-ID`", value="Example: `!unsubscribe JZH-6XY`\nUnsubscribe this channel from updates regarding a specific carrier\nThis cannot be performed via DMs.", inline=False)
    newEmbed.add_field(name = "`!unsubscribe all`", value="Unsubscribe this channel from *all* carrier updates.\nThis cannot be performed via DMs.", inline=False)
    newEmbed.add_field(name = "`!github`", value="Get a GitHub link to ED-FCO", inline=False)
    newEmbed.add_field(name = "`!clear`", value="Clears all messages from ED-FCO in the current channel", inline=False)
    await ctx.send(embed=newEmbed)
    await ctx.message.delete()

@bot.command(name="register")
async def ctx_register(ctx, *args):
    arglist = list(args)
    if ctx.guild is None:
        if len(arglist) == 3:
            if CheckCarrierIDPattern(arglist[0]):
                id= arglist[0].upper()
                name=arglist[1]
                owner=ctx.author.id
                cmdr=arglist[2]
                response = botdb.RegisterCarrier(id, name, owner, cmdr)
                match response:
                    case 200:
                        await ctx.send(f"Success! Carrier {id} \"{name}\" now registered to {ctx.author.mention}")
                    case 401:
                        await ctx.send(f"Error: Carrier ID already registered")
                    case 402:
                        await ctx.send(f"Error: Carrier or owner already registered")
            else:
                await ctx.send(f"Invalid Carrier ID")
        else:
            await ctx.send(f"Incorrect Syntax: please use `{bot.command_prefix}register ID \"NAME\" \"CMDR NAME\"`, for example, `{bot.command_prefix}register JZH-6XY \"The Bad Dragon\" \"ultraviol3nt\"`")
    else:
        message = await ctx.send(f"{ctx.author.mention}, the command `{bot.command_prefix}register` cannot be used here. DM me with this command to get started.")
        await asyncio.sleep(30)
        await message.delete()

    await ctx.message.delete()

@bot.command(name="unregister")
async def ctx_unregister(ctx, *args):
    arglist = list(args)
    if ctx.guild is None:
        if len(arglist) == 2:
            if CheckCarrierIDPattern(arglist[0]):
                id= arglist[0].upper()
                owner=ctx.author.id
                response = botdb.UnregisterCarrier(id, owner)
                match response:
                    case 200:
                        await ctx.send(f"Success! Carrier {id} is no longer registered to {ctx.author.mention}")
                    case 401:
                        await ctx.send(f"Error: Carrier ID not registered or not owned by {ctx.author.mention}")
            else:
                await ctx.send(f"Incorrect Syntax: please use `{bot.command_prefix}unregister ID, for example, `{bot.command_prefix}register JZH-6XY`")
                await ctx.send("Bad Regex Match")
        else:
            await ctx.send(f"Incorrect Syntax: please use `{bot.command_prefix}unregister ID, for example, `{bot.command_prefix}register JZH-6XY`")
            await ctx.send("Invalid Arguments")
    else:
        message = await ctx.send(f"{ctx.author.mention}, the command `{bot.command_prefix}unregister` cannot be used here. DM me with this command to perform this action.")
        await asyncio.sleep(5)
        await message.delete()
    
    await ctx.message.delete()

@bot.command(name="subscribe")
async def ctx_subscribe(ctx, *args):
    arglist = list(args)
    if ctx.guild:
        if len(arglist) > 0:
            if CheckCarrierIDPattern(arglist[0]):
                response = botdb.Subscribe(arglist[0].upper(), ctx.channel.id)
                match response:
                    case 200:
                        await ctx.send(f"{ctx.author.mention} Success! This channel will now receive updates regarding the status of carrier {arglist[0]}")
                    case 401:
                        await ctx.send(f"{ctx.author.mention} This channel is already subscribed to carrier {arglist[0]}")
            else:
                await ctx.send(f"{ctx.author.mention} Carrier ID is not valid")
        else:
            await ctx.send(f"{ctx.author.mention} Incorrect syntax. Please use syntax `fco.subscribe SHIP-ID`, for example `fco.subscribe JZH-6XY`")
    else:
        await ctx.send("This command cannot be used in DMs. Please use this command in a server channel in which you would like to receive updates.")

    await ctx.message.delete()

@bot.command(name="sublist")
async def ctx_sublist(ctx, *args):
    channel = ctx.channel.id
    subs = botdb.GetSubscriptions(channel)
    newEmbed = discord.Embed(title="Subscriptions for this Channel:")
    content = ""
    for s in subs:
        content = content + f"{s.id} - {s.name}\n"
    newEmbed.description = content
    await ctx.send(embed=newEmbed)

    await ctx.message.delete()

@bot.command(name="unsubscribe")
async def ctx_unsubscribe(ctx, *args):
    arglist = list(args)
    if len(arglist) > 0:
        if CheckCarrierIDPattern(arglist[0]):
            response = botdb.Unsubscribe(arglist[0].upper(), ctx.channel.id)
            match response:
                case 200:
                    await ctx.send(f"{ctx.author.mention} Success! This channel will no longer receive updates for carrier {arglist[0]}")
        elif arglist[0].lower() == "all":
            await ctx.message.delete()
            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel
            
            channel = ctx.channel.id
            
            confirm_req = await ctx.send("Type 'confirm' to confirm unsubscribing this channel from all carrier updates")
            confirm_resp = await bot.wait_for('message', timeout=30.0, check=check)
            if confirm_resp.content.lower() == "confirm":
                await confirm_req.delete()
                await confirm_resp.delete()
                response = botdb.UnsubscribeAll(channel)
                match response:
                    case 200:
                        message = await ctx.send(f"{ctx.author.mention} Success! This channel has been unsubscribed from all carrier updates.")
                        await asyncio.sleep(10)
                        await message.delete()
                        return
                    
                
        else:
            await ctx.send(f"{ctx.author.mention} Carrier ID is not valid")
    else:
        await ctx.send(f"{ctx.author.mention} Incorrect syntax. Please use syntax `fco.unsubscribe SHIP-ID`, for example `fco.unsubscribe JZH-6XY`")
    
    await ctx.message.delete()

@bot.command(name="jump")
async def ctx_jump(ctx, *args):
    def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

    arglist = list(args)
    if ctx.guild is None:
        await ctx.send("What system is your carrier jumping to?")
        try:
            destination_resp = await bot.wait_for('message', timeout=60.0, check=check)
            await ctx.send(f"And what will be the objective once you arrive?")
            objective_resp = await bot.wait_for('message', timeout=60.0, check=check)
            await ctx.send(f"Copy that, CMDR! I will notify all subscribed parties that your carrier is preparing to jump.\nUse 'cancel' to cancel the jump. Otherwise, I will assume the jump is complete in 20 minutes!")
            info = botdb.GetCarrier(ctx.author.id)
            posts = list()
            for channel_id in info.subs:
                channel = bot.get_channel(channel_id)
                newEmbed = discord.Embed(title=(f"ALERT: {info.id} \"{info.name}\" has scheduled a hyperspace jump"), description="Please conclude any remaining business in the system prior to departure.", color=0x9b59b6)
                newEmbed.add_field(name="Destination", value=destination_resp.content, inline=True)
                newEmbed.add_field(name="Objective", value=objective_resp.content, inline=True)
                newEmbed.set_footer(text=f"This carrier is operated by CMDR {info.cmdr}")
                newPost = await channel.send(embed=newEmbed)
                posts.append(newPost)

            cancel_resp = await bot.wait_for('message', check=check, timeout=1200.0)
            if cancel_resp.content.lower() == "cancel":
                await ctx.send("Jump has been canceled")
                for p in posts:
                    newEmbed = discord.Embed(title=(f"ALERT: {info.id} \"{info.name}\" has canceled a hyperspace jump"), color=0x9b59b6)
                    newEmbed.set_footer(text=f"This carrier is operated by CMDR {info.cmdr}")
                    newPost = await p.channel.send(embed=newEmbed)
                    await p.delete()
                return

            await asyncio.sleep(1200.0)
            for p in posts:
                newEmbed = discord.Embed(title=(f"ALERT: {info.id} \"{info.name}\" has completed a hyperspace jump"), color=0x9b59b6)
                newEmbed.add_field(name="Location", value=destination_resp.content, inline=True)
                newEmbed.add_field(name="Objective", value=objective_resp.content, inline=True)
                await channel.send(embed=newEmbed)
                await p.delete()

        except asyncio.TimeoutError:
            await ctx.send("Timed out. Please try again.")

    else:
        message = await ctx.send(f"{ctx.author.mention}, the command `{bot.command_prefix}register` cannot be used here. DM me to perform this action.")
        await asyncio.sleep(5)
        await message.delete()
    
    await ctx.message.delete()

@bot.command(name="github")
async def ctx_github(ctx):
    newEmbed = discord.Embed(title="Fork me on GitHub!", description="Made with <3 by Sebastian.#0083", url="https://github.com/sebbett/ED-FCO", color=0x9b59b6)
    newEmbed.set_thumbnail(url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
    await ctx.send(embed=newEmbed)
    await ctx.message.delete()

@bot.command(name="clear")
async def ctx_clear(ctx):
    channel = ctx.channel
    messages = []
    async for m in channel.history(limit=None):
        if m.author.id == bot.user.id:
            messages.append(m)

    await channel.delete_messages(messages)
    await ctx.message.delete()

Setup()
bot.run(bot_token)