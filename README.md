# 🎮 Pokémon Battle Simulator (Python)

¡Bienvenido al simulador de batallas Pokémon basado en la consola! Este proyecto es una implementación interactiva y por turnos construida en Python utilizando **Programación Orientada a Objetos (POO)**. Permite recrear combates estratégicos entre dos entrenadores, gestionando estadísticas, efectividad de tipos y estados de salud en tiempo real.

---

## ✨ Características Principales

* **Sistema de Combate por Turnos:** La prioridad de ataque se determina dinámicamente según la estadística de **velocidad** de cada Pokémon.
* **Mecánica de Daño Avanzada:** El daño final calculado incluye factores como la potencia del movimiento, el ataque del emisor, la defensa del receptor y una **variación aleatoria (85%-100%)** para simular la aleatoriedad de los juegos originales.
* **Tabla de Tipos Básica:** Lógica integrada para calcular ventajas y desventajas elementales (`Fuego`, `Agua`, `Planta`, `Eléctrico`, `Normal`). ¡Los ataques acertados te avisarán si son *"Muy efectivos"* o *"No muy efectivos"*!
* **Gestión de Equipos y Rotación:** Si un Pokémon es derrotado, el sistema obliga al jugador (o a la IA) a reemplazarlo por un miembro vivo de su equipo de hasta 6 Pokémon.
* **Interfaz Visual en Consola:** Incluye barras de salud dinámicas dibujadas con caracteres Unicode (`█░`) y porcentajes precisos.

---

## 🛠️ Arquitectura del Código

El script está estructurado bajo componentes modulares e independientes:

1.  `TipoPokemon (Enum)`: Define los tipos elementales disponibles.
2.  `Pokemon`: Gestiona las estadísticas base (PS, Ataque, Defensa, Velocidad), movimientos aprendidos y estados actuales del Pokémon.
3.  `Movimiento`: Define la potencia, precisión y tipo de daño, además de procesar si el ataque acierta o falla.
4.  `Entrenador`: Administra el equipo de Pokémon, la lógica de cambio de combatiente y la verificación de miembros debilitados.
5.  `Batalla`: El motor del juego. Controla el flujo de las rondas, la IA simple del rival y procesa los turnos interactivos.

---

## 🚀 Cómo Ejecutar el Proyecto

### Prerrequisitos
Solo necesitas tener instalado **Python 3.x** en tu sistema. No requiere dependencias externas de `pip`.

### Instrucciones
1. Clona este repositorio o descarga el archivo `pokemon.py`.
2. Abre tu terminal o consola de comandos en la ruta del archivo.
3. Ejecuta el siguiente comando:

```bash
python pokemon.py
```

## 🎮 Demostración de Juego
Al iniciar el script, tomarás el rol de Ash en un combate contra Brock. El juego te guiará de manera interactiva a través de menús numéricos:

```bash
============================================================
RONDA 1
============================================================

Ash:
Charizard (Fuego)
PS: 78/78 [████████] 100.0%

Brock:
Dragonite (Eléctrico)
PS: 91/91 [█████████] 100.0%

Ash, es tu turno:
Movimientos de Charizard:
1. Lanzallamas (Potencia: 90, Precisión: 100%)
2. Placaje (Potencia: 40, Precisión: 100%)
3. Mordida (Potencia: 60, Precisión: 100%)
4. Vuelo (Potencia: 70, Precisión: 100%)

Selecciona un movimiento (1-4): 1
```

## 📈 Próximas Mejoras (Roadmap)
[ ] Implementar movimientos de estado (curación, aumentos de estadísticas como Danza Dragón).

[ ] Añadir la tabla completa de tipos oficial (Inclusión de tipos Volador, Dragón, Psíquico, etc.).

[ ] Crear una interfaz gráfica (GUI) utilizando Tkinter o Pygame.
