import hashlib


def md5_encrypt(content, encoding='utf-8', type_='str'):
    content = '' if content is None else content
    if type_ == 'str':
        return hashlib.md5(content.encode(encoding)).hexdigest()
    elif type_ == 'obj':
        md5_ = hashlib.md5()
        content = open(content, 'rb').read()
        md5_.update(content)
        return md5_.hexdigest()


if __name__ == '__main__':
    print(md5_encrypt('小依曦'))
