from flask import Flask, render_template, request, send_file
import pandas as pd
from fpdf import FPDF
import io
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/export', methods=['POST'])
def export():
    file = request.files['csvFile']
    pdf_name = request.form['pdfName']
    data = pd.read_csv(file)

    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()

    # 加上 LOGO
 #   logo_path = os.path.join('static', 'icon.png')
  #  if os.path.exists(logo_path):
   #     pdf.image(logo_path, x=10, y=10, w=30)

    # 動態調整字體大小
    pdf.set_xy(10, 10)
    font_size = 12
    col_width = 277 / len(data.columns)
    row_height = 8
    pdf.set_font("Arial", size=font_size)

    for i, row in data.iterrows():
        if i == 0:
            for col in data.columns:
                pdf.cell(col_width, row_height, str(col), border=1)
            pdf.ln(row_height)

        for col in data.columns:
            content = str(row[col])
            while pdf.get_string_width(content) > col_width:
                font_size -= 0.5
                pdf.set_font("Arial", size=font_size)
            pdf.cell(col_width, row_height, content, border=1)
        pdf.ln(row_height)

    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name=f"{pdf_name}.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
