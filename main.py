import telebot
from flask import Flask    
from threading import Thread
from flask import Flask    
from threading import Thread
import os

API_KEY = os.getenv("API_KEY")
API_ID = os.getenv("API_ID")

app = Flask('')

@app.route('/')    
def home():    
    return "Bot started! Running..."

def run():    
    app.run(host='0.0.0.0',port=8080)

def keep_alive():    
    t = Thread(target=run)    
    t.start()

keep_alive()

# Replace 'YOUR_BOT_TOKEN' with your actual bot token from BotFather
TOKEN = API_KEY
bot = telebot.TeleBot(TOKEN)

# Dictionary to store count per user
user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Oh noes!! Looks like the evil cupid was jealous of your love for crystal, so he has decided to steal Obby away from you!! Fret not, for I am the cupid bot, designed to help you find Obby, and bring him back to you! Your task for these 2 days will be to collect love shards. These love shards will allow you to buy items from my almighty love shop, but be aware to spend wisely as it is not easy to earn shards! If you need any additonal help, just search /help for all my functions. Good luck, and may the cupid be with you!")

@bot.message_handler(commands=['help'])
def help(message):
    help_text = (
        "Hello! I'm cupid. Here are my commands:\n"
        "/help - Well, it leads you back here. Duh.\n"
        "/earn - Learn how to earn shards.\n"
        "/quest - Quests to be completed for love shards.\n"
        "/shards - Check your current love shards count.\n"
        "/shop - View available shop items.\n"
    )
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['earn'])
def earn(message):
    bot.reply_to(message, "To earn shards, you will need to complete love acts. Each love act will be determined by the cupid himself, in which he will give you love shards based on how much love is involved. Additionally, you can also complete quests (under /quest) to find out how to earn as many shards as possible. Go out there and earn some shards now!!")

@bot.message_handler(commands=['opengift'])
def gift(message):
    bot.reply_to(message, "You carefully open your gift to find out that... there was nothing. Yes, you wasted your love shards. No refunds. Womp womp.")

@bot.message_handler(commands=['obbyclue'])
def clue(message):
    bot.reply_to(message, "Obby screams out: JUST BUY THE FREAKING SHOP ITEM THAT LITERALLY HAS MY NAME ON IT WHY WOULD YOU WASTE MONEY ON CLUES???")

@bot.message_handler(commands=['JJ'])
def jj(message):
    bot.reply_to(message, "You crack open their safe box to find that... WOW they really do have lots of love shards saved up! Time to take it from them... \nObtained: 500 love shards")

@bot.message_handler(commands=['obbysock'])
def sock(message):
    bot.reply_to(message, "You looked at it and took a huge sniff. Yes that smells like him, you told yourself.")

@bot.message_handler(commands=['summonobby'])
def summon(message):
    bot.reply_to(message, "You saved me!! YAYYYY heheh I knew you would be able to find me :D.")

@bot.message_handler(commands=['potion'])
def summon(message):
    bot.reply_to(message, "Received 1x free drink of your choice! Claim it from your love now :D")

@bot.message_handler(commands=['useticket'])
def ticket(message):
    bot.reply_to(message, "With trembling hands, you scratched off the numbers on the ticket to find... THAT YOU WON 100 DOLLARS!! Time to claim it and go out for a meal <3")    

@bot.message_handler(commands=['userincrement'])
def increment_number(message):
    user_id = API_ID     #replace with lil jx number
    try:
        parts = message.text.split()
        if len(parts) > 1:
            increment_value = int(parts[1])
        else:
            increment_value = 0  # Default increment if no number provided

        if user_id not in user_data:
            user_data[user_id] = 0

        user_data[user_id] += increment_value
        bot.send_message(user_id, f"You have earned love shards! Your current count is:  {user_data[user_id]}")
        bot.reply_to(message, f"Current updated count: {user_data[user_id]}")
    except ValueError:
        bot.reply_to(message, "Please provide a valid number. Usage: /increment <number>")

@bot.message_handler(commands=['shards'])
def get_count(message):
    user_id = message.from_user.id
    count = user_data.get(user_id, 0)
    bot.reply_to(message, f"Your current number of shards: {count}")

quests = {
    1: {"name": "Escaper", "description": "Follow your love on an adventure and successfully complete the activity. Take pictures for proof of completion. Reward: 500 love shards"},
    2: {"name": "Gamer", "description": "Play valorant with your love and win 5 matches. Reward: 300 love shards"},
    3: {"name": "Brawl Starssss", "description": "Win 5 battles of brawl stars with your love. Reward: 200 love shards"},
    4: {"name": "Bolster Madness","description": "Willingly give up bolster for a night. Reward: 200 love shards"}
}

@bot.message_handler(commands=['quest'])
def quest(message):
    quest_text = "Here are the quests available:\n"
    for quest_id, q in quests.items():
        quest_text += f"{quest_id}: {q['name']} - {q['description']} \n"
        quest_text += "\n"
    bot.reply_to(message, quest_text)

# Shop items
shop_items = {
    1: {"name": "Back Scratch Ticket (15 minutes)", "cost": 200},
    3: {"name": "Bolster Privilege", "cost": 250},
    7: {"name": "A car", "cost": 400},
    8: {"name": "Obby", "cost": 1000},
    9: {"name": "Scratch Ticket", "cost": 1500},
    10: {"name": "Potion?", "cost": 300},
}

@bot.message_handler(commands=['shop'])
def show_shop(message):
    shop_text = "Welcome to the shop! Here are the items available:\n"
    for item_id, item in shop_items.items():
        shop_text += f"{item_id}: {item['name']} - {item['cost']} shards\n"
    shop_text += "\nTo buy an item, type 'buy <item number>'."
    shop_text += "\nTo exit the shop, type 'exit'."
    bot.reply_to(message, shop_text)

@bot.message_handler(func=lambda message: message.text.lower().startswith('buy '))
def buy_item(message):
    user_id = message.from_user.id
    parts = message.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        bot.reply_to(message, "Invalid command. Use 'buy <item number>'.")
        return

    item_id = int(parts[1])
    if item_id not in shop_items:
        bot.reply_to(message, "Item not found. Check the shop again using /shop.")
        return

    item = shop_items[item_id]
    user_shards = user_data.get(user_id, 0)

    if user_shards < item['cost']:
        bot.reply_to(message, "Not enough shards!")
        return

    user_data[user_id] -= item['cost']
    del shop_items[item_id]  # Remove the item from the shop

    if item_id == 2:
        bot.reply_to(message, f"Thank you for your purchase! You bought {item['name']}!\nYour current number of shards is: {user_data[user_id]}\nYou can open your mystery gift using /opengift.")
    elif item_id == 4:
        bot.reply_to(message, f"Thank you for your purchase! You bought {item['name']}!\nYour current number of shards is: {user_data[user_id]}\nYou can check your clue using /obbyclue.")
    elif item_id == 5:
        bot.reply_to(message, f"Thank you for your purchase! You bought {item['name']}!\nYour current number of shards is: {user_data[user_id]}\nYou can check their savings using /JJ.")
    elif item_id == 6:
        bot.reply_to(message, f"Thank you for your purchase! You bought {item['name']}!\nYour current number of shards is: {user_data[user_id]}\nYou can check the contents using /obbysock.")
    elif item_id == 7:
        bot.reply_to(message, f"Thank you for your purchase! You bought {item['name']}!\nYour current number of shards is: {user_data[user_id]}\nYou can check the contents using /redeemcar.")
    elif item_id == 8:
        bot.reply_to(message, f"Thank you for your purchase! You bought {item['name']}!\nYour current number of shards is: {user_data[user_id]}\nYou can check the contents using /summonobby.")
    elif item_id == 9:
        bot.reply_to(message, f"Thank you for your purchase! You bought {item['name']}!\nYour current number of shards is: {user_data[user_id]}\nYou can check the contents using /useticket.")
    elif item_id == 10:
        bot.reply_to(message, f"Thank you for your purchase! You bought {item['name']}!\nYour current number of shards is: {user_data[user_id]}\nYou can check the contents using /potion.")    
    else:
        bot.reply_to(message, f"Thank you for your purchase! You bought {item['name']}!\nYour current number of shards is: {user_data[user_id]}")
    

@bot.message_handler(func=lambda message: message.text.lower() == 'exit')
def exit_shop(message):
    bot.reply_to(message, "You have exited the shop.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Invalid command. Please type '/help' to see available commands.")


print("Bot is running...")
bot.polling()
