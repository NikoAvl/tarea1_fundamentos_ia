# Definición de una clase llamada 'JuegoReversi' para gestionar el juego de Reversi
class JuegoReversi:
  #Comienza el raton, valor=-1

  # Constructor de la clase
  # Inicializa el juego con un tablero de tamaño 'size_tablero'
  # El parámetro 'estado' es opcional y representa el estado inicial del tablero (por defecto, vacío)
  # El parámetro 'turno' es opcional y establece el jugador actual (-1 para el jugador humano, 1 para el bot)
  def __init__(self, size_tablero, estado=None, turno=-1):

    self.size_tablero = size_tablero
    # Si el estado no se proporciona, se crea un tablero vacío
    if estado is None:
      estado = [[0 for _ in range(self.size_tablero)]
                for _ in range(size_tablero)]
    # Inicialización de las propiedades del juego
    self.tablero = estado
    self.completo = False
    self.ganador = None
    self.jugador = turno

  # Método para reiniciar el juego
  def reiniciar(self):
    self.tablero = [[0 for _ in range(self.size_tablero)]
                    for _ in range(self.size_tablero)]
    self.completo = False
    self.ganador = None
    self.jugador = -1

  # Método para generar jugadas posibles (todas las posiciones válidas en el tablero)
  def generar_jugadas_posibles(self):
    return [[i for i in range(self.size_tablero)]
            for j in range(self.size_tablero)]

  # Método para determinar si el juego ha llegado a su estado final
  def estado_final(self):
    self.evaluar()
    if self.ganador is not None or self.completo:
      return True
    else:
      return False

  # Método para evaluar el resultado del juego
  def evaluar(self):
    # Comprueba si el tablero está completo (sin casillas vacías)
    if 0 in self.tablero:
      self.completo = True

    else:
      self.completo = False
    # Si el tablero está completo, cuenta las fichas de cada jugador para determinar al ganador o empate
    if self.completo:
      contador_player = 0
      contador_bot = 0
      for casilla in self.tablero:
        if casilla == 1:
          contador_player += 1
        if casilla == 2:
          contador_bot += 1
      if contador_player > contador_bot:
        self.ganador = 1
        return
      elif contador_player < contador_bot:
        self.ganador = 2
        return
      else:
        self.ganador = None
        
  # Método para calcular la utilidad del juego (el ganador)
  def calcular_utilidad(self):
    return self.ganador

  # Método para realizar una jugada en el tablero
  def jugar(self, fila, columna):
    self.tablero[fila][columna] = self.jugador
    self.jugador *= -1

  # Método para deshacer una jugada en el tablero
  def deshacer_jugada(self, fila, columna):
    self.tablero[fila][columna] = 0
    self.jugador *= -1


#-1: Ratón (Inicia, es el jugador humano)
# 1: Gato (Responde, es el computador)
# cuando gana el gato el valor es   1
# cuando gana el ratón el valor es -1
# un empate tiene utilidad 0
# etapa  1: maximizar
# etapa -1: minimizar

# Método para verificar si un movimiento en una dirección específica es válido
  def movimiento_valido_en_direccion(self,tablero, fila, columna, jugador, delta_fila, delta_columna):
      # Determinar el rival del jugador actual
      rival = -1 if jugador == 1 else 1
      # Moverse en la dirección especificada
      fila += delta_fila
      columna += delta_columna
      # Verificar si el movimiento es válido
      if (0 <= fila < self.size_tablero) and (0 <= columna < self.size_tablero) and tablero[fila][columna] == rival:
          fila += delta_fila
          columna += delta_columna
          while (0 <= fila < self.size_tablero) and (0 <= columna < self.size_tablero):
              # Comprobar si se encuentra una ficha del jugador actual
              if tablero[fila][columna] == jugador:
                  return True
              # Comprobar si se encuentra una casilla vacía
              elif tablero[fila][columna] == 0:
                  return False
              fila += delta_fila
              columna += delta_columna
      return False

  # Método para verificar si un movimiento en una posición específica es válido en todas las direcciones posibles
  def movimiento_valido(self,tablero, fila, columna, jugador):
      if tablero[fila][columna] != 0:
          return False

      movimientos_validos = []

      direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

            
      for delta_fila, delta_columna in direcciones:
          if self.movimiento_valido_en_direccion(tablero, fila, columna, jugador, delta_fila, delta_columna):
              movimientos_validos.append((delta_fila, delta_columna))
              
      return movimientos_validos
  
  # Método para realizar un movimiento en el tablero y actualizar el estado
  def realizar_movimiento(self,tablero, fila, columna, jugador):
    movimientos_validos = self.movimiento_valido(tablero, fila, columna, jugador)
    

    if not movimientos_validos:
        return False

    tablero[fila][columna] = jugador

    rival = -1 if jugador == 1 else 1

    for delta_fila, delta_columna in movimientos_validos:
        fila_actual, columna_actual = fila + delta_fila, columna + delta_columna
        while tablero[fila_actual][columna_actual] == rival:
            tablero[fila_actual][columna_actual] = jugador
            fila_actual += delta_fila
            columna_actual += delta_columna

    return True  
  
  # Método para contar las fichas del jugador y del bot en el tablero
  def contar_fichas(self, tablero):
    contador_player = sum(row.count(-1) for row in tablero)
    contador_bot = sum(row.count(1) for row in tablero)
    return contador_player, contador_bot
  
  # Método para calcular la puntuación del juego (diferencia entre las fichas del jugador y del bot)
  def puntuacion(self, tablero):
    puntuacion_player = sum(row.count(-1) for row in tablero)
    puntuacion_bot = sum(row.count(1) for row in tablero)
    return puntuacion_player - puntuacion_bot

  # Método para obtener todos los movimientos válidos para un jugador en el tablero
  def obtener_movimientos_validos(self,tablero, jugador):
      movimientos_validos = []

      for fila in range(self.size_tablero):
          for columna in range(self.size_tablero):
              if self.movimiento_valido(tablero, fila, columna, jugador):
                  movimientos_validos.append((fila, columna))

      return movimientos_validos

  # Método minimax para encontrar el mejor movimiento en un árbol de búsqueda de profundidad 'profundidad'
  def minimax(self,tablero, jugador, profundidad):
      # Comprueba si se alcanzó la profundidad máxima o si el juego está completo
      if profundidad == 0 or self.completo:
          # Calcular la puntuación en esta hoja del árbol de búsqueda (heurística)
          return self.puntuacion(tablero), None

      # Obtiene los movimientos válidos para el jugador actual
      movimientos_validos = self.obtener_movimientos_validos(tablero, jugador)
      print(f"movimientos validos1: {movimientos_validos}")
      if jugador == -1:
          # Jugador humano (maximizador)
          mejor_valor = float('-inf')
          mejor_movimiento = None
          for movimiento in movimientos_validos:
              # Realiza una copia del tablero para simular el movimiento
              copia_tablero = [fila[:] for fila in tablero]
              self.realizar_movimiento(copia_tablero, movimiento[0], movimiento[1], jugador)
              # Llama recursivamente al minimax para el siguiente nivel del árbol
              valor, _ = self.minimax(copia_tablero, 1, profundidad - 1)
              # Actualiza el mejor valor y movimiento si es necesario
              if valor > mejor_valor:
                  mejor_valor = valor
                  mejor_movimiento = movimiento
          print(f"movimientos validos2: {movimientos_validos}")
          return mejor_valor, mejor_movimiento
      else:
          # Jugador bot (minimizador)
          mejor_valor = float('inf')
          mejor_movimiento = None
          for movimiento in movimientos_validos:
              # Realiza una copia del tablero para simular el movimiento
              copia_tablero = [fila[:] for fila in tablero]
              self.realizar_movimiento(copia_tablero, movimiento[0], movimiento[1], jugador)
              # Llama recursivamente al minimax para el siguiente nivel del árbol
              valor, _ = self.minimax(copia_tablero, -1, profundidad - 1)
              # Actualiza el mejor valor y movimiento si es necesario
              if valor < mejor_valor:
                  mejor_valor = valor
                  mejor_movimiento = movimiento
          print(f"movimientos validos3: {movimientos_validos}")
          return mejor_valor, mejor_movimiento 