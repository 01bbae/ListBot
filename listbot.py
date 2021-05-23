import discord
import os
client = discord.Client()
TOKEN = '' #BOT TOKEN HERE

@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

        
    # add list items
    if message.content.startswith('!add'):
        store=message.content.replace('!add', '').strip()
        await message.delete()
        print(store)

        msg = await message.channel.history().get(author__name=client.user.name)
        print(msg)
        if msg != None:
            number = len(msg.content.split('\n')) + 1
            await msg.edit(content=str(msg.content + "\n**" +str(number) + ')** ' +  store))
        else:
            await message.channel.send('**1)** ' +store)
    
    # delete list items
    if message.content.startswith('!del'): 
        store = message.content.replace('!del','').strip()
        await message.delete()
        if store.isnumeric(): #!del 5 delete 5th list item
            msg = await message.channel.history(oldest_first=True).get(author__name=client.user.name) #.flatten() one msg, dont need
            store = int(store)
            counter = 1
            for lines in msg.content.split('\n'):
                if counter == store and store != 1:
                    await msg.edit(content=msg.content.replace('\n'+lines,''))
                elif counter == store and store == 1:
                    await msg.edit(content=msg.content.replace(lines,''))
                elif counter>store:
                    list = lines.split(' ')
                    await msg.edit(content=msg.content.replace(list[0],'**'+str(counter-1)+')**'))
                counter+=1
                    

                

    #clear channel
    if message.content =='!clear':
        await message.delete()
        await message.channel.send('*Are you sure you want to clear this channel?*')
        msg = await message.channel.history().get(author__name=client.user.name)
        await msg.add_reaction('\U00002705')
        await msg.add_reaction('\U0000274C') #https://www.reddit.com/r/Discord_Bots/comments/gz3rjv/get_emoji_id/

        def check(reaction,user): #https://discordpy.readthedocs.io/en/latest/api.html?highlight=wait#discord.Client.wait_for
            return user == message.author and (reaction.emoji == '\U00002705' or reaction.emoji == '\U0000274C')
        reaction, user = await client.wait_for('reaction_add',check=check)
        print(reaction)
        print(user)
        if(reaction.emoji == '\U00002705'):
            await msg.delete()
            await message.channel.purge()
        else:
            await msg.delete()
        

client.run(TOKEN)