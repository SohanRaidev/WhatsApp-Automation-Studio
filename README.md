# WhatsApp Messages Automation

## Overview

The **WhatsApp Messages Automation** project automates the process of sending and managing WhatsApp messages using Selenium WebDriver. This tool is designed to handle repetitive messaging tasks.

## Key Features:
+ **Automated Messaging: Send personalized or pre-defined 
  messages to multiple contacts or groups automatically.

+ **Message Templates: Use customizable templates to streamline 
  the messaging process for frequent or repetitive messages.

+ **Error Handling: Includes mechanisms to handle errors ensuring 
  reliability and stability.

+ **User-Friendly Configuration.

## Technologies Used:
+ **Selenium Chrome webdriver: For interaction with browser and whatsapp web.
+ **Python: For scripting and automation.
---

# Installation

1. Clone the repository: ``` git clone https://github.com/SohanRaidev/WhatsApp-Messages-Automation ```

2. Navigate to the project directory: ` cd Whatsapp-Messages-Automation `

3. Install the required dependencies: ``` pip install -r requirements.txt ```

4. Adjust the script parameters as needed: Refer USAGE section below.

5. Run the script: ``` python whatsapp_msg_automation.py ```

# Usage

1. #### Customize: > Modify the script to use message templates or handle specific automation needs.

    = **Initially when running the code is configured to message a bunch of invisible character to the selected person or a group. 
       
    = **You can customize the script to send your own messages by modifying the `sentences` list. For example: ` sentences = [ "Hi", "Hello", "Your'e Amazing", "WOW Nice Code"]  ` 
    
    = **` sentences = [ "Hi", "Hello", "Your'e Amazing", "WOW Nice Code"]  ` : In this example, the script will send 4 messages. You can increase or decrease the number of messages by adding or removing items in the sentences list. 
    
    = ** You can further add a time delay after each message sent by uncommenting the time.sleep in line 35 of the code. **

2. ####  Run the script: ` python whatsapp_msg_automation.py `

3. #### When the script opens WhatsApp Web, you have 30 seconds to scan the QR code from your mobile device and select the chat or group. If your internet is slow or login is taking time, you can increase the 30-second timer in line 15 of the script.

4. #### Boom! leave the rest on the script.

---

# Contribution.

### Contributions to enhance functionality, add new features, or fix bugs are welcome! Please follow the contribution guidelines:

1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch). 
3. Make your changes.
4. Commit your changes (git commit -am 'Add new feature'). 
5. Push to the branch (git push origin feature-branch).
6. Create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
   
