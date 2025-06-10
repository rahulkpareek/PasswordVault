import tkinter as tk
from tkinter import ttk
from tkinter.font import BOLD
import os
import logging
from typing import Optional, Dict, Any
import Handlers

class RegistrationWindow:
    """Registration window class for Password Vault"""
    
    def __init__(self, parent_window: Optional[tk.Tk] = None):
        self.parent_window = parent_window
        self.window = None
        self.form_vars = {}
        self.form_entries = {}
        self.setup_logging()
        self.create_registration_window()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('password_vault_registration.log'),
                logging.StreamHandler()
            ]
        )
    
    def create_registration_window(self):
        """Create and configure the registration window"""
        try:
            # Close parent window if provided
            if self.parent_window:
                self.parent_window.destroy()
            
            # Create new window
            self.window = tk.Tk()
            self.window.title("PasswordVault 2.0 - User Registration")
            self.window.geometry('600x700')
            self.window.resizable(False, False)
            
            # Center the window
            self.center_window()
            
            # Configure window icon
            self.set_window_icon()
            
            # Setup UI components
            self.setup_variables()
            self.create_header()
            self.create_registration_form()
            self.create_buttons()
            self.create_footer()
            
            # Setup keyboard bindings
            self.setup_keyboard_bindings()
            
            # Focus on first field
            if 'firstname' in self.form_entries:
                self.form_entries['firstname'].focus_set()
            
            logging.info("Registration window created successfully")
            
        except Exception as e:
            logging.error(f"Failed to create registration window: {str(e)}")
            tk.messagebox.showerror("Error", f"Failed to initialize registration window: {str(e)}")
    
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
        """Initialize tkinter variables for form fields"""
        self.form_vars = {
            'firstname': tk.StringVar(),
            'lastname': tk.StringVar(),
            'email': tk.StringVar(),
            'userid': tk.StringVar(),
            'password': tk.StringVar(),
            'confirm_password': tk.StringVar()
        }
    
    def create_header(self):
        """Create application header with logo and title"""
        header_frame = tk.Frame(self.window, bg='#2c3e50', height=100)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Logo
        try:
            if os.path.exists("Logo.png"):
                logo_image = tk.PhotoImage(file="Logo.png")
                # Scale down logo if needed
                logo_label = tk.Label(header_frame, image=logo_image, bg='#2c3e50')
                logo_label.image = logo_image  # Keep a reference
                logo_label.pack(side='left', padx=20, pady=10)
        except Exception as e:
            logging.warning(f"Could not load logo: {str(e)}")
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="Create New Account",
            font=("Arial", 18, BOLD),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(side='left', padx=20, pady=30)
    
    def create_registration_form(self):
        """Create the registration form with all input fields"""
        # Main form frame
        form_frame = tk.Frame(self.window, bg='#ecf0f1', padx=40, pady=20)
        form_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Form fields configuration
        form_fields = [
            {
                'key': 'firstname',
                'label': 'First Name *',
                'placeholder': 'Enter your first name',
                'show': None
            },
            {
                'key': 'lastname',
                'label': 'Last Name *',
                'placeholder': 'Enter your last name',
                'show': None
            },
            {
                'key': 'email',
                'label': 'Email Address *',
                'placeholder': 'Enter your email address',
                'show': None
            },
            {
                'key': 'userid',
                'label': 'Username *',
                'placeholder': 'Choose a username (3-20 characters)',
                'show': None
            },
            {
                'key': 'password',
                'label': 'Password *',
                'placeholder': 'Enter a strong password',
                'show': '*'
            },
            {
                'key': 'confirm_password',
                'label': 'Confirm Password *',
                'placeholder': 'Re-enter your password',
                'show': '*'
            }
        ]
        
        self.form_entries = {}
        
        for i, field in enumerate(form_fields):
            # Create field frame
            field_frame = tk.Frame(form_frame, bg='#ecf0f1')
            field_frame.pack(fill='x', pady=8)
            
            # Label
            label = tk.Label(
                field_frame,
                text=field['label'],
                font=("Arial", 11, BOLD),
                fg='#2c3e50',
                bg='#ecf0f1',
                anchor='w'
            )
            label.pack(fill='x', pady=(0, 5))
            
            # Entry field
            entry = tk.Entry(
                field_frame,
                textvariable=self.form_vars[field['key']],
                font=("Arial", 11),
                bd=2,
                relief='solid',
                show=field['show'],
                width=40
            )
            entry.pack(fill='x', ipady=8)
            
            # Add placeholder text (simulated)
            self.add_placeholder(entry, field['placeholder'])
            
            # Store reference
            self.form_entries[field['key']] = entry
            
            # Bind validation events
            entry.bind('<FocusOut>', lambda e, key=field['key']: self.validate_field(key))
            entry.bind('<KeyRelease>', lambda e, key=field['key']: self.on_field_change(key))
        
        # Password strength indicator
        self.create_password_strength_indicator(form_frame)
        
        # Requirements text
        self.create_requirements_text(form_frame)
    
    def add_placeholder(self, entry: tk.Entry, placeholder: str):
        """Add placeholder text to entry field"""
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg='black')
        
        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg='grey')
        
        # Set initial placeholder
        entry.insert(0, placeholder)
        entry.config(fg='grey')
        
        # Bind events
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
    
    def create_password_strength_indicator(self, parent):
        """Create password strength indicator"""
        strength_frame = tk.Frame(parent, bg='#ecf0f1')
        strength_frame.pack(fill='x', pady=5)
        
        tk.Label(
            strength_frame,
            text="Password Strength:",
            font=("Arial", 9),
            fg='#2c3e50',
            bg='#ecf0f1'
        ).pack(side='left')
        
        self.strength_label = tk.Label(
            strength_frame,
            text="",
            font=("Arial", 9, BOLD),
            bg='#ecf0f1'
        )
        self.strength_label.pack(side='left', padx=(10, 0))
    
    def create_requirements_text(self, parent):
        """Create password requirements text"""
        req_frame = tk.Frame(parent, bg='#ecf0f1')
        req_frame.pack(fill='x', pady=10)
        
        requirements = [
            "• At least 8 characters long",
            "• Contains uppercase and lowercase letters",
            "• Contains at least one number",
            "• Contains at least one special character"
        ]
        
        tk.Label(
            req_frame,
            text="Password Requirements:",
            font=("Arial", 10, BOLD),
            fg='#2c3e50',
            bg='#ecf0f1'
        ).pack(anchor='w')
        
        for req in requirements:
            tk.Label(
                req_frame,
                text=req,
                font=("Arial", 9),
                fg='#34495e',
                bg='#ecf0f1'
            ).pack(anchor='w', padx=10)
    
    def validate_field(self, field_key: str):
        """Validate individual field"""
        value = self.form_vars[field_key].get()
        entry = self.form_entries[field_key]
        
        # Remove placeholder styling
        if entry.cget('fg') == 'grey':
            return
        
        # Basic validation
        is_valid = True
        if field_key == 'email' and value:
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            is_valid = re.match(email_pattern, value) is not None
        
        # Visual feedback
        if is_valid or not value:
            entry.config(bg='white')
        else:
            entry.config(bg='#ffebee')
    
    def on_field_change(self, field_key: str):
        """Handle field value changes"""
        if field_key == 'password':
            self.update_password_strength()
        elif field_key == 'confirm_password':
            self.check_password_match()
    
    def update_password_strength(self):
        """Update password strength indicator"""
        password = self.form_vars['password'].get()
        
        if not password or self.form_entries['password'].cget('fg') == 'grey':
            self.strength_label.config(text="", fg='black')
            return
        
        strength = self.calculate_password_strength(password)
        
        if strength < 2:
            self.strength_label.config(text="Weak", fg='#e74c3c')
        elif strength < 4:
            self.strength_label.config(text="Medium", fg='#f39c12')
        else:
            self.strength_label.config(text="Strong", fg='#27ae60')
    
    def calculate_password_strength(self, password: str) -> int:
        """Calculate password strength score"""
        score = 0
        if len(password) >= 8:
            score += 1
        if any(c.isupper() for c in password):
            score += 1
        if any(c.islower() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c in '!@#$%^&*(),.?":{}|<>' for c in password):
            score += 1
        return score
    
    def check_password_match(self):
        """Check if passwords match"""
        password = self.form_vars['password'].get()
        confirm_password = self.form_vars['confirm_password'].get()
        confirm_entry = self.form_entries['confirm_password']
        
        if confirm_entry.cget('fg') == 'grey':
            return
        
        if confirm_password and password != confirm_password:
            confirm_entry.config(bg='#ffebee')
        else:
            confirm_entry.config(bg='white')
    
    def create_buttons(self):
        """Create action buttons"""
        button_frame = tk.Frame(self.window, bg='#ecf0f1')
        button_frame.pack(fill='x', padx=20, pady=20)
        
        # Register button
        register_btn = tk.Button(
            button_frame,
            text="Create Account",
            command=self.handle_registration,
            font=("Arial", 12, BOLD),
            bg='#27ae60',
            fg='white',
            padx=30,
            pady=10,
            cursor='hand2',
            relief='flat'
        )
        register_btn.pack(side='right', padx=10)
        
        # Cancel button
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.handle_cancel,
            font=("Arial", 12),
            bg='#95a5a6',
            fg='white',
            padx=30,
            pady=10,
            cursor='hand2',
            relief='flat'
        )
        cancel_btn.pack(side='right', padx=10)
        
        # Back to Login button
        back_btn = tk.Button(
            button_frame,
            text="Back to Login",
            command=self.back_to_login,
            font=("Arial", 10),
            bg='#3498db',
            fg='white',
            padx=20,
            pady=8,
            cursor='hand2',
            relief='flat'
        )
        back_btn.pack(side='left', padx=10)
    
    def create_footer(self):
        """Create footer with additional information"""
        footer_frame = tk.Frame(self.window, bg='#34495e', height=40)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        footer_label = tk.Label(
            footer_frame,
            text="© 2024 PasswordVault - Secure Password Management",
            font=("Arial", 9),
            fg='white',
            bg='#34495e'
        )
        footer_label.pack(expand=True)
    
    def setup_keyboard_bindings(self):
        """Setup keyboard shortcuts"""
        self.window.bind('<Return>', lambda e:
