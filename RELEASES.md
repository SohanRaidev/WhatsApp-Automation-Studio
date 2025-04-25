# Download and Installation Guide

## Download Options

### For macOS Users
1. Download the latest release: [WhatsApp-Automation-Studio.dmg](https://github.com/SohanRaidev/WhatsApp-Automation-Studio/releases/latest/download/WhatsApp-Automation-Studio.dmg)
2. Open the DMG file
3. Drag the WhatsApp Automation Studio app to your Applications folder
4. Right-click on the app and select "Open" (required the first time to bypass macOS security)

### For Windows Users
1. Download the latest release: [WhatsApp Automation Studio.exe](https://github.com/SohanRaidev/WhatsApp-Automation-Studio/releases/latest/download/WhatsApp%20Automation%20Studio.exe)
2. Run the executable
3. If Windows SmartScreen appears, click "More info" and then "Run anyway"

## Running from Source

If you prefer to run the application from source:

```bash
# Clone the repository
git clone https://github.com/SohanRaidev/WhatsApp-Automation-Studio.git

# Navigate to the project directory
cd WhatsApp-Automation-Studio

# Install dependencies
pip install -r requirements.txt

# Run the application
python whatsapp_msg_automation.py
```

## Troubleshooting

### Common Issues

#### macOS: "App is damaged and can't be opened"
Solution: Open Terminal and run:
```bash
xattr -cr /Applications/WhatsApp\ Automation\ Studio.app
```

#### Windows: Missing DLL files
Solution: Make sure you have the latest Microsoft Visual C++ Redistributable installed.

## Support

If you encounter any issues, please [create an issue](https://github.com/SohanRaidev/WhatsApp-Automation-Studio/issues/new) on GitHub.