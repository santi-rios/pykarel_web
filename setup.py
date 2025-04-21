from setuptools import setup

with open("pykarel_web/version.py", "r") as f:
    exec(f.read())  # Esto carga __version__

setup(
    name="pykarel_web",
    version=__version__,
    packages=["pykarel_web"],
    install_requires=["matplotlib>=3.0", "ipython"],
    python_requires=">=3.8",
    author="Tu Nombre",
    description="Karel para Python en el navegador con Pyodide"
)