# Discord Chatbot v2

### **Overview**
A Discord "chatbot" that replies with pre-generated responses that appropriately match your message.

If you say "How are you?", the chatbot will respond with something like "I'm good! And you?".

### **Features**
- Profanity detection
- Fast responses
- Extendable code
- Easy to setup

### **lnstallation**
1) `git clone` this repo.
```
git clone https://github.com/Cuh4/DiscordChatbotV2
```

2) Run the following commands:
```
py -m pip install -r requirements.txt
py -m spacy download en
```

3) Create a Discord bot at https://discord.com/developers/applications.

4) In the `src` folder, edit `example_config.py` then rename to `config.py` when completed. Be sure to plop your bot's token in the config file.

5) Start the bot using the following commands:
```
cd src
py main.py
```

6) Invite your bot to a server.

7) Talk to the bot by mentioning it and saying whatever.

### **Images**
![Conversation](imgs/conversation.png)

![Status updates in terminal](imgs/terminalMessages.png)

![Profanity detection](imgs/profanityDetection.png)

![Teach the chatbot from Discord](imgs/teachingForm.png)