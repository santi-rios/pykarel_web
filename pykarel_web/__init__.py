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
    
    def move(self):
        if self.front_is_clear():
            offsets = [(1,0), (0,1), (-1,0), (0,-1)]
            self.x += offsets[self.direction][0]
            self.y += offsets[self.direction][1]
            self._render()
    
    def turn_left(self):
        self.direction = (self.direction + 1) % 4
        self._render()
    
    def put_beeper(self):
        self.beepers[(self.x, self.y)] = self.beepers.get((self.x, self.y), 0) + 1
        self._render()
    
    def pick_beeper(self):
        if self.beepers.get((self.x, self.y), 0) > 0:
            self.beepers[(self.x, self.y)] -= 1
            self._render()
    
    def front_is_clear(self):
        next_x = self.x + [(1,0), (0,1), (-1,0), (0,-1)][self.direction][0]
        next_y = self.y + [(1,0), (0,1), (-1,0), (0,-1)][self.direction][1]
        return 0 <= next_x < len(self.mundo[0]) and 0 <= next_y < len(self.mundo)
    
    def show_animation(self):
        html = "<div style='display:flex;flex-wrap:wrap'>"
        for img in self.images:
            html += f"<img src='data:image/png;base64,{img}' style='margin:5px;width:200px'>"
        html += "</div>"
        display(HTML(html))