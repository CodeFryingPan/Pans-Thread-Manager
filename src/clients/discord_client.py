import requests
import discord
import os


async def create_thread(self,name,minutes,message):
    token = 'Bot ' + self._state.http.token
    url = f"https://discord.com/api/v9/channels/{self.id}/messages/{message.id}/threads"
    headers = {
        "authorization" : token,
        "content-type" : "application/json"
    }
    data = {
        "name" : name,
        "type" : 11,
        "auto_archive_duration" : minutes
    }
 
    return requests.post(url,headers=headers,json=data).json()

discord.TextChannel.create_thread = create_thread

class DiscordClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.thread_channels = [907810748430950410]
        self.emojis_to_add = [911326534923583498, 911326527357083730]
        self.format = """ 
            --------
            **TITLE** (Atleast 10 characters long)
                        
            CONTENT (Alteast 30 characters long)
            --------
            ```Required: \n\nTo bold: **title*\n\nOptional: \n\nTo add block quote to single message: > message\nTo add block quote to all message: >>> message ```
        """

    def _validate_format(self, content):
        lines = content.split("\n")

        if len(lines) < 3:
            return False, "Post does not follow the post format."
        
        title, text = lines[0], lines[1: len(lines)]

        if len(title) < 14:
            return False, "Title needs to be atleast 10 characters long!"
        
        if title[:2] != "**" or title[-2:] != "**":
            return False, "Title needs to be bolded!"

        joined_text = " ".join(text)
        if len(joined_text) < 20:
            return False, "Content needs to be atleast 20 characters long!"

        return True, title[2:-2]

    async def on_ready(self):
        print('BOT IS ONLINE as {0}!'.format(self.user))

    async def on_message(self, message):
        # Skip if its the bots message
        if message.author == self.user:
            return

        # Thread creation
        if message.channel.id in self.thread_channels:
            if message.type == discord.MessageType.default:
                channel = message.channel
                content = message.content
                valid, status = self._validate_format(content)
                if valid:
                    for emoji_id in self.emojis_to_add:
                        emoji = discord.utils.get(self.emojis, id=emoji_id)
                        if emoji == None: # Does not exist in the guild
                            continue
                        await message.add_reaction(emoji)
                    await channel.create_thread(status, minutes=60, message=message)
                else:
                    await message.delete()
                    await channel.send("**{} the message you sent does not pass post validation for a thread with the following reason:** \n{} \n\n**Message:** \n{} \n\n\n**Please make it into a thread with the format:** \n{}".format(
                            message.author.mention, 
                            status,
                            content, 
                            self.format), 
                        delete_after=30)

            if message.type == discord.MessageType.thread_created:
                # TEST
                for emoji_id in self.emojis_to_add:
                    emoji = discord.utils.get(self.emojis, id=emoji_id)
                    if emoji == None: # Does not exist in the guild
                        continue
                    await message.add_reaction(emoji)
            
                
        # await self.get_channel(907810748430950410).send('Message from {0.author}: {0.content} in {0.channel.id}'.format(message))

if __name__ == "__main__":
    if os.path.exists(".env"):
        print("Importing environment from .env file")
        for line in open(".env"):
            var = line.strip().split("=")
            os.environ[var[0]] = var[1]

    token = os.getenv("DISCORD_TOKEN")
    bot = DiscordClient()
    bot.run(token)