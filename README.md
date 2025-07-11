# Inventario-Servitae

Repositorio para llevar un control de Bodegas

## Barcode generation

Run the application with Flask to generate barcodes:

```bash
pip install flask python-barcode reportlab
python app.py
```

Request the `/local/barcodes` endpoint providing `sku` and `name` query parameters. It returns a PDF page with 32 barcodes.
