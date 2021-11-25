import requests
import discord
import os

class DiscordClient(discord.Client):
    def __init__(self, thread_channels, thread_emojis, thread_role, embed_posts = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.thread_to_remove = dict()
        self.thread_channels = thread_channels.copy()
        self.thread_emojis = thread_emojis.copy()
        self.thread_role = thread_role
        
        self.embed_posts = embed_posts

        self.format = """--------
**TITLE** (Atleast 10 characters long + CTRL+B or COMMAND+B)            

CONTENT (Alteast 30 characters long)
--------"""
        self.footer = "How to bold title in markdown: **title**"

    def _format_embed(self, message, title, user = None, footer = None):
        embed = discord.Embed(title=title, description=message, color=0xFFFFFF)
        if user:
            embed.add_field(name="Author", value="{}".format(user.mention), inline=True)
            embed.set_author(name=user.name, icon_url=user.avatar.url)
        if footer:
            embed.set_footer(text=footer)
        return embed

    def _validate_format(self, content):
        lines = content.split("\n")

        if len(lines) < 3:
            return False, "Post does not follow the post format.", None
        
        title, text = lines[0], lines[1: len(lines)]

        if len(title) < 14:
            return False, "Title needs to be atleast 10 characters long!", None
        
        if title[:2] != "**" or title[-2:] != "**":
            return False, "Title needs to be bolded!", None

        joined_text = " ".join(text)
        if len(joined_text) < 20:
            return False, "Content needs to be atleast 20 characters long!", None

        return True, title[2:-2], "\n".join(text)

    async def on_ready(self):
        print('BOT IS ONLINE as {0}!'.format(self.user))

    async def on_message(self, message):
        # Skip if its the bots message
        if message.author == self.user:
            return
        # Thread creation
        if message.channel.id in self.thread_channels:
            channel = message.channel
            content = message.content
            author = message.author

            if message.mention_everyone or len(message.role_mentions) > 0:
                await message.delete()
                embed = self._format_embed(title="Invalid Action", message="{} we do not allow mentions in this channel!".format(
                    message.author.mention))
                await channel.send(embed=embed, delete_after=10)
                return

            if message.type == discord.MessageType.default:
                valid, status, text = self._validate_format(content)
                if valid:
                    if self.embed_posts:
                        embed = self._format_embed(title=status, message=text, user=author)
                        embed_sent = await channel.send(embed=embed)
                        for emoji_id in self.thread_emojis:
                            emoji = discord.utils.get(self.emojis, id=emoji_id)
                            if emoji == None: # Does not exist in the guild
                                continue
                            await embed_sent.add_reaction(emoji)
                        thread = await embed_sent.create_thread(name=status)
                        await thread.add_user(author)
                        role = discord.utils.get(message.guild.roles, id=self.thread_role)
                        await author.add_roles(role)
                        await message.delete()
                    else:
                        for emoji_id in self.thread_emojis:
                            emoji = discord.utils.get(self.emojis, id=emoji_id)
                            if emoji == None: # Does not exist in the guild
                                continue
                            await message.add_reaction(emoji)
                        await message.create_thread(name=status)
                        role = discord.utils.get(message.guild.roles, id=self.thread_role)
                        await author.add_roles(role)
                else:
                    await message.delete()
                    embed = self._format_embed(title="Wrong Format", message="{} the message you sent does not pass post validation for a thread: \n__**{}**__ \n\n**Message:** \n{} \n\n\n **Please make it into a thread with the format:** \n{}".format(
                            message.author.mention, status, content, self.format),
                            footer="{}".format(self.footer))
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
    
    test_channel = int(os.getenv("TEST_CHANNEL_ID"))
    production_channel = int(os.getenv("PRODUCTION_CHANNEL_ID"))
    thread_channels = [test_channel]

    upvode_id = int(os.getenv("UPVOTE_ID"))
    thread_emojis = [upvode_id]


    insight_role = int(os.getenv("REACTION_ROLE_ID"))
    thread_role = insight_role

    token = os.getenv("DISCORD_TOKEN")
    bot = DiscordClient(thread_channels=thread_channels, thread_emojis=thread_emojis, thread_role = thread_role)
    bot.run(token)