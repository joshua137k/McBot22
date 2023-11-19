from tkinter import * 
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from fpdf import FPDF
from webget import *
import os


    



class App():

    def __init__(self):
        self.root = Tk()
        self.root.geometry("600x600")
        self.root.title("McDonald")
        self.root.pack_propagate(0)
        imagem_caminho = os.path.join(os.path.dirname(__file__), 'lg.png')
        background_image = PhotoImage(file=imagem_caminho)
        background_label = Label(self.root, image=background_image)
        background_label.place(relwidth=1, relheight=1)
        self.root.resizable(0, 0)

        self.frame = Frame(self.root, bg='white', bd=1)


        style = ttk.Style()
        style.theme_use("clam")

        self.root.configure(bg="#ECECEC")

        self.start_button = Button(self.frame, text="Start", command=self.on_start_click, bg="#4CAF50", fg="white", font=("Arial", 14))

        self.voltar =  Button(self.root, text="Voltar", command=self.pac, bg="#FF8197", fg="white", font=("Arial", 14))
        self.voltar.place(x=0,y=0)



        self.menu = Menu(self.root, tearoff=0)
        self.menu.add_command(label="Cortar", command=self.cortar)
        self.menu.add_command(label="Copiar", command=self.copiar)
        self.menu.add_command(label="Colar", command=self.colar)
        self.menuobj=None
        self.root.bind("<Button-1>", lambda event: self.menu.unpost())


        self.go_button=None


        self.start=[self.start_button,]
        self.widgets=[]

        self.pac()

        self.root.mainloop()


    def show_context_menu(self,event,obj):
        self.menu.post(event.x_root, event.y_root)
        self.menuobj=obj

    def cortar(self):
        self.menuobj.event_generate("<<Cut>>")

    def copiar(self):
        self.menuobj.event_generate("<<Copy>>")

    def colar(self):
        self.menuobj.event_generate("<<Paste>>")


    def forget(self):
        self.menuobj=None
        self.frame.forget()

        self.widgets+=self.start
        if self.go_button!=None:
            self.widgets.append(self.go_button)

        for i in self.widgets:
            i.pack_forget()
        self.widgets=[]#limpar tela 


    def pac(self):

        self.forget()

        self.frame.pack(pady=100)

        for i in self.start:
            i.pack(side=TOP, padx=10, pady=10)#colocar botões em tela
        




    def on_go_click(self,name,text):
        print(name)
        
        file_path = filedialog.asksaveasfilename(
            initialdir="/",  # Diretório inicial
            title="Selecione o local para salvar o arquivo",  # Título da janela
            filetypes=(("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")),  # Tipos de arquivo permitidos
            defaultextension=".pdf"  # Extensão padrão
        )

        if file_path:
            print(f"Arquivo PDF selecionado: {file_path}")
            urls=[]
            for i in text.split("\n"):
                i.strip()
                if "mcdonaldspt.workplace.com" in i:
                    i=i.replace("mcdonaldspt.workplace","mcdonaldspt.m.workplace")
                    urls.append(i)
                elif "mcdonaldspt.m.workplace.com" in i:
                    urls.append(i)
            f=open("teste.txt","w")
            f.write("")
            f.close()
            main(urls)



            # Cria um arquivo PDF usando a biblioteca reportlab
            
            self.create_pdf(file_path,name, self.getContent(name))


        self.pac()


    def getContent(self,t):
        a = open("teste.txt","r")
        f = ""
        for i,v in enumerate(a):
            if i%2==0:
                new={}
                v=eval(v)
                for dicionario in v:
                    for pessoa, contagem in dicionario.items():
                        new[pessoa] = new.get(pessoa, 0) + contagem
                
                f+=("Nº Comment:" + str(len(v))   +"\n"+str(str(new)))
            else:
                f+=(" LINK: "+v+"\n")
                

        a.close()



        a=f.split("\n")
        newa=[]
        for i in a:
            if i!="":
                newa.append(i)




        new={}

        for i,v in enumerate(newa):
            if i%2!=0:
                v=eval(v.split("LINK")[0])
                for k in v:
                    if k in new:
                        new[k]+=v[k]
                    else:
                        new[k]=v[k]
        f+="\n\nTotal:\n"+str(new)+"\n\n"
        return t+"\n\n"+f


    def create_pdf(self,file_path, title, content):
        pdf = FPDF()
        pdf.add_page()
        
        # Font settings
        pdf.set_font("Helvetica", size=12)
        
        # Title
       # pdf.cell(200, 10, text="Title: " + title)
        
        # Content
        pdf.multi_cell(0, 10, text=content)
        
        # Save the PDF
        pdf.output(file_path)



       
    def on_start_click(self):
        self.forget()

        l=Label(self.root, text="Coloque aqui os link para os posts que serão \n avaliados, obs:Title é o aonde o arquivo que irá salvar os dados \n")
        l.pack(side = TOP)

        self.widgets.append(l)

        l=Label(self.root, text="Title")
        l.pack(side = TOP)

        self.widgets.append(l)

        v = Entry(self.root,width=50)
        v.pack(side = TOP, padx=10, pady=5)
        v.bind("<Button-3>", lambda event:self.show_context_menu(event,v))

        self.widgets.append(v)



        l=Label(self.root, text="URL")
        l.pack(side = TOP)

        self.widgets.append(l)
        
        entry =Text(self.root, width=50, height=20)
        entry.pack(side = TOP, padx=10, pady=5)
        entry.bind("<Button-3>", lambda event, entry=entry:self.show_context_menu(event,entry))

        self.widgets.append(entry)
            
        # Cria o botão "Go"
        self.go_button = Button(self.root, text="Go", command=lambda:self.on_go_click(v.get(),entry.get("1.0", "end-1c")), bg="#FFC107", fg="white", font=("Arial", 14))
        self.go_button.pack()

if __name__ == "__main__":
    app = App()
