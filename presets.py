# presets.py
"""
Module to manage message presets for WhatsApp Automation Studio.
"""
import json
import os

# Default preset definitions
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
        "message": "ㅤ" "HELP ME",
        "description": "Set repeat message to 200 times to prank someone"
    },
    {
        "name": "My Love(toggle random in settings to send them in random order.)",
        "messages": [
            "I love you ❤️",
            "I miss you so much 💔",
            "You're my everything 🌍",
            "Can't wait to see you again 😍",
            "Thinking of you 💭",
            "Miss you baby 👶",
            "ILY 💕",
            "IMU 💓",
            "Baby how are you? 🤗",
            "Hope your day is going well! 🌞"
            "LOVE YOU SO MUCH! 💖",
        ],
        "description": "Various love messages sent one after another. toggle randomize to send them in random order."
    },
    {
        "name": "Fancy Love",
        "messages": [
            "✨💖 𝓘 𝓛𝓸𝓿𝓮 𝓨𝓸𝓾 𝓢𝓸 𝓜𝓾𝓬𝓱! 💖✨",
            "❣️ 𝒴𝑜𝓊 𝒶𝓇𝑒 𝓉𝒽𝑒 𝓁𝑜𝓋𝑒 𝑜𝒻 𝓂𝓎 𝓁𝒾𝒻𝑒 ❣️",
            "💕 ℬ𝓎 𝓎𝑜𝓊𝓇 𝓈𝒾𝒹𝑒 𝒾𝓈 𝓌𝒽𝑒𝓇𝑒 𝐼 𝒷𝑒𝓁𝑜𝓃𝑔 💕",
            "✨ 𝓨𝓸𝓾'𝓻𝓮 𝓶𝔂 𝓯𝓪𝓿𝓸𝓻𝓲𝓽𝓮 𝓹𝓮𝓻𝓼𝓸𝓷 ✨",
            "💫 𝕀 𝕒𝕕𝕠𝕣𝕖 𝕪𝕠𝕦 💫"
        ],
        "description": "Fancy stylized love messages"
    },
    {
        "name": "Good Morning Messages",
        "messages": [
            "Good morning sunshine! ☀️",
            "Rise and shine! Hope you have an amazing day! 🌞",
            "Morning! Sending you positive vibes for the day ahead! ✨",
            "Wakey wakey! Time to start a beautiful day! 🌅",
            "Good morning! I was thinking about you as soon as I woke up! 💭"
        ],
        "description": "Morning greeting messages"
    },
    {
        "name": "Good Night Messages",
        "messages": [
            "Good night! Sweet dreams! 🌙✨",
            "Sleep tight, don't let the bed bugs bite! 😴",
            "Nighty night! See you in my dreams! 💫",
            "Rest well my love! Tomorrow is a new day! 🌃",
            "Good night! Can't wait for tomorrow! 😊"
        ],
        "description": "Night greeting messages"
    },
    {
        "name": "Love Poetry",
        "messages": [
            "Roses are red,\nViolets are blue,\nSugar is sweet,\nAnd so are you! ❤️",
            "Every time I see you,\nMy heart skips a beat,\nYou make me feel complete,\nMy love so sweet. 💕",
            "Like stars in the night,\nYour love shines so bright,\nIn darkness you guide me,\nMy perfect delight. ✨",
            "My love for you grows,\nWith each passing day,\nIn my heart you'll stay,\nForever and always. 🌹"
        ],
        "description": "Romantic poetry messages"
    },
    {
        "name": "Miss You Messages",
        "messages": [
            "I miss your touch, your smile, and everything about you. Can't wait to hold you in my arms again! 💕",
            "Missing you is my heart's full-time job 💔",
            "The hardest part of my day is not being with you 😢",
            "Distance means so little when someone means so much. I miss you! 🌍",
            "Every song I hear reminds me of you. Missing you terribly! 🎵"
        ],
        "description": "Messages expressing longing"
    },
    {
        "name": "Forever Yours",
        "messages": [
            "Forever and always, my heart belongs to you. You're the love of my life. ❤️",
            "No matter where life takes us, my love for you will never fade. Forever yours. 💕",
            "My heart is yours, today, tomorrow, and for all eternity. 💞",
            "I am yours and you are mine, now until the end of time. 🔒",
            "In this lifetime and the next, I will always choose you. ✨"
        ],
        "description": "Commitment messages"
    },
    {
        "name": "Flirty Messages",
        "messages": [
            "You must be a magician, because every time I look at you, everyone else disappears! ✨",
            "Is your name Google? Because you've got everything I'm searching for! 🔍",
            "Are you made of copper and tellurium? Because you're Cu-Te! 😉",
            "If you were a vegetable, you'd be a cute-cumber! 🥒",
            "Do you have a map? Because I keep getting lost in your eyes! 🗺️"
        ],
        "description": "Playful flirty messages"
    },
    {
        "name": "Emoji Bombs",
        "messages": [
            "😂",
            "❤️",
            "😘",
            "🥰",
            "💕",
            "😎",
            "🤩",
            "😜",
            "🔥",
            "🙈",
            "🎉",
            "✨",
            "😈",
            "🤯",
            "🤪",
            "💯",
            "💓",
            "💥",
            "👻",
            "💃",
            "🕺",
            "🍀",
            "🤟",
            "👀",
            "💦",
            "🌈",
            "💫",
            "🦄",
            "👾",
            "🎊"
        ],
        "description": "Various emoji spam messages"
    },
    {
        "name": "Appreciation Messages",
        "messages": [
            "Thank you for always being there for me. You mean the world to me. 🌍",
            "I appreciate everything you do. You're amazing! ✨",
            "Your kindness never goes unnoticed. Thank you for being you! 💝",
            "You make my life so much better just by being in it. Grateful for you! 🙏",
            "Words cannot express how thankful I am to have you in my life. 💖"
        ],
        "description": "Messages expressing gratitude"
    },
   
    {
        "name": "Massive Pickup Lines",
        "messages": [
            "Are you a parking ticket? Because you’ve got FINE written all over you.",
            "Do you believe in love at first sight, or should I walk by again?",
            "If you were a Transformer, you’d be Optimus Fine.",
            "My phone has a problem—it doesn’t have your number in it.",
            "Trust me, I’m not drunk; I’m just intoxicated by you.",
            "Are you French? Because Eiffel for you.",
            "I must be in a museum, because you truly are a work of art.",
            "If I could rearrange the alphabet, I’d put U and I together.",
            "Do you have a sunburn, or are you always this hot?",
            "You stole my heart, but I’ll let you keep it."
        ],
        "description": "A jumbo set of cheesy pickup lines."
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