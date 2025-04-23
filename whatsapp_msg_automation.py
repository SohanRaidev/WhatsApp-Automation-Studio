#!/usr/bin/env python3
"""
WhatsApp Message Automation Tool
Advanced version with multiple features for automating WhatsApp Web messaging
"""

import time
import random
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

class WhatsAppAutomation:
    def __init__(self):
        self.driver = None
        self.wait_time = 30  # Default wait time in seconds
        self.delay_between_msgs = 1  # Default delay between messages
        self.current_contact = None
        self.messages = []
        self.should_randomize = False
    
    def initialize_driver(self):
        """Initialize the Chrome WebDriver with custom options"""
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        # Uncomment to run in headless mode (no GUI)
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-notifications")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
    def start(self):
        """Start the WhatsApp Web session and wait for login"""
        if not self.driver:
            self.initialize_driver()
        
        self.driver.get("https://web.whatsapp.com/")
        print("\n" + "="*50)
        print("Please scan the QR code to log in to WhatsApp Web")
        print("="*50)
        
        # Wait for the user to scan the QR code and load WhatsApp Web
        try:
            # Wait until the search box appears, indicating successful login
            WebDriverWait(self.driver, self.wait_time * 2).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true" and @data-tab="3"]'))
            )
            print("Login successful!")
            return True
        except TimeoutException:
            print("Timeout while waiting for login. Please try again.")
            return False
    
    def wait_for_manual_chat_selection(self):
        """Wait for user to manually select a chat and confirm it"""
        print("\n" + "="*50)
        print("MANUAL CHAT SELECTION MODE")
        print("="*50)
        print("Please manually click on the chat/group you want to message.")
        print("Take your time to find the right chat.")
        
        ready = input("\nPress Enter when you've selected the chat...")
        
        try:
            # Try to detect the currently selected chat
            chat_title = WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-testid="conversation-header-content"]//span'))
            ).text
            
            print(f"\nSelected chat: {chat_title}")
            
            # Send a confirmation message that this is the targeted chat
            confirm = input("\nIs this the correct chat to message? (y/n): ").lower()
            if confirm == 'y' or confirm == 'yes':
                self.current_contact = chat_title
                
                # Send a test message if requested
                test_msg = input("\nSend a test message to confirm? (y/n): ").lower()
                if test_msg == 'y' or test_msg == 'yes':
                    test_content = input("Enter test message: ")
                    if test_content.strip():
                        self.send_message(test_content)
                        print("Test message sent.")
                    else:
                        print("Test message was empty. No message sent.")
                
                return True
            else:
                print("Please select another chat.")
                return False
        except Exception as e:
            print(f"Error detecting chat: {str(e)}")
            return False
    
    def send_message(self, message):
        """Send a single message to the current chat"""
        try:
            # Find message input box and send message
            message_box = WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'))
            )
            message_box.clear()
            message_box.click()
            
            # For multi-line messages, handle each line
            for line in message.split('\n'):
                message_box.send_keys(line)
                message_box.send_keys(Keys.SHIFT + Keys.ENTER)
            
            # Remove the last newline and send the message
            message_box.send_keys(Keys.BACKSPACE)
            
            # Click send button
            send_button = WebDriverWait(self.driver, self.wait_time).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="send"]'))
            )
            send_button.click()
            return True
        except Exception as e:
            print(f"Error sending message: {str(e)}")
            return False
    
    def send_bulk_messages(self):
        """Send all messages to the current chat"""
        if not self.current_contact or not self.messages:
            print("Please select a chat and add messages first.")
            return
        
        print(f"\nSending {len(self.messages)} messages to {self.current_contact}")
        success_count = 0
        
        messages_to_send = self.messages.copy()
        if self.should_randomize:
            random.shuffle(messages_to_send)
        
        for i, msg in enumerate(messages_to_send):
            print(f"Sending message {i+1}/{len(messages_to_send)}...", end="", flush=True)
            if self.send_message(msg):
                success_count += 1
                print(" ✓")
            else:
                print(" ✗")
                
            # Wait between messages
            if i < len(messages_to_send) - 1:  # Don't wait after the last message
                time.sleep(self.delay_between_msgs)
        
        print(f"\nSuccessfully sent {success_count} out of {len(messages_to_send)} messages.")
    
    def send_repeated_message(self, message, repeat_count):
        """Send the same message multiple times"""
        if not self.current_contact:
            print("Please select a chat first.")
            return
        
        print(f"\nSending message '{message[:20]}...' {repeat_count} times to {self.current_contact}")
        success_count = 0
        
        for i in range(repeat_count):
            print(f"Sending repetition {i+1}/{repeat_count}...", end="", flush=True)
            if self.send_message(message):
                success_count += 1
                print(" ✓")
            else:
                print(" ✗")
                
            # Wait between messages
            if i < repeat_count - 1:  # Don't wait after the last message
                time.sleep(self.delay_between_msgs)
        
        print(f"\nSuccessfully sent {success_count} out of {repeat_count} messages.")
    
    def add_message(self, message):
        """Add a message to the list"""
        self.messages.append(message)
        print(f"Added message: '{message[:30]}...' ({len(message)} chars)")
    
    def clear_messages(self):
        """Clear all messages"""
        self.messages = []
        print("All messages cleared.")
    
    def set_delay(self, delay_seconds):
        """Set the delay between messages"""
        try:
            delay = float(delay_seconds)
            if delay < 0:
                print("Delay must be a positive number.")
                return
            self.delay_between_msgs = delay
            print(f"Message delay set to {delay} seconds.")
        except ValueError:
            print("Invalid delay value. Please enter a number.")
    
    def toggle_randomize(self):
        """Toggle whether to randomize messages"""
        self.should_randomize = not self.should_randomize
        status = "ON" if self.should_randomize else "OFF"
        print(f"Message randomization is now {status}")
    
    def load_messages_from_file(self, filename):
        """Load messages from a text file (one message per line)"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
            # Group lines together if they're part of a multi-line message
            # (Empty lines separate different messages)
            messages = []
            current_message = ""
            
            for line in lines:
                if line.strip() == "":
                    if current_message:
                        messages.append(current_message)
                        current_message = ""
                else:
                    current_message += line.rstrip() + "\n"
            
            # Add the last message if any
            if current_message:
                messages.append(current_message.rstrip())
            
            # Add loaded messages to the list
            self.messages.extend(messages)
            print(f"Loaded {len(messages)} messages from {filename}")
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"Error loading messages from file: {str(e)}")
    
    def close(self):
        """Close the browser and clean up"""
        if self.driver:
            self.driver.quit()
            print("Browser closed.")


def display_banner():
    """Display a fancy banner for the application"""
    banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║   ██╗    ██╗██╗  ██╗ █████╗ ████████╗███████╗ █████╗ ║
    ║   ██║    ██║██║  ██║██╔══██╗╚══██╔══╝██╔════╝██╔══██╗║
    ║   ██║ █╗ ██║███████║███████║   ██║   ███████╗███████║║
    ║   ██║███╗██║██╔══██║██╔══██║   ██║   ╚════██║██╔══██║║
    ║   ╚███╔███╔╝██║  ██║██║  ██║   ██║   ███████║██║  ██║║
    ║    ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝║
    ║                                                       ║
    ║   ███╗   ███╗███████╗ ██████╗  █████╗                ║
    ║   ████╗ ████║██╔════╝██╔════╝ ██╔══██╗               ║
    ║   ██╔████╔██║███████╗██║  ███╗███████║               ║
    ║   ██║╚██╔╝██║╚════██║██║   ██║██╔══██║               ║
    ║   ██║ ╚═╝ ██║███████║╚██████╔╝██║  ██║               ║
    ║   ╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝               ║
    ║                                                       ║
    ║   ██████╗  ██████╗ ███╗   ███╗██████╗ ███████╗██████╗║
    ║   ██╔══██╗██╔═══██╗████╗ ████║██╔══██╗██╔════╝██╔══██║║
    ║   ██████╔╝██║   ██║██╔████╔██║██████╔╝█████╗  ██████╔╝║
    ║   ██╔══██╗██║   ██║██║╚██╔╝██║██╔══██╗██╔══╝  ██╔══██╗║
    ║   ██████╔╝╚██████╔╝██║ ╚═╝ ██║██████╔╝███████╗██║  ██║║
    ║   ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """
    print(banner)
    print("\nAdvanced WhatsApp Message Automation Tool")
    print("-------------------------------------------")


def display_menu():
    """Display the main menu options"""
    print("\nMAIN MENU:")
    print("1. Start WhatsApp Web and scan QR")
    print("2. Select chat manually")
    print("3. Manage messages")
    print("4. Send messages")
    print("5. Configure settings")
    print("6. Exit")
    return input("\nSelect an option (1-6): ")


def message_menu(whatsapp):
    """Submenu for message management"""
    while True:
        print("\nMESSAGE MENU:")
        print("1. Add a single message")
        print("2. Add multiple messages (interactive)")
        print("3. Load messages from file")
        print("4. View current messages")
        print("5. Clear all messages")
        print("6. Back to main menu")
        
        choice = input("\nSelect an option (1-6): ")
        
        if choice == "1":
            msg = input("Enter your message (press Enter twice when done):\n")
            whatsapp.add_message(msg)
        
        elif choice == "2":
            print("Enter messages (one per line, enter a blank line when finished):")
            messages = []
            while True:
                line = input()
                if not line:
                    break
                messages.append(line)
            
            if messages:
                for msg in messages:
                    whatsapp.add_message(msg)
        
        elif choice == "3":
            filename = input("Enter the path to the message file: ")
            whatsapp.load_messages_from_file(filename)
        
        elif choice == "4":
            if not whatsapp.messages:
                print("No messages added yet.")
            else:
                print("\nCurrent messages:")
                for i, msg in enumerate(whatsapp.messages):
                    print(f"[{i+1}] {msg[:50]}{'...' if len(msg) > 50 else ''}")
        
        elif choice == "5":
            whatsapp.clear_messages()
        
        elif choice == "6":
            break
        
        else:
            print("Invalid option. Please try again.")


def send_menu(whatsapp):
    """Submenu for sending messages"""
    while True:
        print("\nSEND MENU:")
        print("1. Send all configured messages")
        print("2. Send a single message multiple times")
        print("3. Back to main menu")
        
        choice = input("\nSelect an option (1-3): ")
        
        if choice == "1":
            if not whatsapp.current_contact:
                print("Error: No chat selected. Please select a chat first (option 2 in main menu).")
            elif not whatsapp.messages:
                print("Error: No messages added. Please add messages first (option 3 in main menu).")
            else:
                whatsapp.send_bulk_messages()
        
        elif choice == "2":
            if not whatsapp.current_contact:
                print("Error: No chat selected. Please select a chat first (option 2 in main menu).")
            else:
                message = input("Enter the message to repeat: ")
                try:
                    repeat_count = int(input("How many times do you want to send this message? "))
                    if repeat_count > 0:
                        whatsapp.send_repeated_message(message, repeat_count)
                    else:
                        print("Please enter a positive number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        
        elif choice == "3":
            break
        
        else:
            print("Invalid option. Please try again.")


def settings_menu(whatsapp):
    """Submenu for configuring settings"""
    while True:
        print("\nSETTINGS MENU:")
        print(f"1. Set delay between messages (current: {whatsapp.delay_between_msgs}s)")
        print(f"2. Toggle message randomization (current: {'ON' if whatsapp.should_randomize else 'OFF'})")
        print("3. Back to main menu")
        
        choice = input("\nSelect an option (1-3): ")
        
        if choice == "1":
            delay = input("Enter delay between messages (seconds): ")
            whatsapp.set_delay(delay)
        
        elif choice == "2":
            whatsapp.toggle_randomize()
        
        elif choice == "3":
            break
        
        else:
            print("Invalid option. Please try again.")


def main():
    """Main function to run the WhatsApp automation tool"""
    display_banner()
    
    whatsapp = WhatsAppAutomation()
    logged_in = False
    chat_selected = False
    
    try:
        while True:
            choice = display_menu()
            
            if choice == "1":
                logged_in = whatsapp.start()
                if not logged_in:
                    print("\nFailed to log in to WhatsApp Web. Please try again.")
            
            elif choice == "2":
                if not logged_in:
                    print("\nPlease log in to WhatsApp Web first (option 1).")
                else:
                    chat_selected = whatsapp.wait_for_manual_chat_selection()
                    if chat_selected:
                        print("\nChat selection confirmed!")
                    else:
                        print("\nChat selection was not confirmed. Please try again.")
            
            elif choice == "3":
                message_menu(whatsapp)
            
            elif choice == "4":
                if not logged_in:
                    print("\nPlease log in to WhatsApp Web first (option 1).")
                elif not chat_selected:
                    print("\nPlease select a chat first (option 2).")
                else:
                    send_menu(whatsapp)
            
            elif choice == "5":
                settings_menu(whatsapp)
            
            elif choice == "6":
                print("\nExiting WhatsApp Message Automation Tool...")
                whatsapp.close()
                break
            
            else:
                print("Invalid option. Please try again.")
                
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Cleaning up...")
    finally:
        if whatsapp.driver:
            whatsapp.close()
        print("Thank you for using WhatsApp Message Automation Tool!")


if __name__ == "__main__":
    main()

