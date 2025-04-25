#!/usr/bin/env python3
"""
WhatsApp Messaging Automation - Beautiful PyQt Edition
A feature-rich desktop application for automating WhatsApp Web messaging
"""

import sys
import os
import time
import json
import random
import threading
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QTextEdit, QLineEdit, 
                            QSpinBox, QDoubleSpinBox, QCheckBox, QComboBox, QListWidget, QListWidgetItem,
                            QFileDialog, QMessageBox, QSplashScreen, QProgressBar, 
                            QScrollArea, QSlider, QGroupBox, QRadioButton, QToolButton,
                            QInputDialog, QStyledItemDelegate)
from PyQt5.QtGui import QIcon, QPixmap, QColor, QPalette, QFont, QMovie, QTextCursor, QKeySequence, QPen
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect, QSize, QUrl, QThread, pyqtSignal
from PyQt5.QtMultimedia import QSound

# Selenium imports for WhatsApp automation
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (TimeoutException, NoSuchElementException,
                                      ElementClickInterceptedException, StaleElementReferenceException)

from presets import PresetManager

# Application constants
APP_NAME = "WhatsApp Automation Studio"
APP_VERSION = "1.0.0"
DEFAULT_CONFIG_PATH = os.path.expanduser("~/whatsapp_automation_config.json")
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# Default configuration
DEFAULT_CONFIG = {
    "delay_min": 1.0,
    "delay_max": 3.0,
    "typing_simulation": True,
    "typing_speed": 0.01,
    "randomize_order": False,
    "sound_effects": True,
    "dark_mode": False,
    "first_run": True,
    "session_path": "whatsapp_session",
    "xpaths": {
        "message_box": '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div/p',
        "message_area_click": '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]',
        "send_button": '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[2]/button',
        "chat_title": '//div[@data-testid="conversation-header-content"]//span'
    }
}

# Color schemes
COLOR_SCHEMES = {
    "light": {
        "primary": "#25D366",       # WhatsApp green
        "secondary": "#DCF8C6",     # WhatsApp message bubble
        "background": "#F0F2F5",    # WhatsApp background
        "text": "#111B21",          # Dark text
        "accent": "#34B7F1",        # WhatsApp blue accent
        "success": "#25D366",       # Success green
        "warning": "#FFA000",       # Warning orange
        "error": "#F44336",         # Error red
        "info": "#2196F3"           # Info blue
    },
    "dark": {
        "primary": "#00A884",       # Darker WhatsApp green
        "secondary": "#2A2F32",     # Dark message bubble
        "background": "#111B21",    # Dark background
        "text": "#E9EDF0",          # Light text
        "accent": "#00BCD4",        # Cyan accent
        "success": "#4CAF50",       # Success green
        "warning": "#FFC107",       # Warning yellow
        "error": "#FF5252",         # Error red
        "info": "#03A9F4"           # Info light blue
    }
}

# Move the ConfigManager class definition above its usage
# Ensure the ConfigManager class is defined before initializing config_manager
class ConfigManager:
    """Configuration manager for saving/loading settings"""
    def __init__(self, config_path=DEFAULT_CONFIG_PATH):
        self.config_path = config_path
        self.config = DEFAULT_CONFIG.copy()
        self.load_config()

    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as file:
                    loaded_config = json.load(file)
                    # Update only existing keys
                    for key, value in loaded_config.items():
                        if key in self.config:
                            if isinstance(value, dict) and isinstance(self.config[key], dict):
                                self.config[key].update(value)
                            else:
                                self.config[key] = value
                return True
            except Exception as e:
                print(f"Error loading config: {e}")
        return False

    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as file:
                json.dump(self.config, file, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    def get(self, key):
        """Get configuration value"""
        if key in self.config:
            return self.config[key]
        return None

    def set(self, key, value):
        """Set configuration value"""
        self.config[key] = value
        return True

    def update(self, updates):
        """Update multiple configuration values"""
        self.config.update(updates)
        return True

# Ensure config_manager is initialized after the ConfigManager class definition
config_manager = ConfigManager()

# Update the play_button_click_sound function to dynamically check the sound_effects setting
# Ensure the sound_effects setting is respected immediately without requiring a restart
def play_button_click_sound():
    button_click_sound = os.path.join(ASSETS_DIR, "button-202966.wav")
    if config_manager.get("sound_effects"):
        QSound.play(button_click_sound)

# Modified BounceButton class - simplify or remove if causing issues
class BounceButton(QPushButton):
    """Button with bounce animation on click that preserves text"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Simply connect click event without animation that might distort layout
        self.clicked.connect(self.animate)
        
    def animate(self):
        """Simple animation that won't affect text display"""
        # Play the button click sound
        play_button_click_sound()
        # Just flash the background slightly
        original_style = self.styleSheet()
        self.setStyleSheet(original_style + "background-color: #128C7E;")
        QTimer.singleShot(100, lambda: self.setStyleSheet(original_style))

class SeparatorDelegate(QStyledItemDelegate):
    """Custom delegate to draw separators between list items"""
    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        
        # Draw a horizontal separator line at the bottom of each item
        painter.save()
        painter.setPen(QPen(QColor("#CCCCCC"), 1, Qt.SolidLine))
        painter.drawLine(
            option.rect.left() + 5, 
            option.rect.bottom(), 
            option.rect.right() - 5, 
            option.rect.bottom()
        )
        painter.restore()
        
    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        # Add a bit of extra height for the separator
        size.setHeight(size.height() + 2)
        return size

class Browser(QThread):
    """Thread for handling browser operations"""
    status_update = pyqtSignal(str, str)  # message, type (info, success, error, etc)
    qr_ready = pyqtSignal()
    logged_in = pyqtSignal(bool)
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.driver = None
        self.wait_time = 30
        self.stop_requested = False
        
    def initialize_driver(self, headless=False, session_path=None):
        """Initialize Selenium WebDriver for Chrome"""
        self.status_update.emit("Initializing browser...", "info")
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        
        if headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
        
        # Use session if available
        if session_path and os.path.exists(session_path):
            chrome_options.add_argument(f"user-data-dir={session_path}")
            self.status_update.emit(f"Using existing session: {session_path}", "info")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.status_update.emit("Browser initialized", "success")
            return True
        except Exception as e:
            self.status_update.emit(f"Browser initialization failed: {str(e)}", "error")
            return False
    
    def run(self):
        """Run browser thread: Login to WhatsApp Web"""
        session_path = self.config["session_path"]
        if not self.initialize_driver(False, session_path):
            return
        
        try:
            self.driver.get("https://web.whatsapp.com/")
            self.status_update.emit("Loading WhatsApp Web...", "info")
            self.qr_ready.emit()
            
            # Wait for login to complete by looking for the search box
            WebDriverWait(self.driver, self.wait_time * 2).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true" and @data-tab="3"]'))
            )
            self.status_update.emit("Successfully logged in!", "success")
            self.logged_in.emit(True)
        except TimeoutException:
            self.status_update.emit("Login timed out. Please try again.", "error")
            self.logged_in.emit(False)
        except Exception as e:
            self.status_update.emit(f"Error during login: {str(e)}", "error")
            self.logged_in.emit(False)

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            self.status_update.emit("Browser closed", "info")


class MessageSender(QThread):
    """Thread for sending messages"""
    status_update = pyqtSignal(str, str)  # message, type (info, success, error, etc)
    progress_update = pyqtSignal(int, int)  # current, total
    finished = pyqtSignal()
    
    def __init__(self, driver, messages, config, repeat_count=1):
        super().__init__()
        self.driver = driver
        self.messages = messages
        self.config = config
        self.stop_requested = False
        self.repeat_count = repeat_count  # How many times to send each message
        
    def run(self):
        """Run sender thread: Send all messages"""
        if not self.messages:
            self.status_update.emit("No messages to send", "warning")
            self.finished.emit()
            return
        
        total_count = len(self.messages) * self.repeat_count
        self.status_update.emit(f"Starting to send {total_count} messages...", "info")
        
        # Play start sound
        if self.config["sound_effects"]:
            try:
                start_sound = os.path.join(ASSETS_DIR, "start.wav")
                if os.path.exists(start_sound):
                    QSound.play(start_sound)
            except Exception:
                pass
        
        # Expand messages based on repeat count
        expanded_messages = []
        for message in self.messages:
            for _ in range(self.repeat_count):
                expanded_messages.append(message)
        
        # Randomize if requested
        if self.config["randomize_order"]:
            random.shuffle(expanded_messages)
            
        for i, message in enumerate(expanded_messages):
            if self.stop_requested:
                self.status_update.emit("Message sending stopped", "warning")
                break
                
            success = self.send_message(message)
            
            if success:
                self.status_update.emit(f"Sent message {i+1}/{total_count}", "success")
                # Play message sent sound
                if self.config["sound_effects"]:
                    try:
                        send_sound = os.path.join(ASSETS_DIR, "message_sent.wav")
                        if os.path.exists(send_sound):
                            QSound.play(send_sound)
                    except Exception:
                        pass
            else:
                self.status_update.emit(f"Failed to send message {i+1}", "error")
                # Play error sound
                if self.config["sound_effects"]:
                    try:
                        error_sound = os.path.join(ASSETS_DIR, "error.wav")
                        if os.path.exists(error_sound):
                            QSound.play(error_sound)
                    except Exception:
                        pass
                
            self.progress_update.emit(i+1, total_count)
            
            # Delay before next message
            if i < total_count - 1:
                delay = random.uniform(self.config["delay_min"], self.config["delay_max"])
                time.sleep(delay)
                
        # Play completion sound
        if self.config["sound_effects"] and not self.stop_requested:
            try:
                complete_sound = os.path.join(ASSETS_DIR, "complete.wav")
                if os.path.exists(complete_sound):
                    QSound.play(complete_sound)
            except Exception:
                pass
                
        self.finished.emit()

    def send_message(self, message):
        """Send a single message to the current chat"""
        if not message or not self.driver:
            return False
            
        try:
            # Find and click the message area
            message_area = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, self.config["xpaths"]["message_area_click"]))
            )
            message_area.click()
            
            # Find the text input element
            message_box = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, self.config["xpaths"]["message_box"]))
            )
            
            # Clear any existing text
            message_box.clear()
            
            # For multiline messages we need to handle differently
            lines = message.split("\n")
            
            # Type the message (with or without simulation)
            if self.config["typing_simulation"]:
                for i, line in enumerate(lines):
                    # Type character by character with random delays
                    for char in line:
                        message_box.send_keys(char)
                        # Random delay between keystrokes
                        delay = self.config["typing_speed"] * random.uniform(0.8, 1.2)
                        time.sleep(delay)
                    
                    # Add newline between lines (except last line)
                    if i < len(lines) - 1:
                        message_box.send_keys(Keys.SHIFT + Keys.ENTER)
            else:
                # For non-simulation, we still need to handle multiline
                for i, line in enumerate(lines):
                    message_box.send_keys(line)
                    if i < len(lines) - 1:
                        message_box.send_keys(Keys.SHIFT + Keys.ENTER)
                
            # Click send button
            send_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, self.config["xpaths"]["send_button"]))
            )
            send_button.click()
            
            # Short wait to ensure message is sent
            time.sleep(0.5)
            
            return True
        except Exception as e:
            self.status_update.emit(f"Error sending message: {str(e)}", "error")
            return False
            
    def stop(self):
        """Stop sending messages"""
        self.stop_requested = True
        self.status_update.emit("Stopping message sending...", "warning")


class SplashScreen(QSplashScreen):
    """Custom splash screen with logo"""
    def __init__(self):
        # Use logo.png instead of a colored background
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
        pixmap = QPixmap(logo_path)
        
        # If logo exists, use it and resize it to a smaller size
        if not pixmap.isNull():
            # Resize to a more reasonable size (300x200)
            pixmap = pixmap.scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            # Fallback to a smaller green background
            pixmap = QPixmap(300, 200)
            pixmap.fill(QColor("#25D366"))
            
        super().__init__(pixmap)
            
        # Create layout for fallback if needed
        if pixmap.isNull():
            layout = QVBoxLayout()
            layout.setContentsMargins(20, 20, 20, 20)
            
            # Add logo placeholder
            self.logo_label = QLabel()
            self.logo_label.setAlignment(Qt.AlignCenter)
            self.logo_label.setText("<h1>WhatsApp Automation</h1>")
            self.logo_label.setStyleSheet("QLabel { color: white; }")
            layout.addWidget(self.logo_label)
            
            # Set the layout to a widget
            self.widget = QWidget()
            self.widget.setLayout(layout)
        
        # Add progress bar at the bottom
        self.progress = QProgressBar(self)
        self.progress.setGeometry(10, pixmap.height() - 30, pixmap.width() - 20, 20)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet("""
            QProgressBar {
                border-radius: 5px;
                background-color: rgba(255, 255, 255, 0.5);
            }
            QProgressBar::chunk {
                background-color: white;
                border-radius: 5px;
            }
        """)
        
        # Add status label
        self.status_label = QLabel("Loading...", self)
        self.status_label.setGeometry(10, pixmap.height() - 50, pixmap.width() - 20, 20)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("QLabel { color: white; font-weight: bold; }")

    def update_progress(self, value, status_text=None):
        """Update progress bar value and optionally status text"""
        self.progress.setValue(value)
        if status_text:
            self.status_label.setText(status_text)
        self.repaint()  # Force repaint to show updates

    def mousePressEvent(self, event):
        """Override to prevent closing splash by clicking"""
        pass


class OnboardingScreen(QWidget):
    """First-time user onboarding tutorial"""
    finished = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Don't set this as an independent window - keep the parent relationship
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("OnboardingScreen { background-color: #25D366; }")
        
        # Set up as a proper dialog with a parent
        self.setWindowFlags(Qt.Dialog)
        self.setWindowModality(Qt.ApplicationModal)
        self.setMinimumSize(600, 400)
        
        self.current_step = 0
        self.steps = [
            {
                "title": "Welcome to WhatsApp Automation Studio!",
                "content": "This app helps you automate sending WhatsApp messages. Let's walk through the basics.",
                "image": None
            },
            {
                "title": "Step 1: Login to WhatsApp",
                "content": "First, you'll need to scan a QR code to login to WhatsApp Web.",
                "image": None
            },
            {
                "title": "Step 2: Prepare Your Messages",
                "content": "Type or import the messages you want to send. You can also save them as presets for later use.",
                "image": None
            },
            {
                "title": "Step 3: Configure Settings",
                "content": "Set delays between messages, enable typing simulation, and customize other options.",
                "image": None
            },
            {
                "title": "Step 4: Start Sending",
                "content": "Select a chat in the browser, then click 'Start' to begin sending your messages.",
                "image": None
            },
            {
                "title": "Ready to Begin!",
                "content": "You're all set! Remember to use this tool responsibly and follow WhatsApp's policies.",
                "image": None
            }
        ]
        
        # Create UI
        layout = QVBoxLayout()
        
        # Title
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white; margin-top: 40px;")
        layout.addWidget(self.title_label)
        
        # Content
        self.content_label = QLabel()
        self.content_label.setAlignment(Qt.AlignCenter)
        self.content_label.setWordWrap(True)
        self.content_label.setStyleSheet("font-size: 18px; color: white; margin: 20px;")
        layout.addWidget(self.content_label)
        
        # Image
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)
        layout.addStretch(1)
        
        # Navigation buttons
        btn_layout = QHBoxLayout()
        self.prev_btn = QPushButton("Previous")
        self.prev_btn.clicked.connect(self.prev_step)
        self.prev_btn.setEnabled(False)
        
        self.next_btn = QPushButton("Next")
        self.next_btn.clicked.connect(self.next_step)
        
        self.skip_btn = QPushButton("Skip Tutorial")
        self.skip_btn.clicked.connect(self.skip)
        
        btn_layout.addWidget(self.skip_btn)
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.prev_btn)
        btn_layout.addWidget(self.next_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        self.update_ui()
    
    def update_ui(self):
        """Update UI with current step content"""
        step = self.steps[self.current_step]
        
        # Animate content change
        self.title_label.setText(step["title"])
        self.content_label.setText(step["content"])
        
        if step["image"]:
            self.image_label.setPixmap(QPixmap(step["image"]))
        else:
            self.image_label.clear()
        
        # Update button states
        self.prev_btn.setEnabled(self.current_step > 0)
        if self.current_step == len(self.steps) - 1:
            self.next_btn.setText("Finish")
        else:
            self.next_btn.setText("Next")
    
    def next_step(self):
        """Go to next step or finish"""
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.update_ui()
        else:
            # Just emit the signal instead of closing directly
            self.finished.emit()
    
    def prev_step(self):
        """Go to previous step"""
        if self.current_step > 0:
            self.current_step -= 1
            self.update_ui()
    
    def skip(self):
        """Skip onboarding"""
        # Just emit the signal instead of closing directly
        self.finished.emit()


class LogView(QTextEdit):
    """Custom text edit for displaying colored logs"""
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setLineWrapMode(QTextEdit.WidgetWidth)
        self.setStyleSheet("QTextEdit { background-color: #F0F2F5; }")
        
    def append_log(self, text, level="info"):
        """Append colored log message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        color_map = {
            "info": "#2196F3",    # Blue
            "success": "#4CAF50", # Green
            "warning": "#FFC107", # Yellow
            "error": "#FF5252"    # Red
        }
        
        color = color_map.get(level, "#2196F3")
        
        # Format HTML with timestamp and colored text
        html = f'<p><span style="color: #666;">[{timestamp}]</span> <span style="color: {color};">{text}</span></p>'
        
        # Append HTML and scroll to bottom
        self.append(html)
        self.moveCursor(QTextCursor.End)


class MainWindow(QMainWindow):
    """Main application window"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setGeometry(100, 100, 1000, 700)
        
        # Initialize configuration
        self.config_manager = ConfigManager()
        self.config = self.config_manager.config
        
        # Initialize PresetManager
        self.preset_manager = PresetManager()
        
        # Initialize browser
        self.browser = None
        self.sender = None
        self.is_logged_in = False
        
        # Set application font
        font = QFont("Segoe UI", 10)  # More playful than default
        QApplication.setFont(font)
        
        # Setup UI
        self.setup_ui()
        self.setup_connections()
        self.apply_theme()
        
        # Load presets into combo box
        QTimer.singleShot(100, self.delayed_preset_loading)
        
        # Show onboarding for first-time users
        if self.config["first_run"]:
            QTimer.singleShot(500, self.show_onboarding)  # Show after a short delay

    def setup_ui(self):
        """Setup the application UI"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Toolbar
        toolbar_layout = QHBoxLayout()
        
        # Login button
        self.login_btn = QPushButton("Login to WhatsApp")
        self.login_btn.setIcon(QIcon.fromTheme("network-wired"))
        toolbar_layout.addWidget(self.login_btn)
        
        # Theme toggle
        self.theme_btn = QPushButton()
        self.theme_btn.setIcon(QIcon.fromTheme("preferences-desktop-theme"))
        self.theme_btn.setText("Toggle Theme")
        toolbar_layout.addWidget(self.theme_btn)
        
        # Status indicator
        self.status_indicator = QLabel("Status: Not logged in")
        toolbar_layout.addStretch(1)
        toolbar_layout.addWidget(self.status_indicator)
        
        main_layout.addLayout(toolbar_layout)
        
        # Tab widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Tab 1: Message Composer
        self.composer_tab = QWidget()
        self.setup_composer_tab()
        self.tabs.addTab(self.composer_tab, "Message Composer")
        
        # Tab 2: Settings
        self.settings_tab = QWidget()
        self.setup_settings_tab()
        self.tabs.addTab(self.settings_tab, "Settings")
        
        # Tab 3: Logs
        self.logs_tab = QWidget()
        self.setup_logs_tab()
        self.tabs.addTab(self.logs_tab, "Logs")
    
    def setup_composer_tab(self):
        """Setup the message composer tab"""
        layout = QVBoxLayout(self.composer_tab)
        
        # Messages grid
        message_layout = QHBoxLayout()
        
        # Left side: Message editor
        editor_layout = QVBoxLayout()
        editor_title = QLabel(" Message Editor")
        editor_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #25D366; margin: 5px;")
        editor_layout.addWidget(editor_title)
        
        self.message_editor = QTextEdit()
        self.message_editor.setPlaceholderText("Type your message here...")
        self.message_editor.setFont(QFont("Segoe UI", 12))
        self.message_editor.setMinimumHeight(150)
        editor_layout.addWidget(self.message_editor)
        
        # Message buttons
        btn_layout = QHBoxLayout()
        self.add_message_btn = BounceButton("Add Message")
        self.add_message_btn.setIcon(QIcon.fromTheme("list-add"))
        self.add_message_btn.setMinimumHeight(40)
        # Make the Add Message button stand out with a custom color
        self.add_message_btn.setStyleSheet("""
            QPushButton {
                background-color: #1E88E5;
                color: white;
                font-weight: bold;
                border-radius: 6px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.clear_editor_btn = BounceButton("Clear")
        self.clear_editor_btn.setIcon(QIcon.fromTheme("edit-clear"))
        self.clear_editor_btn.setMinimumHeight(40)
        btn_layout.addWidget(self.add_message_btn)
        btn_layout.addWidget(self.clear_editor_btn)
        editor_layout.addLayout(btn_layout)
        
        # Preview area
        preview_group = QGroupBox("👁️ Message Preview")
        preview_group.setFont(QFont("Segoe UI", 12, QFont.Bold))
        preview_layout = QVBoxLayout()
        self.message_preview = QTextEdit()
        self.message_preview.setReadOnly(True)
        self.message_preview.setPlaceholderText("Message preview will appear here...")
        self.message_preview.setFont(QFont("Segoe UI", 12))
        self.message_preview.setMinimumHeight(100)
        preview_layout.addWidget(self.message_preview)
        preview_group.setLayout(preview_layout)
        editor_layout.addWidget(preview_group)
        
        message_layout.addLayout(editor_layout, 2)
        
        # Right side: Message list
        list_layout = QVBoxLayout()
        list_title = QLabel("📝 Messages to Send")
        list_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #25D366; margin: 5px;")
        list_layout.addWidget(list_title)
        
        self.message_list = QListWidget()
        self.message_list.setFont(QFont("Segoe UI", 12))
        self.message_list.setMinimumHeight(200)
        self.message_list.setItemDelegate(SeparatorDelegate())  # Apply separator delegate
        list_layout.addWidget(self.message_list)
        
        # Message list buttons
        list_btn_layout = QHBoxLayout()
        self.remove_message_btn = BounceButton("Remove")
        self.remove_message_btn.setIcon(QIcon.fromTheme("list-remove"))
        self.remove_message_btn.setMinimumHeight(40)
        self.clear_all_btn = BounceButton("Clear All")
        self.clear_all_btn.setIcon(QIcon.fromTheme("edit-clear-all"))
        self.clear_all_btn.setMinimumHeight(40)
        list_btn_layout.addWidget(self.remove_message_btn)
        list_btn_layout.addWidget(self.clear_all_btn)
        list_layout.addLayout(list_btn_layout)
        
        # Repeat count for message
        repeat_layout = QHBoxLayout()
        repeat_label = QLabel("🔄 Repeat each message:")
        repeat_label.setStyleSheet("font-weight: bold;")
        repeat_layout.addWidget(repeat_label)
        self.repeat_count_spin = QSpinBox()
        self.repeat_count_spin.setRange(1, 1000)
        self.repeat_count_spin.setValue(1)
        self.repeat_count_spin.setMinimumHeight(30)
        self.repeat_count_spin.setMinimumWidth(80)
        repeat_layout.addWidget(self.repeat_count_spin)
        list_layout.addLayout(repeat_layout)
        
        # Presets
        preset_label = QLabel("✨ Message Presets")
        preset_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #25D366; margin-top: 10px;")
        list_layout.addWidget(preset_label)
        
        preset_layout = QHBoxLayout()
        
        # Create a new combo box with fixed styling to ensure it displays properly
        self.preset_combo = QComboBox()
        self.preset_combo.setFont(QFont("Segoe UI", 11))
        self.preset_combo.setMinimumHeight(40)
        self.preset_combo.setMinimumWidth(200)
        self.preset_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid gray;
                border-radius: 3px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left: 1px solid gray;
            }
        """)
        
        self.load_preset_btn = QPushButton("📥 Load Preset")
        self.load_preset_btn.setMinimumHeight(40)
        
        self.save_preset_btn = QPushButton("💾 Save Preset")
        self.save_preset_btn.setMinimumHeight(40)
        
        preset_layout.addWidget(self.preset_combo)
        preset_layout.addWidget(self.load_preset_btn)
        preset_layout.addWidget(self.save_preset_btn)
        list_layout.addLayout(preset_layout)
        
        message_layout.addLayout(list_layout, 1)
        layout.addLayout(message_layout)
        
        # Send controls
        send_group = QGroupBox("🚀 Send Controls")
        send_group.setFont(QFont("Segoe UI", 12, QFont.Bold))
        send_layout = QVBoxLayout(send_group)
        
        controls_layout = QHBoxLayout()
        
        # Delay settings
        delay_layout = QVBoxLayout()
        delay_label = QLabel("⏱ Delay between messages (seconds):")
        delay_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        delay_layout.addWidget(delay_label)
        
        delay_controls = QHBoxLayout()
        self.delay_min_spin = QDoubleSpinBox()
        self.delay_min_spin.setRange(0.1, 60.0)
        self.delay_min_spin.setValue(self.config["delay_min"])
        self.delay_min_spin.setSingleStep(0.1)
        self.delay_min_spin.setMinimumHeight(30)
        
        self.delay_max_spin = QDoubleSpinBox()
        self.delay_max_spin.setRange(0.1, 60.0)
        self.delay_max_spin.setValue(self.config["delay_max"])
        self.delay_max_spin.setSingleStep(0.1)
        self.delay_max_spin.setMinimumHeight(30)
        
        delay_controls.addWidget(QLabel("Min:"))
        delay_controls.addWidget(self.delay_min_spin)
        delay_controls.addWidget(QLabel("Max:"))
        delay_controls.addWidget(self.delay_max_spin)
        delay_layout.addLayout(delay_controls)
        
        controls_layout.addLayout(delay_layout)
        controls_layout.addStretch(1)
        
        # Start/stop buttons
        btn_layout = QVBoxLayout()
        
        # Clean Start button with text clearly visible
        self.start_btn = QPushButton("▶ Start Sending")
        self.start_btn.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #25D366;
                color: white;
                padding: 12px;
                border-radius: 10px;
                min-width: 180px;
                text-align: center;
            }
        """)
        self.start_btn.setMinimumHeight(50)
        
        # Clean Stop button with text clearly visible
        self.stop_btn = QPushButton("⏹  Stop")
        self.stop_btn.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF5252;
                color: white;
                padding: 12px;
                border-radius: 10px;
                min-width: 180px;
                text-align: center;
            }
        """)
        self.stop_btn.setMinimumHeight(50)
        self.stop_btn.setEnabled(False)
        
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        controls_layout.addLayout(btn_layout)
        
        send_layout.addLayout(controls_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%v/%m (%p%)")
        self.progress_bar.setMinimumHeight(25)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #25D366;
                border-radius: 8px;
                text-align: center;
                font-weight: bold;
                color: #000;
                background-color: #F0F2F5;
            }
            QProgressBar::chunk {
                background-color: #25D366;
                width: 10px;
                margin: 0.5px;
                border-radius: 5px;
            }
        """)
        send_layout.addWidget(self.progress_bar)
        
        layout.addWidget(send_group)

    def setup_settings_tab(self):
        """Setup the settings tab"""
        layout = QVBoxLayout(self.settings_tab)
        
        # General Settings
        general_group = QGroupBox("General Settings")
        general_group.setFont(QFont("Segoe UI", 12, QFont.Bold))
        general_layout = QVBoxLayout()
        
        # Dark Mode
        self.dark_mode_check = QCheckBox("🌙 Dark Mode")
        self.dark_mode_check.setChecked(self.config["dark_mode"])
        self.dark_mode_check.setFont(QFont("Segoe UI", 12))
        general_layout.addWidget(self.dark_mode_check)
        
        # Sound Effects
        self.sound_effects_check = QCheckBox("🔊 Sound Effects")
        self.sound_effects_check.setChecked(self.config["sound_effects"])
        self.sound_effects_check.setFont(QFont("Segoe UI", 12))
        general_layout.addWidget(self.sound_effects_check)
        
        general_group.setLayout(general_layout)
        layout.addWidget(general_group)
        
        # Message Settings
        message_group = QGroupBox("💬 Message Settings")
        message_group.setFont(QFont("Segoe UI", 12, QFont.Bold))
        message_layout = QVBoxLayout()
        
        # Typing Simulation
        self.typing_simulation_check = QCheckBox("Simulate Real Typing")
        self.typing_simulation_check.setChecked(self.config["typing_simulation"])
        self.typing_simulation_check.setFont(QFont("Segoe UI", 12))
        message_layout.addWidget(self.typing_simulation_check)
        
        # Typing Speed
        typing_speed_layout = QHBoxLayout()
        typing_speed_layout.addWidget(QLabel("🔤 Typing Speed:"))
        self.typing_speed_slider = QSlider(Qt.Horizontal)
        self.typing_speed_slider.setRange(1, 100)
        self.typing_speed_slider.setValue(int(self.config["typing_speed"] * 1000))
        typing_speed_layout.addWidget(self.typing_speed_slider)
        self.typing_speed_label = QLabel(f"{self.config['typing_speed']:.3f} sec/char")
        typing_speed_layout.addWidget(self.typing_speed_label)
        message_layout.addLayout(typing_speed_layout)
        
        # Randomize Order
        self.randomize_order_check = QCheckBox("🔀 Randomize Message Order")
        self.randomize_order_check.setChecked(self.config["randomize_order"])
        self.randomize_order_check.setFont(QFont("Segoe UI", 12))
        message_layout.addWidget(self.randomize_order_check)
        
        # Session Path - moved from Advanced to here
        session_layout = QHBoxLayout()
        session_layout.addWidget(QLabel("💾 Session Path:"))
        self.session_path_edit = QLineEdit(self.config["session_path"])
        session_layout.addWidget(self.session_path_edit)
        message_layout.addLayout(session_layout)
        
        message_group.setLayout(message_layout)
        layout.addWidget(message_group)
        
        layout.addStretch(1)
        
        # Save/Discard buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        self.settings_save_btn = BounceButton("💾 Save Settings")
        self.settings_save_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.settings_save_btn.setMinimumHeight(45)
        self.settings_save_btn.setStyleSheet("""
            QPushButton {
                background-color: #25D366;
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #128C7E;
            }
        """)
        btn_layout.addWidget(self.settings_save_btn)
        
        self.settings_discard_btn = BounceButton("❌ Discard Changes")
        self.settings_discard_btn.setFont(QFont("Segoe UI", 12))
        self.settings_discard_btn.setMinimumHeight(45)
        self.settings_discard_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF5252;
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        """)
        btn_layout.addWidget(self.settings_discard_btn)
        layout.addLayout(btn_layout)
    
    def setup_logs_tab(self):
        """Setup the logs tab"""
        layout = QVBoxLayout(self.logs_tab)
        
        # Log viewer
        self.log_view = LogView()
        layout.addWidget(self.log_view)
        
        # Controls
        controls_layout = QHBoxLayout()
        self.clear_logs_btn = QPushButton("Clear Logs")
        controls_layout.addWidget(self.clear_logs_btn)
        controls_layout.addStretch(1)
        self.export_logs_btn = QPushButton("Export Logs")
        controls_layout.addWidget(self.export_logs_btn)
        layout.addLayout(controls_layout)
        
        # Add initial log entry
        self.log("Welcome to WhatsApp Automation Studio!", "info")

    def setup_connections(self):
        """Connect signals to slots"""
        # Login
        self.login_btn.clicked.connect(self.login_to_whatsapp)
        
        # Theme toggle
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.dark_mode_check.toggled.connect(self.update_dark_mode)
        
        # Message editor
        self.message_editor.textChanged.connect(self.update_preview)
        self.add_message_btn.clicked.connect(self.add_message)
        self.clear_editor_btn.clicked.connect(self.clear_editor)
        
        # Message list
        self.remove_message_btn.clicked.connect(self.remove_message)
        self.clear_all_btn.clicked.connect(self.clear_messages)
        self.message_list.itemClicked.connect(self.preview_message)
        
        # Send controls
        self.start_btn.clicked.connect(lambda: (play_button_click_sound(), self.start_sending()))
        self.stop_btn.clicked.connect(lambda: (play_button_click_sound(), self.stop_sending()))
        
        # Settings
        self.typing_speed_slider.valueChanged.connect(self.update_typing_speed_label)
        self.settings_save_btn.clicked.connect(self.save_settings)
        self.settings_discard_btn.clicked.connect(self.discard_settings)
        
        # Log controls
        self.clear_logs_btn.clicked.connect(self.clear_logs)
        self.export_logs_btn.clicked.connect(self.export_logs)
        
        # Presets
        self.load_preset_btn.clicked.connect(self.load_selected_preset)
        self.save_preset_btn.clicked.connect(self.save_new_preset)
        
        # Connect the sound_effects_check toggle to apply the setting dynamically
        self.sound_effects_check.toggled.connect(lambda checked: config_manager.set("sound_effects", checked))

    def apply_theme(self):
        """Apply current theme (light/dark)"""
        scheme = COLOR_SCHEMES["dark" if self.config["dark_mode"] else "light"]
        
        # Apply palette colors
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(scheme["background"]))
        palette.setColor(QPalette.WindowText, QColor(scheme["text"]))
        palette.setColor(QPalette.Base, QColor(scheme["secondary"]))
        palette.setColor(QPalette.AlternateBase, QColor(scheme["background"]))
        palette.setColor(QPalette.Text, QColor(scheme["text"]))
        palette.setColor(QPalette.Button, QColor(scheme["secondary"]))
        palette.setColor(QPalette.ButtonText, QColor(scheme["text"]))
        palette.setColor(QPalette.Link, QColor(scheme["primary"]))
        palette.setColor(QPalette.Highlight, QColor(scheme["primary"]))
        palette.setColor(QPalette.HighlightedText, QColor(scheme["text"]))
        
        self.setPalette(palette)
        
        # Additional styling
        base_style = f"""
            QMainWindow, QWidget {{ background-color: {scheme["background"]}; color: {scheme["text"]}; }}
            QTabWidget::pane {{ border: 1px solid {scheme["secondary"]}; border-radius: 8px; }}
            QTabWidget::tab-bar {{ alignment: center; }}
            QTabBar::tab {{ background: {scheme["secondary"]}; color: {scheme["text"]}; padding: 10px 20px; margin: 2px; border-radius: 8px 8px 0 0; font-weight: bold; }}
            QTabBar::tab:selected {{ background: {scheme["primary"]}; color: white; }}
            QPushButton {{ background-color: {scheme["secondary"]}; color: {scheme["text"]}; padding: 8px; border-radius: 6px; }}
            QPushButton:hover {{ background-color: {scheme["primary"]}; color: white; }}
            QLineEdit, QTextEdit, QListWidget {{ background-color: {scheme["secondary"]}; color: {scheme["text"]}; padding: 8px; border-radius: 6px; }}
            QGroupBox {{ font-weight: bold; border: 2px solid {scheme["secondary"]}; border-radius: 8px; margin-top: 10px; padding-top: 15px; }}
            QGroupBox::title {{ subcontrol-origin: margin; subcontrol-position: top center; padding: 0 10px; }}
        """
        
        self.setStyleSheet(base_style)
        # Update the app icon to use the actual app logo
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")))

    def show_onboarding(self):
        self.onboarding = OnboardingScreen(self)
        self.onboarding.finished.connect(self.finish_onboarding)
        # Hide main window temporarily while showing the tutorial
        self.hide()
        # Make the onboarding screen modal so it must be interacted with
        self.onboarding.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint)
        self.onboarding.setWindowModality(Qt.ApplicationModal)
        self.onboarding.setMinimumSize(600, 400)  # Set a reasonable size
        self.onboarding.show()
    
    def finish_onboarding(self):
        """Complete onboarding process"""
        # Close onboarding window
        if hasattr(self, 'onboarding'):
            self.onboarding.close()
            self.onboarding = None
        
        # Update config
        self.config["first_run"] = False
        self.config_manager.save_config()
        
         # Make sure main window is visible again
        self.show()
        self.raise_() 
        self.activateWindow()
    
    def reset_and_show_tutorial(self):
        """Reset first_run flag and show tutorial again"""
        self.config["first_run"] = True
        self.config_manager.save_config()
        self.show_onboarding()
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        self.config["dark_mode"] = not self.config["dark_mode"]
        self.dark_mode_check.setChecked(self.config["dark_mode"])
        self.apply_theme()
    
    def update_dark_mode(self, checked):
        """Update dark mode from checkbox"""
        self.config["dark_mode"] = checked
        self.apply_theme()
    
    def update_preview(self):
        """Update message preview as user types"""
        text = self.message_editor.toPlainText()
        self.message_preview.setText(text)
    
    def add_message(self):
        """Add message from editor to list"""
        text = self.message_editor.toPlainText().strip()
        if not text:
            self.log("Cannot add empty message", "warning")
            return
        
        # Show full message in tooltip, truncate display text
        display_text = (text[:30] + "...") if len(text) > 30 else text
        display_text = display_text.replace("\n", "↵")  # Show newlines with symbol
        
        # Fixed to use QListWidgetItem directly instead of QListWidget.QListWidgetItem
        item = QListWidgetItem(display_text)
        item.setToolTip(text)
        item.setData(Qt.UserRole, text)  # Store full message
        self.message_list.addItem(item)
        
        self.log(f"Added message: '{text[:20]}...'", "success")
        
        # Play sound effect
        if self.config["sound_effects"]:
            # You could add sound effect here if you have sound files
            pass
    
    def clear_editor(self):
        """Clear message editor"""
        self.message_editor.clear()
        self.message_preview.clear()
    
    def remove_message(self):
        """Remove selected message from list"""
        selected_items = self.message_list.selectedItems()
        if not selected_items:
            self.log("No message selected to remove", "warning")
            return
        
        for item in selected_items:
            row = self.message_list.row(item)
            self.message_list.takeItem(row)
            self.log("Message removed", "info")
    
    def clear_messages(self):
        """Clear all messages from list"""
        if self.message_list.count() == 0:
            self.log("No messages to clear", "info")
            return
        
        reply = QMessageBox.question(self, "Clear Messages", 
                                    "Are you sure you want to clear all messages?",
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.message_list.clear()
            self.log("All messages cleared", "info")
    
    def preview_message(self, item):
        """Preview selected message from list"""
        self.message_preview.setText(item.text())
    
    def login_to_whatsapp(self):
        """Login to WhatsApp Web"""
        if self.browser and self.browser.isRunning():
            self.log("Browser already running", "warning")
            return
        
        self.log("Starting WhatsApp Web login...", "info")
        self.status_indicator.setText("Status: Connecting...")
        
        self.browser = Browser(self.config)
        self.browser.status_update.connect(self.log)
        self.browser.qr_ready.connect(self.qr_code_ready)
        self.browser.logged_in.connect(self.handle_login_result)
        self.browser.start()
    
    def qr_code_ready(self):
        """QR code is ready to be scanned"""
        self.log("Please scan the QR code with your phone", "info")
        self.status_indicator.setText("Status: Waiting for QR scan...")

    def handle_login_result(self, success):
        """Handle login result"""
        if success:
            self.is_logged_in = True
            self.status_indicator.setText("Status: Logged in")
            self.start_btn.setEnabled(True)
        else:
            self.is_logged_in = False
            self.status_indicator.setText("Status: Not logged in")
            self.start_btn.setEnabled(False)
    
    def start_sending(self):
        """Start sending messages"""
        if not self.is_logged_in or not self.browser or not self.browser.driver:
            self.log("You must be logged in to send messages", "error")
            return
        
        messages = []
        for i in range(self.message_list.count()):
            item = self.message_list.item(i)
            # Fix: Make sure we're getting the full message content stored in UserRole
            full_message = item.data(Qt.UserRole)
            messages.append(full_message)
            
        if not messages:
            self.log("No messages to send", "warning")
            return
        
        repeat_count = self.repeat_count_spin.value()
        self.log(f"Starting to send {len(messages)} unique messages (each repeated {repeat_count} times)...", "info")
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        
        self.sender = MessageSender(self.browser.driver, messages, self.config, repeat_count)
        self.sender.status_update.connect(self.log)
        self.sender.progress_update.connect(self.update_progress)
        self.sender.finished.connect(self.sending_finished)
        self.sender.start()
    
    def stop_sending(self):
        """Stop sending messages"""
        if self.sender and self.sender.isRunning():
            self.sender.stop()
            self.log("Sending operation stopping...", "warning")
        else:
            self.log("No sending operation in progress", "warning")
    
    def sending_finished(self):
        """Handle sending finished"""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.log("Sending operation completed", "success")
        
        # Play sound effect
        if self.config["sound_effects"]:
            # You can add sound effect here
            pass
    
    def update_progress(self, current, total):
        """Update progress bar"""
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
    
    def update_typing_speed_label(self, value):
        """Update typing speed label when slider changes"""
        speed = value / 1000.0
        self.typing_speed_label.setText(f"{speed:.3f} sec/char")
    
    def save_settings(self):
        """Save settings to config"""
        # General settings
        self.config["dark_mode"] = self.dark_mode_check.isChecked()
        self.config["sound_effects"] = self.sound_effects_check.isChecked()
        
        # Message settings
        self.config["typing_simulation"] = self.typing_simulation_check.isChecked()
        self.config["typing_speed"] = self.typing_speed_slider.value() / 1000.0
        self.config["randomize_order"] = self.randomize_order_check.isChecked()
        
        # Advanced settings
        self.config["session_path"] = self.session_path_edit.text()
        
        # Save to file
        if self.config_manager.save_config():
            self.log("Settings saved successfully", "success")
            # Apply theme
            self.apply_theme()
        else:
            self.log("Failed to save settings", "error")
    
    def discard_settings(self):
        """Discard settings changes"""
        # Reload from config
        self.dark_mode_check.setChecked(self.config["dark_mode"])
        self.sound_effects_check.setChecked(self.config["sound_effects"])
        self.typing_simulation_check.setChecked(self.config["typing_simulation"])
        self.typing_speed_slider.setValue(int(self.config["typing_speed"] * 1000))
        self.randomize_order_check.setChecked(self.config["randomize_order"])
        self.session_path_edit.setText(self.config["session_path"])
        
        self.log("Settings changes discarded", "info")
    
    def log(self, message, level="info"):
        """Add log message to log view"""
        self.log_view.append_log(message, level)
    
    def clear_logs(self):
        """Clear log view"""
        self.log_view.clear()
        self.log("Logs cleared", "info")
    
    def export_logs(self):
        """Export logs to a file"""
        filename, _ = QFileDialog.getSaveFileName(self, "Export Logs", "", "Text Files (*.txt);;All Files (*)")
        if filename:
            try:
                with open(filename, 'w') as file:
                    file.write(self.log_view.toPlainText())
                self.log(f"Logs exported to: {filename}", "success")
            except Exception as e:
                self.log(f"Failed to export logs: {str(e)}", "error")
    
    def load_presets(self):
        """Load presets into combo box."""
        self.preset_combo.clear()
        presets = self.preset_manager.get_presets()
        for preset in presets:
            self.preset_combo.addItem(preset["name"])
        self.log(f"Loaded {len(presets)} message presets", "info")
    
    def load_selected_preset(self):
        """Load the selected preset into the editor"""
        current_index = self.preset_combo.currentIndex()
        if current_index >= 0:
            preset_name = self.preset_combo.currentText()
            preset = self.preset_manager.get_preset_by_name(preset_name)
            
            if preset:
                # Clear the current message list
                self.message_list.clear()
                
                # Check if this is a multi-message preset
                if "messages" in preset:
                    messages = preset["messages"]
                    for msg in messages:
                        # Add each message to the message list as a separate item
                        display_text = (msg[:30] + "...") if len(msg) > 30 else msg
                        display_text = display_text.replace("\n", "↵")
                        
                        item = QListWidgetItem(display_text)
                        item.setToolTip(msg)
                        item.setData(Qt.UserRole, msg)  # Store the full message
                        self.message_list.addItem(item)
                        
                    # Show the first message in editor for preview
                    if messages:
                        self.message_editor.setText(messages[0])
                        self.message_preview.setText(messages[0])
                        
                    self.log(f"Loaded multi-message preset: {preset['name']} ({len(messages)} messages)", "success")
                else:
                    # Single message preset
                    message = preset["message"]
                    self.message_editor.setText(message)
                    self.message_preview.setText(message)
                    
                    # Also add to the message list for convenience
                    display_text = (message[:30] + "...") if len(message) > 30 else message
                    display_text = display_text.replace("\n", "↵")
                    
                    item = QListWidgetItem(display_text)
                    item.setToolTip(message)
                    item.setData(Qt.UserRole, message)
                    self.message_list.addItem(item)
                    
                    self.log(f"Loaded preset: {preset['name']}", "success")
                
                # Add bounce animation to the message preview
                current_geometry = self.message_preview.geometry()
                animation = QPropertyAnimation(self.message_preview, b"geometry")
                animation.setDuration(300)
                animation.setStartValue(QRect(current_geometry.x(), current_geometry.y() + 20, 
                                            current_geometry.width(), current_geometry.height()))
                animation.setEndValue(current_geometry)
                animation.setEasingCurve(QEasingCurve.OutBounce)
                animation.start()
    
    def save_new_preset(self):
        """Save current editor content as a new preset."""
        text = self.message_editor.toPlainText().strip()
        if not text:
            self.log("Cannot save empty message as preset", "warning")
            return

        name, ok = QInputDialog.getText(self, "Save Preset", "Enter a name for this preset:")
        if ok and name:
            self.preset_manager.add_preset(name, text)
            self.log(f"Saved new preset: {name}", "success")
            self.load_presets()
            self.config_manager.save_config()
    
    def delayed_preset_loading(self):
        """Load presets after a slight delay to ensure UI is fully initialized"""
        self.load_presets()
        self.log("Preset dropdown initialized", "info")
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Cleanup browser if still running
        if hasattr(self, 'browser') and self.browser and self.browser.isRunning():
            self.browser.close()
        
        # Save settings
        self.config_manager.save_config()
        event.accept()


def main():
    """Main function to run the application"""
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    
    # Set default font for entire app
    font = QFont("Segoe UI", 11)
    app.setFont(font)
    
    # Show splash screen
    splash = SplashScreen()
    splash.show()
    app.processEvents()  # Force processing to ensure splash shows immediately
    
    # Create main window but don't show yet
    window = MainWindow()
    
    # Faster loading with immediate processing
    for i in range(1, 101):
        time.sleep(0.002)  # Even shorter delay for faster startup
        splash.update_progress(i, f"Loading {i}%...")
        app.processEvents()  # Force processing events
    
    # Show main window and close splash
    window.show()
    splash.finish(window)
    
    sys.exit(app.exec_())

import sys
import traceback

# Add this at the very beginning of your file
def exception_hook(exctype, value, tb):
    print(''.join(traceback.format_exception(exctype, value, tb)))
    sys.__excepthook__(exctype, value, tb)
    sys.exit(1)

sys.excepthook = exception_hook

# Now add this to the end, just before if __name__ == '__main__':
try:
    if __name__ == '__main__':
        print('Starting application...')
        main()
except Exception as e:
    print(f'Error in application: {e}')
    traceback.print_exc()

