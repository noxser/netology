import subprocess
import os

if 'Result' in os.listdir(os.path.dirname(__file__)):
    print('Папка Result уже есть делаем преобразование файлов')
else:
    print('Папка Result создана делаем преобразование файлов')
    os.makedirs('Result')

for file_name in os.listdir('Source'):
    subprocess.call('convert Source\\' + file_name + ' -resize 200 result\\' + file_name)
    print(file_name)

print('Преобразованные файлы в папке Result')
