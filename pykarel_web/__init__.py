# pykarel_web/__init__.py
from IPython.display import display, HTML
import matplotlib.pyplot as plt
from io import BytesIO
import base64

class Karel:
    def __init__(self, mundo="default"):
        self.x = 0
        self.y = 0
        self.direction = 0  # 0:Este, 1:Norte, 2:Oeste, 3:Sur
        self.mundo = self._crear_mundo(mundo)
        self.beepers = {}
        self.step = 0
        self.images = []
    
    def _crear_mundo(self, tipo):
        # Configuraciones predefinidas de mundos
        if tipo == "default":
            return [[0]*5 for _ in range(5)]  # Mundo 5x5 vacío
        elif tipo == "obstaculos":
            return [
                [0,0,1,0,0],
                [0,1,0,1,0],
                [0,0,0,0,0]
            ]
        return [[0]*5 for _ in range(5)]  # Default
    
    def _render(self):
        fig, ax = plt.subplots(figsize=(5,5))
        
        # Dibujar mundo
        for y in range(len(self.mundo)):
            for x in range(len(self.mundo[0])):
                if self.mundo[y][x] == 1:
                    ax.add_patch(plt.Rectangle((x, y), 1, 1, color='gray'))
        
        # Dibujar a Karel
        directions = ['→', '↑', '←', '↓']
        ax.text(self.x + 0.5, self.y + 0.5, directions[self.direction],
               fontsize=20, ha='center', va='center')
        
        # Dibujar zumbadores
        if (self.x, self.y) in self.beepers:
            ax.text(self.x + 0.8, self.y + 0.2, str(self.beepers[(self.x, self.y)]),
                   color='red', fontsize=12)
        
        ax.set_xlim(0, len(self.mundo[0]))
        ax.set_ylim(0, len(self.mundo))
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Guardar imagen
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        self.images.append(base64.b64encode(buf.getvalue()).decode('utf-8'))
        self.step += 1
    
    def avanzar(self):
        if self.front_is_clear():
            offsets = [(1,0), (0,1), (-1,0), (0,-1)]
            self.x += offsets[self.direction][0]
            self.y += offsets[self.direction][1]
            self._render()
    
    def girar_izquierda(self):
        self.direction = (self.direction + 1) % 4
        self._render()
    
    def poner_coso(self):
        self.beepers[(self.x, self.y)] = self.beepers.get((self.x, self.y), 0) + 1
        self._render()
    
    def juntar_coso(self):
        if self.beepers.get((self.x, self.y), 0) > 0:
            self.beepers[(self.x, self.y)] -= 1
            self._render()
    
    def frente_abierto(self):
        next_x = self.x + [(1,0), (0,1), (-1,0), (0,-1)][self.direction][0]
        next_y = self.y + [(1,0), (0,1), (-1,0), (0,-1)][self.direction][1]
        return 0 <= next_x < len(self.mundo[0]) and 0 <= next_y < len(self.mundo)
    
    def ejecutar_acciones(self):
        html = "<div style='display:flex;flex-wrap:wrap'>"
        for img in self.images:
            html += f"<img src='data:image/png;base64,{img}' style='margin:5px;width:200px'>"
        html += "</div>"
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
    

def _crear_mundo(self, tipo):
    # Configuraciones predefinidas de mundos
    if tipo == "default":
        return [[0]*5 for _ in range(5)]  # Mundo 5x5 vacío
    elif tipo == "obstaculos":
        return [
            [0,0,1,0,0],
            [0,1,0,1,0],
            [0,0,0,0,0]
        ]
    elif tipo == "laberinto":
        return [
            [0,1,0,0,0],
            [0,1,0,1,0],
            [0,1,0,1,0],
            [0,0,0,1,0],
            [1,1,0,0,0]
        ]
    elif tipo == "zigzag":
        return [
            [0,0,0,0,1],
            [1,1,1,0,1],
            [0,0,0,0,1],
            [1,1,1,0,0],
            [0,0,0,0,0]
        ]
    elif tipo == "espiral":
        return [
            [0,0,0,0,0],
            [0,1,1,1,0],
            [0,1,0,1,0],
            [0,1,0,0,0],
            [0,0,0,0,0]
        ]
    return [[0]*5 for _ in range(5)]  # Default

def ayuda(self):
    """Muestra la ayuda y descripción de los comandos disponibles."""
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

def reiniciar(self, mundo="default", x_inicial=0, y_inicial=0, direccion_inicial=0):
    """Reinicia a Karel a su estado inicial."""
    self.__init__(mundo, x_inicial, y_inicial, direccion_inicial)

def mostrar_ultima_accion(self):
    """Muestra solo la última acción realizada."""
    if len(self.images) > 0:
        html = f"<img src='data:image/png;base64,{self.images[-1]}' style='width:300px'>"
        display(HTML(html))

def avanzar(self):
    if self.frente_abierto():
        offsets = [(1,0), (0,1), (-1,0), (0,-1)]
        self.x += offsets[self.direction][0]
        self.y += offsets[self.direction][1]
        self._render()
    else:
        raise Exception("¡Oops! Karel no puede avanzar porque hay un obstáculo en el camino.")

def juntar_coso(self):
    if self.hay_coso():
        self.beepers[(self.x, self.y)] -= 1
        self._render()
    else:
        raise Exception("¡Oops! No hay cosos/zumbadores para juntar en esta posición.")
    
º1
class Karel:
    """
    Karel es un robot virtual que puede moverse en un mundo de cuadrícula.
    
    Esta clase implementa las acciones básicas de Karel y permite visualizar
    sus movimientos en un entorno interactivo de Jupyter Notebook.
    
    Parámetros:
    -----------
    mundo : str
        Tipo de mundo predefinido ("default", "obstaculos", "laberinto", etc.)
    x_inicial : int
        Posición inicial de Karel en el eje X
    y_inicial : int
        Posición inicial de Karel en el eje Y
    direccion_inicial : int
        Dirección inicial de Karel (0:Este, 1:Norte, 2:Oeste, 3:Sur)
    """