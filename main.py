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
        image_boton_jugar_6x6 = PhotoImage(file="boton_jugar_6x6.png")
        image_boton_jugar_8x8 = PhotoImage(file="boton_jugar_8x8.png")
            #BOTONES --> CREAR BOTONES
        self.boton1 = Button(self.ventana,text="Jogar",command=lambda: self.Jugar(6),width=128,height=48, image=image_boton_jugar_6x6,borderwidth=0)
        self.boton1.pack(side=TOP)
        self.boton1.place(x=47,y=100)

        self.boton2 = Button(self.ventana,text="Jogar",command=lambda: self.Jugar(8),width=128,height=48, image=image_boton_jugar_8x8,borderwidth=0)
        self.boton2.pack(side=TOP)
        self.boton2.place(x=47,y=200)
        
        mainloop()


        




    def Jugar(self,size_tablero):
    #VENTANA DE JUEGO
        
        self.ventana.destroy()
        
        self.principal = Tk()
        self.principal.title("Reversi")
        self.botones=[]
        self.bot=PhotoImage(file="bot.png")
        self.raton=PhotoImage(file="player.png")
        self.vacio=PhotoImage(file="vacio.gif")
        self.juego=aisearch.JuegoGato(size_tablero)
        
        

         # Obtener el ancho y alto de la pantalla
        self.ancho_pantalla = self.principal.winfo_screenwidth()
        self.alto_pantalla = self.principal.winfo_screenheight()

        # Calcular las coordenadas para centrar la ventana
        x = (self.ancho_pantalla - self.principal.winfo_reqwidth()) / 3
        y = (self.alto_pantalla - self.principal.winfo_reqheight()) / 7

        # Establecer la ubicación de la ventana centrada
        self.principal.geometry("+%d+%d" % (x, y))

        for i in range(size_tablero):
            fila=[]
            for j in range(size_tablero):
                b1=Button(self.principal,image=self.vacio,width="60",height="60")
                b1.bind("<Button-1>",lambda event, size_tablero=size_tablero: self.click(event,size_tablero))
                b1.x=i
                b1.y=j
                b1.grid(row=i,column=j)
                fila.append(b1)
            self.botones.append(fila)

        fila_centro = size_tablero // 2 - 1  # Restar 1 porque las listas comienzan desde 0
        columna_centro = size_tablero // 2 - 1

            # Convertir coordenadas a índices y colocar fichas en el centro
        self.indice_1 = self.convertir_coordenadas_a_indice(fila_centro, columna_centro,size_tablero)
        self.indice_2 = self.convertir_coordenadas_a_indice(fila_centro, columna_centro + 1,size_tablero)
        self.indice_3 = self.convertir_coordenadas_a_indice(fila_centro + 1, columna_centro,size_tablero)
        self.indice_4 = self.convertir_coordenadas_a_indice(fila_centro + 1, columna_centro + 1,size_tablero)
        self.juego.tablero[self.indice_1] = 1  # Jugador 1
        self.juego.tablero[self.indice_2] = -1  # Jugador 2
        self.juego.tablero[self.indice_3] = -1  # Jugador 2
        self.juego.tablero[self.indice_4] = 1  # Jugador 1
        self.botones[fila_centro][columna_centro].config(image = self.raton)
        self.botones[fila_centro+1][columna_centro+1].config(image = self.raton)
        self.botones[fila_centro+1][columna_centro].config(image = self.bot)
        self.botones[fila_centro][columna_centro+1].config(image = self.bot)
        
    
    def convertir_coordenadas_a_indice(self, fila, columna,size_tablero):
        # Convertir coordenadas 2D en índice 1D
        return fila * size_tablero + columna

    def victoria(self,size_tablero):
        if self.juego.estado_final():
            if self.juego.ganador == -1:
                messagebox.showinfo("Juego del Gato", "Has ganado!")
            elif self.juego.ganador == 0:
                messagebox.showinfo("Juego del Gato", "Empate")
            else:
                messagebox.showinfo("Juego del Gato", "Has perdido")
            self.juego.reiniciar()
            for i in range(size_tablero):
                for j in range(size_tablero):
                    self.botones[i][j]["image"] = self.vacio
            return True
        else:
            return False
    
    def click(self,evento,size_tablero):
        
        if self.juego.tablero[evento.widget.x * size_tablero + evento.widget.y]==0:
            self.juego.jugar(evento.widget.x * size_tablero + evento.widget.y)
            evento.widget["image"] = self.raton
            print(self.juego.tablero)
            
            
            self.principal.update()
            if not self.victoria(size_tablero):
                o=[]
                #m=aisearch.negascout(self.juego,-1000,1000, [], o)
                #m=aisearch.alfabeta(self.juego,1,-1000,1000, [], o)
                m=aisearch.minimax(self.juego, 1, [], o)
                #m=aisearch.negamax(self.juego,[],o)
                print(len(o))
                self.juego.jugar(m[1])
                self.botones[m[1]//3][m[1]%3]["image"]=self.bot
                self.principal.update()
                self.victoria(size_tablero)

        




juego=Gato()

