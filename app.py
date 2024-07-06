import io

from flask import Flask, render_template, send_file, request

import combine_pdf as fp

app = Flask(__name__)


# Pipenv——最好用的python虚拟环境和包管理工具 - ZingpLiu - 博客园  https://www.cnblogs.com/zingp/p/8525138.html

@app.route('/fp_upload', methods=['POST'])
def fp_upload():
    files = request.files.getlist('files')
    all_pdf = []
    for file in files:
        # if file
        filename = file.filename
        # print(f"File name: {filename}")

        if filename.lower().endswith('.pdf'):
            all_pdf.append(file)

    result = fp.main1(all_pdf)

    pdf_stream = io.BytesIO()
    result.write(pdf_stream)
    pdf_stream.seek(0)
    return send_file(pdf_stream, mimetype='application/pdf', as_attachment=True, download_name='output.pdf')


@app.route('/fp')
def hello_world_fp():
    return render_template('fp.html')


@app.route('/')
def hello_world():  # put application's code here
    return ('<h2>'
            '<a href="/fp">发票</a> <br/> '
            '</h2>  ')


if __name__ == '__main__':
    app.run()
