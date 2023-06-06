# ED-FCO
Buy me a coffee? https://ko-fi.com/kofisupporter28697
Elite Dangerous Fleet Carrier Operations bot for Discord

This bot addresses an issue I've had with tools that try to achieve more automation. This sacrifices automation
to allow you to quickly and easily update subscribed parties on the movements of your fleet carrier.

Subscriptions to specific carriers allow you to control what carriers you receive updates for and in what channels.

Notify players that your carrier will be jumping and where

***To Do:***

Detail services currently active on the carrier

Allow for updating on location

Allow for status querying from other players

***Setup:***

If you don't want to host this yourself, just invite my instance to your server:
https://discord.com/api/oauth2/authorize?client_id=1114197311191535667&permissions=8&scope=bot

Although the bot is meant to be centralized for all servers, you can run your own instance of it. Within the bot.py file, go to the last line where `bot.run()` is called and replace the parameter with your Discord bot token, and comment out the line calling `Setup()`. These lines exist to call a method that reads Discord tokens from an external file for security reasons, and you're free to use them, but I haven't quite figured out how relative paths work on Linux (where this is deployed) vs. Windows (where I develop).
