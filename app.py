from flask import Flask, request, send_file, abort
import io
from backend.barcodes.local import generate_barcode_pdf

app = Flask(__name__)


@app.route('/local/barcodes')
def local_barcodes():
    sku = request.args.get('sku')
    name = request.args.get('name')
    if not sku or not name:
        abort(400, 'SKU and name parameters are required')

    pdf_bytes = generate_barcode_pdf(sku, name)
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name='barcodes.pdf'
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
