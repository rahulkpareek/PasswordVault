import tkinter as tk
from tkinter import ttk
from tkinter.font import BOLD
import os
import sys
from typing import Optional, Callable
import logging
import Handlers
import RegisterScreen

class PasswordVaultApp:
    """Main application class for Password Vault"""
    
    def __init__(self):
        self.window = None
        self.username_var = None
        self.password_var = None
        self.current_user = None
        self.setup_logging()
        self.create_main_window()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('password_vault_ui.log'),
                logging.StreamHandler()
            ]
        )
    
    def create_main_window(self):
        """Create and configure the main application window"""
        try:
            self.window = tk.Tk()
            self.window.title("PasswordVault 2.0")
            self.window.geometry('500x600')
            self.window.resizable(False, False)
            
            # Center the window on screen
            self.center_window()
            
            # Configure window icon if available
            self.set_window_icon()
            
            # Setup UI components
            self.setup_variables()
            self.create_header()
            self.create_login_form()
            self.create_buttons()
            self.create_footer()
            
            # Bind keyboard events
            self.setup_keyboard_bindings()
            
            logging.info("Main window created successfully")
            
        except Exception as e:
            logging.error(f"Failed to create main window: {str(e)}")
            self.show_error("Initialization Error", f"Failed to initialize application: {str(e)}")
            sys.exit(1)
    
    def center_window(self):
        """Center the window on the screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def set_window_icon(self):
        """Set window icon if logo file exists"""
        try:
            if os.path.exists("Logo.png"):
                icon = tk.PhotoImage(file="Logo.png")
                self.window.iconphoto(True, icon)
        except Exception as e:
            logging.warning(f"Could not set window icon: {str(e)}")
    
    def setup_variables(self):
        """Initialize tkinter variables"""
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
    
    def create_header(self):
        """Create application header with logo and title"""
        header_frame = tk.Frame(self.window, bg='#2c3e50', height=120)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Logo
        try:
            if os.path.exists("Logo.png"):
                logo_image = tk.PhotoImage(file="Logo.png")
                # Resize logo if too large
                logo_label = tk.Label(header_frame, image=logo_image, bg='#2c3e50')
                logo_label.image = logo_image  # Keep a reference
        except Exception as e:
            logging.warning(f"Could not load logo image: {str(e)}")
        
        # Title
        title_label = tk.Label(header_frame, text="Password Vault", bg='#2c3e50', fg='white', font=("Arial", 16, BOLD))
        title_label.pack(side='right', padx=20, pady=20)
    
    def create_login_form(self):
        """Create login form with username and password fields"""
        form_frame = tk.Frame(self.window, bg='#ecf0f1', height=120)
        form_frame.pack(fill='x', pady=(0, 20))
        form_frame.pack_propagate(False)
        
        # Username label and entry
        username_label = tk.Label(form_frame, text="Username", bg='#ecf0f1', fg='black', font=("Arial", 12))
        username_label.pack(side='left', padx=20, pady=10)
        
        username_entry = tk.Entry(form_frame, bd=5, textvariable=self.username_var)
        username_entry.pack(side='left', padx=20, pady=10)
        
        # Password label and entry
        password_label = tk.Label(form_frame, text="Password", bg='#ecf0f1', fg='black', font=("Arial", 12))
        password_label.pack(side='left', padx=20, pady=10)
        
        password_entry = tk.Entry(form_frame, bd=5, show='*', textvariable=self.password_var)
        password_entry.pack(side='left', padx=20, pady=10)
    
    def create_buttons(self):
        """Create login and register buttons"""
        button_frame = tk.Frame(self.window, bg='#ecf0f1', height=60)
        button_frame.pack(fill='x', pady=(0, 20))
        button_frame.pack_propagate(False)
        
        # Sign in button
        sign_in_button = tk.Button(button_frame, text="Sign in", command=self.sign_in_callback)
        sign_in_button.pack(side='left', padx=20, pady=10)
        
        # Register button
        register_button = tk.Button(button_frame, text="Register New User", command=self.signup_callback)
        register_button.pack(side='left', padx=20, pady=10)
    
    def create_footer(self):
        """Create footer with copyright information"""
        footer_frame = tk.Frame(self.window, bg='#2c3e50', height=40)
        footer_frame.pack(fill='x', pady=(0, 20))
        footer_frame.pack_propagate(False)
        
        # Copyright label
        copyright_label = tk.Label(footer_frame, text="© 2023 Password Vault. All rights reserved.", bg='#2c3e50', fg='white', font=("Arial", 10))
        copyright_label.pack(side='left', padx=20, pady=10)
    
    def setup_keyboard_bindings(self):
        """Setup keyboard bindings for the application"""
        self.window.bind('<Return>', self.sign_in_callback)
    
    def sign_in_callback(self):
        """Callback function for sign in button"""
        Handlers.SignInHandler(self.username_var.get(), self.password_var.get())
    
    def signup_callback(self):
        """Callback function for register button"""
        RegisterScreen.SignUpHandler(self.window)
    
    def show_error(self, title, message):
        """Show error message to the user"""
        error_window = tk.Toplevel(self.window)
        error_window.title(title)
        error_window.geometry('300x150')
        error_window.resizable(False, False)
        
        # Center the error window on screen
        error_window.update_idletasks()
        width = error_window.winfo_width()
        height = error_window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        error_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Error message label
        error_label = tk.Label(error_window, text=message, bg='#ecf0f1', fg='black', font=("Arial", 12))
        error_label.pack(pady=20)
        
        # OK button
        ok_button = tk.Button(error_window, text="OK", command=error_window.destroy)
        ok_button.pack(pady=10)
    
    def run(self):
        """Run the main application loop"""
        self.window.mainloop()
