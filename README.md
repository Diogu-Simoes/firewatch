# UPDATE: This discord bot will now be staying permanently offline. 

### This was a personal project I started during the summer in my freshman year of Computer Engineering so as you would expect the code is let's say... not the best, and documentation is of course non-existent. 

### I will be leaving this repository public for posterity sake and to maybe give inspiration to anyone who has a similar idea. 

### You can still add the bot to your server if for whatever reason you would like to do so, the link should still probably work but the bot itself will of course do nothing. 

### Under this line will now continue the original README.

# _____________________________________________________

### [Click here to add this bot to your Discord!](https://discord.com/api/oauth2/authorize?client_id=999712607227359274&permissions=140123827264&scope=bot%20applications.commands)

## INFO:

FIREWATCH is an open-source Discord bot capable of giving real time information about wildfires in Portugal, making use of an intuitive interface where the user can select the region whose fires they would like to be alerted of, along with a variety of options.

The fact that it allows for channel select on where to send the alerts allows admins to create roles that make it so the bot will only ping people that opt-in to it by having the specific role that allows them to view that channel.

All the bot commands are slash commands so you can type a '/' and see all avaliable commands in a very user-friendly and instant way. The commands also come with descriptions for even better understanding of their functions and capabilities.

I came up with the idea for FIREWATCH due to the increasingly amount of wildifres in Portugal over the last couple of years, especially during summers. Since 2017 most of our country's damage from natural disasters has been solely from wildfires, either set by acident or intentionally.

This was my first atempt at a Discord bot and my first interaction with the discord.py library after coming up with the idea for FIREWATCH. I know there is a lot that can be improved and I'm open to all type of constructive criticism.

When adding the bot to your Discord you may notice that it requires more permissions than it uses, this is because there are plans to improve upon the current framework and display methods, making it so users don't have to re-add the bot if it ever does get updated.

And on that note, below is a task list with some of the plans I would personaly love to see on the FIREWATCH bot.

### TASK LIST:

- [ ] Add compatibility for mobile (I've been trying but can't seem to get the app commands to work on mobile)
- [x] Add data persitence (Channel/Region/On/Off) troughout bot shortages, reboots or updates using a database
- [ ] Make the fire list display more user friendly through the use of webhooks
- [ ] Allow searching/alert for fires in a whole district, without forcing a town
- [ ] Add images to this description, to bettber represent functionality
- [ ] Show a satelite image of the fire location when displaying it (Using LAT/LONG coordinates from the api)~~




