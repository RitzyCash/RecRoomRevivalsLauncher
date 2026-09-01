import customtkinter as ctk
from PIL import Image, ImageTk
import subprocess
import json
import os
import urllib.request
from tkinter import filedialog, messagebox

# Set the theme and appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GameLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Smaller, more rectangular window
        self.title("Revivals Launcher")
        self.geometry("500x420")
        self.minsize(450, 380)
        
        self.data_file = "profiles.json"
        self.profiles = self.load_profiles()
        
        # Ensure icons are downloaded locally
        self.ensure_icons()
        self.load_icons()

        # Build the UI dynamically based on whether profiles exist
        self.current_frame = None
        self.update_view()
        
        # Smooth fade-in animation on startup
        self.attributes('-alpha', 0.0)
        self.fade_in()

    def fade_in(self):
        """Creates a smooth fade-in animation when the app opens."""
        alpha = self.attributes('-alpha')
        if alpha < 1.0:
            alpha += 0.05
            self.attributes('-alpha', alpha)
            self.after(20, self.fade_in)

    def ensure_icons(self):
        """Downloads icons locally if they don't exist."""
        os.makedirs("icons", exist_ok=True)
        icons_to_fetch = {
            "vr": ("https://raw.githubusercontent.com/RitzyCash/RecRoomRevivalsLauncher/refs/heads/main/images/VR.png", "icons/vr.png"),
            "screen": ("https://raw.githubusercontent.com/RitzyCash/RecRoomRevivalsLauncher/refs/heads/main/images/ScreenMode.png", "icons/screen.png"),
            "logo": ("https://raw.githubusercontent.com/RitzyCash/RecRoomRevivalsLauncher/refs/heads/main/images/MainLogo.png", "icons/MainLogo.png")
        }
        for key, (url, path) in icons_to_fetch.items():
            if not os.path.exists(path):
                try:
                    urllib.request.urlretrieve(url, path)
                except Exception as e:
                    print(f"Warning: Could not download {key} icon. Falling back to text only. ({e})")

    def load_icons(self):
        """Loads the images into CTkImage objects and sets the window icon."""
        try:
            # 1. Window Bar / Taskbar Icon (using ImageTk for PNG support)
            logo_img = Image.open("icons/MainLogo.png")
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            self.iconphoto(True, self.logo_photo) # Sets the main app icon
            
            # 2. UI Display Logo (for the top of the screens)
            self.ui_logo = ctk.CTkImage(
                light_image=logo_img,
                dark_image=logo_img,
                size=(80, 80)
            )
            
            # 3. VR icon (forced black while preserving transparency)
            vr_img = Image.open("icons/vr.png").convert("RGBA")
            black_vr = Image.new("RGBA", vr_img.size, (0, 0, 0, 255))
            black_vr.putalpha(vr_img.getchannel("A"))
            self.vr_icon = ctk.CTkImage(
                light_image=black_vr, 
                dark_image=black_vr, 
                size=(36, 36)
            )
            
            # 4. Screen icon
            screen_img = Image.open("icons/screen.png").convert("RGBA")
            self.screen_icon = ctk.CTkImage(
                light_image=screen_img, 
                dark_image=screen_img, 
                size=(36, 36)
            )
        except Exception as e:
            print(f"Icon load error: {e}")
            self.ui_logo = None
            self.vr_icon = None
            self.screen_icon = None

    def load_profiles(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []

    def save_profiles(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.profiles, f, indent=4)

    def update_view(self):
        """Clears the window and builds the appropriate view."""
        if self.current_frame:
            self.current_frame.pack_forget()
            self.current_frame.destroy()
            
        if not self.profiles:
            self.current_frame = self.build_onboarding_ui()
        else:
            self.current_frame = self.build_main_ui()
            
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def build_onboarding_ui(self):
        """The friendly first-time setup screen."""
        frame = ctk.CTkFrame(self, fg_color="transparent")
        
        # App Logo at the top
        if self.ui_logo:
            ctk.CTkLabel(frame, image=self.ui_logo, text="").pack(pady=(20, 10))
        
        # Welcome Message
        title = ctk.CTkLabel(frame, text="Welcome to the Launcher! 🎮", font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=(0, 10))
        
        desc = ctk.CTkLabel(
            frame, 
            text="It looks like you haven't added any revivals yet.\nLet's get your first revival set up so you can jump right in!",
            font=ctk.CTkFont(size=15),
            text_color="gray",
            justify="center"
        )
        desc.pack(pady=(0, 30))

        # Steps
        steps = ctk.CTkLabel(
            frame,
            text="1. Click the button below\n2. Give your revival a custom name\n3. Select the revival's .exe file\n4. Start playing!",
            font=ctk.CTkFont(size=13),
            text_color="gray",
            justify="left"
        )
        steps.pack(pady=(0, 25))

        # Action Button
        add_btn = ctk.CTkButton(
            frame,
            text="✨ Add Your First Revival",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            width=220,
            corner_radius=10,
            command=self.open_manage_window
        )
        add_btn.pack()

        return frame

    def build_main_ui(self):
        """The main launcher screen."""
        frame = ctk.CTkFrame(self, fg_color="transparent")
        
        # App Logo at the top
        if self.ui_logo:
            ctk.CTkLabel(frame, image=self.ui_logo, text="").pack(pady=(10, 0))

        # Top Bar: Profile Selector + Settings
        top_bar = ctk.CTkFrame(frame, fg_color="transparent")
        top_bar.pack(fill="x", pady=(10, 10))

        self.profile_menu = ctk.CTkOptionMenu(
            top_bar, 
            values=[p['name'] for p in self.profiles],
            command=self.change_profile,
            width=240,
            font=ctk.CTkFont(size=14, weight="bold"),
            dropdown_font=ctk.CTkFont(size=13)
        )
        self.profile_menu.pack(side="left", padx=(0, 10))
        self.profile_menu.set(self.profiles[0]['name'])

        self.manage_btn = ctk.CTkButton(
            top_bar, 
            text="⚙️ Manage Revivals", 
            width=120,
            height=32,
            command=self.open_manage_window,
            fg_color="#2b2b2b",
            hover_color="#3d3d3d",
            font=ctk.CTkFont(size=13)
        )
        self.manage_btn.pack(side="left")

        # Pronounced Selected Revival Title
        self.selected_revival_label = ctk.CTkLabel(
            frame, 
            text=f"Launching: {self.profiles[0]['name']}", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FFFFFF"
        )
        self.selected_revival_label.pack(pady=(15, 20))

        # Launch Buttons Area
        btn_container = ctk.CTkFrame(frame, fg_color="transparent")
        btn_container.pack(fill="both", expand=True, pady=10)

        # VR Button (Smaller)
        self.vr_btn = ctk.CTkButton(
            btn_container,
            text="Start In VR",
            image=self.vr_icon,
            compound="left",
            font=ctk.CTkFont(size=18, weight="bold"),
            height=65,
            corner_radius=12,
            fg_color="#5e35b1",
            hover_color="#7e57c2",
            command=lambda: self.launch_game("vr")
        )
        self.vr_btn.pack(fill="x", pady=10, ipady=2)

        # Screen Button (Smaller)
        self.screen_btn = ctk.CTkButton(
            btn_container,
            text="Start In Screen",
            image=self.screen_icon,
            compound="left",
            font=ctk.CTkFont(size=18, weight="bold"),
            height=65,
            corner_radius=12,
            fg_color="#00897b",
            hover_color="#26a69a",
            command=lambda: self.launch_game("screen")
        )
        self.screen_btn.pack(fill="x", pady=10, ipady=2)

        # Status Label
        self.status_label = ctk.CTkLabel(frame, text="Ready to play!", text_color="gray", font=ctk.CTkFont(size=12))
        self.status_label.pack(side="bottom", pady=(0, 5))

        return frame

    def change_profile(self, choice):
        """Updates the pronounced title and status when a new profile is selected."""
        self.selected_revival_label.configure(text=f"Launching: {choice}")
        self.status_label.configure(text="Ready to play!", text_color="gray")

    def launch_game(self, mode):
        # Find current profile based on dropdown selection
        current_name = self.profile_menu.get()
        profile = next((p for p in self.profiles if p['name'] == current_name), None)
        
        if not profile or not profile['path'] or not os.path.exists(profile['path']):
            messagebox.showerror("Error", "No valid executable selected for this revival!\nClick 'Manage Revivals' to set it.")
            return

        command = [profile['path'], f"+forcemode:{mode}"]
        
        try:
            subprocess.Popen(command)
            mode_text = "VR" if mode == "vr" else "Screen"
            self.status_label.configure(text=f"🚀 Launched successfully in {mode_text} mode!", text_color="#4CAF50")
        except Exception as e:
            messagebox.showerror("Launch Failed", f"Could not start the game.\nError: {e}")

    def open_manage_window(self):
        manage_win = ctk.CTkToplevel(self)
        manage_win.title("Manage Revivals")
        manage_win.geometry("480x420")
        manage_win.transient(self)
        manage_win.grab_set()

        ctk.CTkLabel(manage_win, text="Revival Profiles", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=15)

        scroll_frame = ctk.CTkScrollableFrame(manage_win, width=430, height=250)
        scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        def refresh_list():
            for widget in scroll_frame.winfo_children():
                widget.destroy()
            
            if not self.profiles:
                ctk.CTkLabel(scroll_frame, text="No revivals added yet.", text_color="gray").pack(pady=20)
                return

            for i, profile in enumerate(self.profiles):
                row = ctk.CTkFrame(scroll_frame, fg_color="#2b2b2b", corner_radius=8)
                row.pack(fill="x", pady=6, padx=5)
                
                ctk.CTkLabel(row, text=profile['name'], width=160, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10, pady=8)
                
                path_text = profile['path'] if profile['path'] else "Not set"
                ctk.CTkLabel(row, text=path_text, width=130, anchor="w", text_color="gray", font=ctk.CTkFont(size=11)).pack(side="left", padx=5)

                def set_path(idx=i):
                    path = filedialog.askopenfilename(title="Select Revival Executable", filetypes=[("Executables", "*.exe"), ("All Files", "*.*")])
                    if path:
                        self.profiles[idx]['path'] = path
                        self.save_profiles()
                        refresh_list()

                def delete(idx=i):
                    if messagebox.askyesno("Delete", f"Delete '{self.profiles[idx]['name']}'?"):
                        self.profiles.pop(idx)
                        self.save_profiles()
                        refresh_list()
                        # If we deleted the last one, update main window to show onboarding
                        if not self.profiles:
                            manage_win.destroy()
                            self.update_view()

                ctk.CTkButton(row, text="Browse", width=65, height=26, font=ctk.CTkFont(size=11), command=set_path).pack(side="right", padx=5)
                ctk.CTkButton(row, text="🗑", width=30, height=26, fg_color="#d32f2f", hover_color="#f44336", command=delete).pack(side="right", padx=5)

        refresh_list()

        # Add new profile section
        add_frame = ctk.CTkFrame(manage_win, fg_color="transparent")
        add_frame.pack(pady=15)
        
        new_name_entry = ctk.CTkEntry(add_frame, placeholder_text="Enter custom revival name...", width=200, height=32)
        new_name_entry.pack(side="left", padx=(0, 10))

        def add_profile():
            name = new_name_entry.get().strip()
            if name:
                # Check for duplicate names
                if any(p['name'] == name for p in self.profiles):
                    messagebox.showwarning("Duplicate", "A profile with this name already exists!")
                    return
                    
                self.profiles.append({"name": name, "path": ""})
                self.save_profiles()
                new_name_entry.delete(0, 'end')
                refresh_list()
                
                # If this was the first profile, update the main window
                if len(self.profiles) == 1:
                    manage_win.destroy()
                    self.update_view()
            else:
                messagebox.showwarning("Empty Name", "Please enter a name for the revival.")

        ctk.CTkButton(add_frame, text="+ Add Revival", height=32, font=ctk.CTkFont(size=13), command=add_profile).pack(side="left")


if __name__ == "__main__":
    app = GameLauncher()
    app.mainloop()
