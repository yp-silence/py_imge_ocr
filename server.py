"""
一个基于flask的图片上传及图片内容识别的程序
"""

from flask import Flask, request, jsonify, g

from ocr_utils import MyOcr
from com_utils import md5_encrypt
from db_utils import SqlLiteHelper

app = Flask(__name__)


@app.before_first_request
def init_db():
    SqlLiteHelper().init_db()


@app.route('/file/ocr', methods=['post'])
def file_ocr():
    tmp_type = int(request.form.get('type'))
    if tmp_type == 0:
        # 解析本地图片
        file_obj = request.files.get('uri')
        print('type_file_obj:', type(file_obj))
        file_name = file_obj.filename
        file_obj.save(file_name)
        uri = file_name
    else:
        # 解析网络图片
        uri = request.form.get('uri')
    type_ = 'obj' if tmp_type == 0 else 'str'
    key = md5_encrypt(uri, type_=type_)
    driver = SqlLiteHelper()
    data = driver.fetch_data(key)
    if len(data) > 0:
        # 命中缓存
        response_content = {
            'parse_valid': True,
            'content': data[0],
            'rows': data[1]
        }
    else:
        ocr_obj = MyOcr(uri, tmp_type)
        response_content = ocr_obj.parse_content()
        if response_content['parse_valid']:
            driver.update_data((key,
                                response_content['content'],
                                response_content['rows'])
                               )
        else:
            pass
    return jsonify(response_content)


if __name__ == '__main__':
    app.run(port=5004)
