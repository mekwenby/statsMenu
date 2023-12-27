# MD处理器
import os

import markdown2


def md_to_html(file):
    with open(file, encoding='utf-8') as f:
        md = f.read()
    html = markdown2.markdown(md, extras=['fenced-code-blocks', 'code-friendly', 'tables'])
    return html


def read_file(file):  # 读取文件
    with open(file, 'r', encoding='utf-8') as file:
        Data = file.read()
        return Data


def get_md_file_list():
    return os.listdir(os.path.join('static', 'markdown'))


def save_to_file(file_path, content):
    with open(file_path, 'w') as f:
        f.write(content)
