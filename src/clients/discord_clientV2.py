from asyncio import threads
from re import M
import requests
import discord
import os
import json
import sys

class DiscordClientV2(discord.Client):
    def __init__(self, threads, *args, **kwargs):
        super().__init__( intents= discord.Intents.default(), *args, **kwargs)        
        self.thread_channels = dict()
        self.thread_to_remove = dict()

        for thread in threads:
            self.thread_channels[thread["id"]] = {
                "embed": thread["embed"],
                "template" : thread["template"],
                "footer" : thread["footer"],
                "emojis" : thread["emojis"],
                "role_to_give": thread["role_to_give"],
                "validator": thread["validator"]
            }
        
        print(self.thread_channels)

    def _format_embed(self, message, title, user = None, footer = None):
        embed = discord.Embed(title=title, description=message, color=0xFFFFFF)
        if user:
            embed.add_field(name="Author", value="{}".format(user.mention), inline=True)
            embed.set_author(name=user.name, icon_url=user.avatar.url)
        if footer:
            embed.set_footer(text=footer)
        return embed

    def _validate_format(self, validator, content):
        lines = content.split("\n")
        minimum_lines = validator['minimum_lines']
        title_bold = validator['title_bold']
        title_length = validator['title_length']
        description_length = validator['description_length']

        if len(lines) < minimum_lines:
            return False, "Post does not follow the post format.", None
        
        title, text = lines[0], lines[1: len(lines)]

        if title_bold:
            if len(title) < title_length + 4:
                return False, "Title needs to be atleast {} characters long and bolded!".format(title_length), None
            
            if title[:2] != "**" or title[-2:] != "**":
                return False, "Title needs to be bolded!", None

            joined_text = " ".join(text)
            if len(joined_text) < description_length:
                return False, "Content needs to be atleast {} characters long!".format(description_length), None

            return True, title[2:-2], "\n".join(text)
        else:
            if len(title) < title_length:
                return False, "Title needs to be atleast {}} characters long!".format(title_length), None
            
            joined_text = " ".join(text)
            if len(joined_text) < description_length:
                return False, "Content needs to be atleast {} characters long!".format(description_length), None

            return True, title, "\n".join(text)

        

    async def on_ready(self):
        print('BOT IS ONLINE as {0}!'.format(self.user))

    async def on_message(self, message):
        # Skip if its the bots message
        if message.author == self.user:
            return
        # Thread creation
        print("CHECKING THREAD")
        if message.channel.id in self.thread_channels:
            print("TRUE")
            channel = message.channel
            content = message.content
            author = message.author
            template = self.thread_channels[message.channel.id]["template"]
            footer = self.thread_channels[message.channel.id]["footer"]
            thread_emojis = self.thread_channels[message.channel.id]["emojis"]
            embed_post = self.thread_channels[message.channel.id]["embed"]
            thread_role = self.thread_channels[message.channel.id]["role_to_give"]
            validator = self.thread_channels[message.channel.id]["validator"]

            if message.mention_everyone or len(message.role_mentions) > 0:
                await message.delete()
                embed = self._format_embed(title="Invalid Action", message="{} we do not allow mentions in this channel!".format(
                    message.author.mention))
                await channel.send(embed=embed, delete_after=10)
                return

            if message.type == discord.MessageType.default:
                valid, status, text = self._validate_format(validator, content)
                if valid:
                    if embed_post:
                        embed = self._format_embed(title=status, message=text, user=author)
                        embed_sent = await channel.send(embed=embed)
                        for emoji_id in thread_emojis:
                            emoji = discord.utils.get(self.emojis, id=emoji_id)
                            if emoji == None: # Does not exist in the guild
                                continue
                            await embed_sent.add_reaction(emoji)
                        thread = await embed_sent.create_thread(name=status)
                        await thread.add_user(author)
                        role = discord.utils.get(message.guild.roles, id=thread_role)
                        await author.add_roles(role)
                        await message.delete()
                    else:
                        for emoji_id in thread_emojis:
                            emoji = discord.utils.get(self.emojis, id=emoji_id)
                            if emoji == None: # Does not exist in the guild
                                continue
                            await message.add_reaction(emoji)
                        await message.create_thread(name=status)
                        role = discord.utils.get(message.guild.roles, id=thread_role)
                        await author.add_roles(role)
                else:
                    await message.delete()
                    embed = self._format_embed(title="Wrong Format", message="{} the message you sent does not pass post validation for a thread: \n__**{}**__ \n\n**Message:** \n{} \n\n\n **Please make it into a thread with the format:** \n{}".format(
                            message.author.mention, status, content, template),
                            footer="{}".format(footer))
                    await channel.send(embed=embed, delete_after=30)

            if message.type == discord.MessageType.reply:
                channel = message.channel
                await message.delete()
                embed = self._format_embed(title="Invalid Action", message="{} we do not allow replies in this channel!".format(
                        message.author.mention))
                await channel.send(embed=embed, delete_after=10)
            if message.type == discord.MessageType.thread_created:
                channel = message.channel
                if message.guild.id in self.thread_to_remove:
                    self.thread_to_remove[message.guild.id].append(message.id)
                else:
                    self.thread_to_remove[message.guild.id] = []
                    self.thread_to_remove[message.guild.id].append(message.id)
                
                await message.delete()
                embed = self._format_embed(title="Invalid Action", message="{} we do not allow for the direct creation of threads please write a normal message in this channel!".format(
                    message.author.mention))
                await channel.send(embed=embed, delete_after=10)
    
    async def on_thread_join(self, thread):
        if thread.guild.id in self.thread_to_remove:
            if thread.id in self.thread_to_remove[thread.guild.id]:
                await thread.delete()                
                self.thread_to_remove[thread.guild.id].remove(thread.id)

if __name__ == "__main__":
    if os.path.exists(".env"):
        print("Importing environment from .env file")
        for line in open(".env"):
            var = line.strip().split("=")
            os.environ[var[0]] = var[1]

    if os.path.exists('channels.json'):
        f = open('channels.json')
        json_threads = json.load(f)        
        
        token = os.getenv("DISCORD_TOKEN")
        bot = DiscordClientV2(threads=json_threads['channels'])
        bot.run(token)  
    else:
        print("ERROR: channels.json file does not exist failing the script.")
        sys.exit("FAILED TO RUN SCRIPT MISSING channels.json")
