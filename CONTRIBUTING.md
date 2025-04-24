# Contributing to WhatsApp Automation Studio

First of all, thank you for considering contributing to WhatsApp Automation Studio! 🎉

This document provides guidelines and steps for contributing to this project. By participating in this project, you agree to abide by its terms and the [Code of Conduct](#code-of-conduct).

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Adding Presets](#adding-presets)
  - [Code Contributions](#code-contributions)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [License Considerations](#license-considerations)

## 🤝 Code of Conduct

This project follows a Code of Conduct that all contributors are expected to adhere to. Please read [the full text](CODE_OF_CONDUCT.md) to understand what actions will and will not be tolerated.

In short:
- Use welcoming and inclusive language
- Be respectful of different viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other community members

## 🚀 How Can I Contribute?

### Reporting Bugs

Before submitting a bug report:
1. Check the [issue tracker](https://github.com/yourusername/WhatsApp-Messages-Automation/issues) to see if the problem has already been reported
2. If not, create a new issue with:
   - A clear, descriptive title
   - A detailed description of the issue
   - Steps to reproduce the behavior
   - Expected vs actual behavior
   - Screenshots if applicable
   - System information (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are always welcome! Please include:
- A clear and descriptive title
- A detailed description of the proposed feature
- Explanation of why this enhancement would be useful
- Possible implementation approach (if you have ideas)
- Mockups/examples if applicable

### Adding Presets

One of the easiest ways to contribute is by adding useful message presets:

1. Fork and clone the repository
2. Add your presets to `presets.py` in the appropriate format:
   ```python
   {
       "name": "Your Preset Name",
       "messages": [
           "Message 1",
           "Message 2",
           # More messages...
       ],
       "description": "Description of your preset"
   }
   ```
3. For single-message presets:
   ```python
   {
       "name": "Your Single Message Preset",
       "message": "Your message here",
       "description": "Description of your preset"
   }
   ```
4. Submit a pull request with your additions

### Code Contributions

Code contributions are highly appreciated! Here's how to contribute code:

1. Fork the repository
2. Create a branch for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
   or
   ```bash
   git checkout -b fix/issue-you-are-fixing
   ```
3. Make your changes following our [Style Guidelines](#style-guidelines)
4. Test your changes thoroughly
5. Submit a pull request

## 💻 Development Setup

To set up the development environment:

1. Clone your fork of the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/WhatsApp-Messages-Automation.git
   cd WhatsApp-Messages-Automation
   ```

2. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application in development mode:
   ```bash
   python whatsapp_msg_automation.py
   ```

## 📝 Pull Request Process

1. Update the README.md if needed with details of changes to the interface
2. Update documentation as needed
3. The PR should work on Python 3.8 and above
4. Ensure your PR does not break any existing functionality
5. Your PR needs to be reviewed and approved by a maintainer before merging

## 🎨 Style Guidelines

### Python Code Style

- Follow [PEP 8](https://pep8.org/) coding standards
- Use 4 spaces for indentation (not tabs)
- Keep line length under 100 characters
- Write meaningful docstrings for classes and functions
- Use descriptive variable names

### Commit Messages

- Start with a short summary line (50 chars or less)
- Optionally followed by a blank line and a more detailed explanation
- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Reference issue numbers at the end of the summary line when applicable

Example:
```
Add Spanish language preset collection (#42)

This adds a collection of common Spanish phrases and greetings
that can be used for Spanish-speaking contacts.
```

## 📄 License Considerations

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License](LICENSE).

By contributing to this project, you agree that your contributions will be licensed under this license. Please ensure that any third-party code you contribute is compatible with this license.

---

Thank you for contributing to WhatsApp Automation Studio! ❤️
