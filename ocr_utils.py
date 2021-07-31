"""
基于baidu-aip 文字识别 sdk 进行简单封装
"""
from aip import AipOcr
from io import StringIO
import os


class MyOcr(object):

    def __init__(self, uri, type_):
        """ type_ = 0 本地图片  type_ = 1 网络 url"""
        self._uri = uri
        self._type_ = type_
        self._img_obj = None
        self._options = MyOcr._get_default_options()

    @staticmethod
    def _get_default_options():
        options = dict()
        # 中英文混合
        options["language_type"] = "CHN_ENG"
        # 自动检测文字的朝向
        options["detect_direction"] = "true"
        # 自动检测文字的类型
        options["detect_language"] = "true"
        # 置信度
        options["probability"] = "true"
        return options

    def recognize_image(self):
        assert self._type_ in (0, 1), f'only (0,1) type_ is supported'
        self._get_image_content()
        client = MyOcr._get_instance()
        if self._type_ == 0:
            return client.basicGeneral(self._img_obj, self._options)
        else:
            return client.basicGeneralUrl(self._img_obj, self._options)

    def parse_content(self):
        row_data = self.recognize_image()
        io = StringIO()
        result = dict()
        print(row_data)
        if 'words_result' in row_data:
            result['rows'] = row_data['words_result_num']
            for row in row_data['words_result']:
                io.write(row['words'])
                io.write('\n')
            io.flush()
            result['content'] = io.getvalue()
            result['parse_valid'] = True
            io.close()
        elif 'error_msg' or 'error_code' in row_data:
            result['parse_valid'] = False
            result['error_msg'] = row_data['error_msg']
        return result

    def _get_image_content(self):
        if self._type_ == 0:
            if os.path.isfile(self._uri):
                with open(self._uri, 'rb') as f:
                    print(type(f))
                    self._img_obj = f.read()
            else:
                self._img_obj = self._uri
        else:
            self._img_obj = self._uri

    @staticmethod
    def _get_instance():
        app_id = '24631612'
        api_key = 'GThbtwdB7sfGZGaaaQXaMVp1'
        secret_key = 'xZzmmKTX2yQDHtGF64femfuqajv1lAgE'
        client = AipOcr(app_id, api_key, secret_key)
        return client


if __name__ == '__main__':
    print(MyOcr('ocr_test_01.png').parse_content())
    print(MyOcr('flask学习笔记.md').parse_content())
