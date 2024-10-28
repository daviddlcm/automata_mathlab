from tkinter import *
from tkinter import filedialog, messagebox, ttk
import os
from automaton import Automaton
from extracts import extract_text_pdf, extract_text_txt, extract_text_docx

automaton = Automaton('grafoFinalFinal.xml')
valids = []

def select_file():
    file = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=[
            ("All Files", "*.docx *.txt *.pdf"), 
            ("Word files", "*.docx"),
            ("Text files", "*.txt"),
            ("PDF files", "*.pdf")
        ]
    )

    if file:
        extension = os.path.splitext(file)[1].lower()
        if extension in ['.pdf', '.txt', '.docx']:
            if extension == '.pdf':
                data = extract_text_pdf(file)
                sentData(data)
            elif extension == '.txt':
                data = extract_text_txt(file)
                sentData(data)
            elif extension == '.docx':
                data = extract_text_docx(file)
                sentData(data)
            
            messagebox.showinfo("Información", "Archivo seleccionado correctamente")
        else:
            messagebox.showerror("Error", "Archivo no permitido")
    else:
        messagebox.showerror("Sin selección", "No seleccionaste ningún archivo")

def sentData(data):
    global valids
    valids = readData(data)
    print(valids)
    update_table()

def readData(data):
    return automaton.find_automaton(data)

def update_table():
    for row in table.get_children():
        table.delete(row)

    for idx, (funcion, inicio, fin) in enumerate(valids, 1):
        table.insert('', 'end', text=str(idx), values=(funcion, inicio, fin))


raiz = Tk()
raiz.title("Validador de funciones mathLab")
raiz.minsize(600, 600)
raiz.config(bg="#dedede")


title_frame = Frame(raiz, bg="#dedede")
title_frame.pack(pady=10)

label_title = Label(title_frame, text="MathLab", font=("Arial", 16))
label_title.pack(padx=10)

label_subtitle = Label(title_frame, text="Validador de funciones mathLab", font=("Arial", 10))
label_subtitle.pack()

label_select_file = Label(title_frame, text="Selecciona un archivo para analizar en el autómata", font=("Arial", 10))
label_select_file.pack(pady=20)

button_select_file = Button(title_frame, text="Selecciona un archivo", font=("Arial", 10), command=select_file)
button_select_file.pack()

table_frame = Frame(raiz)
table_frame.pack(pady=20, fill='both', expand=True)


table = ttk.Treeview(table_frame, columns=("Función", "Inicio", "Fin"), show="headings")
table.heading("Función", text="Función")
table.heading("Inicio", text="Posición Inicial")
table.heading("Fin", text="Posición Final")
table.column("Función", width=400)  
table.column("Inicio", width=100)
table.column("Fin", width=100)


scrollbar = Scrollbar(table_frame, orient="vertical", command=table.yview)
table.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")


table.pack(fill='both', expand=True)

raiz.mainloop()
