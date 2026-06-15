import random
from enum import Enum

class TipoPokemon(Enum):
    FUEGO = "Fuego"
    AGUA = "Agua"
    PLANTA = "Planta"
    ELECTRICO = "Eléctrico"
    NORMAL = "Normal"

class Pokemon:
    def __init__(self, nombre, tipo, ps, ataque, defensa, velocidad):
        self.nombre = nombre
        self.tipo = tipo
        self.ps_max = ps
        self.ps = ps
        self.ataque = ataque
        self.defensa = defensa
        self.velocidad = velocidad
        self.movimientos = []
    
    def agregar_movimiento(self, movimiento):
        """Agrega un movimiento al Pokémon"""
        self.movimientos.append(movimiento)
    
    def recibir_daño(self, daño):
        """Reduce los PS del Pokémon"""
        daño_real = max(1, daño - self.defensa // 2)
        self.ps -= daño_real
        return daño_real
    
    def esta_vivo(self):
        """Verifica si el Pokémon sigue vivo"""
        return self.ps > 0
    
    def curar(self, cantidad):
        """Cura al Pokémon"""
        self.ps = min(self.ps_max, self.ps + cantidad)
    
    def mostrar_estado(self):
        """Muestra el estado actual del Pokémon"""
        barra = "█" * (self.ps // 10) + "░" * ((self.ps_max - self.ps) // 10)
        porcentaje = (self.ps / self.ps_max) * 100
        print(f"\n{self.nombre} ({self.tipo.value})")
        print(f"PS: {self.ps}/{self.ps_max} [{barra}] {porcentaje:.1f}%")

class Movimiento:
    def __init__(self, nombre, tipo_daño, potencia, precision):
        self.nombre = nombre
        self.tipo_daño = tipo_daño
        self.potencia = potencia
        self.precision = precision
    
    def calcular_daño(self, ataque_base):
        """Calcula el daño del movimiento"""
        if random.randint(1, 100) > self.precision:
            return 0
        daño = (ataque_base * self.potencia) // 100
        variacion = random.randint(85, 100) / 100
        return int(daño * variacion)

class Entrenador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.pokemon_equipo = []
        self.pokemon_activo = None
    
    def agregar_pokemon(self, pokemon):
        """Agrega un Pokémon al equipo"""
        self.pokemon_equipo.append(pokemon)
    
    def cambiar_pokemon(self, indice):
        """Cambia el Pokémon activo"""
        if 0 <= indice < len(self.pokemon_equipo):
            if self.pokemon_equipo[indice].esta_vivo():
                self.pokemon_activo = self.pokemon_equipo[indice]
                return True
        return False
    
    def obtener_pokemon_vivos(self):
        """Retorna la cantidad de Pokémon vivos"""
        return sum(1 for p in self.pokemon_equipo if p.esta_vivo())
    
    def tiene_pokemon_vivos(self):
        """Verifica si el entrenador tiene Pokémon vivos"""
        return self.obtener_pokemon_vivos() > 0

class Batalla:
    def __init__(self, entrenador1, entrenador2):
        self.entrenador1 = entrenador1
        self.entrenador2 = entrenador2
        self.ronda = 0
        self.batalla_activa = True
        
        # Inicia con el primer Pokémon de cada entrenador
        self.entrenador1.cambiar_pokemon(0)
        self.entrenador2.cambiar_pokemon(0)
    
    def calcular_efectividad(self, tipo_ataque, tipo_defensa):
        """Calcula la efectividad del tipo de movimiento"""
        efectividades = {
            TipoPokemon.FUEGO: {TipoPokemon.PLANTA: 1.5, TipoPokemon.AGUA: 0.5},
            TipoPokemon.AGUA: {TipoPokemon.FUEGO: 1.5, TipoPokemon.PLANTA: 0.5},
            TipoPokemon.PLANTA: {TipoPokemon.AGUA: 1.5, TipoPokemon.FUEGO: 0.5},
            TipoPokemon.ELECTRICO: {TipoPokemon.AGUA: 1.5, TipoPokemon.PLANTA: 0.5},
        }
        
        if tipo_ataque in efectividades:
            return efectividades[tipo_ataque].get(tipo_defensa, 1.0)
        return 1.0
    
    def mostrar_estado_batalla(self):
        """Muestra el estado actual de la batalla"""
        print("\n" + "="*60)
        print(f"RONDA {self.ronda}")
        print("="*60)
        print(f"\n{self.entrenador1.nombre}:")
        self.entrenador1.pokemon_activo.mostrar_estado()
        print(f"\n{self.entrenador2.nombre}:")
        self.entrenador2.pokemon_activo.mostrar_estado()
    
    def mostrar_movimientos(self, pokemon):
        """Muestra los movimientos disponibles"""
        print(f"\nMovimientos de {pokemon.nombre}:")
        for i, mov in enumerate(pokemon.movimientos):
            print(f"{i + 1}. {mov.nombre} (Potencia: {mov.potencia}, Precisión: {mov.precision}%)")
    
    def ejecutar_turno(self, ataque1, ataque2):
        """Ejecuta un turno de batalla"""
        p1 = self.entrenador1.pokemon_activo
        p2 = self.entrenador2.pokemon_activo
        
        # Determina quién ataca primero por velocidad
        if p1.velocidad >= p2.velocidad:
            primero, segundo = (p1, p2, ataque1, ataque2), (p2, p1, ataque2, ataque1)
        else:
            primero, segundo = (p2, p1, ataque2, ataque1), (p1, p2, ataque1, ataque2)
        
        # Ataque del primer Pokémon
        atacante1, defensor1, mov1, mov2 = primero
        daño1 = mov1.calcular_daño(atacante1.ataque)
        efectividad1 = self.calcular_efectividad(mov1.tipo_daño, defensor1.tipo)
        daño1 = int(daño1 * efectividad1)
        daño_recibido1 = defensor1.recibir_daño(daño1)
        
        if daño1 == 0:
            print(f"\n{atacante1.nombre} usa {mov1.nombre}... ¡Pero falló!")
        else:
            print(f"\n{atacante1.nombre} usa {mov1.nombre}!")
            if efectividad1 > 1:
                print("¡Es muy efectivo!")
            elif efectividad1 < 1:
                print("No es muy efectivo...")
            print(f"{defensor1.nombre} recibe {daño_recibido1} de daño")
        
        if not defensor1.esta_vivo():
            return
        
        # Ataque del segundo Pokémon
        atacante2, defensor2, mov2_act, mov1_act = segundo
        daño2 = mov2_act.calcular_daño(atacante2.ataque)
        efectividad2 = self.calcular_efectividad(mov2_act.tipo_daño, defensor2.tipo)
        daño2 = int(daño2 * efectividad2)
        daño_recibido2 = defensor2.recibir_daño(daño2)
        
        if daño2 == 0:
            print(f"\n{atacante2.nombre} usa {mov2_act.nombre}... ¡Pero falló!")
        else:
            print(f"\n{atacante2.nombre} usa {mov2_act.nombre}!")
            if efectividad2 > 1:
                print("¡Es muy efectivo!")
            elif efectividad2 < 1:
                print("No es muy efectivo...")
            print(f"{defensor2.nombre} recibe {daño_recibido2} de daño")
    
    def iniciar_batalla(self):
        """Inicia la batalla interactiva"""
        print("\n" + "="*60)
        print(f"¡COMIENZA LA BATALLA!")
        print(f"{self.entrenador1.nombre} vs {self.entrenador2.nombre}")
        print("="*60)
        
        while self.batalla_activa:
            self.ronda += 1
            self.mostrar_estado_batalla()
            
            # Jugador 1 elige movimiento
            print(f"\n{self.entrenador1.nombre}, es tu turno:")
            self.mostrar_movimientos(self.entrenador1.pokemon_activo)
            while True:
                try:
                    opcion1 = int(input("Selecciona un movimiento (1-4): ")) - 1
                    if 0 <= opcion1 < len(self.entrenador1.pokemon_activo.movimientos):
                        break
                    print("Opción inválida")
                except ValueError:
                    print("Ingresa un número válido")
            
            # Jugador 2 elige movimiento (IA simple)
            opcion2 = random.randint(0, len(self.entrenador2.pokemon_activo.movimientos) - 1)
            print(f"\n{self.entrenador2.nombre} elige {self.entrenador2.pokemon_activo.movimientos[opcion2].nombre}")
            
            # Ejecuta el turno
            ataque1 = self.entrenador1.pokemon_activo.movimientos[opcion1]
            ataque2 = self.entrenador2.pokemon_activo.movimientos[opcion2]
            self.ejecutar_turno(ataque1, ataque2)
            
            # Verifica si alguien fue derrotado
            if not self.entrenador1.pokemon_activo.esta_vivo():
                print(f"\n{self.entrenador1.pokemon_activo.nombre} fue derrotado!")
                if self.entrenador1.tiene_pokemon_vivos():
                    print(f"\n{self.entrenador1.nombre} debe enviar otro Pokémon")
                    self.mostrar_pokemon_disponibles(self.entrenador1)
                    while True:
                        try:
                            indice = int(input("Selecciona un Pokémon (1-6): ")) - 1
                            if self.entrenador1.cambiar_pokemon(indice):
                                print(f"¡Vamos, {self.entrenador1.pokemon_activo.nombre}!")
                                break
                            print("Pokémon no disponible")
                        except ValueError:
                            print("Ingresa un número válido")
                else:
                    print(f"\n¡{self.entrenador2.nombre} ganó la batalla!")
                    self.batalla_activa = False
            
            elif not self.entrenador2.pokemon_activo.esta_vivo():
                print(f"\n{self.entrenador2.pokemon_activo.nombre} fue derrotado!")
                if self.entrenador2.tiene_pokemon_vivos():
                    indice = random.randint(0, len(self.entrenador2.pokemon_equipo) - 1)
                    while not self.entrenador2.cambiar_pokemon(indice):
                        indice = random.randint(0, len(self.entrenador2.pokemon_equipo) - 1)
                    print(f"{self.entrenador2.nombre} envía a {self.entrenador2.pokemon_activo.nombre}")
                else:
                    print(f"\n¡{self.entrenador1.nombre} ganó la batalla!")
                    self.batalla_activa = False
    
    def mostrar_pokemon_disponibles(self, entrenador):
        """Muestra los Pokémon disponibles"""
        print(f"\nPokémon disponibles en el equipo de {entrenador.nombre}:")
        for i, pokemon in enumerate(entrenador.pokemon_equipo):
            estado = "Vivo" if pokemon.esta_vivo() else "Derrotado"
            print(f"{i + 1}. {pokemon.nombre} ({pokemon.tipo.value}) - {estado}")

def crear_juego():
    """Crea y configura un juego de Pokémon"""
    
    # Crear movimientos
    mov_fuego = Movimiento("Lanzallamas", TipoPokemon.FUEGO, 90, 100)
    mov_agua = Movimiento("Torrente", TipoPokemon.AGUA, 90, 100)
    mov_planta = Movimiento("Rayo Solar", TipoPokemon.PLANTA, 80, 100)
    mov_tackling = Movimiento("Placaje", TipoPokemon.NORMAL, 40, 100)
    mov_rayo = Movimiento("Rayo", TipoPokemon.ELECTRICO, 90, 100)
    mov_mordida = Movimiento("Mordida", TipoPokemon.NORMAL, 60, 100)
    
    # Crear Pokémon del Entrenador 1
    charizard = Pokemon("Charizard", TipoPokemon.FUEGO, 78, 84, 78, 100)
    charizard.agregar_movimiento(mov_fuego)
    charizard.agregar_movimiento(mov_tackling)
    charizard.agregar_movimiento(mov_mordida)
    charizard.agregar_movimiento(Movimiento("Vuelo", TipoPokemon.NORMAL, 70, 100))
    
    blastoise = Pokemon("Blastoise", TipoPokemon.AGUA, 79, 83, 100, 78)
    blastoise.agregar_movimiento(mov_agua)
    blastoise.agregar_movimiento(mov_tackling)
    blastoise.agregar_movimiento(mov_rayo)
    blastoise.agregar_movimiento(Movimiento("Hidrobomba", TipoPokemon.AGUA, 110, 80))
    
    venusaur = Pokemon("Venusaur", TipoPokemon.PLANTA, 80, 82, 83, 80)
    venusaur.agregar_movimiento(mov_planta)
    venusaur.agregar_movimiento(mov_agua)
    venusaur.agregar_movimiento(mov_tackling)
    venusaur.agregar_movimiento(Movimiento("Polvo Veneno", TipoPokemon.PLANTA, 75, 100))
    
    # Crear Pokémon del Entrenador 2
    dragonite = Pokemon("Dragonite", TipoPokemon.ELECTRICO, 91, 134, 95, 80)
    dragonite.agregar_movimiento(mov_rayo)
    dragonite.agregar_movimiento(mov_tackling)
    dragonite.agregar_movimiento(mov_mordida)
    dragonite.agregar_movimiento(Movimiento("Danza Dragón", TipoPokemon.NORMAL, 85, 100))
    
    alakazam = Pokemon("Alakazam", TipoPokemon.NORMAL, 55, 50, 65, 120)
    alakazam.agregar_movimiento(Movimiento("Destructor", TipoPokemon.NORMAL, 120, 50))
    alakazam.agregar_movimiento(mov_tackling)
    alakazam.agregar_movimiento(mov_rayo)
    alakazam.agregar_movimiento(Movimiento("Psicorrayo", TipoPokemon.NORMAL, 90, 100))
    
    lapras = Pokemon("Lapras", TipoPokemon.AGUA, 130, 85, 80, 60)
    lapras.agregar_movimiento(mov_agua)
    lapras.agregar_movimiento(mov_fuego)
    lapras.agregar_movimiento(mov_hielo)
    lapras.agregar_movimiento(Movimiento("Canción Triste", TipoPokemon.NORMAL, 0, 100))
    
    # Crear entrenadores
    entrenador1 = Entrenador("Ash")
    entrenador1.agregar_pokemon(charizard)
    entrenador1.agregar_pokemon(blastoise)
    entrenador1.agregar_pokemon(venusaur)
    
    entrenador2 = Entrenador("Brock")
    entrenador2.agregar_pokemon(dragonite)
    entrenador2.agregar_pokemon(alakazam)
    entrenador2.agregar_pokemon(lapras)
    
    # Iniciar batalla
    batalla = Batalla(entrenador1, entrenador2)
    batalla.iniciar_batalla()

if __name__ == "__main__":
    mov_hielo = Movimiento("Rayo Hielo", TipoPokemon.AGUA, 90, 100)
    crear_juego()
