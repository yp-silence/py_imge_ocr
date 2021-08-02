"""
一个基于flask的图片上传及图片内容识别的程序
"""

from flask import Flask, request, jsonify
from ocr_utils import MyOcr

app = Flask(__name__)


@app.route('/file/ocr', methods=['post'])
def file_ocr():
    tmp_type = int(request.form.get('type'))
    if tmp_type == 0:
        print('解析本地图片')
        file_obj = request.files.get('uri')
        file_name = file_obj.filename
        file_obj.save(file_name)
        uri = file_name
    else:
        print('解析网络图片')
        uri = request.form.get('uri')
    ocr_obj = MyOcr(uri, tmp_type)
    return jsonify(ocr_obj.parse_content())


if __name__ == '__main__':
    app.run()
