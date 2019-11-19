import os
from os.path import isfile, join
from bs4 import BeautifulSoup

files_path = input('files_path (case sensitive):')

os.chdir(files_path)

dirs_name = [f for f in os.listdir(files_path) if (not isfile(join(files_path, f)))]

for dir_name in dirs_name:

    dir_path = files_path + '/' + dir_name
    os.chdir(dir_path)

    files_name = [f for f in os.listdir(dir_path) if isfile(join(dir_path, f))]

    for file_name in files_name:
        file_content = None
        file = open(dir_path + '/' + file_name)
        try:
            file_content = file.read()
        finally:
            file.close()

        if(file_content is not None):
            html = BeautifulSoup(file_content, 'html.parser')
            text = html.text

            css_content = [s.extract() for s in html('style')]

            for css in css_content:
                text = text.replace(css.text, '')


            with open(dir_path + '/' + file_name, 'w') as f:
                f.write(text)
