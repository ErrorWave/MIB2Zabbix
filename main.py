"""
MIB to Zabbix Template Converter - GUI Application
Modern UI with Dark/Light Mode Support
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
from pathlib import Path
from mib_parser import parse_mib_file, MIBObject
from zabbix_generator import create_template_from_mib


class ModernTheme:
    """Modern color themes for light and dark modes"""
    
    LIGHT = {
        'bg': '#FFFFFF',
        'bg_secondary': '#F5F5F5',
        'bg_tertiary': '#E8E8E8',
        'fg': '#1A1A1A',
        'fg_secondary': '#555555',
        'fg_muted': '#888888',
        'accent': '#2E7D32',
        'accent_hover': '#1B5E20',
        'accent_light': '#E8F5E9',
        'button_bg': '#F5F5F5',
        'button_fg': '#1A1A1A',
        'border': '#CCCCCC',
        'hover': '#E0E0E0',
        'success': '#2E7D32',
        'warning': '#F57C00',
        'error': '#C62828',
        'info': '#1976D2'
    }
    
    DARK = {
        'bg': '#1E1E1E',
        'bg_secondary': '#2D2D2D',
        'bg_tertiary': '#3D3D3D',
        'fg': '#E0E0E0',
        'fg_secondary': '#B0B0B0',
        'fg_muted': '#808080',
        'accent': '#4CAF50',
        'accent_hover': '#66BB6A',
        'accent_light': '#1B5E20',
        'button_bg': '#2D2D2D',
        'button_fg': '#E0E0E0',
        'border': '#444444',
        'hover': '#3D3D3D',
        'success': '#4CAF50',
        'warning': '#FFA726',
        'error': '#EF5350',
        'info': '#42A5F5'
    }


class MIB2ZabbixGUI:
    """Main GUI application for converting MIB files to Zabbix templates"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("MIB to Zabbix Template Converter")
        self.root.geometry("1100x800")
        self.root.resizable(True, True)
        
        # Theme management
        self.current_theme = 'dark'
        self.theme = ModernTheme.DARK
        self.root.configure(bg=self.theme['bg'])
        
        # Data
        self.mib_file_path = tk.StringVar()
        self.template_name = tk.StringVar()
        self.template_description = tk.StringVar()
        self.group_name = tk.StringVar(value="Templates")
        self.mib_objects = []
        self.is_processing = False
        
        # Configure styles
        self._setup_styles()
        
        # Create GUI
        self._create_widgets()
    
    def _setup_styles(self):
        """Setup custom ttk styles for the current theme"""
        style = ttk.Style()
        style.theme_use('clam')  # Use clam theme as base
        
        # Configure colors based on current theme
        style.configure('TFrame', background=self.theme['bg'], foreground=self.theme['fg'])
        style.configure('TLabel', background=self.theme['bg'], foreground=self.theme['fg'])
        style.configure('TLabelframe', background=self.theme['bg'], foreground=self.theme['fg'], 
                       borderwidth=2, relief='solid')
        style.configure('TLabelframe.Label', background=self.theme['bg'], foreground=self.theme['fg'],
                       font=('Segoe UI', 10, 'bold'))
        
        style.configure('TEntry', fieldbackground=self.theme['bg_secondary'], 
                       foreground=self.theme['fg'], 
                       borderwidth=1, relief='solid',
                       padding=5)
        style.map('TEntry',
                 fieldbackground=[('focus', self.theme['bg_tertiary'])])
        
        # Button styles
        style.configure('TButton', background=self.theme['button_bg'],
                       foreground=self.theme['button_fg'],
                       borderwidth=1,
                       relief='raised',
                       padding=6)
        style.map('TButton',
                 background=[('active', self.theme['hover']),
                            ('pressed', self.theme['border'])],
                 foreground=[('active', self.theme['fg'])])
        
        style.configure('Accent.TButton', background=self.theme['accent'],
                       foreground='white',
                       borderwidth=0,
                       padding=8)
        style.map('Accent.TButton',
                 background=[('active', self.theme['accent_hover']),
                            ('pressed', self.theme['accent'])],
                 foreground=[('active', 'white')])
        
        # Treeview styles
        style.configure('Treeview', background=self.theme['bg_secondary'],
                       foreground=self.theme['fg'],
                       fieldbackground=self.theme['bg_secondary'],
                       borderwidth=1)
        style.map('Treeview',
                 background=[('selected', self.theme['accent_light'])],
                 foreground=[('selected', self.theme['fg'])])
        style.configure('Treeview.Heading', background=self.theme['bg_tertiary'],
                       foreground=self.theme['fg'],
                       borderwidth=1)
        style.map('Treeview.Heading',
                 background=[('active', self.theme['hover'])])
        
        style.configure('Title.TLabel', font=('Segoe UI', 14, 'bold'),
                       background=self.theme['bg'], foreground=self.theme['fg'])
        style.configure('Header.TLabel', font=('Segoe UI', 11, 'bold'),
                       background=self.theme['bg'], foreground=self.theme['fg'])
        style.configure('Status.TLabel', font=('Segoe UI', 9),
                       background=self.theme['bg'], foreground=self.theme['fg_secondary'])
    
    def _create_widgets(self):
        """Create the GUI widgets"""
        
        # Create header bar with title and theme toggle
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        # Left side - title
        title_container = ttk.Frame(header_frame)
        title_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        ttk.Label(title_container, text="MIB to Zabbix Converter", style='Title.TLabel').pack(anchor=tk.W)
        ttk.Label(title_container, text="Convert SNMP MIB files to Zabbix templates", 
                 style='Status.TLabel').pack(anchor=tk.W)
        
        # Right side - theme toggle
        button_container = ttk.Frame(header_frame)
        button_container.pack(side=tk.RIGHT, padx=20, pady=15)
        
        self.theme_button = ttk.Button(button_container, text="☀️ Light Mode", 
                                       command=self._toggle_theme)
        self.theme_button.pack()
        
        # Separator
        separator = ttk.Frame(self.root, height=1)
        separator.pack(fill=tk.X, padx=0)
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # ===== FILE SELECTION SECTION =====
        file_frame = ttk.LabelFrame(main_frame, text="Step 1: Select MIB File", padding="15")
        file_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Label(file_frame, text="MIB File Path:", style='Header.TLabel').grid(row=0, column=0, sticky=tk.W, pady=10)
        
        file_entry = ttk.Entry(file_frame, textvariable=self.mib_file_path, state='readonly')
        file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 10), pady=10)
        
        button_sub_frame = ttk.Frame(file_frame)
        button_sub_frame.grid(row=0, column=2, columnspan=2, padx=(0, 0), pady=10)
        
        ttk.Button(button_sub_frame, text="Browse", command=self._browse_mib_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_sub_frame, text="Parse", command=self._parse_mib, 
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        
        # ===== TEMPLATE INFO SECTION =====
        info_frame = ttk.LabelFrame(main_frame, text="Step 2: Configure Template", padding="15")
        info_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        info_frame.columnconfigure(1, weight=1)
        
        # Template Name
        ttk.Label(info_frame, text="Template Name:", style='Header.TLabel').grid(row=0, column=0, sticky=tk.W, pady=8)
        ttk.Entry(info_frame, textvariable=self.template_name, width=40).grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=8)
        
        # Template Description
        ttk.Label(info_frame, text="Description:", style='Header.TLabel').grid(row=1, column=0, sticky=tk.W, pady=8)
        ttk.Entry(info_frame, textvariable=self.template_description, width=40).grid(
            row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=8)
        
        # Group Name
        ttk.Label(info_frame, text="Group Name:", style='Header.TLabel').grid(row=2, column=0, sticky=tk.W, pady=8)
        ttk.Entry(info_frame, textvariable=self.group_name, width=40).grid(
            row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=8)
        
        # ===== OBJECTS PREVIEW SECTION =====
        preview_frame = ttk.LabelFrame(main_frame, text="Step 3: Review Parsed Objects", padding="15")
        preview_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(1, weight=1)
        
        # Status label
        status_frame = ttk.Frame(preview_frame)
        status_frame.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text="No file loaded", style='Status.TLabel')
        self.status_label.pack(side=tk.LEFT)
        
        # Treeview for objects
        columns = ('Name', 'OID', 'Syntax', 'Access')
        tree_frame = ttk.Frame(preview_frame)
        tree_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        
        self.tree = ttk.Treeview(tree_frame, columns=columns, height=12,
                                  yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('Name', anchor=tk.W, width=200)
        self.tree.column('OID', anchor=tk.W, width=250)
        self.tree.column('Syntax', anchor=tk.W, width=150)
        self.tree.column('Access', anchor=tk.W, width=150)
        
        self.tree.heading('#0', text='', anchor=tk.W)
        self.tree.heading('Name', text='Name', anchor=tk.W)
        self.tree.heading('OID', text='OID', anchor=tk.W)
        self.tree.heading('Syntax', text='Syntax', anchor=tk.W)
        self.tree.heading('Access', text='Access', anchor=tk.W)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # ===== ACTION BUTTONS =====
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Button(button_frame, text="Generate Template", 
                   command=self._generate_template, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Clear All", command=self._clear_all).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(side=tk.RIGHT, padx=5)
        
        # Progress label
        self.progress_label = ttk.Label(button_frame, text="", style='Status.TLabel')
        self.progress_label.pack(side=tk.LEFT, padx=20)
    
    def _toggle_theme(self):
        """Toggle between light and dark themes"""
        if self.current_theme == 'light':
            self.current_theme = 'dark'
            self.theme = ModernTheme.DARK
            self.theme_button.config(text="☀️ Light Mode")
        else:
            self.current_theme = 'light'
            self.theme = ModernTheme.LIGHT
            self.theme_button.config(text="🌙 Dark Mode")
        
        # Update root window background
        self.root.configure(bg=self.theme['bg'])
        
        # Reconfigure all styles
        self._setup_styles()
        
        # Update all frames and widgets
        self._update_theme_recursive(self.root)
    
    def _update_theme_recursive(self, widget):
        """Recursively update theme colors for all widgets"""
        try:
            if isinstance(widget, (ttk.Frame, ttk.Label, ttk.LabelFrame, ttk.Button, ttk.Entry)):
                widget.configure(style=widget.option_get('style', ''))
            elif isinstance(widget, tk.Frame):
                widget.configure(bg=self.theme['bg'])
            elif isinstance(widget, tk.Label):
                widget.configure(bg=self.theme['bg'], fg=self.theme['fg'])
        except tk.TclError:
            pass
        
        # Recursively update children
        try:
            for child in widget.winfo_children():
                self._update_theme_recursive(child)
        except tk.TclError:
            pass
    
    def _browse_mib_file(self):
        """Open file browser to select MIB file"""
        file_path = filedialog.askopenfilename(
            title="Select MIB File",
            filetypes=[("MIB files", "*.mib"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            self.mib_file_path.set(file_path)
            # Auto-populate template name from filename
            filename = Path(file_path).stem
            self.template_name.set(filename)
    
    def _parse_mib(self):
        """Parse the selected MIB file"""
        if not self.mib_file_path.get():
            messagebox.showwarning("Warning", "Please select a MIB file first")
            return
        
        self.progress_label.config(text="Parsing...", foreground=self.theme['info'])
        self.root.update()
        
        try:
            file_path = self.mib_file_path.get()
            module_name, self.mib_objects = parse_mib_file(file_path)
            
            # Update status
            if module_name:
                self.status_label.config(
                    text=f"✓ Parsed: {module_name} ({len(self.mib_objects)} objects found)",
                    foreground=self.theme['success']
                )
                if not self.template_name.get():
                    self.template_name.set(module_name)
            else:
                self.status_label.config(
                    text=f"✓ Parsed: {len(self.mib_objects)} objects found",
                    foreground=self.theme['success']
                )
            
            # Populate tree view
            self._populate_tree()
            
            self.progress_label.config(text="✓ Done!", foreground=self.theme['success'])
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse MIB file:\n{str(e)}")
            self.progress_label.config(text="✗ Error", foreground=self.theme['error'])
    
    def _populate_tree(self):
        """Populate the treeview with MIB objects"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add objects
        for obj in self.mib_objects:
            self.tree.insert('', 'end', values=(
                obj.name,
                obj.oid,
                obj.syntax[:50] if obj.syntax else '',
                obj.access
            ))
    
    def _generate_template(self):
        """Generate Zabbix template from parsed objects"""
        if not self.mib_objects:
            messagebox.showwarning("Warning", "Please parse a MIB file first")
            return
        
        if not self.template_name.get():
            messagebox.showwarning("Warning", "Please enter a template name")
            return
        
        # Ask where to save
        file_path = filedialog.asksaveasfilename(
            title="Save Zabbix Template",
            defaultextension=".xml",
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")],
            initialfile=f"{self.template_name.get()}_template.xml"
        )
        
        if not file_path:
            return
        
        self.progress_label.config(text="Generating template...", foreground=self.theme['info'])
        self.root.update()
        
        try:
            # Generate template
            generator = create_template_from_mib(
                self.mib_objects,
                self.template_name.get(),
                self.template_description.get(),
                self.group_name.get()
            )
            
            # Save to file
            generator.save_to_file(file_path)
            
            self.progress_label.config(text="✓ Template generated!", foreground=self.theme['success'])
            messagebox.showinfo(
                "Success",
                f"Zabbix template created successfully!\n\nFile saved to:\n{file_path}"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate template:\n{str(e)}")
            self.progress_label.config(text="✗ Error", foreground=self.theme['error'])
    
    def _clear_all(self):
        """Clear all fields and data"""
        self.mib_file_path.set("")
        self.template_name.set("")
        self.template_description.set("")
        self.group_name.set("Templates")
        self.mib_objects = []
        self.status_label.config(text="No file loaded", foreground=self.theme['fg_muted'])
        self.progress_label.config(text="")
        
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = MIB2ZabbixGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
