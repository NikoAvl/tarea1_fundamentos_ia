import aisearch
from tkinter import *
from tkinter import messagebox
from tkinter import PhotoImage

class Gato:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.title("Menu Principal")
        self.ventana.geometry("800x400+0+0")
        self.ventana.minsize(800,400)

        #Imagen de fondo 
        imagen_fondo = PhotoImage(file="fondo.png")
        fondo_label = Label(self.ventana, image=imagen_fondo, text="Imagen de fondo",bd=0)
        fondo_label.place(x=0,y=0,relwidth=1, relheight=1)
        

        # Obtener el ancho y alto de la pantalla
        self.ancho_pantalla = self.ventana.winfo_screenwidth()
        self.alto_pantalla = self.ventana.winfo_screenheight()

        # Calcular las coordenadas para centrar la ventana
        x = (self.ancho_pantalla - self.ventana.winfo_reqwidth()) / 3.8
        y = (self.alto_pantalla - self.ventana.winfo_reqheight()) / 3.8

        # Establecer la ubicación de la ventana centrada
        self.ventana.geometry("+%d+%d" % (x, y))

        #Menu Bar
        self.menubar = Menu(self.ventana)
        self.ventana.config(menu= self.menubar)
        self.ventana.config(bg= "#ECECEC")

        #BOTONES

            #BOTONES --> IMAGEN BOTONES
        image_boton_jugar = PhotoImage(file="boton_jugar.png")
        
            #BOTONES --> CREAR BOTONES
        self.boton1 = Button(self.ventana,text="Jogar",command=self.Jugar,width=128,height=48, image=image_boton_jugar,borderwidth=0)
        self.boton1.pack(side=TOP)
        self.boton1.place(x=47,y=100)
        
        mainloop()


        




    def Jugar(self):
    #VENTANA DE JUEGO
        self.ventana.destroy()

        self.principal = Tk()
        self.principal.title("Gato")
        self.botones=[]
        self.gato=PhotoImage(file="gato.gif")
        self.raton=PhotoImage(file="raton.gif")
        self.vacio=PhotoImage(file="vacio.gif")
        self.juego=aisearch.JuegoGato()

         # Obtener el ancho y alto de la pantalla
        self.ancho_pantalla = self.principal.winfo_screenwidth()
        self.alto_pantalla = self.principal.winfo_screenheight()

        # Calcular las coordenadas para centrar la ventana
        x = (self.ancho_pantalla - self.principal.winfo_reqwidth()) / 3
        y = (self.alto_pantalla - self.principal.winfo_reqheight()) / 5

        # Establecer la ubicación de la ventana centrada
        self.principal.geometry("+%d+%d" % (x, y))

        for i in range(6):
            fila=[]
            for j in range(6):
                b1=Button(self.principal,image=self.vacio,width="80",height="80")
                b1.bind("<Button-1>",self.click)
                b1.x=i
                b1.y=j
                b1.grid(row=i,column=j)
                fila.append(b1)
            self.botones.append(fila)
        
    def victoria(self):
        if self.juego.estado_final():
            if self.juego.ganador == -1:
                messagebox.showinfo("Juego del Gato", "Has ganado!")
            elif self.juego.ganador == 0:
                messagebox.showinfo("Juego del Gato", "Empate")
            else:
                messagebox.showinfo("Juego del Gato", "Has perdido")
            self.juego.reiniciar()
            for i in range(6):
                for j in range(6):
                    self.botones[i][j]["image"] = self.vacio
            return True
        else:
            return False
    
    def click(self,evento):
        if self.juego.tablero[evento.widget.x * 6 + evento.widget.y]==0:
            self.juego.jugar(evento.widget.x * 6 + evento.widget.y)
            evento.widget["image"] = self.raton
            self.principal.update()
            if not self.victoria():
                o=[]
                #m=aisearch.negascout(self.juego,-1000,1000, [], o)
                #m=aisearch.alfabeta(self.juego,1,-1000,1000, [], o)
                m=aisearch.minimax(self.juego, 1, [], o)
                #m=aisearch.negamax(self.juego,[],o)
                print(len(o))
                self.juego.jugar(m[1])
                self.botones[m[1]//3][m[1]%3]["image"]=self.gato
                self.principal.update()
                self.victoria()

        


    

juego=Gato()
