import numpy as np
import os
import urllib
import urllib.request
import hashlib

# sha256:63d4344077849053dc3036b247fa012b2b381de53fd055a66b539dffd76cf08e
mnist_file_url = 'https://oneflow-public.oss-cn-beijing.aliyuncs.com/datasets/mnist.npz'


def _get_sha256hash(file_path, Bytes=1024):
    sha256hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(Bytes)
            if data:
                sha256hash.update(data)
            else:
                break
    ret = sha256hash.hexdigest()
    return ret


def _process_bar(percent, start_str='', end_str='', total_length=0):
    bar = ''.join(["="] * int(percent * total_length))
    bar = '\r' + start_str + bar.ljust(total_length) + ' {:0>4.1f}%|'.format(percent * 100) + end_str
    print(bar, end='', flush=True)


def _cb_progress_bar(blocknum, blocksize, totalsize):
    percent = blocknum * blocksize / totalsize
    if percent > 1:
        percent = 1
    try:
        column_size = int(os.get_terminal_size().columns * 0.8)
    except OSError:
        # Ubuntu系统调用os.get_terminal_size()有bug
        column_size = 80
    _process_bar(percent, end_str="100%", total_length=column_size)


def _download_mnist_file(outputfile):
    # global mnist_file_url
    urllib.request.urlretrieve(mnist_file_url, outputfile, _cb_progress_bar)
    print("")


def _get_mnist_file():
    path = os.path.join(".", "mnist.npz")
    if not (os.path.isfile(path)):
        _download_mnist_file(path)

    sha256 = "63d4344077849053dc3036b247fa012b2b381de53fd055a66b539dffd76cf08e"
    if not _get_sha256hash(path) == sha256:
        cheksum_fail = "sha256 verification failed, remove {0} and try again".format(path)
        raise Exception(cheksum_fail)
    return path


def load_data(train_batch_size=100, test_batch_size=100, data_format='NCHW'):
    path = _get_mnist_file()
    with np.load(path, allow_pickle=True) as f:
        x_train, y_train = f['x_train'], f['y_train']
        x_test, y_test = f['x_test'], f['y_test']

    def _normalize(x, y, batch_size):
        x = (x.astype(np.float32) - 128.0) / 255.0
        y = y.astype(np.int32)
        if data_format == 'NCHW':
            images = x.reshape((-1, batch_size, 1, x.shape[1], x.shape[2]))
        else:
            images = x.reshape((-1, batch_size, x.shape[1], x.shape[2], 1))
        labels = y.reshape((-1, batch_size))
        return images, labels

    train_images, train_labels = _normalize(x_train, y_train, train_batch_size)
    test_images, test_labels = _normalize(x_test, y_test, test_batch_size)

    return (train_images, train_labels), (test_images, test_labels)


if __name__ == "__main__":
    (x_train, y_train), (x_test, y_test) = load_data()

    print(x_train.shape,
          y_train.shape,
          x_test.shape,
          y_test.shape)
