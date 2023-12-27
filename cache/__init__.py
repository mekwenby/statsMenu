import os
from random import randint

import psutil
import yaml

import Mek_master
from cache.application import Application as cApp

"""
缓存,将常用的固定资源和数据加载到内存以降低IO负担
"""

color_list = [  # 前端颜色列表
    (121, 82, 179), (66, 133, 244), (234, 67, 53), (251, 188, 5), (52, 168, 83), (0, 143, 0), (0, 191, 242),
    (218, 83, 44), (188, 29, 73), (212, 74, 39), (160, 0, 167), (44, 134, 238)
]

wallpaper_list = os.listdir(os.path.join('static', 'wallpaper'))  # 壁纸加载路径
token = []

app_list = []


def new_app_list():
    return sorted(app_list, key=lambda x: x.serial)


# 获取颜色,前端使用
def get_color():
    return color_list[randint(0, len(color_list) - 1)]


# 获取壁纸,前端使用
def get_wallpaper():
    return 'static/wallpaper/' + wallpaper_list[randint(0, len(wallpaper_list) - 1)]


def get_sys_info():
    return {'load': f"{psutil.getloadavg()[0]}|{psutil.getloadavg()[1]}", 'cpuusage': psutil.cpu_percent(),
            'memusage': psutil.virtual_memory().percent}


# 写入yaml 文件
def w_yaml(file, data):
    with open(file, 'w', encoding='utf8') as file:
        yaml.dump(data, file, default_flow_style=False)


# 读取yaml 文件
def r_yaml(file):
    with open(file, 'r', encoding='utf8') as file:
        data = yaml.safe_load(file)
        return data


def restore_app_object(dics):
    """
    从字典 dics 中提取Application对象并返回
    :param dics:
    :return: App
    """
    app = cApp()
    app.name = dics.get('name')
    app.genre = dics.get('genre')
    app.value = dics.get('value')
    app.ico_genre = dics.get('ico_genre')
    app.ico_value = dics.get('ico_value')
    app.ico_size = dics.get('ico_size')
    app.serial = dics.get('serial')

    return app


def build_list_apps():
    """
    遍历 static/apps 目录,读取所有yaml文件
    """
    for file in os.listdir(os.path.join('static', 'apps')):
        file_path = os.path.join('static', 'apps', file)
        if Mek_master.get_file_class(file)[1] == '.yaml':
            try:
                app_data = r_yaml(file_path)
                app = restore_app_object(app_data)
                app.file = file
                app_list.append(app)
            except:
                pass


build_list_apps()
