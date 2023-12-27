from view.translate import bp as translate

"""
Flask 拓展蓝图
"""


def expand(app):
    # 挂载翻译插件
    app.register_blueprint(translate, url_prefix='/translate')

