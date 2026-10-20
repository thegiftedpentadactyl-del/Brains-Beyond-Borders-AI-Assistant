import os
import random
from flask import Flask, request as flask_request
import telebot
from google import genai
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- SECURE CREDENTIALS ---
TELEGRAM_BOT_TOKEN = "8845212664:AAHq9pMp4xA5rlrIH669kSf5_88frWe8o0U"
GEMINI_API_KEY = "AQ.Ab8RN6Ln8amKuFVL8FNepn0simY9_Hpx6LCpibWKVdN6AhQRHA"

# Set environment variable so the GenAI client recognizes the OAuth token format
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

# Initialize Flask, GenAI Client & Bot
app = Flask(__name__)
client = genai.Client()
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, threaded=False)

# In-memory storage for user profiles and onboarding states
user_states = {}
user_profiles = {}

# 10-Step Onboarding States
STATE_NAME = 1
STATE_AI_NAME = 2
STATE_LEVEL = 3
STATE_MAJOR = 4
STATE_COUNTRY = 5
STATE_TARGET_DEGREE = 6
STATE_GPA = 7
STATE_TEST_STATUS = 8
STATE_CHALLENGE = 9
STATE_STYLE = 10
STATE_COMPLETED = 11

INSPIRATIONAL_QUOTES = [
    "Education is the most powerful weapon which you can use to change the world. It is the great engine of personal development, bridging the gap between humble beginnings and extraordinary achievement. — Nelson Mandela",
    "It always seems impossible until it's done. Every grand scholarly pursuit starts with a single step into the unknown, driven by relentless curiosity and disciplined execution. — Nelson Mandela",
    "The future belongs to those who prepare for it today. Preparation, vision, and uncompromising commitment are the true architects of global opportunity. — Malcolm X",
    "An investment in knowledge pays the best interest. When you dedicate yourself to mastering your craft, the dividends reshape generations. — Benjamin Franklin",
    "Live as if you were to die tomorrow. Learn as if you were to live forever. True scholarship is an infinite journey of expansion and discovery. — Mahatma Gandhi"
]

def get_community_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("WhatsApp Channel", url="https://whatsapp.com/channel/0029Vb70gca0LKZBZ1XBkx1s"),
        InlineKeyboardButton("WhatsApp Community Group", url="https://chat.whatsapp.com/BMlr2QoQVuc9um7r5kxacT"),
        InlineKeyboardButton("LinkedIn Page", url="https://www.linkedin.com/company/brains-beyond-borders-ng/"),
        InlineKeyboardButton("Official Portal", url="https://www.brainsbeyondboders.org")
    )
    return markup

@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def webhook():
    if flask_request.headers.get('content-type') == 'application/json':
        json_data = flask_request.get_json(force=True)
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_updates([update])
        return "OK", 200
    return "OK", 200

@app.route("/", methods=["GET"])
def index():
    return "Brains Beyond Borders AI Assistant is live and operational via Webhook.", 200

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chat_id = message.chat.id
    user_states[chat_id] = STATE_NAME
    user_profiles[chat_id] = {}
    
    selected_quote = random.choice(INSPIRATIONAL_QUOTES)
    
    welcome_text = (
        "Welcome aboard.\n\n"
        f"As you step into your future, reflect upon this wisdom: \"{selected_quote}\"\n\n"
        "We are honored to welcome you to the Brains Beyond Borders community. "
        "To curate an elite, highly personalized experience tailored precisely to your ambitions, let us walk through 10 brief intake questions.\n\n"
        "Question 1/10: What is your full name?"
    )
    bot.send_message(chat_id, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    chat_id = message.chat.id
    text = message.text.strip()
    
    state = user_states.get(chat_id)
    
    if state == STATE_NAME:
        user_profiles[chat_id]['name'] = text
        user_states[chat_id] = STATE_AI_NAME
        bot.send_message(chat_id, "Question 2/10: What would you like to name your personal AI assistant?")
        return
        
    elif state == STATE_AI_NAME:
        user_profiles[chat_id]['ai_name'] = text
        user_states[chat_id] = STATE_LEVEL
        bot.send_message(chat_id, "Question 3/10: What is your current academic level? (e.g., Undergraduate, Bachelor's Graduate, Master's)")
        return
        
    elif state == STATE_LEVEL:
        user_profiles[chat_id]['level'] = text
        user_states[chat_id] = STATE_MAJOR
        bot.send_message(chat_id, "Question 4/10: What is your major or specific field of study?")
        return
        
    elif state == STATE_MAJOR:
        user_profiles[chat_id]['major'] = text
        user_states[chat_id] = STATE_COUNTRY
        bot.send_message(chat_id, "Question 5/10: What is your target country or region for international scholarships?")
        return
        
    elif state == STATE_COUNTRY:
        user_profiles[chat_id]['country'] = text
        user_states[chat_id] = STATE_TARGET_DEGREE
        bot.send_message(chat_id, "Question 6/10: What specific degree or program type are you targeting next? (e.g., Direct PhD, Master's Funded, Fellowship)")
        return

    elif state == STATE_TARGET_DEGREE:
        user_profiles[chat_id]['target_degree'] = text
        user_states[chat_id] = STATE_GPA
        bot.send_message(chat_id, "Question 7/10: What is your current academic standing or GPA range? (e.g., First Class, 4.8/5.0, Top 5%)")
        return

    elif state == STATE_GPA:
        user_profiles[chat_id]['gpa'] = text
        user_states[chat_id] = STATE_TEST_STATUS
        bot.send_message(chat_id, "Question 8/10: Have you taken or planned your English proficiency tests or standardized exams? (e.g., IELTS, GRE, None yet)")
        return

    elif state == STATE_TEST_STATUS:
        user_profiles[chat_id]['test_status'] = text
        user_states[chat_id] = STATE_CHALLENGE
        bot.send_message(chat_id, "Question 9/10: What is your single biggest hurdle or challenge in your scholarship journey right now?")
        return

    elif state == STATE_CHALLENGE:
        user_profiles[chat_id]['challenge'] = text
        user_states[chat_id] = STATE_STYLE
        bot.send_message(chat_id, "Question 10/10: What is your preferred communication style for our advisory sessions? (e.g., Direct and concise, Highly detailed and structured)")
        return
        
    elif state == STATE_STYLE:
        user_profiles[chat_id]['style'] = text
        user_states[chat_id] = STATE_COMPLETED
        
        profile = user_profiles[chat_id]
        completion_text = (
            f"Profile Configuration Complete.\n\n"
            f"It is an absolute privilege to partner with you, {profile['name']}.\n\n"
            f"Your personal assistant, {profile['ai_name']}, is fully initialized for your {profile['level']} background in {profile['major']}, targeting {profile['target_degree']} opportunities in {profile['country']}.\n\n"
            "Please connect with our official community channels below before diving into your scholarship journey:"
        )
        bot.send_message(chat_id, completion_text, reply_markup=get_community_markup())
        return

    try:
        bot.send_message(chat_id, "Your message is under processing. Please allow 15 to 30 seconds for our secure cloud server to compile your comprehensive guidance...")
        bot.send_chat_action(chat_id, 'typing')
        
        profile = user_profiles.get(chat_id, {})
        p_name = profile.get('name', 'Scholar')
        ai_name = profile.get('ai_name', 'Assistant')
        p_level = profile.get('level', 'Student')
        p_major = profile.get('major', 'General')
        p_country = profile.get('country', 'Global')
        p_degree = profile.get('target_degree', 'Postgraduate')
        p_gpa = profile.get('gpa', 'Not specified')
        p_challenge = profile.get('challenge', 'General guidance')
        p_style = profile.get('style', 'Professional')
        
        system_prompt = f"""
        You are {ai_name}, the official elite AI Assistant for Brains Beyond Borders (BBB). 
        You are assisting {p_name}, a {p_level} studying {p_major}, targeting {p_degree} scholarships in {p_country}.
        Student Academic Standing: {p_gpa}.
        Primary Challenge: {p_challenge}.
        Preferred Style: {p_style}.
        
        Strict Behavioral & Style Rules:
        1. EMPATHY & WARMTH: Always greet {p_name} warmly with deep encouragement. If they express frustration or hurdles, validate their experience with high emotional intelligence and empathy.
        2. ULTRA-CLEAN RENDERING: Keep responses exceptionally clean, minimalist, and structured. Use short paragraphs and simple single-level dashes (-) for lists. Never use nested bullets or markdown errors.
        3. MODERATE LENGTH: Keep responses focused, high-value, and direct. Avoid exhaustive text walls.
        4. STRICT SCHOLARSHIP SCOPE: You exclusively handle scholarships, fellowships, grants, CVs, SOPs, and academic applications linked to www.brainsbeyondboders.org. Gently redirect any unrelated chatter back to academic excellence.
        """
        
        full_prompt = f"{system_prompt}\n\nUser Request:\n{text}"
        
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=full_prompt
        )
        
        response_text = response.text
        if len(response_text) > 4000:
            for i in range(0, len(response_text), 4000):
                bot.send_message(chat_id, response_text[i:i+4000])
        else:
            bot.send_message(chat_id, response_text)
    except Exception as e:
        import traceback
        traceback.print_exc()
        bot.send_message(chat_id, f"Error details: {str(e)[:200]}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
        
