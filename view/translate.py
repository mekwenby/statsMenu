from flask import request, render_template, Blueprint

from setting import Config
from view.Baidu_Text_transAPI import Translation

bp = Blueprint('S', __name__)
config = Config('config.yaml')
config.read()
translation = Translation(appid=config.data.get('Baidu_Translate_appid'),
                          appkey=config.data.get('Baidu_Translate_appkey'))


@bp.route('/', methods=['POST', 'GET'])
def translate():
    if request.method == 'GET':
        return render_template('translate.html')
    else:
        text = request.form.get('source')
        mode = request.form.get('mode')
        if mode == 'ez':
            out = translation.query_en_zh(text)
        elif mode == 'ze':
            out = translation.query_zh_en(text)
        elif mode == 'jz':
            out = translation.query_jp_zh(text)
        elif mode == 'zj':
            out = translation.query_zh_jp(text)
        else:
            out = 'Error'

        return out
