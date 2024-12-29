# ----> Assalamoalikum !
# ---> I'm Muzammil_Teachtreasure1

# ---> How to make Language Translator in python language  
# --< Lets do it >--

# --> Libraries
from tkinter import *
from tkinter import ttk
from googletrans import Translator, LANGUAGES

# --> Initialize the main window
root = Tk()
root.geometry('500x500')  #--: Increase size for better layout
root.resizable(0, 0)
root.title("Language Translator by Muzammil_teachtreasure1")
root['bg'] = 'skyblue'

# --> Initialize the translator
translator = Translator()

# --> Function to perform translation
def translate_text():
    try:
        input_text = Input_text.get("1.0", END).strip()  #--: Get input text
        src_lang = source_lang.get()  #--: Get source language
        dest_lang = target_lang.get()  #--: Get target language

        #--> Perform translation
        translated = translator.translate(input_text, src=src_lang, dest=dest_lang)
        Output_text.delete("1.0", END)  #--: Clear previous output
        Output_text.insert(END, translated.text)  #--: Insert translated text
    except Exception as e:
        Output_text.delete("1.0", END)  #--: Clear previous output
        Output_text.insert(END, f"Error: {e}")

# ---> Add Widgets
Label(root, text="Language Translator", font="Arial 20 bold", bg='skyblue').pack(pady=10)
Label(root, text="Enter Text:", font="Arial 13 bold", bg='skyblue').place(x=20, y=70)
Input_text = Text(root, font="Arial 12 bold", height=5, width=40, wrap=WORD)
Input_text.place(x=20, y=100)

Label(root, text="Select Source Language:", font="Arial 10 bold", bg='skyblue').place(x=20, y=220)
source_lang = ttk.Combobox(root, values=list(LANGUAGES.values()), width=22)
source_lang.place(x=200, y=220)
source_lang.set('English')  #--: Default Language

Label(root, text="Select Target Language:", font="Arial 10 bold", bg='skyblue').place(x=20, y=260)
target_lang = ttk.Combobox(root, values=list(LANGUAGES.values()), width=22)
target_lang.place(x=200, y=260)
target_lang.set('Urdu')  #--: Default Language

#--> Button to translate
Button(root, text="Translate", font="Arial 12 bold", bg='green', fg='white', command=translate_text).place(x=200, y=300)

Label(root, text="Output:", font="Arial 12 bold", bg='skyblue').place(x=20, y=350)
Output_text = Text(root, font="Arial 12 bold", height=5, width=40, wrap=WORD)
Output_text.place(x=20, y=380)

#--> Run the application
root.mainloop()
