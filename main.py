import telebot
from flask import Flask    
from threading import Thread
from flask import Flask    
from threading import Thread
import os
from datetime import datetime, timedelta
import pytz
import time

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
todo_list = {}
tz = pytz.timezone('Asia/Singapore')

def check_reminders():
    while True:
        now = datetime.now(tz)
        for task_id, task in list(todo_list.items()):
            if task['reminder_date'] <= now:
                bot.send_message(task['user_id'], f"Reminder: Task '{task['task']}' is due on {task['due_date'].strftime('%Y-%m-%d %H:%M')}")
                del todo_list[task_id]
        time.sleep(60)  # Check every minute

reminder_thread = Thread(target=check_reminders, daemon=True)
reminder_thread.start()

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
        "/todo - View your todo list.\n"
        "/addlist - Add an item to your list.\n"
        "/complete - Mark an item in todo list as completed.\n"
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

@bot.message_handler(commands=['kiss'])
def summon(message):
    bot.reply_to(message, "Received forehead kiss ticket! Claim it from your love now :D")

@bot.message_handler(commands=['unknown'])
def summon(message):
    bot.reply_to(message, "!!&%@!&*^&*@^*%!!@#^%&^!*!&@^#)(!@&*#^!@$#&%!(*)!@#^!%@&#%*!@#")

@bot.message_handler(commands=['sword'])
def summon(message):
    bot.reply_to(message, "You patiently wait for the shopkeeper to reach for the cool sword from his storage... still waiting... anddd you got scammed there's no sword. But you gained experience points in wisdom! I guess that's something at least.")

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
    user_id = API_ID
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
    11: {"name": "Forehead kiss", "cost": 50},
    12: {"name": "???", "cost": 200},
    13: {"name": "Really cool looking sword (discounted)", "cost": 150}
}

# Add a quest
@bot.message_handler(commands=['add_quest'])
def add_quest(message):
    parts = message.text.split(' ', 1)  # Expecting: /add_quest <quest_name> <description>
    
    if len(parts) < 2:
        bot.reply_to(message, "Usage: /add_quest <quest_name> <quest_description>")
        return
    
    quest_name, quest_description = parts[1].split(' ', 1)
    
    if quest_name in quests:
        bot.reply_to(message, f"⚠ A quest named '{quest_name}' already exists.")
        return
    
    quests[quest_name] = quest_description
    bot.reply_to(message, f"Quest '{quest_name}' added!\n📖 **Description:** {quest_description}")

# Remove a quest
@bot.message_handler(commands=['remove_quest'])
def remove_quest(message):
    parts = message.text.split(' ', 1)
    
    if len(parts) < 2:
        bot.reply_to(message, "Usage: /remove_quest <quest_name>")
        return
    
    quest_name = parts[1].strip()
    
    if quest_name in quests:
        del quests[quest_name]
        bot.reply_to(message, f"Quest '{quest_name}' has been removed.")
    else:
        bot.reply_to(message, f"⚠ No quest found with the name '{quest_name}'.")

# Add an item to the shop
@bot.message_handler(commands=['add_item'])
def add_item(message):
    parts = message.text.split(' ', 2)  # Expecting: /add_item <item_name> <cost>
    
    if len(parts) < 3 or not parts[2].isdigit():
        bot.reply_to(message, "Usage: /add_item <item_name> <cost>")
        return
    
    item_name = parts[1].strip()
    item_cost = int(parts[2])
    
    if item_name in shop_items:
        bot.reply_to(message, f"⚠ An item named '{item_name}' already exists.")
        return
    
    shop_items[item_name] = item_cost
    bot.reply_to(message, f"Item '{item_name}' added to the shop!\n**Cost:** {item_cost} shards")

# Remove an item from the shop
@bot.message_handler(commands=['remove_item'])
def remove_item(message):
    parts = message.text.split(' ', 1)
    
    if len(parts) < 2:
        bot.reply_to(message, "Usage: /remove_item <item_name>")
        return
    
    item_name = parts[1].strip()
    
    if item_name in shop_items:
        del shop_items[item_name]
        bot.reply_to(message, f"Item '{item_name}' has been removed from the shop.")
    else:
        bot.reply_to(message, f"⚠ No item found with the name '{item_name}'.")

# Notify that the bot is down for maintenance
@bot.message_handler(commands=['down'])
def bot_down(message):
    bot.send_message(API_ID, "The bot is currently down for maintenance. Please check back later.")
    bot.reply_to(message, "The bot is currently down for maintenance. Please check back later.")

# Notify that the bot is live again
@bot.message_handler(commands=['up'])
def bot_up(message):
    bot.send_message(API_ID, "The bot is now live and fully operational!")
    bot.reply_to(message, "The bot is now live and fully operational!")

@bot.message_handler(commands=['addlist'])
def add_list(message):
    bot.reply_to(message, "Enter the task description:")
    bot.register_next_step_handler(message, process_add_list)

def process_add_list(message):
    task_description = message.text.strip()
    task_id = len(todo_list) + 1
    bot.reply_to(message, "Input due date and time (YYYY-MM-DD HH:MM) in Singapore time:")
    bot.register_next_step_handler(message, lambda msg: process_due_date(msg, task_id, task_description))

def process_due_date(message, task_id, task_description):
    try:
        due_date = datetime.strptime(message.text.strip(), "%Y-%m-%d %H:%M").replace(tzinfo=tz)
        bot.reply_to(message, "Input reminder date and time (YYYY-MM-DD HH:MM) in Singapore time:")
        bot.register_next_step_handler(message, lambda msg: process_reminder(msg, task_id, task_description, due_date))
    except ValueError:
        bot.reply_to(message, "Invalid format. Please use YYYY-MM-DD HH:MM")

def process_reminder(message, task_id, task_description, due_date):
    try:
        reminder_date = datetime.strptime(message.text.strip(), "%Y-%m-%d %H:%M").replace(tzinfo=tz)
        todo_list[task_id] = {"task": task_description, "due_date": due_date, "reminder_date": reminder_date}
        bot.reply_to(message, f"Task '{task_description}' added successfully with ID {task_id}!")
    except ValueError:
        bot.reply_to(message, "Invalid format. Please use YYYY-MM-DD HH:MM")

@bot.message_handler(commands=['todo'])
def view_todo(message):
    if not todo_list:
        bot.reply_to(message, "Your to-do list is empty.")
    else:
        response = "Your current tasks:\n"
        for task_id, task in todo_list.items():
            response += f"ID: {task_id} | Task: {task['task']} | Due: {task['due_date'].strftime('%Y-%m-%d %H:%M')} | Reminder: {task['reminder_date'].strftime('%Y-%m-%d %H:%M')}\n"
        bot.reply_to(message, response)

@bot.message_handler(commands=['complete'])
def complete_task(message):
    bot.reply_to(message, "Enter the task ID to mark as completed:")
    bot.register_next_step_handler(message, process_complete_task)

def process_complete_task(message):
    try:
        task_id = int(message.text.strip())
        if task_id in todo_list:
            bot.reply_to(message, f"Are you sure you want to mark task {task_id} as completed? Reply 'Yes' to confirm.")
            bot.register_next_step_handler(message, lambda msg: confirm_complete(msg, task_id))
        else:
            bot.reply_to(message, "Task ID not found.")
    except ValueError:
        bot.reply_to(message, "Invalid task ID.")

def confirm_complete(message, task_id):
    if message.text.lower() == 'Yes':
        del todo_list[task_id]
        bot.reply_to(message, f"Task {task_id} marked as completed!")
    else:
        bot.reply_to(message, "Task completion cancelled.")

@bot.message_handler(commands=['shop'])
def show_shop(message):
    shop_text = "Welcome to the shop! Here are the items available:\n"
    for item_id, item in shop_items.items():
        shop_text += f"{item_id}: {item['name']} - {item['cost']} shards\n"
    shop_text += "\nTo buy an item, type 'Buy <item number>'."
    shop_text += "\nTo exit the shop, type 'exit'."
    bot.reply_to(message, shop_text)

@bot.message_handler(func=lambda message: message.text.lower().startswith('Buy '))
def buy_item(message):
    user_id = API_ID
    parts = message.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        bot.reply_to(message, "Invalid command. Use 'Buy <item number>'.")
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
    elif item_id == 11:
        bot.reply_to(message, f"Thank you for your purchase! You bought {item['name']}!\nYour current number of shards is: {user_data[user_id]}\nYou can check the contents using /kiss.")    
    elif item_id == 12:
        bot.reply_to(message, f"Thank you for your purchase! You bought {item['name']}!\nYour current number of shards is: {user_data[user_id]}\nYou can check the contents using /unknown.")    
    elif item_id == 13:
        bot.reply_to(message, f"Thank you for your purchase! You bought {item['name']}!\nYour current number of shards is: {user_data[user_id]}\nYou can check the contents using /sword.")    
    else:
        bot.reply_to(message, f"Thank you for your purchase! You bought {item['name']}!\nYour current number of shards is: {user_data[user_id]}")
    

@bot.message_handler(func=lambda message: message.text.lower() == 'Exit')
def exit_shop(message):
    bot.reply_to(message, "You have exited the shop.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Invalid command. Please type '/help' to see available commands.")


print("Bot is running...")
bot.polling(non_stop=True, timeout=60, long_polling_timeout=10)
