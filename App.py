import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import os
import re
from namedentities import unicode_entities as uni

class App():
    def __init__(self):
        self.window = tk.Tk()
        self.window_width = self.window_height = 400
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.window.title("ANALISADOR XML")
        self.window.resizable(False, False)
        self.window.configure(background="white")
        self.widgets = {}
        self.desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
        self.isCanceled = False
        self.origin_path = self.destiny_path = ""
        self.selected_option = tk.StringVar()
        self.characters_table = {
            "á" : "a", "à" : "a", "â" : "a", "ã" : "a", "Á" : "A", "À" : "A", 
            "Â" : "A", "Ã" : "A", "ç" : "c", "Ç" : "C", "é" : "e", "è" : "e",
            "ê" : "e", "É" : "E", "È" : "E", "Ê" : "E", "í" : "i", "ì" : "i",
            "î" : "i", "Í" : "I", "Ì" : "I", "Î" : "I", "ñ" : "n", "Ñ" : "N",
            "ó" : "o", "ò" : "o", "ô" : "o", "õ" : "o", "Ó" : "O", "Ò" : "O",
            "Ô" : "O", "Õ" : "O", "ú" : "u", "ù" : "u", "û" : "u", "ü": "u",
             "Ú" : "U", "Ù" : "U", "Û" : "U", "Ü" : "U", "º" : ""}

        self.set_window_geometry(
            self.window,
            self.window_width,
            self.window_height)
        self.create_window_elements()
        self.window.mainloop()

    def set_window_geometry(self, window, w_width, w_heigth):
        x_cordinate = int((self.screen_width/2) - (w_width/2))
        y_cordinate = int((self.screen_height/2) - (w_heigth/2))

        window.geometry(f'{w_width}x{w_heigth}+{x_cordinate}+{y_cordinate}')

    def create_window_elements(self):
        xml_image = tk.PhotoImage(file='./images/xml.png')
        xml_label = tk.Label(
            self.window,
            image=xml_image,
            borderwidth=0)
        self.widgets["xml_label"] = xml_label
        self.widgets["xml_image"] = xml_image
        xml_label.place(x=5, y=35)

        origin_label = tk.Label(
            self.window,
            text="ORIGEM:",
            font=("Arial", 14, "bold"),
            background="white")
        self.widgets["origin_label"] = origin_label
        origin_label.place(x=5, y=245)

        destiny_label = tk.Label(
            self.window,
            text="DESTINO:",
            font=("Arial", 14, "bold"),
            background="white")
        self.widgets["destiny_label"] = destiny_label
        destiny_label.place(x=5, y=290)

        origin_text = tk.Text(
            self.window,
            state="disabled",
            width=30)
        self.widgets["origin_text"] = origin_text

        origin_text.place(x=105, y=250, height=22)

        destiny_text = tk.Text(
            self.window,
            state="disabled",
            width=30)
        self.widgets["destiny_text"] = destiny_text
        destiny_text.place(x=105, y=293, height=22)

        folder_image = tk.PhotoImage(file="./images/folder1.png")
        self.widgets["folder_image"] = folder_image
        
        origin_label_folder = tk.Button(
            self.window,
            image=folder_image,
            borderwidth=0,
            cursor="hand2",
            command=self.choose_origin_path)
        self.widgets["origin_label_folder"] = origin_label_folder
        origin_label_folder.place(x=355, y=245)

        destiny_label_folder = tk.Button(
            self.window,
            image=folder_image,
            borderwidth=0,
            cursor="hand2",
            command=self.choose_destiny_path)
        self.widgets["destiny_label_folder"] = destiny_label_folder
        destiny_label_folder.place(x=355, y=288)

        option1_image = tk.PhotoImage(file="./images/option1.png")
        option1_radio = tk.Radiobutton(
            self.window,
            image=option1_image,
            borderwidth=0,
            bg="white",
            variable=self.selected_option,
            value=1)
        option1_radio.select()
        self.widgets["option1_image"] = option1_image
        self.widgets["option1_radio"] = option1_radio
        option1_radio.place(x=180, y=40)

        option2_image = tk.PhotoImage(file="./images/option2.png")
        option2_radio = tk.Radiobutton(
            self.window,
            image=option2_image,
            borderwidth=0,
            bg="white",
            variable=self.selected_option,
            value=2)
        self.widgets["option2_image"] = option2_image
        self.widgets["option2_radio"] = option2_radio
        option2_radio.place(x=180, y=100)

        option3_image = tk.PhotoImage(file="./images/option3.png")
        option3_radio = tk.Radiobutton(
            self.window,
            image=option3_image,
            borderwidth=0,
            bg="white",
            variable=self.selected_option,
            value=3)
        self.widgets["option3_image"] = option3_image
        self.widgets["option3_radio"] = option3_radio
        option3_radio.place(x=180, y=160)

        init_button_image = tk.PhotoImage(file="./images/init_button.png")
        init_button = tk.Button(
            self.window,
            image=init_button_image,
            borderwidth=0,
            bg="white",
            cursor="hand2",
            command=self.start)
        self.widgets["init_button_image"] = init_button_image
        self.widgets["init_button"] = init_button
        init_button.bind("<Enter>", lambda x: self.button_change(init_button, "enter"))
        init_button.bind("<Leave>", lambda x: self.button_change(init_button, "leave"))
        init_button.place(x=130, y=340)

    def choose_origin_path(self):
        filename = fd.askopenfilenames(
            filetypes=[("Arquivos XML", "*.xml")],
            initialdir=self.desktop_path,
            parent=self.window,
            title="SELECIONE UM OU MAIS ARQUIVOS XML:")

        if(not filename.__len__() == 0):
            self.origin_path = filename
            text_box_origin = self.widgets.get("origin_text")
            self.update_text_box([text_box_origin], filename[0])

    def choose_destiny_path(self):
        filename = fd.askdirectory(
            parent=self.window,
            initialdir=(self.origin_path
                            if self.origin_path != ""
                            else self.desktop_path),
             title="SELECIONE A PASTA DE DESTINO:")

        if(not filename.__len__() == 0):
            self.destiny_path = f'{filename}/saída'
            text_box_destiny = self.widgets.get("destiny_text")
            self.update_text_box([text_box_destiny], filename)

    def update_text_box(self, text_boxes, text):
        for box in text_boxes:
            box.configure(state="normal")
            box.delete("1.0", "end")
            box.insert(tk.END, text)
            box.configure(state="disabled")

    def button_change(self, button, event):
        image = tk.PhotoImage(
            file=("./images/init_button_hover.png"
                if event == "enter"
                else "./images/init_button.png"))
        self.widgets["init_button_image"] = image
        button.config(image=image)

    def clear_special_characters(self):
        output_file = ""
        file_qty = self.origin_path.__len__() 

        try:
            for file in self.origin_path:
                with open(file, "r", encoding="latin1") as input:
                    unidecoded_read_file = uni(input.read())
                    translation_table = unidecoded_read_file.maketrans(self.characters_table)
                    output_file =  unidecoded_read_file.translate(translation_table)

                self.create_destiny_folder()

                with open(os.path.join(self.destiny_path, os.path.basename(file)), "w", encoding="latin1") as output:
                    output.write(output_file)

            message = (f'{file_qty} arquivo processado com sucesso!'
                        if file_qty == 1
                        else f'{file_qty} arquivos processados com sucesso!')

            mb.showinfo("AVISO!", message)

        except FileNotFoundError:
            mb.showerror("ERRO!", "Caminho de origem ou destino não existe!")
            self.origin_path = self.destiny_path = ""
            text_box_origin = self.widgets.get("origin_text")
            text_box_destiny = self.widgets.get("destiny_text")
            self.update_text_box([text_box_origin, text_box_destiny], "")

        except UnicodeDecodeError:
            mb.showerror("ERRO!", "Falha ao realizar o decode do arquivo!")

        except BaseException as e:
            mb.showerror("ERRO!", e)

    def split_file(self):
        try:
            if(self.origin_path.__len__() > 1): raise Exception("Selecione apenas um arquivo!")

            with open(self.origin_path[0], "r", encoding="latin1") as input:
                tag_name = self.get_user_input('INFORME A TAG DE SEPARAÇÃO \n NO FORMATO "<TAG>"') 

                if(self.isCanceled is True): return
                elif(tag_name is False): raise Exception("Informe uma tag para realizar a divisão!")

                unidecoded_read_file = uni(input.read())
                doc_headers_result = re.findall("<\?[\s\S]*\?>", unidecoded_read_file)
                doc_headers = doc_headers_result[0] if doc_headers_result.__len__() > 0 else ""
                delimiter_tag_wo_prefix = self.remove_prefixes(tag_name)
                unidecoded_read_file_wo_prefix = self.remove_prefixes(unidecoded_read_file)

            separated_docs = re.findall(
                f'{delimiter_tag_wo_prefix}[\s\S]*?</{delimiter_tag_wo_prefix.replace("<", "")}',
                unidecoded_read_file_wo_prefix)

            if (separated_docs.__len__() < 1): 
                raise Exception("Não foi possível dividir o arquivo, verifique a tag informada!")

            self.create_destiny_folder()

            for index, doc in enumerate(separated_docs):
                with open(f'{self.destiny_path}/{index + 1}.xml', "w", encoding="latin1") as output:
                    output.write(doc_headers + doc)
            
            mb.showinfo("AVISO!",
             'Separação concluída!'
             '\nO arquivo gerou '
             f'{separated_docs.__len__()} {"notas." if separated_docs.__len__() > 1 else "nota."}')
        
        
        except FileNotFoundError:
            mb.showerror("ERRO!", "Arquivo de origem ou destino não encontrado!")

        except UnicodeDecodeError:
            mb.showerror("ERRO!", "Falha ao realizar o decode do arquivo!")
   
        except BaseException as e:
            mb.showerror("ERRO!", e)

    def create_destiny_folder(self):
        if(not os.path.exists(self.destiny_path)): os.mkdir(self.destiny_path)

    def remove_prefixes(self, doc):
        remove_prefix_opentag = "<[^\/][\S]{0,10}:"
        remove_prefix_closetag = "<\/[\S]{0,10}:"

        output_string = re.sub(remove_prefix_opentag, "<", doc)
        return re.sub(remove_prefix_closetag, "</", output_string)
        
    def get_user_input(self, message):
        self.isCanceled=False
        user_input = tk.StringVar()

        def cancel_handler():
            top_level.destroy()
            self.isCanceled=True

        top_level = tk.Toplevel(
            master=self.window,
            background="white",
            highlightthickness=4)
        top_level.configure(highlightbackground="black")
        top_level.overrideredirect(True)
        top_level.focus()
        self.set_window_geometry(top_level, 250, 110)
        top_level.bind("<FocusOut>", lambda x: cancel_handler())

        label = tk.Label(
            master=top_level,
            text=message,
            font=("Arial", 10, "bold"),
            background="white")
        label.pack()

        delimiter_tag = tk.Entry(
            master=top_level,
            width=30,
            highlightthickness=1,
            textvariable=user_input,
            font=("Arial", 10))
        delimiter_tag.configure(highlightbackground="black")
        delimiter_tag.pack()

        ok_button = tk.Button(
            master=top_level,
            background="#66FF00",
            font=("Arial", 12, "bold"),
            text="✔",
            cursor="hand2",
            width=3,
            borderwidth=0,
            command=lambda: top_level.destroy())

        cancel_button = tk.Button(
            master=top_level,
            background="red",
            font=("Arial", 12, "bold"),
            text="❌",
            cursor="hand2",
            width=3,
            borderwidth=0,
            command=cancel_handler)
        
        ok_button.place(x=78, y=68)
        cancel_button.place(x=132, y=68)

        self.window.wait_window(top_level)

        return user_input.get() if user_input.get() !="" else False
        
    def remove_tag(self):
        try:
            tag_name = self.get_user_input('INFORME A TAG QUE DESEJA \n REMOVER NO FORMATO "<TAG>":')

            if(self.isCanceled is True): return
            elif(tag_name is False): raise Exception("Informe uma tag para remover!")

            sanitized_tag_name = self.sanitize_tag_name(tag_name)
            self.create_destiny_folder()

            for index, file in enumerate(self.origin_path):
                output = ""

                with open(file, "r", encoding="latin1") as input:
                    output = re.sub("<{tag}>[\s\S]*<\/{tag}>".format(tag=sanitized_tag_name), "", input.read())
                
                with open(f'{self.destiny_path}/{index + 1}.xml', "w", encoding="latin1") as output_file:
                    output_file.write(output)

            path_length = self.origin_path.__len__()
            message = (f'{path_length} notas processadas com sucesso.'
                        if path_length > 1
                        else f'{path_length} nota processada com sucesso.')
            mb.showinfo("AVISO!", message)

        except FileNotFoundError:
            mb.showerror("ERRO!", "Arquivo de origem ou destino não encontrado!")

        except UnicodeDecodeError:
            mb.showerror("ERRO!", "Falha ao realizar o decode do arquivo!")

        except BaseException as e:
            mb.showerror("ERRO!", e)

    def sanitize_tag_name(self, tag):
        return re.sub("[<|>]", "", tag)  

    def start(self):
        if(self.origin_path.__len__() < 1 and self.destiny_path == ""):
             mb.showerror("ERRO!", "Selecione a origem e o destino!")
             return
        elif(self.origin_path.__len__() < 1): 
            mb.showerror("ERRO!", "Arquivo de origem não selecionado!")
            return
        elif(self.destiny_path == ""): 
            mb.showerror("ERRO!", "Caminho de destino não selecionado!")
            return

        match self.selected_option.get():
            case "1": self.clear_special_characters()
            case "2": self.split_file()
            case "3": self.remove_tag()

if __name__ == "__main__":
    app = App()
    




