import os

estructura = [
    "controllers",
    "core",
    "database",
    "interfaces",
    "models",
    "repositories",
    "routes",
    "schemas",
    "services",
]

def crear_estructura():
    base_dir = os.getcwd()
    print(f"Creando estructura en: {base_dir}/app")
    app_path = os.path.join(base_dir, "app")

    # Crear carpeta principal app/
    os.makedirs(app_path, exist_ok=True)

    # Crear subcarpetas
    for carpeta in estructura:
        ruta = os.path.join(app_path, carpeta)
        os.makedirs(ruta, exist_ok=True)
        print(f"📁 {carpeta}/ creada.")

    # Crear main.py vacío si no existe
    main_py = os.path.join(app_path, "main.py")
    if not os.path.exists(main_py):
        with open(main_py, "w") as f:
            f.write("# Punto de entrada de la aplicación FastAPI\n\n")
            f.write("from fastapi import FastAPI\n\n")
            f.write("app = FastAPI()\n\n")
            f.write('@app.get("/")\n')
            f.write("def read_root():\n")
            f.write("    return {'message': 'Hello World'}\n")
        print("📄 main.py creado.")

if __name__ == "__main__":
    crear_estructura()
