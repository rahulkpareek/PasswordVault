import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import logging
from typing import Optional, Dict
from tinydb import TinyDB
import DBhelper

class UserDashboard:
    """Dashboard window shown after successful login"""
    
    def __init__(self, username: str, parent_window: Optional[tk.Tk] = None):
        self.username = username
        self.parent_window = parent_window
        self.window = None
        self.credentials_tree = None
        self.setup_logging()
        self.create_dashboard()
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('password_vault_dashboard.log'),
                logging.StreamHandler()
            ]
        )

    def create_dashboard(self):
        """Create the dashboard window"""
        if self.parent_window:
            self.parent_window.withdraw()
            
        self.window = tk.Toplevel()
        self.window.title(f"Password Vault - {self.username}'s Dashboard")
        self.window.geometry('800x600')
        self.window.protocol("WM_DELETE_WINDOW", self.handle_close)
        
        # Create main container
        main_container = tk.Frame(self.window, bg='white')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_container, bg='#2c3e50')
        header_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            header_frame,
            text=f"Welcome, {self.username}",
            font=("Arial", 16, BOLD),
            fg='white',
            bg='#2c3e50'
        ).pack(pady=20)
        
        # Buttons frame
        button_frame = tk.Frame(main_container, bg='white')
        button_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Button(
            button_frame,
            text="Add New Credentials",
            command=self.show_add_credentials_dialog
        ).pack(side='left', padx=5)
        
        ttk.Button(
            button_frame,
            text="Delete Selected",
            command=self.delete_selected_credentials
        ).pack(side='left', padx=5)
        
        ttk.Button(
            button_frame,
            text="Refresh List",
            command=self.refresh_credentials_list
        ).pack(side='left', padx=5)
        
        ttk.Button(
            button_frame,
            text="Sign Out",
            command=self.handle_close
        ).pack(side='right', padx=5)
        
        # Credentials list
        list_frame = tk.Frame(main_container)
        list_frame.pack(fill='both', expand=True)
        
        # Treeview for credentials
        columns = ('service', 'username', 'password')
        self.credentials_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Configure columns
        self.credentials_tree.heading('service', text='Service/Website')
        self.credentials_tree.heading('username', text='Username')
        self.credentials_tree.heading('password', text='Password')
        
        # Hide actual password with asterisks in the view
        self.credentials_tree.column('password', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.credentials_tree.yview)
        self.credentials_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack list and scrollbar
        self.credentials_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Load initial data
        self.refresh_credentials_list()

    def show_add_credentials_dialog(self):
        """Show dialog to add new credentials"""
        dialog = tk.Toplevel(self.window)
        dialog.title("Add New Credentials")
        dialog.geometry('400x300')
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Form fields
        tk.Label(dialog, text="Service/Website:").pack(pady=5)
        service_entry = tk.Entry(dialog, width=40)
        service_entry.pack(pady=5)
        
        tk.Label(dialog, text="Username:").pack(pady=5)
        username_entry = tk.Entry(dialog, width=40)
        username_entry.pack(pady=5)
        
        tk.Label(dialog, text="Password:").pack(pady=5)
        password_entry = tk.Entry(dialog, width=40, show='*')
        password_entry.pack(pady=5)
        
        def save_credentials():
            service = service_entry.get().strip()
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            
            if not all([service, username, password]):
                messagebox.showwarning("Validation Error", "All fields are required!")
                return
                
            try:
                db = DBhelper.connect_to_database(f'vault_{self.username}.json')
                DBhelper.insert_in_db(db, {
                    'service': service,
                    'username': username,
                    'password': password
                })
                dialog.destroy()
                self.refresh_credentials_list()
                messagebox.showinfo("Success", "Credentials saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save credentials: {str(e)}")
        
        # Save button
        ttk.Button(dialog, text="Save", command=save_credentials).pack(pady=20)

    def delete_selected_credentials(self):
        """Delete selected credentials from the list"""
        selected_item = self.credentials_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an item to delete!")
            return
            
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected credentials?"):
            try:
                item_values = self.credentials_tree.item(selected_item)['values']
                db = DBhelper.connect_to_database(f'vault_{self.username}.json')
                query = DBhelper.make_query()
                DBhelper.delete_from_db(db, 
                    (query.service == item_values[0]) & 
                    (query.username == item_values[1]))
                self.refresh_credentials_list()
                messagebox.showinfo("Success", "Credentials deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete credentials: {str(e)}")

    def refresh_credentials_list(self):
        """Refresh the credentials list from database"""
        try:
            # Clear existing items
            for item in self.credentials_tree.get_children():
                self.credentials_tree.delete(item)
                
            # Load credentials from database
            db = DBhelper.connect_to_database(f'vault_{self.username}.json')
            credentials = db.all()
            
            for cred in credentials:
                self.credentials_tree.insert('', 'end', values=(
                    cred['service'],
                    cred['username'],
                    '*' * 8  # Show asterisks instead of actual password
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load credentials: {str(e)}")

    def handle_close(self):
        """Handle window close"""
        if messagebox.askyesno("Confirm Sign Out", "Are you sure you want to sign out?"):
            self.window.destroy()
            if self.parent_window:
                self.parent_window.deiconify()