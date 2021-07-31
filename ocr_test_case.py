import requests

BASE_URL = 'http://127.0.0.1:5000/file/ocr'


def test_local_image(file_name='img/ocr_test_01.png'):
    file_obj = open(file_name, 'rb').read()
    data = {
        'uri': file_obj,
        'type': 0
    }
    data = requests.post(url=BASE_URL, data=data).json()
    print(data['content'])
    assert data['rows'] == 9, 'api call error'
    print('test_local_image success')


def test_network_image():
    data = {
        'uri': 'https://i.loli.net/2021/08/01/47bag9V52LSu8DG.png',
        'type': 0
    }
    response = requests.post(url=BASE_URL, data=data)
    data = response.json()
    print(data['content'])
    assert data['rows'] == 9, 'api call error'
    print('test_network_image success')


def run_test_case():
    test_local_image()
    test_network_image()


if __name__ == '__main__':
    run_test_case()
