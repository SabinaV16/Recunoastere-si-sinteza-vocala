"""
    Importuri si biblioteci
"""
import os
import tkinter as tk
from tkinter import filedialog
import threading
import speech_recognition as sr
import pygame
from gtts import gTTS

def selecteaza_limba():
    """
    In aceasta functie utilizatorul trebuie sa selecteze limba in care vrea
    sa fie aplicatia in continuare. Limba implicita este romana.
    """
    root.title("Alegere limba")
    for widget in root.winfo_children():
        widget.destroy()

    selected_variable = tk.StringVar(root)
    selected_variable.set(options[INDEX])

    label = tk.Label(root, text=limba[INDEX], **entry_style)
    label.pack(pady= 50)

    option_menu = tk.OptionMenu(root, selected_variable, *options, command=save_option)
    option_menu.configure(bg='#AF9FBF', fg='black', font=('Calibri Light', 12))
    option_menu.pack(side='top', pady=40)

    submit_to_home = tk.Button(root, text= submit_home[INDEX], command = home, **button_style)
    submit_to_home.pack(side='top', pady=10, padx= 5)

def save_option(value):
    """
    Funcția care se ocupă de salvarea indexului.
    Aceste este necesar pentru ca mesajele din interfata sa fie in limba selectata
    """
    # pylint: disable=global-statement
    global INDEX
    INDEX = options.index(value)
    for widget in root.winfo_children():
        widget.destroy()
    label = tk.Label(root, text=limba[INDEX], **entry_style)
    label.pack(pady= 50)
    selected_variable = tk.StringVar(root)
    selected_variable.set(options[INDEX])
    option_menu = tk.OptionMenu(root, selected_variable, *options, command=save_option)
    option_menu.configure(bg='#AF9FBF', fg='black', font=('Calibri Light', 12))
    option_menu.pack(side='top', pady=40)

    submit_to_home = tk.Button(root, text= submit_home[INDEX], command = home, **button_style)
    submit_to_home.pack(side='top', pady=10, padx= 5)

def home():
    """
    Funcția pentru afisarea meniului principal.
    Distruge orice wedget ar fi in pagina anterioara si afiseaza 
    intructiuni alaturi de cele 4 butoane.
    """
    root.title('Home')
    for widget in root.winfo_children():
        widget.destroy()

    label_home = tk.Label(root, text=text_home[INDEX], **entry_style)
    label_home.pack(pady = 20)

    stt_button = tk.Button(root, text=btn1[INDEX], command = speech_to_text, **button_style)
    tts_button = tk.Button(root, text=btn2[INDEX], command = text_to_speech_main, **button_style)
    search_button = tk.Button(root, text=btn4[INDEX], command = search, **button_style)
    change_button = tk.Button(root, text=btn5[INDEX], command = selecteaza_limba, **button_style)

    stt_button.place(relx=0.5, rely=0.25, anchor=tk.CENTER)
    tts_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    search_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)
    change_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

def speech_to_text():
    """
    Funcția care se ocupă de conversia discursului in text.
    """
    root.title('Speech to text')

    for widget in root.winfo_children():
        widget.destroy()

    label2 = tk.Label(root, text= nume_fisier[INDEX], bg="#E0D6EB", fg="black")
    label2.pack(anchor=tk.W, padx=10)
    # pylint: disable=global-statement
    global RECOGNIZED_TEXT, FILE_NAME_STT
    FILE_NAME_STT = tk.Entry(root)
    FILE_NAME_STT.pack(fill=tk.X, padx=10, pady=5)
    RECOGNIZED_TEXT = tk.Text(root, wrap=tk.WORD, height=10, bg="white", fg="black")
    RECOGNIZED_TEXT.pack(fill=tk.BOTH, expand=True)
    RECOGNIZED_TEXT.config(state=tk.DISABLED)

    start_button = tk.Button(root, text="Start", command=start_speech_to_text, **button_style)
    start_button.pack(side='top', padx=10, pady=5)

    stop_button = tk.Button(root, text="Stop", command=stop_listening, **button_style)
    stop_button.pack(side='top', padx=10, pady=5)

    save_button = tk.Button(root, text="Save", command=save_text_to_file, **button_style)
    save_button.pack(side='top', padx=10, pady=5)

    back_home = tk.Button(root, text=back_home_v[INDEX], command=home, **button_style)
    back_home.pack(side='right', pady=10, padx=5)

def start_speech_to_text():
    """
    Funcția care se ocupă de conversia discursului in text
    """
    # pylint: disable=global-statement
    global LISTENING
    if not LISTENING:
        LISTENING = True
        threading.Thread(target=listen).start()

def listen():
    """
    Funcția care se ocupă de conversia discursului in text
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        while LISTENING:
            print("Ascult...")
            try:
                audio = recognizer.listen(source, phrase_time_limit=30)
                if LISTENING:
                    text = recognizer.recognize_google(audio, language= option[INDEX])
                    RECOGNIZED_TEXT.config(state=tk.NORMAL)
                    RECOGNIZED_TEXT.insert(tk.END, text + "\n")
                    RECOGNIZED_TEXT.config(state=tk.DISABLED)
            except sr.WaitTimeoutError:
                print("Timpul de așteptare a expirat. Încercăm din nou...")
            except sr.UnknownValueError:

                print("Nu am putut recunoaște mesajul.")
            except sr.RequestError as e:
                print(f"Eroare la cererea de la serviciul de recunoaștere a vorbirii: {e}")

def stop_listening():
    """
    Funcția care se ocupă de oprirea ascultarii
    """
    # pylint: disable=global-statement
    global LISTENING
    LISTENING = False

def save_text_to_file():
    """
    Funcția care se ocupă de salvarea continutului intr un fisier
    """
    # pylint: disable=global-statement
    global LISTENING
    LISTENING = False
    content = RECOGNIZED_TEXT.get("1.0", tk.END)
    file_name = FILE_NAME_STT.get()
    if not file_name:
        file_name = "output.txt"
    if not file_name.endswith(".txt"):
        file_name += ".txt"
    save_directory = fisier_stt[INDEX]
    file_path = os.path.join(save_directory, file_name)
    if os.path.exists(file_path):

        file_name_no_ext, file_ext = os.path.splitext(file_name)
        index = 1
        while os.path.exists(os.path.join(save_directory, f"{file_name_no_ext} ({index}){file_ext}")):
            index += 1
        file_name = f"{file_name_no_ext} ({index}){file_ext}"
    file_path = os.path.join(save_directory, file_name)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
    FILE_NAME_STT.delete(0, tk.END)
    RECOGNIZED_TEXT.config(state=tk.NORMAL)
    RECOGNIZED_TEXT.delete("1.0", tk.END)
    RECOGNIZED_TEXT.config(state=tk.DISABLED)

def text_to_speech_main():
    """
    Funcția care se ocupă de conversia textului în discurs.
    """
    root.title('Text to speech')
    # pylint: disable=global-statement
    global TEXT, FILE_NAME_ENTRY
    for widget in root.winfo_children():
        widget.destroy()
    label_tts = tk.Label(root, text=introducere_text[INDEX], pady=10, **entry_style)
    label_tts.pack()
    TEXT = tk.Text(root, height=20, bg ='white')
    TEXT.pack()
    label_tts = tk.Label(root, text=nume_fisier[INDEX], pady=10,
                                   font =  ('Calibri Light', 12), bg = "#E0D6EB",fg= "black")
    label_tts.pack()

    FILE_NAME_ENTRY = tk.Entry(root, width=100, bg='white')
    FILE_NAME_ENTRY.pack()

    btn_tts = tk.Button(root, text=submit_home[INDEX], command = text_to_speech, **button_style)
    btn_tts.pack(side='left', pady=10, padx=5)

    back_home = tk.Button(root, text=back[INDEX], command = home, **button_style)
    back_home.pack(side='left', pady=10, padx=5)

def text_to_speech():
    """
    Funcția pentru text_to_speech.
    """
    content = TEXT.get("1.0", tk.END)
    directory = fisier_tts[INDEX]
    file_name = FILE_NAME_ENTRY.get()
    if not file_name:
        file_name = "output.txt"
    if not file_name.endswith(".txt"):
        file_name += ".txt"

    file_path = os.path.join(directory, file_name)
    if os.path.exists(file_path):

        file_name_no_ext, file_ext = os.path.splitext(file_name)
        index = 1
        while os.path.exists(os.path.join(directory, f"{file_name_no_ext} ({index}){file_ext}")):
            index += 1
        file_name = f"{file_name_no_ext} ({index}){file_ext}"
    file_path = os.path.join(directory, file_name)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    tts = gTTS(text=content, lang=option[INDEX])

    temp_file = "temp.mp3"
    tts.save(temp_file)
    pygame.mixer.init()
    sound = pygame.mixer.Sound(temp_file)
    sound.play()
    while pygame.mixer.get_busy():
        pygame.time.Clock().tick(10)
    os.remove(temp_file)

def search():
    """
    Funcția care se ocupă de crearea butoanelor pentru functionalitatea 
    de search si de stergerea tuturor celorlalte wirget uri
    """
    root.title('Search')
    for widget in root.winfo_children():
        widget.destroy()
    label_search = tk.Label(root, text=fisier_search[INDEX], pady=10, **entry_style)
    label_search.pack()
    btn_search_text = tk.Button(root, text=search_textt[INDEX], command = lambda:
        select_comand(1), **button_style)
    btn_search_text.place(relx=0.3, rely=0.3, anchor=tk.CENTER)

    btn_search_speech= tk.Button(root, text=search_speech[INDEX], command = lambda:
        select_comand(2), **button_style)

    btn_search_speech.place(relx=0.7, rely=0.3, anchor=tk.CENTER)

    back_home = tk.Button(root, text=back[INDEX], command = home, **button_style)
    back_home.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

def select_comand(comand):
    """
    Funcția care se ocupă de salvarea comenzii
    """
    # pylint: disable=global-statement
    global COMAND
    COMAND = comand
    print(COMAND)
    if comand == 2 or comand == 1:
        search_text()

def search_text():
    """
    Funcția care se ocupă de crearea butoanelor pentru functionalitatea 
    de search si de stergerea tuturor celorlalte wirget uri
    """
    for widget in root.winfo_children():
        # Șterge widget-ul din interfață
        widget.destroy()

    selected_var = tk.StringVar(root)

    selected_var.set(options[0])

    instructions_label = tk.Label(root, text=tx[INDEX], pady=10,
                                  font =  ('Calibri Light', 18), bg = "#E0D6EB",fg= "black")
    instructions_label.pack(pady= 20)

    option_menu = tk.OptionMenu(root, selected_var, *options, command=save_option2)
    option_menu.configure(bg='#AF9FBF', fg='black', font=('Arial', 12))
    option_menu.pack(pady=40)

    btn_search = tk.Button(root, text=cautare_tts[INDEX],command = open_file_dialog, **button_style)
    btn_search.pack(side='top', pady=10, padx=5)
    btn_back = tk.Button(root, text=back[INDEX], command = search, **button_style)
    btn_back.pack(side='top', pady=10, padx=5)

def save_option2(value):
    """
    Funcția care se ocupă de salvarea optiunii de limba
    """
     # pylint: disable=global-statement
    global INDEX2
    INDEX2 = options.index(value)
def open_file_dialog():
    """
    Funcția care se ocupă de deschiderea fisierului selectat
    """

    if COMAND == 1:
        directory = fisier_tts[INDEX2]
    else:
        if COMAND == 2:
            directory = fisier_stt[INDEX2]

    file_path = filedialog.askopenfilename(initialdir=directory, title="Selectați fisierul",
                filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if file_path:
        print("Fișierul selectat:", file_path)
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        for widget in root.winfo_children():
            widget.destroy()
        label = tk.Label(root, wraplength=500, justify="left")
        label.pack(fill="both", expand=True, padx=20, pady=10)
        label.config(text=content)

        btn_back = tk.Button(root, text=back[INDEX], command = search_text, **button_style)
        btn_back.pack(side='top', pady=10, padx=5)

FILE_NAME_STT= None
RECOGNIZED_TEXT = None
LISTENING = False
DISPLAY_TEXT = None
TEXT = None
FILE_NAME_ENTRY = None
TEXT_RECOGNIZER = None
INDEX = 0
COMAND = 0
INDEX2 = 0
options= ["Romana", "Engleza"]
option = ["ro", "en"]
text_home = ["Selectati optiunea dorita din lista de actiuni!",
             "Select the desired option from the list of actions!"]
btn1 = ["Vorbire in text", "Speech to text"]
btn2 = ["Text in vorbire", "Text to speech"]
btn4 = ["Cautare", "Search"]
btn5 = ["Schimba", "Change"]
fisier_tts = ["Text_to_speech_ro", "Text_to_speech_en"]
fisier_stt = ["Speech_to_text_ro", "Speech_to_text_en"]
search_speech = ["Fisier dictat","Dictation file"]
search_textt = ["Fisier text", "Text File"]
limba = [ "Selectati limba dorita!", "Select the desired language!"]
submit_home = ["Trimite", "Submit"]
back_home_v = ["Acasa", "Home"]
introducere_text=["Introduceți textul aici", "Enter text here"]
nume_fisier = ["Introduceți numele fisierului aici", "Enter filename here"]
back = ["Inapoi", "Back"]
tx = ["Selectati limba in care sunt scrise fisierele pe care le cautati!",
          "Select the language in which the files you are looking for are written!"]
cautare_tts = ["Cauta fisier scris", "Search written file"]
fisier_search = ["Alegeti tipul de fisier pe care doriti sa l cautati!",
                 "Choose the type of file you want to search!"]


button_style = {
    'width': 12,
    'bg': '#AF9FBF',
    'fg': 'black',
    'font': ('Calibri Light', 14)
}
entry_style = {

    'font': ('Calibri Light', 20),
    'bg':'#E0D6EB',
    'fg':'black'
}

root = tk.Tk()
root.geometry('600x500+600+100')
root.config(bg="#E0D6EB")
root.title("Alegere limba")

selecteaza_limba()
root.mainloop()
