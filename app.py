 codex/reintroducir-logica-de-gestion-de-marketplace

codex/add-basic-tests-for-flask-endpoints

import os
import sqlite3
import io
from flask import Flask, request, jsonify, send_file, abort
 codex/reintroducir-logica-de-gestion-de-marketplace

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
=======
from backend.barcodes.local import generate_barcode_pdf

DB_PATH = os.environ.get('DB_PATH', 'marketplaces.db')
UPLOADS_DIR = 'uploads'

app = Flask(__name__, static_folder='frontend', static_url_path='')


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS marketplaces ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        " name TEXT UNIQUE NOT NULL)"
    )
    conn.commit()
    conn.close()


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
        download_name='barcodes.pdf',
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

 1  from flask import Flask, request, send_file, abort
 2  import io
 3  from backend.barcodes.local import generate_barcode_pdf
 4  
 5  app = Flask(__name__)
 6  
 7  
 8  @app.route('/local/barcodes')
 9  def local_barcodes():
10      sku = request.args.get('sku')
11      name = request.args.get('name')
12      if not sku or not name:
13          abort(400, 'SKU and name parameters are required')
14  
15      pdf_bytes = generate_barcode_pdf(sku, name)
16      return send_file(
17          io.BytesIO(pdf_bytes),
18          mimetype='application/pdf',
19          as_attachment=True,
20          download_name='barcodes.pdf'
21      )
22  
23  
24  if __name__ == '__main__':
25      app.run(host='0.0.0.0', port=8000)


