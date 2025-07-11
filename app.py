import os
import sqlite3
import io
from flask import Flask, request, jsonify, send_file, abort

from backend.barcodes.local import generate_barcode_pdf

DB_PATH = 'marketplaces.db'
UPLOADS_DIR = 'uploads'

app = Flask(__name__, static_folder='frontend', static_url_path='')


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS marketplaces (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL)"
    )
    conn.commit()
    conn.close()
    os.makedirs(UPLOADS_DIR, exist_ok=True)


init_db()


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/marketplaces', methods=['GET'])
def get_marketplaces():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, name FROM marketplaces')
    markets = [{'id': row[0], 'name': row[1]} for row in c.fetchall()]
    conn.close()
    return jsonify(markets)


@app.route('/marketplaces/add', methods=['POST'])
def add_marketplace():
    data = request.get_json() or {}
    name = data.get('name')
    if not name:
        return jsonify({'error': 'name field required'}), 400

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('INSERT INTO marketplaces (name) VALUES (?)', (name,))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Marketplace already exists'}), 400
    conn.close()

    os.makedirs(os.path.join(UPLOADS_DIR, name), exist_ok=True)
    return jsonify({'message': 'Marketplace added'}), 201


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
