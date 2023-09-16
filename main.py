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
    self.jugador = -1 #se define el jugador que partira jugando (-1 player, 1 bot)
    self.movimientos_posibles = True
    self.elegir_dificultad = 0 #variable a utilizar para definir la dificultad (profundidad minimax)

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
    if dificultad == "facil":
      self.elegir_dificultad = 2
    elif dificultad == "medio":
      self.elegir_dificultad = 3
    elif dificultad == "dificil":
      self.elegir_dificultad = 4
    
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
    reiniciar_boton = Button(self.principal, text="Reiniciar", command=lambda: self.reiniciar_partida(),bg="blue",fg="white")
    reiniciar_boton.grid(row=0, column=5) 

    # Obtener el ancho y alto de la pantalla
    self.ancho_pantalla = self.principal.winfo_screenwidth()
    self.alto_pantalla = self.principal.winfo_screenheight()

    # Calcular las coordenadas para centrar la ventana
    x = (self.ancho_pantalla - self.principal.winfo_reqwidth()) / 3
    y = (self.alto_pantalla - self.principal.winfo_reqheight()) / 7

    # Establecer la ubicación de la ventana centrada
    self.principal.geometry("+%d+%d" % (x, y))

    try:
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
    except:
      print("Algo salió mal")

    fila_centro = size_tablero // 2 - 1  # Restar 1 porque las listas comienzan desde 0
    columna_centro = size_tablero // 2 - 1

    # Colocar fichas iniciales al centro

    self.juego.tablero[fila_centro][columna_centro] = 1  # Jugador 1
    self.juego.tablero[fila_centro][columna_centro+1] = -1  # Jugador 2
    self.juego.tablero[fila_centro+1][columna_centro] = -1  # Jugador 2
    self.juego.tablero[fila_centro+1][columna_centro+1] = 1  # Jugador 1
    self.botones[fila_centro][columna_centro].config(image=self.bot)
    self.botones[fila_centro + 1][columna_centro + 1].config(image=self.bot)
    self.botones[fila_centro + 1][columna_centro].config(image=self.raton)
    self.botones[fila_centro][columna_centro + 1].config(image=self.raton)

    #mostrar puntaje
    contador_player, contador_bot = self.juego.contar_fichas(self.juego.tablero)

    label_puntaje_player = Label(self.principal,text=f"player: {contador_player}",bg="green",fg="red")  
    label_puntaje_bot = Label(self.principal,text=f"bot: {contador_bot}",bg="green",fg="blue")  
    label_puntaje_player.grid(row=0,column=0)
    label_puntaje_bot.grid(row=0,column=1)
    
    #BOTON PARA AYUDAR AL PLAYER
    self.imagen_ayuda_jugador = PhotoImage(file="vacio_movimiento_posible.gif")
    solicitar_ayuda = Button(self.principal, text="ayuda", command=lambda: self.ayudar_player(),bg="blue",fg="white")
    solicitar_ayuda.grid(row=0, column=4)
    
  def ayudar_player(self):
    try:
      valor,movimiento = self.juego.minimax(self.juego.tablero,-1,profundidad=4)
      self.botones[movimiento[0]][movimiento[1]].config(image=self.imagen_ayuda_jugador)
    except:
      messagebox.showinfo("No se ha encontrado ningun movimiento posible!")
    
  def reiniciar_partida(self):
    self.juego.reiniciar()  # Reinicia el juego
    # Limpia el tablero
    self.principal.destroy()
    nueva_partida = Reversi()
    
  def victoria(self):
    contador_player, contador_bot = self.juego.contar_fichas(self.juego.tablero)

    if contador_player > contador_bot:
      messagebox.showinfo(message="GANASTE!",title="Ganador")
              
    elif contador_bot > contador_player:
      messagebox.showinfo(message="Perdiste :c",title="Ganador")
    else:
      messagebox.showinfo(message="Empate...",title="Ganador")
  
  def click(self, evento, size_tablero):
    self.movimientos_posibles = True
    
    if self.juego.tablero[evento.widget.x][evento.widget.y] == 0:
      print("aqui si")
      if self.jugador == -1:
        print("hola")
        fila = evento.widget.x
        columna = evento.widget.y
        
        if self.juego.movimiento_valido(self.juego.tablero,fila,columna,self.jugador):
        
          self.juego.realizar_movimiento(self.juego.tablero,fila,columna,self.jugador)
          self.jugador = 1
          self.movimientos_posibles = True

          self.principal.update()
          print(self.juego.tablero)

          for fila,ilera in enumerate(self.juego.tablero):
            for columna,casilla in enumerate(ilera):
              if casilla == -1:
                self.botones[fila][columna].config(image=self.raton)
                self.principal.update()
              if casilla == -0:
                self.botones[fila][columna].config(image=self.vacio)
                self.principal.update()

          self.principal.update()
          
      while True:
        if self.jugador == 1:
          
          movimientos_validos = self.juego.obtener_movimientos_validos(self.juego.tablero,self.jugador)

          if movimientos_validos:
            valor,movimiento = self.juego.minimax(self.juego.tablero,self.jugador,profundidad=self.elegir_dificultad)
            if movimiento:
              self.juego.realizar_movimiento(self.juego.tablero,movimiento[0],movimiento[1],self.jugador)
              self.movimientos_posibles = True
              
              time.sleep(1)
              for fila,ilera in enumerate(self.juego.tablero):
                for columna,casilla in enumerate(ilera):
                  if casilla == 1:
                    self.botones[fila][columna].config(image=self.bot)
                    self.principal.update()
              
              self.principal.update()
        
        saltar_turno = self.juego.obtener_movimientos_validos(self.juego.tablero,-1)
        print(saltar_turno)
        if saltar_turno:
          print("Saltando turno")
          self.jugador = -1
          break
        
        elif not movimientos_validos:
          break
        
    self.principal.update()
    
    saltar_turno = self.juego.obtener_movimientos_validos(self.juego.tablero,-1)
    movimientos_validos = self.juego.obtener_movimientos_validos(self.juego.tablero,self.jugador)
    
    if not saltar_turno and not movimientos_validos:
      self.victoria()
      self.reiniciar_partida()
      
    contador_player, contador_bot = self.juego.contar_fichas(self.juego.tablero)

    label_puntaje_player = Label(self.principal,text=f"player: {contador_player}",bg="green",fg="red")  
    label_puntaje_bot = Label(self.principal,text=f"bot: {contador_bot}",bg="green",fg="blue")  
    label_puntaje_player.grid(row=0,column=0)
    label_puntaje_bot.grid(row=0,column=1)
    
    self.principal.update()

try:
  juego = Reversi()
except:       
  print("Epsilon")