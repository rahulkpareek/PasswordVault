import tkinter as tk
from tkinter import ttk
from tkinter.font import BOLD
import os
import logging
from typing import Optional, Dict, Any
import Handlers
import SignUp

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
                self.parent_window.withdraw()  # Hide instead of destroy
            
            # Create new window
            self.window = tk.Toplevel()  # Change to Toplevel instead of Tk
            self.window.title("PasswordVault 2.0 - User Registration")
            self.window.geometry('500x800')  # Adjusted size
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
        """Create application header with title"""
        header_frame = tk.Frame(self.window, bg='#2c3e50', height=80)
        header_frame.pack(fill='x')
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="Create New Account",
            font=("Arial", 16, BOLD),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(pady=20)

    def create_registration_form(self):
        """Create the registration form with all input fields"""
        # Main form frame
        form_frame = tk.Frame(self.window, bg='white')
        form_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Form fields configuration
        form_fields = [
            ('firstname', 'First Name *'),
            ('lastname', 'Last Name *'),
            ('email', 'Email Address *'),
            ('userid', 'Username *'),
            ('password', 'Password *'),
            ('confirm_password', 'Confirm Password *')
        ]
        
        for field, label in form_fields:
            frame = tk.Frame(form_frame, bg='white')
            frame.pack(fill='x', pady=10)
            
            tk.Label(
                frame, 
                text=label,
                font=("Arial", 10),
                bg='white'
            ).pack(anchor='w')
            
            entry = tk.Entry(
                frame,
                textvariable=self.form_vars[field],
                font=("Arial", 11),
                width=40
            )
            
            if field in ['password', 'confirm_password']:
                entry.config(show='*')
                
            entry.pack(fill='x', pady=5)
            self.form_entries[field] = entry

    def create_buttons(self):
        """Create action buttons"""
        button_frame = tk.Frame(self.window, bg='white')
        button_frame.pack(fill='x', padx=40, pady=20)
        
        # Register button
        register_btn = tk.Button(
            button_frame,
            text="Create Account",
            command=self.handle_registration,
            bg='#2c3e50',
            fg='white',
            width=15,
            pady=8
        )
        register_btn.pack(side='left', padx=5)
        
        # Cancel button
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.handle_cancel,
            bg='#95a5a6',
            fg='white',
            width=15,
            pady=8
        )
        cancel_btn.pack(side='left', padx=5)

    def handle_cancel(self):
        """Handle cancel action"""
        if tk.messagebox.askyesno("Cancel", "Are you sure you want to cancel?"):
            self.window.destroy()
            if self.parent_window:
                self.parent_window.deiconify()  # Show main window again

    def create_footer(self):
        """Create footer with additional information"""
        footer_frame = tk.Frame(self.window, bg='#34495e', height=40)
        footer_frame.pack(fill='x', side='bottom')
        
        footer_label = tk.Label(
            footer_frame,
            text="© 2024 PasswordVault",
            font=("Arial", 9),
            fg='white',
            bg='#34495e'
        )
        footer_label.pack(pady=10)

    def setup_keyboard_bindings(self):
        """Setup keyboard shortcuts"""
        self.window.bind('<Return>', lambda e: self.handle_registration())
        self.window.bind('<Escape>', lambda e: self.handle_cancel())
    
    def handle_registration(self):
        """Handle registration logic"""
        try:
            # Get form values
            form_data = {
                field: var.get().strip() 
                for field, var in self.form_vars.items()
            }
            
            # Validate input fields
            valid, message = SignUp.validate_user_input(
                form_data['firstname'],
                form_data['lastname'], 
                form_data['email'],
                form_data['userid'],
                form_data['password']
            )

            if not valid:
                tk.messagebox.showerror("Validation Error", message)
                return

            # Validate password confirmation
            if form_data['password'] != form_data['confirm_password']:
                tk.messagebox.showerror("Validation Error", "Passwords do not match")
                return

            # Register user
            success, message = SignUp.register_user(
                form_data['firstname'],
                form_data['lastname'],
                form_data['email'],
                form_data['userid'],
                form_data['password']
            )

            if success:
                tk.messagebox.showinfo("Success", "Registration successful!")
                self.window.destroy()
                if self.parent_window:
                    self.parent_window.deiconify()
            else:
                tk.messagebox.showerror("Registration Error", message)

        except Exception as e:
            logging.error(f"Registration error: {str(e)}")
            tk.messagebox.showerror("Error", f"Registration failed: {str(e)}")



