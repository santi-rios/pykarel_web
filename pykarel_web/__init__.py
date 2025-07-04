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
            "laberinto_complejo": [
                [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
                [1,1,1,1,1,1,1,1,1,0,1,0,1,0,1],
                [1,0,0,0,0,0,0,0,0,0,1,0,1,0,1],
                [1,0,1,1,1,1,1,1,1,1,1,0,1,0,1],
                [1,0,1,0,0,0,0,0,0,0,0,0,1,0,1],
                [1,0,1,0,1,1,1,1,1,1,1,1,1,0,1],
                [1,0,1,0,1,0,0,0,0,0,0,0,0,0,1],
                [1,0,1,0,1,0,1,1,1,1,1,1,1,1,1],
                [1,0,1,0,1,0,0,0,0,0,1,0,0,0,1],
                [1,0,1,0,1,1,1,1,1,0,1,0,1,0,1],
                [1,0,1,0,0,0,0,0,1,0,1,0,1,0,1],
                [1,0,1,1,1,1,1,0,1,0,1,0,1,0,1],
                [1,0,0,0,0,0,0,0,1,0,0,0,1,0,0],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,0]
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
        if isinstance(self.mundo, list) and len(self.mundo) == 15 and len(self.mundo[0]) == 15:
            # This is likely our complex maze
            return {(14, 14): 1}  # Exit point with a coso
        
        return {
            (2, 2): 5,
            (3, 4): 3,
            (0, 0): 1
        }

    def _render(self):
        """Renderiza el mundo con mejoras visuales"""
        fig, ax = plt.subplots(figsize=(10, 10))  # Increased figure size
        
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
                ax.plot(x + 0.5, y + 0.5, 'ro', markersize=18, alpha=0.5)  # Increased marker size
                ax.text(x + 0.5, y + 0.5, str(cantidad), 
                       ha='center', va='center', 
                       color='white', weight='bold',
                       fontsize=12)  # Increased font size
        
        # Dibujar Karel
        colores = ['#e74c3c', '#2980b9', '#27ae60', '#f1c40f']
        arrow = ['→', '↑', '←', '↓']
        ax.text(
            self.x + 0.5, self.y + 0.5, 
            arrow[self.direction],
            fontsize=60,  # Increased font size
            color=colores[self.direction],
            ha='center', 
            va='center',
            fontweight='bold'
        )
        
        # Configuración del gráfico con coordenadas
        ax.set_xlim(-0.5, len(self.mundo[0])-0.5)
        ax.set_ylim(-0.5, len(self.mundo)-0.5)
        
        # Add coordinate labels
        x_ticks = range(len(self.mundo[0]))
        y_ticks = range(len(self.mundo))
        ax.set_xticks(x_ticks)
        ax.set_yticks(y_ticks)
        ax.set_xticklabels([str(i) for i in x_ticks], fontsize=12)  # Increased font size
        ax.set_yticklabels([str(i) for i in y_ticks], fontsize=12)  # Increased font size
        
        # Add labels for axes
        ax.set_xlabel('X Coordinates', fontsize=14, labelpad=10)  # Increased font size
        ax.set_ylabel('Y Coordinates', fontsize=14, labelpad=10)  # Increased font size
        
        # Additional formatting
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.set_title(f"Karel - Paso {self.step}", fontweight='bold', pad=20, fontsize=16)  # Increased font size
        ax.set_aspect('equal')
        
        # Guardar imagen
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=100)  # Increased DPI
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
    
    def ejecutar_acciones(self, max_images=8, page=1, show_controls=True):
        """
        Displays Karel's actions with pagination and navigation controls.
        
        Parameters:
        -----------
        max_images : int
            Number of images to show per page
        page : int
            Current page to display
        show_controls : bool
            Whether to show pagination controls
        """
        total_pages = ((len(self.images) - 1) // max_images) + 1
        
        # Ensure page is within valid range
        page = max(1, min(page, total_pages))
        
        start = (page - 1) * max_images
        end = min(start + max_images, len(self.images))
        
        # Style for individual images
        img_style = "margin:5px; width:300px; border:1px solid #ddd; border-radius:5px;"
        
        # Create HTML for images
        html = "<div style='display:flex; flex-wrap:wrap; justify-content:center;'>"
        for img in self.images[start:end]:
            html += f"<img src='data:image/png;base64,{img}' style='{img_style}'>"
        html += "</div>"
        
        # Add pagination info and controls if needed
        if show_controls and total_pages > 1:
            html += f"""
            <div style='text-align:center; margin-top:10px;'>
                <span style='margin:0 10px;'>Página {page} de {total_pages}</span>
                <div style='margin-top:5px;'>
                    <button onclick='IPython.notebook.kernel.execute("_{0} = get_ipython().user_ns[\\"{0}\\"]; _{0}.ejecutar_acciones({max_images}, {max(1, page-1)})")' style='padding:5px 10px; margin:0 5px;'>« Anterior</button>
                    <button onclick='IPython.notebook.kernel.execute("_{0} = get_ipython().user_ns[\\"{0}\\"]; _{0}.ejecutar_acciones({max_images}, {min(total_pages, page+1)})")' style='padding:5px 10px; margin:0 5px;'>Siguiente »</button>
                </div>
            </div>
            """.format(id(self))
        elif total_pages > 0:
            html += f"<div style='text-align:center; margin-top:10px;'>Página {page} de {total_pages}</div>"
        
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
    
    def mostrar_animacion(self, delay=500):
        """
        Displays all Karel's actions as an animation.
        
        Parameters:
        -----------
        delay : int
            Delay between frames in milliseconds
        """
        if not self.images:
            display(HTML("<p>No hay acciones para mostrar</p>"))
            return
        
        # Generate unique ID for this animation
        import random
        container_id = f"karel_animation_{random.randint(10000, 99999)}"
        
        # Create HTML with images and animation controls
        html = f"""
        <div id="{container_id}" style="text-align:center;">
            <img id="{container_id}_img" src="data:image/png;base64,{self.images[0]}" 
                 style="width:500px; border:1px solid #ddd; border-radius:5px; margin-bottom:10px;">
            <div style="margin:10px 0;">
                <button id="{container_id}_prev" style="padding:5px 15px; margin:0 5px;">« Anterior</button>
                <button id="{container_id}_play" style="padding:5px 15px; margin:0 5px;">▶ Reproducir</button>
                <button id="{container_id}_pause" style="padding:5px 15px; margin:0 5px; display:none;">⏸ Pausar</button>
                <button id="{container_id}_next" style="padding:5px 15px; margin:0 5px;">Siguiente »</button>
            </div>
            <div style="margin-top:10px;">
                <span id="{container_id}_counter">Paso 1 de {len(self.images)}</span>
                <div style="margin-top:10px;">
                    <label for="{container_id}_speed">Velocidad: </label>
                    <input type="range" id="{container_id}_speed" min="100" max="2000" value="{delay}" style="width:200px;">
                </div>
            </div>
        </div>
        
        <script>
        (function() {{
            // Store images in JavaScript - directly use the encoded images
            const images = {{ {", ".join([f"'{i}': '{img}'" for i, img in enumerate(self.images)])} }};
            
            // Animation variables
            let currentIdx = 0;
            let animationId = null;
            let animDelay = {delay};
            
            // Get DOM elements
            const container = document.getElementById("{container_id}");
            const img = document.getElementById("{container_id}_img");
            const prevBtn = document.getElementById("{container_id}_prev");
            const nextBtn = document.getElementById("{container_id}_next");
            const playBtn = document.getElementById("{container_id}_play");
            const pauseBtn = document.getElementById("{container_id}_pause");
            const counter = document.getElementById("{container_id}_counter");
            const speedControl = document.getElementById("{container_id}_speed");
            
            // Update display
            function updateDisplay() {{
                img.src = "data:image/png;base64," + images[currentIdx];
                counter.textContent = `Paso ${{currentIdx + 1}} de {len(self.images)}`;
            }}
            
            // Animation functions
            function nextFrame() {{
                currentIdx = (currentIdx + 1) % Object.keys(images).length;
                updateDisplay();
            }}
            
            function prevFrame() {{
                currentIdx = (currentIdx - 1 + Object.keys(images).length) % Object.keys(images).length;
                updateDisplay();
            }}
            
            function startAnimation() {{
                if (animationId) clearInterval(animationId);
                animationId = setInterval(nextFrame, animDelay);
                playBtn.style.display = "none";
                pauseBtn.style.display = "inline";
            }}
            
            function stopAnimation() {{
                if (animationId) clearInterval(animationId);
                animationId = null;
                playBtn.style.display = "inline";
                pauseBtn.style.display = "none";
            }}
            
            // Event listeners
            prevBtn.addEventListener("click", () => {{
                stopAnimation();
                prevFrame();
            }});
            
            nextBtn.addEventListener("click", () => {{
                stopAnimation();
                nextFrame();
            }});
            
            playBtn.addEventListener("click", startAnimation);
            pauseBtn.addEventListener("click", stopAnimation);
            
            speedControl.addEventListener("change", () => {{
                animDelay = parseInt(speedControl.value);
                if (animationId) {{
                    stopAnimation();
                    startAnimation();
                }}
            }});
            
            // Initialize display
            updateDisplay();
        }})();
        </script>
        """
        
        display(HTML(html))
        

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