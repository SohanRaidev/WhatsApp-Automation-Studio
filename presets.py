# presets.py
"""
Module to manage message presets for WhatsApp Automation Studio.
"""
import json
import os

# Default preset definitions - expanded with many more messages per category
DEFAULT_PRESETS = [
    {
        "name": "Invisible Bomb (200 chars)",
        "message": "ㅤ" * 200,
        "description": "Send invisible characters to create a 'bomb' effect"
    },
    {
        "name": "Invisible Character(prank)",
        "message": "ㅤ",
        "description": "Set repeat message to 200 times to prank someone"
    },
    {
        "name": "Help prank (toggle random)",
        "messages": ["ㅤ",
                 "HELP ME",
                 "ㅤ",
                 "ㅤ"
                 ],  # Added missing comma here
        "description": "Set repeat message to 200 times to prank someone"
    },
    {
        "name": "Simple Love Messages",
        "messages": [
            "I love you",
            "I miss you so much",
            "You're my everything",
            "Can't wait to see you again",
            "Thinking of you",
            "Miss you baby",
            "ILY",
            "IMU",
            "Baby how are you?",
            "Hope your day is going well!",
            "LOVE YOU SO MUCH!",
            "You mean the world to me",
            "Counting the minutes until I see you again",
            "Just thinking about you makes me smile",
            "You're the best thing that ever happened to me",
            "My day is brighter with you in it",
            "Can't stop thinking about you today",
            "You're always on my mind",
            "Forever yours",
            "I'm so lucky to have you in my life",
            "My heart belongs to you",
            "No one compares to you",
            "You're my favorite person",
            "My love grows stronger every day",
            "I cherish every moment with you",
            "You complete me",
            "Life is better with you in it",
            "I adore you",
            "You're my sunshine on cloudy days",
            "I'm yours forever",
            "Our love story is my favorite",
            "You make my heart skip a beat",
            "I'm so thankful for you",
            "No one understands me like you do",
            "You're the love of my life",
            "I fall more in love with you each day",
            "You're my person",
            "I'm crazy about you",
            "You're my dream come true",
            "Being with you feels like home"
        ],
        "description": "Expanded collection of simple love messages - text only"
    },
    {
        "name": "Good Morning Messages",
        "messages": [
            "Good morning sunshine!",
            "Rise and shine! Hope you have an amazing day!",
            "Morning! Sending you positive vibes for the day ahead!",
            "Wakey wakey! Time to start a beautiful day!",
            "Good morning! I was thinking about you as soon as I woke up!",
            "Morning has broken! Have a wonderful day!",
            "Good morning! Hoping your day is as wonderful as you are!",
            "First thing I thought about today was you. Good morning!",
            "Each morning brings new hope. Have a great day!",
            "Hello sunshine! Hope your day is fantastic!",
            "Morning greetings! May today bring you success and happiness!",
            "A new day has begun. Make it amazing!",
            "Wishing you a refreshing morning and a fantastic day ahead!",
            "Hope your morning is as bright as your smile!",
            "Good morning! Remember that today is a fresh start!",
            "Sending morning wishes your way!",
            "Greeting you with a bright good morning!",
            "Morning glory! Wishing you a day full of pleasant surprises!",
            "Top of the morning to you! Have a great day!",
            "Good morning! I hope your coffee is strong and your Monday is short!",
            "May this morning offer you new strength and fresh purpose!",
            "Morning bells are ringing! Time to start another beautiful day!",
            "Good morning! Today is a new beginning, seize the day!",
            "Wake up and be awesome today! Good morning!",
            "A wonderful morning to the most wonderful person I know!",
            "Morning has arrived! Shine like the star you are!",
            "Wishing you a morning filled with peace and harmony!",
            "Morning! May your day be filled with happy moments!",
            "Start your day with a smile! Good morning!",
            "Good morning! Let your light shine today!"
        ],
        "description": "Expanded morning greeting messages - simple text"
    },
    {
        "name": "Good Night Messages",
        "messages": [
            "Good night! Sweet dreams!",
            "Sleep tight, don't let the bed bugs bite!",
            "Nighty night! See you in my dreams!",
            "Rest well my love! Tomorrow is a new day!",
            "Good night! Can't wait for tomorrow!",
            "Wishing you a peaceful sleep and wonderful dreams!",
            "Good night! Hope you sleep like a baby!",
            "Night night! Rest up for another amazing day tomorrow!",
            "Sweet dreams are coming your way! Good night!",
            "As this day ends, know that I'm thinking of you. Good night!",
            "May your sleep be deep and your dreams be sweet. Good night!",
            "Time to rest your mind and body. Good night!",
            "Stars are shining for you tonight. Sleep well!",
            "Good night! Tomorrow is waiting with new opportunities!",
            "Sending you sleepy vibes and night time wishes!",
            "May your night be filled with tranquility. Good night!",
            "The day is done, it's time for dreams. Good night!",
            "Counting stars and thinking of you. Good night!",
            "Dream big and sleep tight! Good night!",
            "Wishing you a night of peaceful slumber!",
            "Good night! May your sleep restore and rejuvenate you!",
            "Time to cuddle up and drift off to dreamland. Good night!",
            "Rest well tonight, for tomorrow brings new adventures!",
            "Another day done, time for some rest. Good night!",
            "Sending you nighttime serenity and peaceful thoughts!",
            "May the night bring you comfort and relaxation. Sleep well!",
            "Lights out! Time for sweet dreams and peaceful sleep!",
            "Goodnight! May angels watch over your sleep tonight!",
            "Rest your head and close your eyes. Sweet dreams!",
            "Drift off to dreamland and wake up refreshed. Good night!"
        ],
        "description": "Expanded night greeting messages - simple text"
    },
    {
        "name": "Love Poetry",
        "messages": [
            "Roses are red,\nViolets are blue,\nSugar is sweet,\nAnd so are you!",
            "Every time I see you,\nMy heart skips a beat,\nYou make me feel complete,\nMy love so sweet.",
            "Like stars in the night,\nYour love shines so bright,\nIn darkness you guide me,\nMy perfect delight.",
            "My love for you grows,\nWith each passing day,\nIn my heart you'll stay,\nForever and always.",
            "When I look into your eyes,\nTime seems to stand still,\nYou're my greatest thrill,\nAnd you always will be.",
            "Your smile lights up my world,\nYour laugh brings me joy,\nLove without alloy,\nPure and untold.",
            "Words cannot express,\nThe depth of my love,\nSent from above,\nA heavenly caress.",
            "In your arms I find,\nPeace beyond measure,\nMy greatest treasure,\nSoul, heart and mind.",
            "Your love is the anchor,\nThat keeps me steady,\nAlways ready,\nTo weather any storm together.",
            "Like rivers to oceans,\nMy thoughts flow to you,\nConstant and true,\nEndless devotions.",
            "When we're apart,\nI count every minute,\nLife without limit,\nWhen you're in my heart.",
            "Morning sun rises,\nReminding me of you,\nLove ever new,\nFull of surprises.",
            "Moonlight on water,\nReflects how I feel,\nThis love is real,\nAnd growing stronger.",
            "With every heartbeat,\nI whisper your name,\nLove's gentle flame,\nTimeless and sweet.",
            "Through valleys and mountains,\nOur love will endure,\nSteadfast and pure,\nLike magical fountains."
        ],
        "description": "Expanded romantic poetry messages - simple text format"
    },
    {
        "name": "Miss You Messages",
        "messages": [
            "I miss your touch, your smile, and everything about you. Can't wait to hold you in my arms again!",
            "Missing you is my heart's full-time job",
            "The hardest part of my day is not being with you",
            "Distance means so little when someone means so much. I miss you!",
            "Every song I hear reminds me of you. Missing you terribly!",
            "I miss you more than words can express",
            "The world seems empty without you here",
            "Counting down the days until I see you again",
            "Missing you is like missing a piece of myself",
            "There's a you-shaped hole in my daily routine",
            "I keep looking at your photo and wishing you were here",
            "The distance between us only makes my heart grow fonder",
            "I think about you constantly. Miss you so much!",
            "They say absence makes the heart grow fonder, and it's so true. I miss you!",
            "Nothing feels right when you're not here",
            "I miss our conversations, our laughs, our moments together",
            "The house feels so quiet without your presence",
            "I miss your voice most of all",
            "I find myself talking about you all the time because I miss you so much",
            "I miss your hugs more than anything",
            "Each day without you feels like a year",
            "I miss seeing your face and hearing your laugh",
            "I miss your presence in my everyday life",
            "The world is less colorful when you're not around",
            "I miss our inside jokes and special moments",
            "I miss the comfort of having you near",
            "Time moves so slowly when we're apart",
            "I miss your energy and everything you bring to my life",
            "The distance between us feels unbearable some days",
            "I miss making memories with you"
        ],
        "description": "Expanded messages expressing longing - simple text only"
    },
    {
        "name": "Forever Yours",
        "messages": [
            "Forever and always, my heart belongs to you. You're the love of my life.",
            "No matter where life takes us, my love for you will never fade. Forever yours.",
            "My heart is yours, today, tomorrow, and for all eternity.",
            "I am yours and you are mine, now until the end of time.",
            "In this lifetime and the next, I will always choose you.",
            "My commitment to you is unwavering, now and forever.",
            "You're the one I want to build my life with, today and always.",
            "I promise to stand by your side through all of life's journeys.",
            "My love for you is eternal, unchanging through all seasons.",
            "I give you my heart completely, now and forevermore.",
            "You are my forever person, the one I choose every day.",
            "My dedication to you will never waver, that's my solemn promise.",
            "In your love I've found my home, my place, my forever.",
            "I vow to love you through all of life's ups and downs.",
            "Our love story is my favorite, and I'll be writing it with you forever.",
            "I commit myself to you entirely, in all ways and always.",
            "Every day I choose you, and I will continue choosing you forever.",
            "I pledge my heart to you for all my days to come.",
            "You are my constant in this ever-changing world.",
            "My loyalty and love are yours completely.",
            "I promise to walk beside you for all the days of my life.",
            "My devotion to you is endless and unchanging.",
            "You've captured my heart, and I never want it back.",
            "I give you my today, my tomorrow, my always.",
            "Our love is timeless, boundless, and forever.",
            "I'm yours completely, utterly, and eternally.",
            "My commitment to our love grows stronger with each passing day.",
            "I promise to choose you, again and again, without pause, without doubt.",
            "You have my unwavering devotion, now and always.",
            "I'm yours in every sense of the word, forever and completely."
        ],
        "description": "Expanded commitment messages - simple text"
    },
    {
        "name": "Flirty Messages",
        "messages": [
            "You must be a magician, because every time I look at you, everyone else disappears!",
            "Is your name Google? Because you've got everything I'm searching for!",
            "Are you made of copper and tellurium? Because you're Cu-Te!",
            "If you were a vegetable, you'd be a cute-cumber!",
            "Do you have a map? Because I keep getting lost in your eyes!",
            "I must be a snowflake, because I've fallen for you.",
            "Are you a bank loan? Because you have my interest!",
            "Do you have a name, or can I call you mine?",
            "I'm not a photographer, but I can picture us together.",
            "Are you a campfire? Because you're hot and I want s'more.",
            "If you were words on a page, you'd be fine print.",
            "Are you from Tennessee? Because you're the only ten I see!",
            "I must be in a museum, because you're a work of art.",
            "Do you drink coffee? Because I like you a latte.",
            "Is your name Wifi? Because I'm feeling a strong connection.",
            "If you were a fruit, you'd be a fine-apple.",
            "Do you have a Band-Aid? Because I just scraped my knee falling for you.",
            "I think there's something wrong with my phone. Your number's not in it.",
            "Is it hot in here, or is it just you?",
            "You must be a broom, because you've swept me off my feet.",
            "Are you a time traveler? Because I see you in my future.",
            "If you were a triangle, you'd be acute one.",
            "You and I are like nachos with cheese. You're super cheesy, but I like it!",
            "Is your name Ariel? Because we mermaid for each other.",
            "Do you like raisins? How do you feel about a date?",
            "If you were a vegetable, you'd be a sweet potato.",
            "You know what you'd look great in? My arms.",
            "Are you a parking ticket? Because you've got FINE written all over you.",
            "I'm not a mathematician, but I think we add up nicely.",
            "Do you believe in love at first sight, or should I walk by again?"
        ],
        "description": "Expanded flirty messages - simple text only"
    },
    {
        "name": "Appreciation Messages",
        "messages": [
            "Thank you for always being there for me. You mean the world to me.",
            "I appreciate everything you do. You're amazing!",
            "Your kindness never goes unnoticed. Thank you for being you!",
            "You make my life so much better just by being in it. Grateful for you!",
            "Words cannot express how thankful I am to have you in my life.",
            "I just wanted to let you know how much I appreciate your help.",
            "Your support means everything to me. Thank you so much!",
            "I value our friendship more than you know. Thank you for being such a great friend.",
            "Your generosity and kindness are truly inspiring.",
            "I'm so grateful for your guidance and wisdom.",
            "Thank you for always listening when I need someone to talk to.",
            "I appreciate your honesty and the way you always keep it real with me.",
            "You've made such a positive impact on my life. I'm truly grateful.",
            "Your encouragement keeps me going when times are tough.",
            "I appreciate the way you always make time for me.",
            "Thank you for believing in me even when I don't believe in myself.",
            "Your patience and understanding mean so much to me.",
            "I'm grateful for all the little things you do that often go unnoticed.",
            "Thank you for being my rock and my constant support.",
            "I appreciate your positive attitude and the way you lift others up.",
            "You've helped me more than you know. Thank you from the bottom of my heart.",
            "I value your perspective and insights. Thank you for sharing them with me.",
            "Your thoughtfulness never ceases to amaze me. Thank you.",
            "I appreciate the way you challenge me to be better.",
            "Thank you for standing by me through thick and thin.",
            "I'm grateful for your unwavering loyalty and trust.",
            "You've taught me so much. I can't thank you enough.",
            "I appreciate your sense of humor and how you always make me laugh.",
            "Thank you for accepting me exactly as I am.",
            "You're a blessing in my life. I appreciate you more than words can say."
        ],
        "description": "Expanded messages expressing gratitude - simple text only"
    },
   
    {
        "name": "Pickup Lines",
        "messages": [
            "Are you a parking ticket? Because you've got FINE written all over you.",
            "Do you believe in love at first sight, or should I walk by again?",
            "If you were a Transformer, you'd be Optimus Fine.",
            "My phone has a problem—it doesn't have your number in it.",
            "Trust me, I'm not drunk; I'm just intoxicated by you.",
            "Are you French? Because Eiffel for you.",
            "I must be in a museum, because you truly are a work of art.",
            "If I could rearrange the alphabet, I'd put U and I together.",
            "Do you have a sunburn, or are you always this hot?",
            "You stole my heart, but I'll let you keep it.",
            "Is your name Google? Because you have everything I've been searching for.",
            "Are you a magician? Every time I look at you, everyone else disappears.",
            "Do you have a map? I keep getting lost in your eyes.",
            "Are you made of copper and tellurium? Because you're Cu-Te.",
            "Is your dad a boxer? Because you're a knockout!",
            "I'm not a photographer, but I can picture us together.",
            "Are you a bank loan? Because you have my interest!",
            "If you were a vegetable, you'd be a cute-cumber!",
            "Do you have a name, or can I call you mine?",
            "Is your name Wifi? Because I'm feeling a strong connection.",
            "I'd say God bless you, but it looks like he already did.",
            "Are you a campfire? Because you're hot and I want s'more.",
            "If you were words on a page, you'd be fine print.",
            "I'm not a mathematician, but I'm pretty good with numbers. Tell you what, give me yours and watch what I can do with it.",
            "Are you related to Jean-Claude Van Damme? Because Jean-Claude Van Damme you're sexy!",
            "Excuse me, but I think I dropped something. My jaw!",
            "Is your dad an alien? Because there's nothing else like you on Earth!",
            "I was wondering if you had an extra heart, because mine seems to have been stolen.",
            "I'm learning about important dates in history. Wanna be one of them?",
            "Feel my shirt. Know what it's made of? Boyfriend material.",
            "Do you like raisins? How do you feel about a date?",
            "I was blinded by your beauty; I'm going to need your name and phone number for insurance purposes.",
            "If you were a fruit, you'd be a fine-apple.",
            "I'm sorry, but you owe me a drink. Because when I looked at you, I dropped mine.",
            "Can I follow you home? Cause my parents always told me to follow my dreams.",
            "Are you from Tennessee? Because you're the only ten I see!",
            "Do you have a Band-Aid? I just scraped my knee falling for you.",
            "I'm no mathematician, but I'm pretty good with numbers. Tell you what, give me yours and watch what I can do with it.",
            "I bet you're tired because you've been running through my mind all day.",
            "I'm new in town. Could you give me directions to your heart?"
        ],
        "description": "Expanded set of cheesy pickup lines - simple text only"
    }
]

# Preset save location
DEFAULT_PRESETS_PATH = os.path.expanduser("~/whatsapp_automation_presets.json")

class PresetManager:
    def __init__(self, presets=None):
        self.presets_path = DEFAULT_PRESETS_PATH
        
        if presets is not None:
            self.presets = presets
        else:
            self.presets = []
            self.load_presets_from_file()
            
            # If no presets were loaded, use the defaults
            if not self.presets:
                self.presets = DEFAULT_PRESETS.copy()
                self.save_presets_to_file()

    def get_presets(self):
        """Return the list of presets."""
        return self.presets

    def get_preset(self, index):
        """Get a specific preset by index."""
        if 0 <= index < len(self.presets):
            return self.presets[index]
        return None
        
    def get_preset_by_name(self, name):
        """Get a preset by name."""
        for preset in self.presets:
            if preset["name"] == name:
                return preset
        return None

    def add_preset(self, name, message, description="User-created preset"):
        """Add a new preset."""
        # Check if the message is a list
        if isinstance(message, list):
            self.presets.append({
                "name": name,
                "messages": message,
                "description": description
            })
        else:
            self.presets.append({
                "name": name,
                "message": message,
                "description": description
            })
        self.save_presets_to_file()
        return True

    def update_preset(self, index, name, message, description="User-created preset"):
        """Update an existing preset."""
        if 0 <= index < len(self.presets):
            # Check if the message is a list
            if isinstance(message, list):
                self.presets[index] = {
                    "name": name,
                    "messages": message,
                    "description": description
                }
            else:
                self.presets[index] = {
                    "name": name,
                    "message": message,
                    "description": description
                }
            self.save_presets_to_file()
            return True
        return False

    def delete_preset(self, index):
        """Delete a preset by index."""
        if 0 <= index < len(self.presets):
            del self.presets[index]
            self.save_presets_to_file()
            return True
        return False
        
    def load_presets_from_file(self):
        """Load presets from JSON file."""
        try:
            if os.path.exists(self.presets_path):
                with open(self.presets_path, 'r', encoding='utf-8') as f:
                    self.presets = json.load(f)
                return True
        except Exception as e:
            print(f"Error loading presets: {e}")
        return False
        
    def save_presets_to_file(self):
        """Save presets to JSON file."""
        try:
            with open(self.presets_path, 'w', encoding='utf-8') as f:
                json.dump(self.presets, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving presets: {e}")
        return False
        
    def reset_to_defaults(self):
        """Reset presets to default values."""
        self.presets = DEFAULT_PRESETS.copy()
        self.save_presets_to_file()
        return True
        
    def get_messages_from_preset(self, preset_name_or_index):
        """
        Gets all messages from a preset, handling both single message 
        and multiple messages presets.
        
        Args:
            preset_name_or_index: Either the preset name (str) or index (int)
            
        Returns:
            List of messages
        """
        preset = None
        
        if isinstance(preset_name_or_index, int):
            preset = self.get_preset(preset_name_or_index)
        else:
            preset = self.get_preset_by_name(preset_name_or_index)
            
        if not preset:
            return []
            
        if "messages" in preset:
            return preset["messages"]
        elif "message" in preset:
            return [preset["message"]]
            
        return []