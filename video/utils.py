import os
from threading import Thread
from time import sleep


def upload_to_cdn(obj, old_obj=None):
    Thread(target=_upload_to_cdn, args=(obj, old_obj)).start()


def _upload_to_cdn(obj, old_obj=None):
    if old_obj:
        print(f'Удаляю {old_obj} с CDN')
    print(f'Загружаю {obj} на CDN')
    print('Имитация загрузки...')
    sleep(10.)
    print('Загрузка завершена!')
    print('Удаляю локальный файл...')
    if os.path.exists(obj.local_file.path):
        os.remove(obj.local_file.path)
    else:
        print(f'{obj.local_file.path} и так не существует')
    obj.bunny_id = '...'
    obj.save()
