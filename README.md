# Rec Room Revivals Launcher 🎮

Hey everyone! I built this launcher because I wanted an easy-to-use tool that can support multiple Rec Room revivals/builds, rather than having to launch independent `.bat` files or rely on different launchers for different revivals. 

Honestly, I just wanted a clean, central place to manage all my builds and jump straight into the game quickly.

## What it does
- **Multiple Profiles:** Add as many custom revival builds as you want, name them whatever you like, and switch between them instantly.
- **One-Click Launching:** Two big, clear buttons to launch your selected build in either **VR** or **Screen** mode (it automatically handles the `+forcemode` launch arguments for you).
- **Modern & Clean UI:** Built with CustomTkinter for a sleek dark-mode interface, complete with smooth fade-in animations and custom icons.
- **Simple Setup:** If it's your first time, the app guides you step-by-step to add your first revival so you aren't left staring at a blank screen.

## How to get it running 
*(You can ignore these steps if using the executable!)*

### 1. Install Python
If you don't have it already, grab Python from [python.org](https://www.python.org/). 
*(Important: Make sure to check the box that says **"Add Python to PATH"** during installation!)*

### 2. Install the required libraries
Open your command prompt or terminal and run this command to install the UI framework and image handler:
```bash
pip install customtkinter Pillow
```

### 3. Run the launcher
Just double-click `RevLauncher.py`, or run it from your terminal:
```bash
python RevLa.py
```
*(Note: The first time you run it, the app will automatically download the button and window icons from the internet and save them locally, so it works perfectly offline after that!)*

## How to use it
1. When you first open it, you'll see a welcome screen. Click **"Add Your First Revival"**.
2. Type in a custom name for your build (e.g., "Vanilla", "Radium", etc.).
3. Click **Browse** next to that new profile and find your revival's `.exe` file.
4. Close the settings window. You'll now see the main launcher screen!
5. Pick your revival from the dropdown at the top, and hit either **Start In VR** or **Start In Screen**.

## Troubleshooting
- **"No valid executable selected"**: You just need to set the path to your `.exe` file. Click "Manage Revivals" and hit "Browse".
- **Game doesn't launch**: Double-check that the `.exe` path is correct.
- **Icons aren't showing up**: Your firewall or antivirus might be blocking the script from downloading the images on the first run. The app will still work perfectly, it will just fall back to text-only buttons.

## Credits
Made by me, for the community. Built with Python, CustomTkinter, and Pillow. 

Have fun playing! 🥽🖥️
