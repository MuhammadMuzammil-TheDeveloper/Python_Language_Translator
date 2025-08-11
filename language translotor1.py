import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from googletrans import Translator, LANGUAGES
import pyperclip
import webbrowser
from threading import Thread
import json
import os
from datetime import datetime
import gtts
import playsound
import tempfile
from PIL import Image, ImageTk
class ProfessionalTranslator:
    def __init__(self, root):
        self.root = root
        self.setup_main_window()
        self.translator = Translator()
        self.setup_styles()
        self.create_widgets()
        self.load_preferences()
        self.setup_menu()
        
        # Initialize TTS engine
        self.tts_engine = None
        self.current_tts_file = None

    def setup_main_window(self):
        self.root.title("Professional Translator")
        self.root.geometry('1000x800')
        self.root.minsize(900, 700)
        self.root.configure(bg='#f5f5f5')
        
        # Make the window responsive
        for i in range(4):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure styles
        self.style.configure('Main.TFrame', background='#f5f5f5')
        self.style.configure('Header.TLabel', 
                           font=('Segoe UI', 18, 'bold'), 
                           background='#2c3e50', 
                           foreground='white')
        self.style.configure('Section.TLabel', 
                           font=('Segoe UI', 12, 'bold'), 
                           background='#f5f5f5',
                           foreground='#2c3e50')
        self.style.configure('TButton', 
                           font=('Segoe UI', 10), 
                           padding=6,
                           background='#3498db',
                           foreground='white')
        self.style.map('TButton',
                      background=[('active', '#2980b9')])
        self.style.configure('Primary.TButton',
                           font=('Segoe UI', 11, 'bold'),
                           background='#2ecc71',
                           foreground='white')
        self.style.map('Primary.TButton',
                      background=[('active', '#27ae60')])
        self.style.configure('Secondary.TButton',
                           background='#e74c3c',
                           foreground='white')
        self.style.map('Secondary.TButton',
                      background=[('active', '#c0392b')])
        self.style.configure('TCombobox',
                           font=('Segoe UI', 10),
                           padding=5)
        self.style.configure('Status.TLabel',
                           font=('Segoe UI', 9),
                           background='#34495e',
                           foreground='white',
                           padding=5)
        self.style.configure('Dark.TFrame',
                           background='#34495e')
        self.style.configure('Dark.TLabel',
                           background='#34495e',
                           foreground='white')

    def create_widgets(self):
        # Main container
        self.main_frame = ttk.Frame(self.root, style='Main.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        self.header_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        self.header_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.title_label = ttk.Label(self.header_frame, 
                                   text="Professional Translator", 
                                   style='Header.TLabel')
        self.title_label.pack(side=tk.LEFT, padx=15, pady=10)
        
        # Settings button
        self.settings_btn = ttk.Button(self.header_frame, 
                                     text="⚙ Settings", 
                                     command=self.open_settings)
        self.settings_btn.pack(side=tk.RIGHT, padx=15)
        
        # Main content area
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input section
        self.input_frame = ttk.LabelFrame(self.content_frame, 
                                        text=" Source Text ", 
                                        style='Section.TLabel')
        self.input_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5, side=tk.LEFT)
        
        # Source language selection
        self.lang_frame = ttk.Frame(self.input_frame)
        self.lang_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(self.lang_frame, text="Source Language:").pack(side=tk.LEFT, padx=5)
        
        self.source_lang = ttk.Combobox(self.lang_frame, 
                                      values=['Auto Detect'] + list(LANGUAGES.values()), 
                                      state='readonly',
                                      width=25)
        self.source_lang.pack(side=tk.LEFT, padx=5)
        self.source_lang.set('Auto Detect')
        
        # Input text with scrollbar
        self.input_text = scrolledtext.ScrolledText(self.input_frame, 
                                                  wrap=tk.WORD, 
                                                  font=('Segoe UI', 11), 
                                                  padx=10, 
                                                  pady=10,
                                                  undo=True)
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        # Input text buttons
        self.input_btn_frame = ttk.Frame(self.input_frame)
        self.input_btn_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(self.input_btn_frame, 
                 text="Clear", 
                 style='Secondary.TButton',
                 command=self.clear_input).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.input_btn_frame, 
                 text="Paste", 
                 command=self.paste_text).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.input_btn_frame, 
                 text="Open File", 
                 command=self.open_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.input_btn_frame, 
                 text="Detect Language", 
                 command=self.detect_language).pack(side=tk.LEFT, padx=2)
        
        # Translation controls
        self.ctrl_frame = ttk.Frame(self.content_frame)
        self.ctrl_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(self.ctrl_frame, text="Target Language:").pack(side=tk.LEFT, padx=5)
        
        self.target_lang = ttk.Combobox(self.ctrl_frame, 
                                      values=list(LANGUAGES.values()), 
                                      state='readonly',
                                      width=25)
        self.target_lang.pack(side=tk.LEFT, padx=5)
        self.target_lang.set('english')
        
        ttk.Button(self.ctrl_frame, 
                 text="Translate", 
                 style='Primary.TButton',
                 command=self.start_translation_thread).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.ctrl_frame, 
                 text="Swap Languages", 
                 command=self.swap_languages).pack(side=tk.LEFT, padx=10)
        
        # Output section
        self.output_frame = ttk.LabelFrame(self.content_frame, 
                                         text=" Translation ", 
                                         style='Section.TLabel')
        self.output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5, side=tk.RIGHT)
        
        self.output_text = scrolledtext.ScrolledText(self.output_frame, 
                                                   wrap=tk.WORD, 
                                                   font=('Segoe UI', 11), 
                                                   padx=10, 
                                                   pady=10,
                                                   state='normal')
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Output text buttons
        self.output_btn_frame = ttk.Frame(self.output_frame)
        self.output_btn_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(self.output_btn_frame, 
                 text="Clear", 
                 style='Secondary.TButton',
                 command=self.clear_output).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.output_btn_frame, 
                 text="Copy", 
                 command=self.copy_output).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.output_btn_frame, 
                 text="Speak", 
                 command=self.speak_translation).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.output_btn_frame, 
                 text="Save As", 
                 command=self.save_translation).pack(side=tk.LEFT, padx=2)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self.main_frame, 
                                  textvariable=self.status_var, 
                                  style='Status.TLabel',
                                  anchor=tk.W)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Configure tags for text highlighting
        self.input_text.tag_configure('detected', background='#fffacd')
        
        # History button
        self.history_btn = ttk.Button(self.main_frame, 
                                     text="History", 
                                     command=self.show_history)
        self.history_btn.pack(side=tk.RIGHT, padx=10, pady=5)

    def setup_menu(self):
        self.menubar = tk.Menu(self.root)
        
        # File menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="New Translation", command=self.new_translation)
        self.file_menu.add_command(label="Open File...", command=self.open_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save Translation...", command=self.save_translation)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        
        # Edit menu
        self.edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.edit_menu.add_command(label="Undo", command=self.undo_text)
        self.edit_menu.add_command(label="Redo", command=self.redo_text)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut_text)
        self.edit_menu.add_command(label="Copy", command=self.copy_text)
        self.edit_menu.add_command(label="Paste", command=self.paste_text)
        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)
        
        # View menu
        self.view_menu = tk.Menu(self.menubar, tearoff=0)
        self.view_menu.add_command(label="Zoom In", command=self.zoom_in)
        self.view_menu.add_command(label="Zoom Out", command=self.zoom_out)
        self.view_menu.add_separator()
        self.theme_menu = tk.Menu(self.view_menu, tearoff=0)
        self.theme_menu.add_radiobutton(label="Light Theme", command=lambda: self.change_theme('light'))
        self.theme_menu.add_radiobutton(label="Dark Theme", command=lambda: self.change_theme('dark'))
        self.view_menu.add_cascade(label="Theme", menu=self.theme_menu)
        self.menubar.add_cascade(label="View", menu=self.view_menu)
        
        # Help menu
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label="Documentation", command=self.show_docs)
        self.help_menu.add_command(label="About", command=self.show_about)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)
        
        self.root.config(menu=self.menubar)

    # Core translation functionality
    def start_translation_thread(self):
        Thread(target=self.translate_text, daemon=True).start()

    def translate_text(self):
        input_text = self.input_text.get("1.0", tk.END).strip()
        if not input_text:
            self.status_var.set("Error: No text to translate")
            return
            
        src_lang = self.source_lang.get()
        dest_lang = self.target_lang.get()
        
        try:
            self.status_var.set("Translating...")
            self.root.update()
            
            # Get language codes
            src_code = 'auto' if src_lang == 'Auto Detect' else \
                      [k for k, v in LANGUAGES.items() if v.lower() == src_lang.lower()][0]
            dest_code = [k for k, v in LANGUAGES.items() if v.lower() == dest_lang.lower()][0]
            
            # Perform translation
            translated = self.translator.translate(input_text, src=src_code, dest=dest_code)
            
            # Display results
            self.output_text.config(state='normal')
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, translated.text)
            self.output_text.config(state='normal')
            
            # Update source language if it was auto-detected
            if src_lang == 'Auto Detect' and hasattr(translated, 'src'):
                detected_lang = LANGUAGES.get(translated.src, 'Unknown')
                self.source_lang.set(detected_lang)
                
            self.status_var.set(f"Translated from {LANGUAGES.get(translated.src, 'Unknown')} to {dest_lang}")
            
            # Save to history
            self.save_to_history(input_text, translated.text, src_lang, dest_lang)
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Translation Error", f"An error occurred during translation:\n{str(e)}")

    # Additional features
    def detect_language(self):
        input_text = self.input_text.get("1.0", tk.END).strip()
        if not input_text:
            self.status_var.set("Error: No text to analyze")
            return
            
        try:
            self.status_var.set("Detecting language...")
            self.root.update()
            
            detected = self.translator.detect(input_text)
            lang_name = LANGUAGES.get(detected.lang, 'Unknown')
            confidence = detected.confidence * 100
            
            self.input_text.tag_remove('detected', '1.0', tk.END)
            self.input_text.tag_add('detected', '1.0', tk.END)
            
            self.source_lang.set(lang_name)
            self.status_var.set(f"Detected: {lang_name} (confidence: {confidence:.1f}%)")
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Detection Error", f"An error occurred during detection:\n{str(e)}")

    def swap_languages(self):
        current_src = self.source_lang.get()
        current_dest = self.target_lang.get()
        
        if current_src == 'Auto Detect':
            return
            
        self.source_lang.set(current_dest)
        self.target_lang.set(current_src)
        
        if self.output_text.get("1.0", tk.END).strip():
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert(tk.END, self.output_text.get("1.0", tk.END))
            self.output_text.delete("1.0", tk.END)
            self.status_var.set("Languages swapped")

    # Text manipulation
    def clear_input(self):
        self.input_text.delete("1.0", tk.END)
        self.input_text.tag_remove('detected', '1.0', tk.END)
        self.status_var.set("Input cleared")

    def clear_output(self):
        self.output_text.config(state='normal')
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state='normal')
        self.status_var.set("Output cleared")

    def paste_text(self):
        try:
            clipboard_text = pyperclip.paste()
            if clipboard_text:
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert(tk.END, clipboard_text)
                self.status_var.set("Text pasted from clipboard")
        except Exception as e:
            self.status_var.set(f"Error pasting: {str(e)}")

    def copy_output(self):
        output_text = self.output_text.get("1.0", tk.END).strip()
        if output_text:
            pyperclip.copy(output_text)
            self.status_var.set("Translation copied to clipboard")
        else:
            self.status_var.set("No translation to copy")

    def cut_text(self):
        self.input_text.event_generate("<<Cut>>")
        self.status_var.set("Text cut to clipboard")

    def copy_text(self):
        self.input_text.event_generate("<<Copy>>")
        self.status_var.set("Text copied to clipboard")

    def undo_text(self):
        try:
            self.input_text.edit_undo()
            self.status_var.set("Undo last action")
        except:
            self.status_var.set("Nothing to undo")

    def redo_text(self):
        try:
            self.input_text.edit_redo()
            self.status_var.set("Redo last action")
        except:
            self.status_var.set("Nothing to redo")

    # File operations
    def open_file(self):
        filetypes = (
            ('Text files', '*.txt'),
            ('All files', '*.*')
        )
        
        filename = filedialog.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.input_text.delete("1.0", tk.END)
                    self.input_text.insert(tk.END, content)
                    self.status_var.set(f"Opened: {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file:\n{str(e)}")

    def save_translation(self):
        content = self.output_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "No translation to save")
            return
            
        filetypes = (
            ('Text files', '*.txt'),
            ('All files', '*.*')
        )
        
        filename = filedialog.asksaveasfilename(
            title='Save translation',
            defaultextension='.txt',
            filetypes=filetypes)
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                    self.status_var.set(f"Saved: {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{str(e)}")

    # Text-to-speech
    def speak_translation(self):
        output_text = self.output_text.get("1.0", tk.END).strip()
        if not output_text:
            self.status_var.set("No translation to speak")
            return
            
        try:
            self.status_var.set("Generating speech...")
            self.root.update()
            
            # Clean up previous TTS file if exists
            if self.current_tts_file and os.path.exists(self.current_tts_file):
                os.remove(self.current_tts_file)
            
            # Get target language code
            dest_lang = self.target_lang.get()
            lang_code = [k for k, v in LANGUAGES.items() if v.lower() == dest_lang.lower()][0]
            
            # Create temp file for TTS
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
                self.current_tts_file = f.name
            
            # Generate speech
            tts = gtts.gTTS(text=output_text, lang=lang_code)
            tts.save(self.current_tts_file)
            
            # Play the audio
            playsound.playsound(self.current_tts_file)
            
            self.status_var.set("Speech completed")
            
        except Exception as e:
            self.status_var.set(f"TTS error: {str(e)}")
            messagebox.showerror("Text-to-Speech Error", f"Could not generate speech:\n{str(e)}")

    # History functionality
    def save_to_history(self, original, translation, src_lang, dest_lang):
        history_file = "translation_history.json"
        entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'source_lang': src_lang,
            'target_lang': dest_lang,
            'original': original,
            'translation': translation
        }
        
        history = []
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r') as f:
                    history = json.load(f)
            except:
                pass
                
        history.append(entry)
        
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)

    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Translation History")
        history_window.geometry("800x600")
        
        # Create treeview
        columns = ('timestamp', 'source', 'target', 'preview')
        tree = ttk.Treeview(history_window, columns=columns, show='headings')
        
        # Define headings
        tree.heading('timestamp', text='Date/Time')
        tree.heading('source', text='Source Language')
        tree.heading('target', text='Target Language')
        tree.heading('preview', text='Preview')
        
        # Set column widths
        tree.column('timestamp', width=150)
        tree.column('source', width=120)
        tree.column('target', width=120)
        tree.column('preview', width=380)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Load history
        history_file = "translation_history.json"
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r') as f:
                    history = json.load(f)
                    
                    for entry in reversed(history):
                        preview = entry['original'][:50] + "..." if len(entry['original']) > 50 else entry['original']
                        tree.insert('', tk.END, 
                                   values=(entry['timestamp'], 
                                          entry['source_lang'], 
                                          entry['target_lang'], 
                                          preview))
            except Exception as e:
                messagebox.showerror("Error", f"Could not load history:\n{str(e)}")
        
        # Add double-click event
        def on_double_click(event):
            item = tree.selection()[0]
            values = tree.item(item, 'values')
            
            # Find full entry
            timestamp = values[0]
            with open(history_file, 'r') as f:
                history = json.load(f)
                for entry in history:
                    if entry['timestamp'] == timestamp:
                        self.show_history_entry(entry)
                        break
        
        tree.bind("<Double-1>", on_double_click)

    def show_history_entry(self, entry):
        entry_window = tk.Toplevel(self.root)
        entry_window.title(f"Translation from {entry['source_lang']} to {entry['target_lang']}")
        entry_window.geometry("700x500")
        
        # Original text
        ttk.Label(entry_window, text="Original Text:").pack(anchor=tk.W, padx=10, pady=(10, 0))
        original_text = scrolledtext.ScrolledText(entry_window, wrap=tk.WORD, height=10)
        original_text.pack(fill=tk.X, padx=10, pady=5)
        original_text.insert(tk.END, entry['original'])
        original_text.config(state='disabled')
        
        # Translation
        ttk.Label(entry_window, text="Translation:").pack(anchor=tk.W, padx=10, pady=(10, 0))
        trans_text = scrolledtext.ScrolledText(entry_window, wrap=tk.WORD, height=10)
        trans_text.pack(fill=tk.X, padx=10, pady=5)
        trans_text.insert(tk.END, entry['translation'])
        trans_text.config(state='disabled')
        
        # Buttons
        btn_frame = ttk.Frame(entry_window)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(btn_frame, 
                 text="Use This Translation", 
                 command=lambda: self.use_history_entry(entry)).pack(side=tk.LEFT)
        ttk.Button(btn_frame, 
                 text="Close", 
                 command=entry_window.destroy).pack(side=tk.RIGHT)

    def use_history_entry(self, entry):
        self.source_lang.set(entry['source_lang'])
        self.target_lang.set(entry['target_lang'])
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert(tk.END, entry['original'])
        self.output_text.config(state='normal')
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, entry['translation'])
        self.output_text.config(state='normal')
        self.status_var.set("Loaded from history")

    # Settings and preferences
    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("500x400")
        settings_window.resizable(False, False)
        
        ttk.Label(settings_window, 
                 text="Translator Settings", 
                 font=('Segoe UI', 14, 'bold')).pack(pady=10)
        
        # Theme selection
        ttk.Label(settings_window, 
                 text="Application Theme:", 
                 font=('Segoe UI', 10)).pack(anchor=tk.W, padx=20, pady=(10, 0))
        
        self.theme_var = tk.StringVar(value=self.user_prefs.get('theme', 'light'))
        theme_frame = ttk.Frame(settings_window)
        theme_frame.pack(fill=tk.X, padx=20)
        
        ttk.Radiobutton(theme_frame, 
                       text="Light Theme", 
                       variable=self.theme_var, 
                       value='light').pack(side=tk.LEFT)
        ttk.Radiobutton(theme_frame, 
                       text="Dark Theme", 
                       variable=self.theme_var, 
                       value='dark').pack(side=tk.LEFT, padx=20)
        
        # Default languages
        ttk.Label(settings_window, 
                 text="Default Source Language:", 
                 font=('Segoe UI', 10)).pack(anchor=tk.W, padx=20, pady=(20, 0))
        
        self.default_src_var = tk.StringVar(value=self.user_prefs.get('default_source', 'Auto Detect'))
        ttk.Combobox(settings_window, 
                    textvariable=self.default_src_var, 
                    values=['Auto Detect'] + list(LANGUAGES.values())).pack(fill=tk.X, padx=20)
        
        ttk.Label(settings_window, 
                 text="Default Target Language:", 
                 font=('Segoe UI', 10)).pack(anchor=tk.W, padx=20, pady=(10, 0))
        
        self.default_dest_var = tk.StringVar(value=self.user_prefs.get('default_target', 'english'))
        ttk.Combobox(settings_window, 
                    textvariable=self.default_dest_var, 
                    values=list(LANGUAGES.values())).pack(fill=tk.X, padx=20)
        
        # Font settings
        ttk.Label(settings_window, 
                 text="Editor Font Size:", 
                 font=('Segoe UI', 10)).pack(anchor=tk.W, padx=20, pady=(20, 0))
        
        self.font_size_var = tk.IntVar(value=self.user_prefs.get('font_size', 11))
        ttk.Scale(settings_window, 
                 from_=8, 
                 to=20, 
                 variable=self.font_size_var,
                 command=lambda e: self.preview_font_size()).pack(fill=tk.X, padx=20)
        
        # Save button
        btn_frame = ttk.Frame(settings_window)
        btn_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(btn_frame, 
                 text="Save Settings", 
                 style='Primary.TButton',
                 command=lambda: self.save_settings(settings_window)).pack(side=tk.RIGHT, padx=20)
        ttk.Button(btn_frame, 
                 text="Cancel", 
                 command=settings_window.destroy).pack(side=tk.RIGHT)

    def preview_font_size(self):
        size = self.font_size_var.get()
        self.input_text.config(font=('Segoe UI', size))
        self.output_text.config(font=('Segoe UI', size))

    def save_settings(self, settings_window):
        self.user_prefs = {
            'theme': self.theme_var.get(),
            'default_source': self.default_src_var.get(),
            'default_target': self.default_dest_var.get(),
            'font_size': self.font_size_var.get()
        }
        
        self.save_preferences()
        self.apply_preferences()
        settings_window.destroy()
        messagebox.showinfo("Settings Saved", "Your preferences have been saved.")

    def load_preferences(self):
        self.preferences_file = "translator_preferences.json"
        if os.path.exists(self.preferences_file):
            try:
                with open(self.preferences_file, 'r') as f:
                    self.user_prefs = json.load(f)
            except:
                self.user_prefs = {}
        else:
            self.user_prefs = {}

    def save_preferences(self):
        with open(self.preferences_file, 'w') as f:
            json.dump(self.user_prefs, f, indent=2)

    def apply_preferences(self):
        # Apply theme
        if self.user_prefs.get('theme') == 'dark':
            self.change_theme('dark')
        else:
            self.change_theme('light')
        
        # Apply default languages
        self.source_lang.set(self.user_prefs.get('default_source', 'Auto Detect'))
        self.target_lang.set(self.user_prefs.get('default_target', 'english'))
        
        # Apply font size
        font_size = self.user_prefs.get('font_size', 11)
        self.input_text.config(font=('Segoe UI', font_size))
        self.output_text.config(font=('Segoe UI', font_size))

    def change_theme(self, theme):
        if theme == 'dark':
            # Dark theme colors
            bg_color = '#2d2d2d'
            fg_color = '#ffffff'
            text_bg = '#1e1e1e'
            text_fg = '#ffffff'
            highlight = '#3e3e3e'
            self.style.configure('Main.TFrame', background=bg_color)
            self.style.configure('TLabel', background=bg_color, foreground=fg_color)
            self.style.configure('Section.TLabel', background=bg_color, foreground='#3498db')
            self.style.configure('Dark.TFrame', background='#1e1e1e')
            self.style.configure('Dark.TLabel', background='#1e1e1e', foreground=fg_color)
        else:
            # Light theme colors
            bg_color = '#f5f5f5'
            fg_color = '#000000'
            text_bg = '#ffffff'
            text_fg = '#000000'
            highlight = '#f0f0f0'
            self.style.configure('Main.TFrame', background=bg_color)
            self.style.configure('TLabel', background=bg_color, foreground=fg_color)
            self.style.configure('Section.TLabel', background=bg_color, foreground='#2c3e50')
            self.style.configure('Dark.TFrame', background='#34495e')
            self.style.configure('Dark.TLabel', background='#34495e', foreground='white')
        
        # Apply to widgets
        self.root.config(bg=bg_color)
        self.input_text.config(
            bg=text_bg,
            fg=text_fg,
            insertbackground=fg_color,
            selectbackground=highlight
        )
        self.output_text.config(
            bg=text_bg,
            fg=text_fg,
            insertbackground=fg_color,
            selectbackground=highlight
        )
        
        # Update user preferences
        self.user_prefs['theme'] = theme
        self.save_preferences()

    # View options
    def zoom_in(self):
        current_size = self.input_text['font'].split()[-1]
        new_size = min(int(current_size) + 1, 20)
        self.input_text.config(font=('Segoe UI', new_size))
        self.output_text.config(font=('Segoe UI', new_size))
        self.user_prefs['font_size'] = new_size
        self.save_preferences()

    def zoom_out(self):
        current_size = self.input_text['font'].split()[-1]
        new_size = max(int(current_size) - 1, 8)
        self.input_text.config(font=('Segoe UI', new_size))
        self.output_text.config(font=('Segoe UI', new_size))
        self.user_prefs['font_size'] = new_size
        self.save_preferences()

    # Help and about
    def show_docs(self):
        webbrowser.open("https://github.com/yourusername/pro-translator/docs")

    def show_about(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("About Professional Translator")
        about_window.geometry("400x300")
        about_window.resizable(False, False)
        
        ttk.Label(about_window, 
                 text="Professional Translator", 
                 font=('Segoe UI', 16, 'bold')).pack(pady=10)
        
        ttk.Label(about_window, 
                 text="Version 2.0", 
                 font=('Segoe UI', 12)).pack()
        
        ttk.Label(about_window, 
                 text="© 2024 Your Company", 
                 font=('Segoe UI', 10)).pack(pady=20)
        
        ttk.Label(about_window, 
                 text="A professional-grade translation tool\nwith advanced features and customization", 
                 justify=tk.CENTER).pack(pady=10)
        
        ttk.Button(about_window, 
                 text="Close", 
                 command=about_window.destroy).pack(pady=10)

    def new_translation(self):
        self.clear_input()
        self.clear_output()
        self.status_var.set("New translation started")

def main():
    root = tk.Tk()
    app = ProfessionalTranslator(root)
    root.mainloop()

if __name__ == "__main__":
    main()

