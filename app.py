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
