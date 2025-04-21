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

cp dist/pykarel_web-0.1.0-py3-none-any.whl docs/