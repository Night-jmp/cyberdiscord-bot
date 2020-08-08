import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import Member
from discord.utils import get
import hashlib
import base64

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Welcome, {member.name} to Cybersecurity Central. In order to gain access to your class\'s channel you must register.\n NOTE: You must issue the register command in the roll call channel.\nIn order to register you must do the following: \n```!register <firstname> <lastname> <CSE---->```\nExample: ```!register Joshua Connolly CSE4820```\n\nIf you have any problems registering, please reach out to a student moderator')

    role = get(member.guild.roles, name="Unregistered")
    await member.add_roles(role)

@bot.command(name="register", help="Register with the server")
@commands.has_role('Unregistered')
#async def register_name(context, member:Member, first=None, last=None, course=None):
async def register_name(context, first=None, last=None, course=None):

    courses = ['CSE3801','CSE3810','CSE4820']

    member = context.message.author

    if member and first and last and course:
        name = first + " " + last

        if course not in courses:
            await context.send(f"{course} is not an offered course in the cyber track. Please reregister.")
            return

        await member.edit(nick=name)

        role = get(member.guild.roles, name=course)
        await member.add_roles(role)
        unregistered = get(member.guild.roles, name="Unregistered")
        await member.remove_roles(unregistered)

        await context.send(f"{name} is registered for {role}")
    else:
        await context.send("Please register with the following command:\n!register <first name> <last name> <CSE---->\nExample: !register Joshua Connolly CSE4820\n\nIf you are still having problems registering, please reach out to a student moderator")

@bot.command(name="reset", help="Reset all users to Unregistered")
@commands.has_role('Student Moderator')
async def reset(context):

    courses = ['CSE3801','CSE3810','CSE4820']

    members = context.message.author.guild.members

    for member in members:
        for course in courses:
            unregister = get(context.message.author.guild.roles, name=course)
            try:
                print(f"Attempting to remove {unregister} from {member}")
                await member.remove_roles(unregister)
            except:
                print("User doesn't have roll!")

        role = get(context.message.author.guild.roles, name="Unregistered")
        
        print(f"Attempting to add {role} to {member}")
        await member.add_roles(role)

        await member.create_dm()
        await member.dm_channel.send(f'Welcome, {member.name} to Cybersecurity Central. In order to gain access to your class\'s channel you must register with the command below in the role call channel. \nIn order to register you must do the following: \n\n!register <firstname> <lastname> <CSE---->\nExample: !register Joshua Connolly CSE4820\n\nIf you have any problems registering, please reach out to a student moderator')

            
#@bot.command(name="md5sum", help="Provide md5 hash of the value provided. i.e. !md5sum <value>")
#async def md5sum(context, value=None):
#    if value:
#        result = hashlib.md5(value.encode('utf-8'))
#        await context.send(f"Md5 hash of {value} is {result.hexdigest()}")
#    else:
#        await context.send("Please provide a value to be hashed. i.e. !md5sum <value>")

#@bot.command(name="b64encode", help="Base64 encode the value provided. i.e. !b64encode <value>")
#async def b64encode(context, value=None):
#    if value:
#        result = base64.b64encode(value.encode('utf-8'))
#        await context.send(f'Base64 encoded result of {value} is {str(result, "utf-8")}')
#    else:
#        await context.send("Please provide a value to be encoded. i.e. !b64encode <value>")

#@bot.command(name="b64decode", help="Base64 decode the value provided. i.e. !b64decode <value>")
#async def b64decode(context, value=None):
#    if value:
#        result = base64.b64decode(value)
#        await context.send(f'Base64 decoded result of {value} is {str(result, "utf-8")}')
#    else:
#        await context.send("Please provide a value to be decoded. i.e. !b64decode <value>")

bot.run(TOKEN)

