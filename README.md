# Inventario-Servitae

Repositorio para llevar un control de Bodegas.

## Backend de carga de códigos de barras

Se proporciona un pequeño API construido con **FastAPI** que permite subir imágenes de códigos de barras.

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

### Ejecución del servidor

```bash
uvicorn app:app --reload
```

### Endpoint de subida

```
POST /upload/{marketplace}
```

Envía el archivo de imagen como `form-data` usando el campo `file`. La extensión debe ser `.jpg`, `.jpeg`, `.bmp`, `.webp` o `.png`.

Las imágenes se guardan en `uploads/<marketplace>/` y el nombre final contiene el nombre del marketplace para evitar mezcla entre canales.
