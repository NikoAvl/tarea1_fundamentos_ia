class JuegoReversi:
  #Comienza el raton, valor=-1
  def __init__(self, size_tablero, estado=None, turno=-1):

    self.size_tablero = size_tablero

    if estado is None:
      estado = [[0 for _ in range(self.size_tablero)]
                for _ in range(size_tablero)]
    self.tablero = estado
    self.completo = False
    self.ganador = None
    self.jugador = turno

  def reiniciar(self):
    self.tablero = [[0 for _ in range(self.size_tablero)]
                    for _ in range(self.size_tablero)]
    self.completo = False
    self.ganador = None
    self.jugador = -1

  def generar_jugadas_posibles(self):
    return [[i for i in range(self.size_tablero)]
            for j in range(self.size_tablero)]

  def estado_final(self):
    self.evaluar()
    if self.ganador is not None or self.completo:
      return True
    else:
      return False

  def evaluar(self):
    if 0 in self.tablero:
      self.completo = True

    else:
      self.completo = False
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
   
  def calcular_utilidad(self):
    return self.ganador

  def jugar(self, fila, columna):
    self.tablero[fila][columna] = self.jugador
    self.jugador *= -1

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
  def movimiento_valido_en_direccion(self,tablero, fila, columna, jugador, delta_fila, delta_columna):
      rival = -1 if jugador == 1 else 1
      fila += delta_fila
      columna += delta_columna
      if (0 <= fila < self.size_tablero) and (0 <= columna < self.size_tablero) and tablero[fila][columna] == rival:
          fila += delta_fila
          columna += delta_columna
          while (0 <= fila < self.size_tablero) and (0 <= columna < self.size_tablero):
              if tablero[fila][columna] == jugador:
                  return True
              elif tablero[fila][columna] == 0:
                  return False
              fila += delta_fila
              columna += delta_columna
      return False

  def movimiento_valido(self,tablero, fila, columna, jugador):
      if tablero[fila][columna] != 0:
          return False

      movimientos_validos = []

      direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
            
      for delta_fila, delta_columna in direcciones:
          if self.movimiento_valido_en_direccion(tablero, fila, columna, jugador, delta_fila, delta_columna):
              movimientos_validos.append((delta_fila, delta_columna))
              
      return movimientos_validos
    
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
  
  def contar_fichas(self, tablero):
    contador_player = sum(row.count(-1) for row in tablero)
    contador_bot = sum(row.count(1) for row in tablero)
    return contador_player, contador_bot
  
  def puntuacion(self, tablero):
    puntuacion_player = sum(row.count(-1) for row in tablero)
    puntuacion_bot = sum(row.count(1) for row in tablero)
    return puntuacion_player - puntuacion_bot

  def obtener_movimientos_validos(self,tablero, jugador):
      movimientos_validos = []

      for fila in range(self.size_tablero):
          for columna in range(self.size_tablero):
              if self.movimiento_valido(tablero, fila, columna, jugador):
                  movimientos_validos.append((fila, columna))

      return movimientos_validos

  def minimax(self,tablero, jugador, profundidad):
      if profundidad == 0 or self.completo:
          # Calcular la puntuación en esta hoja del árbol de búsqueda (heurística)
          return self.puntuacion(tablero), None

      movimientos_validos = self.obtener_movimientos_validos(tablero, jugador)
      print(f"movimientos validos1: {movimientos_validos}")
      if jugador == -1:
          mejor_valor = float('-inf')
          mejor_movimiento = None
          for movimiento in movimientos_validos:
              copia_tablero = [fila[:] for fila in tablero]
              self.realizar_movimiento(copia_tablero, movimiento[0], movimiento[1], jugador)
              valor, _ = self.minimax(copia_tablero, 1, profundidad - 1)
              if valor > mejor_valor:
                  mejor_valor = valor
                  mejor_movimiento = movimiento
          print(f"movimientos validos2: {movimientos_validos}")
          return mejor_valor, mejor_movimiento
      else:
          mejor_valor = float('inf')
          mejor_movimiento = None
          for movimiento in movimientos_validos:
              copia_tablero = [fila[:] for fila in tablero]
              self.realizar_movimiento(copia_tablero, movimiento[0], movimiento[1], jugador)
              valor, _ = self.minimax(copia_tablero, -1, profundidad - 1)
              if valor < mejor_valor:
                  mejor_valor = valor
                  mejor_movimiento = movimiento
          print(f"movimientos validos3: {movimientos_validos}")
          return mejor_valor, mejor_movimiento 