# PyKarel Web

Paquete Python para enseñar programación con Karel en Pyodide/Quarto-live.

## Instalación
```python
await micropip.install("https://tuusuario.github.io/pykarel_web/pykarel_web-0.1.0-py3-none-any.whl")

### **Paso 3: Construir el Paquete**
Desde la terminal en la carpeta raíz (`pykarel_web/`):

```bash
# Instalar herramientas necesarias
pip install setuptools wheel

# Generar el archivo .whl
python setup.py bdist_wheel


Prepara la carpeta docs/:

    Crea un archivo docs/index.html (puede estar vacío o con documentación).

    Copia el archivo .whl a docs/:
    bash

cp dist/pykarel_web-0.2.7-py3-none-any.whl docs/


Configura el YAML de tu documento Quarto:
yaml

---
format: live-html
pyodide:
  packages:
    - matplotlib
    - ipython
    - https://tuusuario.github.io/pykarel_web/pykarel_web-0.1.0-py3-none-any.whl
---

Y en el código Python:
python

from pykarel_web import Karel

karel = Karel("obstaculos")
karel.move()
karel.turn_left()
karel.show_animation()  # Mostrar todas las imágenes

Solución de Problemas Comunes

    Error 404 al instalar:

        Verifica que la URL sea exactamente igual (incluyendo versión).

        Espera unos minutos después del push (GitHub Pages puede tardar en actualizar).

    Paquete no se instala:

        Asegúrate de que el .whl sea "pure Python" (no tiene dependencias nativas).

        Usa micropip interactivamente para debuggear:
        python

        import micropip
        await micropip.install("https://.../pykarel_web-0.1.0-py3-none-any.whl")

    Actualizar versión:

        Cambia __version__ en version.py.

        Genera nuevo .whl y súbelo a docs/ con nombre actualizado.

        Actualiza la URL en el YAML de Quarto.

Estructura Final en GitHub

https://github.com/tuusuario/pykarel_web/
├── docs/
│   ├── pykarel_web-0.1.0-py3-none-any.whl
│   └── index.html
├── pykarel_web/
│   ├── __init__.py1
│   └── version.py
├── setup.py
└── README.md

Con esto tendrás un paquete listo para usar en tus tutoriales interactivos. ¡El archivo .whl estará disponible públicamente para que Pyodide lo instale directamente desde GitHub Pages!    