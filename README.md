# [Click here to add this bot to your discord!](https://discord.com/api/oauth2/authorize?client_id=999712607227359274&permissions=140123827264&scope=bot%20applications.commands)

FIREWATCH is a discord bot capable of giving real time information about wildfires in Portugal, making use of an intuitive interface where the user can use dropdown menus to search the select regions for fires without ever leaving discord or needing a 3rd party app.  

It is also capable of alerting (if turned on) all discord members of a server to the appearence of a wildfire in the region set by the admin of that specific server through the settings command.  

The fact that it allows for channel select on where to send the alerts allows admins to create roles that make it so the bot will only ping people that opt-in to it by having the specific role that allows them to view that channel.

I came up with the idea for FIREWATCH due to the increasingly amount of wildifres in Portugal over the last couple of years, especially during summers. Since 2017 most of our country's damage from natural disasters has been solely from wildfires, either set by acident or intentionally.

## Extra Info:
This was my first atempt at a discord bot and my first interaction with the discord.py library after coming up with the idea for FIREWATCH. I know there is a lot that can be improved and I'm open to all type of constructive criticism.

When adding the bot to your discord you may notice that it requires more permissions than it uses, this is because there are plans to improve upon the current framework and display methods, making it so users don't have to readd the bot if it ever does get updated. That, of course, is only possible if I ever get some help or learn more about the library on my free time.

And on that note, below is a task list with some of the plans I would personaly love to see on the FIREWATCH bot.  

### Task List:

- [ ] Add compatibility for mobile (I have been trying and can't seem to get the app commands to work on mobile)
- [ ] Add data persitence (Channel/Region/On/Off) troughout bot shortages, reboots or updates using a database
- [ ] Make the fire list display more user friendly through the use of webhooks
- [ ] Show a satelite image of the fire location when displaying it (Using LAT/LONG from the api)




