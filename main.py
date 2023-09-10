import aisearch
from tkinter import *
from tkinter import messagebox
from tkinter import PhotoImage
import time

class Reversi:

  def __init__(self):
    self.ventana = Tk()
    self.ventana.title("Menu Principal")
    self.ventana.geometry("800x400+0+0")
    self.ventana.minsize(800, 400)
    self.ventana.maxsize(800, 400)
    self.ventana.resizable(False, False)

    #Imagen de fondo
    imagen_fondo = PhotoImage(file="fondo.png")
    fondo_label = Label(self.ventana,
                        image=imagen_fondo,
                        text="Imagen de fondo",
                        bd=0)
    fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

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
    self.ventana.config(menu=self.menubar)
    self.ventana.config(bg="#ECECEC")

    #BOTONES

    #BOTONES --> IMAGEN BOTONES
    image_boton_jugar_6x6 = PhotoImage(file="jugar_6x6.png")
    image_boton_jugar_8x8 = PhotoImage(file="jugar_8x8.png")
    #BOTONES --> CREAR BOTONES
    self.boton1 = Button(self.ventana,
                         text="Jogar",
                         command=lambda: self.Dificultad(6),
                         width=128,
                         height=48,
                         image=image_boton_jugar_6x6,
                         borderwidth=0)
    self.boton1.pack(side=TOP)
    self.boton1.place(x=47, y=100)

    self.boton2 = Button(self.ventana,
                         text="Jogar",
                         command=lambda: self.Dificultad(8),
                         width=128,
                         height=48,
                         image=image_boton_jugar_8x8,
                         borderwidth=0)
    self.boton2.pack(side=TOP)
    self.boton2.place(x=47, y=200)

    mainloop()

  def Dificultad(self, size_tablero):
    self.ventana.destroy()
    #NIVEL DE DIFICULTAD
    self.level = Tk()
    self.level.config(bg="green")
    self.level.title("Dificultad")
    self.level.geometry("200x300+0+0")
    self.level.minsize(200, 300)
    self.level.maxsize(200, 300)
    self.level.resizable(False, False)

    # Obtener el ancho y alto de la pantalla
    self.ancho_pantalla = self.level.winfo_screenwidth()
    self.alto_pantalla = self.level.winfo_screenheight()

    # Calcular las coordenadas para centrar la ventana
    x = (self.ancho_pantalla - self.level.winfo_reqwidth()) / 2
    y = (self.alto_pantalla - self.level.winfo_reqheight()) / 3.8
    # Establecer la ubicación de la ventana centrada
    self.level.geometry("+%d+%d" % (x, y))

    #BOTONES --> IMAGEN BOTONES
    image_boton_facil = PhotoImage(file="facil.png")
    image_boton_medio = PhotoImage(file="medio.png")
    image_boton_dificil = PhotoImage(file="dificil.png")

    boton1 = Button(
        self.level,
        text="",
        command=lambda: self.Jugar(size_tablero, dificultad="facil"),
        width=128,
        height=48,
        image=image_boton_facil,
        borderwidth=0)
    boton1.pack(side=TOP)
    boton1.place(x=30, y=60)

    boton2 = Button(
        self.level,
        text="",
        command=lambda: self.Jugar(size_tablero, dificultad="medio"),
        width=128,
        height=48,
        image=image_boton_medio,
        borderwidth=0)
    boton2.pack(side=TOP)
    boton2.place(x=30, y=130)

    boton3 = Button(
        self.level,
        text="",
        command=lambda: self.Jugar(size_tablero, dificultad="dificil"),
        width=128,
        height=48,
        image=image_boton_dificil,
        borderwidth=0)
    boton3.pack(side=TOP)
    boton3.place(x=30, y=200)

    mainloop()

  def Jugar(self, size_tablero, dificultad):
    #VENTANA DE JUEGO

    self.level.destroy()

    self.principal = Tk()
    self.principal.configure(bg="green")
    self.principal.title("Reversi")
    self.botones = []
    self.bot = PhotoImage(file="bot.png")
    self.raton = PhotoImage(file="player.png")
    self.vacio = PhotoImage(file="vacio.gif")
    self.juego = aisearch.JuegoReversi(size_tablero)
    self.principal.resizable(False, False)

    #creo un boton de reinicio
    reiniciar_boton = Button(self.principal, text="Reiniciar", command=lambda: self.reiniciar_partida(size_tablero))
    reiniciar_boton.grid(row=0, column=1) 

    # Obtener el ancho y alto de la pantalla
    self.ancho_pantalla = self.principal.winfo_screenwidth()
    self.alto_pantalla = self.principal.winfo_screenheight()

    # Calcular las coordenadas para centrar la ventana
    x = (self.ancho_pantalla - self.principal.winfo_reqwidth()) / 3
    y = (self.alto_pantalla - self.principal.winfo_reqheight()) / 7

    # Establecer la ubicación de la ventana centrada
    self.principal.geometry("+%d+%d" % (x, y))

    for i in range(size_tablero):
      fila = []
      for j in range(size_tablero):
        b1 = Button(self.principal, image=self.vacio, width="60", height="60")
        b1.bind("<Button-1>",
                lambda event, size_tablero=size_tablero: self.click(
                    event, size_tablero))
        b1.x = i
        b1.y = j
        b1.grid(row=i + 1, column=j)
        fila.append(b1)
      self.botones.append(fila)

    fila_centro = size_tablero // 2 - 1  # Restar 1 porque las listas comienzan desde 0
    columna_centro = size_tablero // 2 - 1

    # Colocar fichas iniciales al centro

    self.juego.tablero[fila_centro][columna_centro] = 1  # Jugador 1
    self.juego.tablero[fila_centro][columna_centro+1] = -1  # Jugador 2
    self.juego.tablero[fila_centro+1][columna_centro] = -1  # Jugador 2
    self.juego.tablero[fila_centro+1][columna_centro+1] = 1  # Jugador 1
    self.botones[fila_centro][columna_centro].config(image=self.raton)
    self.botones[fila_centro + 1][columna_centro + 1].config(image=self.raton)
    self.botones[fila_centro + 1][columna_centro].config(image=self.bot)
    self.botones[fila_centro][columna_centro + 1].config(image=self.bot)

    #PUNTAJE JUGADORES
    puntaje_player = sum(valor == -1 for valor in self.juego.tablero)
    self.mostrar_player_puntaje = Label(self.principal,
                                        text=f"PLAYER: {puntaje_player}",
                                        fg="white",
                                        bg="green")
    self.mostrar_player_puntaje.grid(row=0, column=0)
    puntaje_bot = sum(valor == 1 for valor in self.juego.tablero)
    self.mostrar_bot_puntaje = Label(self.principal,
                                     text=f"BOT: {puntaje_bot}",
                                     fg="white",
                                     bg="green")
    self.mostrar_bot_puntaje.grid(row=0, column=2)
  def reiniciar_partida(self, size_tablero):
    self.juego.reiniciar()  # Reinicia el juego
    # Limpia el tablero
    for fila in self.botones:
        for boton in fila:
            boton.config(image=self.vacio)
    # Restablece las fichas iniciales
    fila_centro = size_tablero // 2 - 1
    columna_centro = size_tablero // 2 - 1
    self.juego.tablero[fila_centro][columna_centro] = 1
    self.juego.tablero[fila_centro][columna_centro + 1] = -1
    self.juego.tablero[fila_centro + 1][columna_centro] = -1
    self.juego.tablero[fila_centro + 1][columna_centro + 1] = 1
    self.botones[fila_centro][columna_centro].config(image=self.raton)
    self.botones[fila_centro + 1][columna_centro + 1].config(image=self.raton)
    self.botones[fila_centro + 1][columna_centro].config(image=self.bot)
    self.botones[fila_centro][columna_centro + 1].config(image=self.bot)
    # Actualiza la pantalla
    self.principal.update()


  def victoria(self, size_tablero):
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

      fila_centro = size_tablero // 2 - 1  # Restar 1 porque las listas comienzan desde 0
      columna_centro = size_tablero // 2 - 1

      # Colocar fichas iniciales al centro

      self.juego.tablero[fila_centro][columna_centro] = 1  # Jugador 1
      self.juego.tablero[fila_centro][columna_centro+1] = -1  # Jugador 2
      self.juego.tablero[fila_centro+1][columna_centro] = -1  # Jugador 2
      self.juego.tablero[fila_centro+1][columna_centro+1] = 1  # Jugador 1
      self.botones[fila_centro][columna_centro].config(image=self.raton)
      self.botones[fila_centro + 1][columna_centro + 1].config(image=self.raton)
      self.botones[fila_centro + 1][columna_centro].config(image=self.bot)
      self.botones[fila_centro][columna_centro + 1].config(image=self.bot)


      #PUNTAJE JUGADORES
      puntaje_player = sum(valor == -1 for valor in self.juego.tablero)
      self.mostrar_player_puntaje = Label(self.principal,
                                          text=f"PLAYER: {puntaje_player}",
                                          fg="white",
                                          bg="green")
      self.mostrar_player_puntaje.grid(row=0, column=0)
      puntaje_bot = sum(valor == 1 for valor in self.juego.tablero)
      self.mostrar_bot_puntaje = Label(self.principal,
                                       text=f"BOT: {puntaje_bot}",
                                       fg="white",
                                       bg="green")
      self.mostrar_bot_puntaje.grid(row=0, column=2)

      return True
    else:
      return False
  
  

  def click(self, evento, size_tablero):
    
    
    
    if self.juego.tablero[evento.widget.x][evento.widget.y] == 0:
      print("aqui si")
      if self.juego.movimiento_valido(self.juego.tablero, evento.widget.x, evento.widget.y, -1):
        print("hola")
        self.juego.jugar(evento.widget.x, evento.widget.y)
        
        evento.widget["image"] = self.raton
        puntaje_player = sum(valor == -1 for valor in self.juego.tablero)
        self.mostrar_player_puntaje = Label(self.principal,
                                            text=f"PLAYER: {puntaje_player}",
                                            fg="white",
                                            bg="green")
        self.mostrar_player_puntaje.grid(row=0, column=0)
        puntaje_bot = sum(valor == 1 for valor in self.juego.tablero)
        self.mostrar_bot_puntaje = Label(self.principal,
                                        text=f"BOT: {puntaje_bot}",
                                        fg="white",
                                        bg="green")
        self.mostrar_bot_puntaje.grid(row=0, column=2)
        self.principal.update()
        print(self.juego.tablero)

        self.principal.update()
      if not self.victoria(size_tablero):
        o = []
        #m=aisearch.negascout(self.juego,-1000,1000, [], o)
        #m=aisearch.alfabeta(self.juego,1,-1000,1000, [], o)
        valor, movimiento = self.juego.minimax(self.juego.tablero, 1, 4)
        #m=aisearch.negamax(self.juego,[],o)
        if movimiento:
          self.juego.realizar_movimiento(self.juego.tablero, movimiento[0], movimiento[1], 1)
        
        
          print(len(o))
          self.juego.jugar( movimiento[0],movimiento[1])
          self.botones[movimiento[0]][movimiento[1]]["image"] = self.bot
          self.victoria(size_tablero)
          self.principal.update()
    
    for fila,ilera in enumerate(self.juego.tablero):
      for columna,casilla in enumerate(ilera):
        if casilla == 1:
          self.botones[fila][columna].config(image=self.bot)
        
        elif casilla == -1:
          self.botones[fila][columna].config(image=self.raton)
    self.principal.update()
          


juego = Reversi()
