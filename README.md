
# telegram-google-calendar-bot
Telegram bot for managing public google calendars for working chats. It has fluent text recognition (by yandex api or google itself).

Consists of:
 - Flask webserver (for tg webhooks + handling google oauth2 routine)
 - PeeWee orm and sqlite to store user data
 - telebot lib 
 - ouath2 client for google api

Also because of oauth2 you should configure ssl certificate on your hosting machine (i've been using letsencrypt). Bot has been implemented to be hosted as an webapp under nginx or any other reverse-proxy web-server.

### Main use case:
Bot can be used by a group of people that are sharing google calendar between them to have actual
data about their time and employment. Main achievement of this bot over manual calendar control is the method of
interaction with calendar that bot can give you: after bot was invited in your chat, it should be configured
by one of the chat's administrators (bot should be attached to google calendar which will be used to work with).
After it any user from chat can write in private messages to bot about their plans in fluent form, examples:
"Tomorrow at 16:00 meeting in Starbucks", "From 20.01 to 25.01 on a business trip", "Today available by phone from 14:00 to 14:50"
and bot will correctly parse time markers & meaning of what you write and will add those events in attached G calendar.

UPDATE:
In developing 2 years ago API of telegram and google calendar could greatly change over time, so do not consider this bot as 
"BUILD-RUN-WORK DONE" solution.

License
----

MIT
