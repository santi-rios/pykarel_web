# pykarel_web/__init__.py
from IPython.display import display, HTML
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np

class KarelError(Exception):
    """Clase personalizada para errores de Karel"""
    pass

class Karel:
    """
    Karel es un robot virtual que puede moverse en un mundo de cuadrícula.
    
    Esta clase implementa las acciones básicas de Karel y permite visualizar
    sus movimientos en un entorno interactivo de Jupyter Notebook.
    
    Parámetros:
    -----------
    mundo : str o list
        Tipo de mundo predefinido o matriz personalizada
    x_inicial : int
        Posición inicial de Karel en el eje X (comienza en 0)
    y_inicial : int
        Posición inicial de Karel en el eje Y (comienza en 0)
    direccion_inicial : int
        Dirección inicial de Karel (0:Este, 1:Norte, 2:Oeste, 3:Sur)
    cosos_iniciales : int
        Cantidad inicial de cosos que lleva Karel
    """
    
    def __init__(self, mundo="default", x_inicial=0, y_inicial=0, direccion_inicial=0, cosos_iniciales=0):
        self.mundo = self._crear_mundo(mundo)
        self._validar_posicion_inicial(x_inicial, y_inicial)
        
        self.x = x_inicial
        self.y = y_inicial
        self.direction = direccion_inicial
        self.beepers = self._inicializar_beepers()
        self.cosos = cosos_iniciales
        self.step = 0
        self.images = []
        self._render()

    def _validar_posicion_inicial(self, x, y):
        """Valida que la posición inicial no esté en un obstáculo"""
        if not (0 <= x < len(self.mundo[0]) and 0 <= y < len(self.mundo)):
            raise KarelError("Posición inicial fuera del mundo")
        if self.mundo[y][x] == 1:
            raise KarelError("Karel no puede iniciar en un obstáculo")

    def _crear_mundo(self, tipo):
        """Crea la matriz del mundo con mejor visualización"""
        if isinstance(tipo, list):
            return tipo  # Permite mundos personalizados
        
        mundos = {
            "default": [
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0]
            ],
            "obstaculos": [
                [0,1,0,1,0],
                [1,0,1,0,1],
                [0,1,0,1,0],
                [1,0,1,0,1],
                [0,1,0,1,0]
            ],
            "laberinto": [
                [0,1,0,0,0],
                [0,1,1,1,0],
                [0,0,0,1,0],
                [1,1,0,1,0],
                [0,0,0,1,0]
            ],
            "cosos": [
                [0,2,0,3,0],
                [1,0,4,0,5],
                [0,6,0,7,0],
                [8,0,9,0,10],
                [0,11,0,12,0]
            ],
            "complejo": [
                [0,1,0,1,0,1],
                [1,0,1,0,1,0],
                [0,1,0,1,0,1],
                [1,0,1,0,1,0],
                [0,1,0,1,0,1],
                [1,0,1,0,1,0]
            ],
            "recta": [
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            ]
        }
        return mundos.get(tipo, mundos["default"])
    
    def _inicializar_beepers(self):
        """Inicializa cosos en posiciones específicas para algunos mundos"""
        return {
            (2,2): 5,
            (3,4): 3,
            (0,0): 1
        }

    def _render(self):
        """Renderiza el mundo con mejoras visuales"""
        fig, ax = plt.subplots(figsize=(7,7))
        
        # Dibujar cuadrícula
        for x in range(len(self.mundo[0])+1):
            ax.axvline(x, color='gray', linestyle=':', linewidth=0.5)
        for y in range(len(self.mundo)+1):
            ax.axhline(y, color='gray', linestyle=':', linewidth=0.5)
        
        # Dibujar obstáculos
        for y in range(len(self.mundo)):
            for x in range(len(self.mundo[0])):
                if self.mundo[y][x] == 1:
                    ax.add_patch(plt.Rectangle(
                        (x, y), 1, 1, 
                        color='#2c3e50', 
                        hatch='//', 
                        alpha=0.7
                    ))
        
        # Dibujar cosos/zumbadores
        for (x, y), cantidad in self.beepers.items():
            if cantidad > 0:
                ax.plot(x + 0.5, y + 0.5, 'ro', markersize=15, alpha=0.5)
                ax.text(x + 0.5, y + 0.5, str(cantidad), 
                       ha='center', va='center', 
                       color='white', weight='bold')
        
        # Dibujar Karel
        colores = ['#e74c3c', '#2980b9', '#27ae60', '#f1c40f']
        arrow = ['→', '↑', '←', '↓']
        ax.text(
            self.x + 0.5, self.y + 0.5, 
            arrow[self.direction],
            fontsize=50,
            color=colores[self.direction],
            ha='center', 
            va='center',
            fontweight='bold'
        )
        
        # Configuración del gráfico
        ax.set_xlim(0, len(self.mundo[0]))
        ax.set_ylim(0, len(self.mundo))
        ax.set_xticks(np.arange(0, len(self.mundo[0])+1))
        ax.set_yticks(np.arange(0, len(self.mundo)+1))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_title(f"Karel - Paso {self.step}", fontweight='bold')
        ax.set_aspect('equal')
        
        # Guardar imagen
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=80)
        plt.close()
        self.images.append(base64.b64encode(buf.getvalue()).decode('utf-8'))
        self.step += 1

    def avanzar(self):
        """Mueve a Karel una celda adelante si el camino está despejado"""
        if not self.frente_abierto():
            raise KarelError("¡Choque! No puedes avanzar - Hay un obstáculo")
        
        # Actualizar posición
        movimientos = {
            0: (1, 0),  # Este
            1: (0, 1),  # Norte
            2: (-1, 0),  # Oeste
            3: (0, -1)   # Sur
        }
        dx, dy = movimientos[self.direction]
        self.x += dx
        self.y += dy
        
        # Verificar posición válida
        if not (0 <= self.x < len(self.mundo[0])) or not (0 <= self.y < len(self.mundo)):
            raise KarelError("¡Karel se salió del mundo!")
        
        self._render()

    def girar_izquierda(self):
        """Gira a Karel 90 grados a la izquierda"""
        self.direction = (self.direction + 1) % 4
        self._render()

    def poner_coso(self):
        """Coloca un coso en la posición actual"""
        if self.cosos <= 0:
            raise KarelError("¡No tienes cosos para poner!")
        
        self.cosos -= 1
        self.beepers[(self.x, self.y)] = self.beepers.get((self.x, self.y), 0) + 1
        self._render()

    def juntar_coso(self):
        """Recoge un coso de la posición actual"""
        if self.beepers.get((self.x, self.y), 0) < 1:
            raise KarelError("¡No hay cosos para recoger aquí!")
        
        self.cosos += 1
        self.beepers[(self.x, self.y)] -= 1
        self._render()

    def frente_abierto(self):
        """Verifica si el frente está despejado"""
        x, y = self.x, self.y
        try:
            dx, dy = {
                0: (1, 0),   # Este
                1: (0, 1),   # Norte
                2: (-1, 0),  # Oeste
                3: (0, -1)   # Sur
            }[self.direction]
            
            new_x = x + dx
            new_y = y + dy
            
            if new_x < 0 or new_y < 0:
                return False
                
            return self.mundo[new_y][new_x] != 1
            
        except IndexError:
            return False

    # Alias para mantener compatibilidad
    def front_is_clear(self):
        return self.frente_abierto()
    
    def ejecutar_acciones(self, max_images=10, page=1):
        """Displays a limited number of images with optional pagination."""
        start = (page - 1) * max_images
        end = start + max_images
        html = "<div style='display:flex;flex-wrap:wrap'>"
        for img in self.images[start:end]:
            html += f"<img src='data:image/png;base64,{img}' style='margin:5px;width:200px'>"
        html += "</div>"
        html += f"<p>Page {page} of {((len(self.images) - 1) // max_images) + 1}</p>"
        display(HTML(html))
    
    def girar_derecha(self):
        """Gira Karel 90 grados a la derecha."""
        # Girar a la izquierda tres veces es equivalente a girar a la derecha una vez
        for _ in range(3):
            self.girar_izquierda()
    
    def hay_coso(self):
        """Verifica si hay un coso/zumbador en la posición actual."""
        return self.beepers.get((self.x, self.y), 0) > 0
    
    def izquierda_abierta(self):
        """Verifica si el camino a la izquierda está libre."""
        # Guardar dirección actual
        dir_actual = self.direction
        self.direction = (self.direction + 1) % 4
        resultado = self.frente_abierto()
        # Restaurar dirección
        self.direction = dir_actual
        return resultado
    
    def derecha_abierta(self):
        """Verifica si el camino a la derecha está libre."""
        # Guardar dirección actual
        dir_actual = self.direction
        self.direction = (self.direction - 1) % 4
        resultado = self.frente_abierto()
        # Restaurar dirección
        self.direction = dir_actual
        return resultado
    
    def frente_bloqueado(self):
        """Verifica si el frente está bloqueado."""
        return not self.frente_abierto()
    
    def contar_cosos(self):
        """Devuelve el número de cosos/zumbadores en la posición actual."""
        return self.beepers.get((self.x, self.y), 0)
    
    def reiniciar(self, mundo="default", x_inicial=0, y_inicial=0, direccion_inicial=0):
        """Reinicia a Karel a su estado inicial."""
        self.__init__(mundo, x_inicial, y_inicial, direccion_inicial)
    
    def mostrar_ultima_accion(self):
        """Muestra solo la última acción realizada."""
        if len(self.images) > 0:
            html = f"<img src='data:image/png;base64,{self.images[-1]}' style='width:300px'>"
            display(HTML(html))
    
    def colocar_cosos_en_posicion(self, x, y, cantidad=1):
        """Coloca una cantidad de cosos/zumbadores en una posición específica."""
        self.beepers[(x, y)] = self.beepers.get((x, y), 0) + cantidad
        self._render()
    
    def crear_mundo_personalizado(self, matriz):
        """Define un mundo personalizado a partir de una matriz."""
        self.mundo = matriz
        self._render()


# Función de ayuda global
def help():
    """Displays help and a description of the available commands."""
    help_text = """
    <h3>Comandos de Karel:</h3>
    <ul>
        <li><b>avanzar()</b> - Mueve a Karel un paso hacia adelante</li>
        <li><b>girar_izquierda()</b> - Gira a Karel 90 grados a la izquierda</li>
        <li><b>girar_derecha()</b> - Gira a Karel 90 grados a la derecha</li>
        <li><b>poner_coso()</b> - Coloca un coso/zumbador en la posición actual</li>
        <li><b>juntar_coso()</b> - Recoge un coso/zumbador de la posición actual</li>
    </ul>
    
    <h3>Condiciones:</h3>
    <ul>
        <li><b>frente_abierto()</b> - Verifica si Karel puede avanzar</li>
        <li><b>frente_bloqueado()</b> - Verifica si Karel no puede avanzar</li>
        <li><b>izquierda_abierta()</b> - Verifica si el camino a la izquierda está libre</li>
        <li><b>derecha_abierta()</b> - Verifica si el camino a la derecha está libre</li>
        <li><b>hay_coso()</b> - Verifica si hay un coso en la posición actual</li>
    </ul>
    """
    display(HTML(help_text))