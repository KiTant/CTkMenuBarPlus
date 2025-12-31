"""
CTkMenuBarPlus Example - Complete Feature Demonstration

This example showcases all enhanced features including:
- Keyboard shortcuts (A-Z, 0-9, F1-F12, special keys)
- Icons in menu items
- Checkable menu items with proper state management
- Context menus
- Scrollable menus with many options
- Dynamic enable/disable of menu items

Author: xzyqox (KiTant) | https://github.com/KiTant
"""

import customtkinter as ctk
from CTkMenuBarPlus import *
import tkinter.messagebox as msgbox
from typing import Optional

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class EnhancedMenuBarDemo:
    """Complete demonstration of CTkMenuBarPlus features."""
    
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("1000x700")
        self.root.title("CTkMenuBarPlus Features Demo")
        self.root.minsize(800, 600)
        
        # Application state variables
        self.word_wrap_enabled = True
        self.status_bar_visible = True
        self.line_numbers_visible = False
        self.dark_mode_enabled = True
        self.auto_save_enabled = False
        self.current_file: Optional[str] = None
        self.is_modified = False
        self.zoom_level = 100
        
        # Create GUI components
        self.setup_menu_bar()
        self.setup_content_area()
        self.setup_context_menus()
        self.setup_status_bar()
        
        # Bind additional events
        self.setup_event_bindings()
        
    def setup_menu_bar(self):
        """Create the main menu bar with all enhanced features."""
        self.menu_bar = CTkMenuBar(self.root, height=30)
        
        self.create_file_menu()
        self.create_edit_menu()
        self.create_view_menu()
        self.create_tools_menu()
        self.create_help_menu()
    
    def create_file_menu(self):
        """File menu with icons, shortcuts, and submenus."""
        file_button = self.menu_bar.add_cascade("📁 File")
        self.file_menu = CustomDropdownMenu(widget=file_button)
        
        # File operations with function keys
        self.file_menu.add_option("New File", self.new_file, accelerator="CmdOrCtrl+N", icon="file-down.png")
        self.file_menu.add_option("Open File", self.open_file, accelerator="CmdOrCtrl+O")
        self.file_menu.add_option("Save", self.save_file, accelerator="CmdOrCtrl+S")
        self.file_menu.add_option("Save as", self.save_file, accelerator="CmdOrCtrl+Shift+S")
        self.file_menu.add_separator()
        
        # Recent files submenu
        recent_submenu = self.file_menu.add_submenu("Recent Files", icon="file-down.png", icon_size=32)
        recent_submenu.add_option("example1.txt", lambda: self.show_info("Recent", "example1.txt"))
        recent_submenu.add_option("project.py", lambda: self.show_info("Recent", "project.py"))
        recent_submenu.add_option("notes.md", lambda: self.show_info("Recent", "notes.md"))
        
        self.file_menu.add_separator()
        
        # Auto-save checkable option
        self.auto_save_option = self.file_menu.add_option("Auto Save", 
                                                         self.toggle_auto_save,
                                                         checkable=True, 
                                                         checked=self.auto_save_enabled)
        
        self.file_menu.add_separator()
        self.file_menu.add_option("Exit", self.exit_application, accelerator="Alt+F4")
    
    def create_edit_menu(self):
        """Edit menu with standard editing operations."""
        edit_button = self.menu_bar.add_cascade("✏️ Edit")
        self.edit_menu = CustomDropdownMenu(widget=edit_button)
        
        self.edit_menu.add_option("Undo", self.undo_action, accelerator="CmdOrCtrl+Z")
        self.edit_menu.add_option("Redo", self.redo_action, accelerator="CmdOrCtrl+Y")
        self.edit_menu.add_separator()
        
        self.edit_menu.add_option("Cut", self.cut_text)
        self.edit_menu.add_option("Copy", self.copy_text)
        self.edit_menu.add_option("Paste", self.paste_text)
        self.edit_menu.add_separator()
        
        self.edit_menu.add_option("Select All", self.select_all_text)
        self.edit_menu.add_option("Find", self.find_text, accelerator="CmdOrCtrl+F")
        
        # Advanced editing submenu
        advanced_submenu = self.edit_menu.add_submenu("Advanced", accelerator="F7")
        advanced_submenu.add_option("Duplicate Line", self.action_demo, accelerator="CmdOrCtrl+D")
        advanced_submenu.add_option("Delete Line", self.action_demo, accelerator="Alt+Delete")
        advanced_submenu.add_option("Move Line Up", self.action_demo, accelerator="Alt+Up")
        
    def create_view_menu(self):
        """View menu with checkable appearance options."""
        view_button = self.menu_bar.add_cascade("👁️ View")
        self.view_menu = CustomDropdownMenu(widget=view_button)
        
        # Checkable view options
        self.word_wrap_option = self.view_menu.add_option("Word Wrap", 
                                                         self.toggle_word_wrap,
                                                         checkable=True, 
                                                         checked=self.word_wrap_enabled)
        
        self.line_numbers_option = self.view_menu.add_option("Line Numbers", 
                                                            self.toggle_line_numbers,
                                                            checkable=True, 
                                                            checked=self.line_numbers_visible)
        
        self.status_bar_option = self.view_menu.add_option("Status Bar", 
                                                          self.toggle_status_bar,
                                                          checkable=True, 
                                                          checked=self.status_bar_visible)
        
        self.view_menu.add_separator()
        
        # Zoom controls
        zoom_submenu = self.view_menu.add_submenu("Zoom")
        zoom_submenu.add_option("Zoom In", self.zoom_in, accelerator="CmdOrCtrl+Plus")
        zoom_submenu.add_option("Zoom Out", self.zoom_out, accelerator="CmdOrCtrl+Minus")
        zoom_submenu.add_option("Reset Zoom", self.reset_zoom, accelerator="CmdOrCtrl+0")
        
        self.view_menu.add_separator()

        # Theme switching
        self.dark_mode_option = self.view_menu.add_option("Dark Mode", 
                                                          self.toggle_theme,
                                                          checkable=True,
                                                          checked=self.dark_mode_enabled,
                                                          accelerator="F6")

        # Layout submenu
        layout_submenu = self.view_menu.add_submenu("Layout")
        layout_submenu.add_option("Full Screen", self.toggle_fullscreen, accelerator="F11")
        layout_submenu.add_option("Always on Top", self.toggle_always_on_top, accelerator="F9")
        
    def create_tools_menu(self):
        """Tools menu with utilities and function key demos."""
        tools_button = self.menu_bar.add_cascade("🔧 Tools")
        self.tools_menu = CustomDropdownMenu(widget=tools_button)
        
        self.tools_menu.add_option("Preferences", self.show_preferences, accelerator="F2")
        self.tools_menu.add_option("Settings", self.show_settings, accelerator="F3")
        self.tools_menu.add_separator()

        func_submenu = self.tools_menu.add_submenu("Function Keys Demo")
        func_submenu.add_option("New Window", self.new_window, accelerator="F4")
        func_submenu.add_option("Refresh", self.refresh_action, accelerator="F5")
        func_submenu.add_option("Developer Tools", self.dev_tools, accelerator="F12")
        func_submenu.add_option("Destroy Demo", lambda: self.tools_menu.remove_option("Function Keys Demo"))
        func_submenu.add_option("Clean Demo", func_submenu.clean)
        
        # Initially disabled item
        self.advanced_tools_option = self.tools_menu.add_option("Advanced Tools", 
                                                               self.show_advanced_tools,
                                                               enabled=False)
        
        self.tools_menu.add_separator()
        self.tools_menu.add_option("Enable Advanced Tools", self.enable_advanced_tools)
        
    def create_help_menu(self):
        """Help menu with documentation."""
        help_button = self.menu_bar.add_cascade("❓ Help")
        self.help_menu = CustomDropdownMenu(widget=help_button, max_visible_options=6)
        
        self.help_menu.add_option("Documentation", self.show_documentation, accelerator="F1")
        self.help_menu.add_option("Keyboard Shortcuts", self.show_shortcuts)
        self.help_menu.add_option("Tips and Tricks", self.show_tips)
        self.help_menu.add_separator()
        
        # Scrollable demo - many items
        for i in range(1, 13):
            self.help_menu.add_option(f"Help Topic {i}", 
                                     lambda n=i: self.show_info("Help", f"Topic {n}"))
        
        self.help_menu.add_separator()
        self.help_menu.add_option("About", self.show_about)

    def setup_content_area(self):
        """Setup the main content area."""
        self.text_area = ctk.CTkTextbox(
            self.root,
            wrap="word" if self.word_wrap_enabled else "none"
        )
        self.text_area.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add comprehensive sample text
        sample_text = """CTkMenuBarPlus Demo - Complete Feature Showcase

🗂️ File Operations:
   CmdOrCtrl+N        - New File
   CmdOrCtrl+O        - Open File  
   CmdOrCtrl+S        - Save File
   CmdOrCtrl+Shift+S  - Save as
   Alt+F4             - Exit Application

✏️ Edit Operations:
   CmdOrCtrl+Z        - Undo
   CmdOrCtrl+Y        - Redo
   CmdOrCtrl+X        - Cut
   CmdOrCtrl+C        - Copy
   CmdOrCtrl+V        - Paste
   CmdOrCtrl+A        - Select All
   CmdOrCtrl+F        - Find
   CmdOrCtrl+D        - Duplicate Line
   Alt+Delete         - Delete Line
   Alt+Up             - Move Line Up
   F7                 - Advanced

👁️ View Controls:
   CmdOrCtrl+Plus     - Zoom In
   CmdOrCtrl+Minus    - Zoom Out
   CmdOrCtrl+0        - Reset Zoom
   F11                - Full Screen
   F9                 - Always on Top

🔧 Tools & Function Keys:
   F1            - Help Documentation
   F2            - Preferences
   F3            - Settings
   F4            - New Window
   F5            - Refresh
   F6            - Toggle Dark Mode
   F12           - Developer Tools

════════════════════════════════════════════════════════════════
🖱️ INTERACTIVE FEATURES TO TRY
════════════════════════════════════════════════════════════════

🎛️ CHECKABLE ITEMS:
• View → Word Wrap
• View → Line Numbers
• View → Status Bar
• View → Dark Mode
• File → Auto Save

🖱️ CONTEXT MENU:
• Right-click this text area
• Try the scrollable submenu
• All shortcuts work from context menu too!

📜 SCROLLABLE MENU:
• Help menu has 12+ items
• Automatically shows scrollbar
• Smooth scrolling experience

🔧 DYNAMIC CONTROL:
• Tools → "Advanced Tools" is initially disabled
• Click "Enable Advanced Tools" to activate it
• Demonstrates programmatic menu control
"""
        self.text_area.insert("1.0", sample_text)
    
    def setup_context_menus(self):
        """Setup context menu for the text area."""
        self.context_menu = ContextMenu(self.text_area, scale=0.9)
        
        self.context_menu.add_option(
            option="Cut",
            command=self.cut_text,
            accelerator="CmdOrCtrl+X"
        )
        self.context_menu.add_option(
            option="Copy",
            command=self.copy_text,
            accelerator="CmdOrCtrl+C"
        )
        self.context_menu.add_option(
            option="Paste",
            command=self.paste_text,
            accelerator="CmdOrCtrl+V"
        )
        self.context_menu.add_separator()
        
        self.context_menu.add_option(
            option="Select All",
            command=self.select_all_text,
            accelerator="CmdOrCtrl+A"
        )
        
        self.context_menu.add_separator()
        
        # Format submenu in context menu  
        format_submenu = self.context_menu.add_submenu("Format", max_visible_options=5)
        format_submenu.add_option("Make Uppercase", self.action_demo)
        format_submenu.add_option("Make Lowercase", self.action_demo)
        format_submenu.add_option("Capitalize Words", self.action_demo)
        format_submenu.add_option("Remove Extra Spaces", self.action_demo)
        format_submenu.add_option("Add Line Numbers", self.action_demo)
        format_submenu.add_option("Remove Line Numbers", self.action_demo)
        format_submenu.add_option("Sort Lines A-Z", self.action_demo)
        format_submenu.add_option("Sort Lines Z-A", self.action_demo)
        
        self.context_menu.add_separator()
        
        # Quick actions
        self.context_menu.add_option("Insert Timestamp", self.action_demo)
        self.context_menu.add_option("Word Count", self.action_demo)
        self.context_menu.add_option("Clear All", self.action_demo)
    
    def setup_status_bar(self):
        """Setup the status bar."""
        if self.status_bar_visible:
            self.status_label = ctk.CTkLabel(
                self.root, 
                text="Ready", 
                anchor="w"
            )
            self.status_label.pack(fill="x", padx=10, pady=(0, 5))
    
    def setup_event_bindings(self):
        """Bind additional events."""
        pass
    
    # Menu command handlers
    def new_file(self):
        self.text_area.delete("1.0", "end")
        self.update_status("New file created")
    
    def open_file(self):
        msgbox.showinfo("Open", "Open file dialog would appear here")
        self.update_status("File opened")
    
    def save_file(self):
        msgbox.showinfo("Save", "Save file dialog would appear here")
        self.update_status("File saved")
    
    def cut_text(self):
        try:
            self.text_area.event_generate("<<Cut>>")
            self.update_status("Text cut to clipboard")
        except:
            pass
    
    def copy_text(self):
        try:
            self.text_area.event_generate("<<Copy>>")
            self.update_status("Text copied to clipboard")
        except:
            pass
    
    def paste_text(self):
        try:
            self.text_area.event_generate("<<Paste>>")
            self.update_status("Text pasted from clipboard")
        except:
            pass
    
    def select_all_text(self):
        self.text_area.tag_add("sel", "0.0", "end")
        self.update_status("All text selected")
    
    def toggle_word_wrap(self, checked):
        self.word_wrap_enabled = checked
        self.update_status(f"Word wrap {'enabled' if checked else 'disabled'}")
    
    def toggle_status_bar(self, checked):
        self.status_bar_visible = checked
        if hasattr(self, 'status_label'):
            if checked:
                self.status_label.pack(fill="x", padx=10, pady=(0, 5))
            else:
                self.status_label.pack_forget()
        self.update_status(f"Status bar {'shown' if checked else 'hidden'}")
    
    def toggle_theme(self, checked):
        self.dark_mode_enabled = checked
        mode = "dark" if checked else "light"
        ctk.set_appearance_mode(mode)
        self.update_status(f"Switched to {mode} mode")
    
    def show_preferences(self):
        msgbox.showinfo("Preferences", "Preferences dialog would open here")
        self.update_status("Preferences opened")
    
    def show_settings(self):
        msgbox.showinfo("Settings", "Settings dialog would open here")
        self.update_status("Settings opened")
    
    def show_documentation(self):
        msgbox.showinfo("Documentation", "Documentation would open here")
        self.update_status("Documentation opened")
    
    def show_shortcuts(self):
        msgbox.showinfo("Keyboard Shortcuts", "Shortcuts would be shown here")
        self.update_status("Shortcuts shown")
    
    def show_tips(self):
        msgbox.showinfo("Tips and Tricks", "Tips and tricks would be shown here")
        self.update_status("Tips and tricks shown")
    
    def show_about(self):
        msgbox.showinfo("About", "About dialog would open here")
        self.update_status("About dialog opened")
    
    def show_info(self, title, message):
        msgbox.showinfo(title, message)
        self.update_status(f"{title} info shown")
    
    def action_demo(self):
        msgbox.showinfo("Demo", "This is a demo action")
        self.update_status("Demo action performed")
    
    def new_window(self):
        msgbox.showinfo("New Window", "New window would open here")
        self.update_status("New window opened")
    
    def refresh_action(self):
        msgbox.showinfo("Refresh", "Refresh action would be performed here")
        self.update_status("Refresh action performed")
    
    def dev_tools(self):
        msgbox.showinfo("Developer Tools", "Developer tools would open here")
        self.update_status("Developer tools opened")
    
    def toggle_auto_save(self, checked):
        self.auto_save_enabled = checked
        self.update_status(f"Auto-save {'enabled' if checked else 'disabled'}")
    
    def toggle_line_numbers(self, checked):
        self.line_numbers_visible = checked
        self.update_status(f"Line numbers {'shown' if checked else 'hidden'}")
    
    def toggle_fullscreen(self):
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))
        self.update_status(f"Fullscreen mode {'enabled' if self.root.attributes('-fullscreen') else 'disabled'}")
    
    def toggle_always_on_top(self):
        self.root.attributes("-topmost", not self.root.attributes("-topmost"))
        self.update_status(f"Always on top mode {'enabled' if self.root.attributes('-topmost') else 'disabled'}")
    
    def enable_advanced_tools(self):
        self.advanced_tools_option.enable()
        self.update_status("Advanced tools enabled")
    
    def show_advanced_tools(self):
        msgbox.showinfo("Advanced Tools", "Advanced tools would open here")
        self.update_status("Advanced tools opened")
    
    def exit_application(self):
        self.root.quit()
        self.update_status("Application exited")
    
    def update_status(self, message):
        """Update the status bar message."""
        if hasattr(self, 'status_label') and self.status_bar_visible:
            self.status_label.configure(text=message)
    
    def undo_action(self):
        """Undo last action."""
        self.update_status("Undo action performed")
        msgbox.showinfo("Undo", "Undo action would be performed here")
    
    def redo_action(self):
        """Redo last action."""
        self.update_status("Redo action performed")
        msgbox.showinfo("Redo", "Redo action would be performed here")
    
    def find_text(self):
        """Find text dialog."""
        self.update_status("Find dialog opened")
        msgbox.showinfo("Find", "Find dialog would open here")
    
    def zoom_in(self):
        """Zoom in."""
        self.zoom_level = min(self.zoom_level + 10, 300)
        self.update_status(f"Zoomed in to {self.zoom_level}%")
    
    def zoom_out(self):
        """Zoom out."""
        self.zoom_level = max(self.zoom_level - 10, 50)
        self.update_status(f"Zoomed out to {self.zoom_level}%")
    
    def reset_zoom(self):
        """Reset zoom to 100%."""
        self.zoom_level = 100
        self.update_status("Zoom reset to 100%")
    
    def run(self):
        """Start the application."""
        self.root.mainloop()

if __name__ == "__main__":
    app = EnhancedMenuBarDemo()
    app.run()
