# Inventario-Servitae

Repositorio para llevar un control de Bodegas

## Marketplace API

Un pequeño servicio Flask permite administrar los marketplaces.

### Instalación

```bash
pip install -r requirements.txt
```

### Uso

```bash
python app.py
```

El servidor expondrá las siguientes rutas:

- `GET /marketplaces` devuelve todos los marketplaces.
- `POST /marketplaces/add` agrega un nuevo marketplace con un cuerpo JSON `{"name": "nombre"}` y crea su carpeta de carga en `uploads/<nombre>`.

La aplicación también sirve un frontend sencillo en la raíz (`/`) que muestra la lista de marketplaces y permite añadir nuevos dinámicamente.
