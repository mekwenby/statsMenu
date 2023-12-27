import os
import time

from flask import Flask, request, jsonify, render_template, make_response, redirect, send_file
from flask_bootstrap import Bootstrap4
import cache
import Mek_master as Mm
import cache.mddispose as mpe
import expand
from setting import Config

app = Flask(__name__)

# 启用拓展
expand.expand(app)

# 加载配置
config = Config('config.yaml')
config.read()

app.my_config = config

bootstrap = Bootstrap4(app=app)

app.config['BOOTSTRAP_SERVE_LOCAL'] = True
SECRET_KEY = 'YOUR_BACKEND_SECRET_KEY'  # 替换为你的后端密钥
correct_password = config.data.get('Lock_screen_password')
print('Your Lock_screen_password :', config.data.get('Lock_screen_password'))


@app.template_filter('wallpaper')
def wallpaper(s):
    """每10分钟换一次壁纸"""
    time_t = int(time.time() // 600) % len(cache.wallpaper_list)  # 时序
    image = cache.wallpaper_list[time_t]
    return '/static/wallpaper/' + image


@app.template_filter('color')
def color(s):
    """随机颜色获取"""
    return cache.get_color()


@app.route("/")
def index():
    return render_template("Lock.html")


@app.route("/start")
def start():
    """
    获取token
    验证是否与cache内一致
    是: 前往首页
    否: 重定向到解锁页
    """

    token = request.cookies.get('token')
    if token in cache.token:
        return render_template('start.html', app_list=cache.new_app_list())
    else:
        return redirect('/')


@app.route('/lock')
def clock():
    response = make_response(redirect('/'))
    response.delete_cookie('token', path='/', domain=None)
    return response


@app.route('/Set')
def Set():
    token = request.cookies.get('token')
    print(token)
    if token in cache.token:
        return render_template('Set.html')
    else:
        return redirect('/')


@app.route('/manage_app')
def manage_app():
    token = request.cookies.get('token')
    if token in cache.token:
        return render_template('Manage_App.html', app_list=cache.new_app_list())
    else:
        return redirect('/')


@app.route('/test')
def test():
    return render_template('upfile.html')


@app.route("/api/check_password", methods=["POST"])
def check_password():
    data = request.get_json()
    provided_password = data.get("password", "")

    # 验证输入的密码是否正确
    is_valid_password = provided_password == correct_password

    if is_valid_password:
        # 生成一个认证Cookie
        response = make_response(jsonify({"isValid": True}))
        token = Mm.get_random_hax()
        cache.token.append(token)
        age = config.data.get('Password_validity_period')
        if age is None:
            age = 86400
        response.set_cookie("token", token, max_age=age)
        return response
    else:
        return jsonify({"isValid": False})


@app.route('/api/get_sys_stats')
def get_sys_stats():
    """
    :return: {'load': '0.0|0.0', 'cpuusage': 9.1, 'memusage': 22.9}
    """
    return cache.get_sys_info()


@app.route('/upload_app', methods=['POST'])
def upload_file():
    def is_allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['yaml', 'json']

    if 'file' in request.files:
        uploaded_file = request.files['file']
        if uploaded_file and is_allowed_file(uploaded_file.filename):
            # 处理上传的文件，例如保存到特定位置
            uploaded_file.save(Mm.file_path_link('static', 'apps', uploaded_file.filename))

            return '应用安装成功'
        else:
            return '只能上传后缀名为.yaml或.json的文件'
    else:
        return '没有选择文件'


@app.route('/upload_image', methods=['POST'])
def upload_file_images():
    def is_allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['png', 'webp']

    if 'file' in request.files:
        uploaded_file = request.files['file']
        if uploaded_file and is_allowed_file(uploaded_file.filename):
            # 处理上传的文件，例如保存到特定位置
            uploaded_file.save(Mm.file_path_link('static', 'images', uploaded_file.filename))

            return '图标上传成功'
        else:
            return '只能上传后缀名为png/webp的文件'
    else:
        return '没有选择文件'


@app.route('/upload_wallpaper', methods=['POST'])
def upload_file_wallpape():
    def is_allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['png', 'webp', 'jpg']

    if 'file' in request.files:
        uploaded_file = request.files['file']
        if uploaded_file and is_allowed_file(uploaded_file.filename):
            # 处理上传的文件，例如保存到特定位置
            uploaded_file.save(Mm.file_path_link('static', 'wallpaper', uploaded_file.filename))

            return '图标上传成功'
        else:
            return '只能上传后缀名为png/webp/jpg的文件'
    else:
        return '没有选择文件'


@app.route('/upload_md', methods=['POST'])
def upload_file_md():
    def is_allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['md']

    if 'file' in request.files:
        uploaded_file = request.files['file']
        if uploaded_file and is_allowed_file(uploaded_file.filename):
            # 处理上传的文件，例如保存到特定位置
            uploaded_file.save(Mm.file_path_link('static', 'markdown', uploaded_file.filename))

            return '文件上传成功'
        else:
            return '只能上传后缀名为.md的文件'
    else:
        return '没有选择文件'


@app.route('/del_app')
def del_app():
    token = request.cookies.get('token')
    if token in cache.token:
        file_name = request.args.get('file')
        print(file_name, request.path)
        file_path = Mm.file_path_link('static', 'apps', file_name)
        if Mm.isfile(file_path):
            Mm.rm(file_path)
        cache.app_list = []
        cache.build_list_apps()
        return redirect('/manage_app')
    else:
        return redirect('/')


@app.route('/get_app')
def get_app():
    token = request.cookies.get('token')
    if token in cache.token:
        file_name = request.args.get('file')
        try:
            # 设置文件路径
            file_path = Mm.file_path_link('static', 'apps', file_name)
            # 发送文件
            return send_file(file_path, as_attachment=True)

        except FileNotFoundError:
            return "File not found"
    else:
        return redirect('/')


@app.route('/get')
def get_file():
    file_name = request.args.get('file')
    try:
        # 设置文件路径
        file_path = Mm.file_path_link('static', 'upload', file_name)
        # 发送文件
        return send_file(file_path, as_attachment=True)

    except FileNotFoundError:
        return "File not found"


@app.route('/wallpaper')
def wallpaper():
    token = request.cookies.get('token')
    if token in cache.token:
        wallpaper_list = os.listdir(os.path.join('static', 'wallpaper'))
        return render_template('wallpaper.html', wallpaper_list=wallpaper_list)
    else:
        return redirect('/')


@app.route('/markdown/<path>', methods=['POST', 'GET'])
def manage_markdown(path):
    if request.method == 'GET':
        file_name = request.args.get('file')
        if file_name is not None:
            file_path = Mm.file_path_link('static', 'markdown', file_name)
        if path == 'manage':  # 查看管理文件列表路由
            return render_template('Manage_MD.html', filelist=mpe.get_md_file_list())
        elif path == 'view':  # 查看文件路由
            if file_name is not None and Mm.isfile(file_path):
                return render_template('md_engine.html', filename=file_name, md=mpe.md_to_html(file_path))
            else:
                return render_template('md_engine.html', filename=file_name, md="没有找到该文件")
        elif path == 'edit':
            if file_name is not None and Mm.isfile(file_path):
                return render_template('md_edit.html', filename=file_name, md=mpe.read_file(file_path))
            else:
                return render_template('md_edit.html', filename=file_name, md="没有找到该文件")

        elif path == 'del':
            if file_name is not None and Mm.isfile(file_path):
                Mm.rm(file_path)

            return redirect('/markdown/manage')

        else:
            return redirect('/start')
    elif request.method == 'POST':
        file_name = request.form['file']
        markdown_content = request.form['markdown']

        # 获取文件路径
        file_path = Mm.file_path_link('static', 'markdown', file_name)

        # 保存Markdown内容到文件
        mpe.save_to_file(file_path, markdown_content)

        # 重定向到查看文件的页面
        return redirect(f'/markdown/view?file={file_name}')

        # 如果是GET请求，直接重定向到编辑页面
    return redirect('/markdown/manage')


@app.route('/Sync')
def flushed():
    """刷新系统缓存"""
    token = request.cookies.get('token')
    if token in cache.token:
        cache.app_list = []
        cache.build_list_apps()
        return redirect('/start')
    else:
        return redirect('/')


@app.route('/del_wallpaper/<name>')
def del_wallpaper(name):
    token = request.cookies.get('token')
    if token in cache.token:
        file_path = Mm.file_path_link('static', 'wallpaper', name)
        if Mm.isfile(file_path):
            Mm.rm(file_path)
        cache.wallpaper_list = os.listdir(os.path.join('static', 'wallpaper'))  # 壁纸加载路径
        return redirect('/wallpaper')
    else:
        return redirect('/')


@app.route('/set_wallpaper/<name>')
def set_wallpaper(name):
    token = request.cookies.get('token')
    if token in cache.token:
        if name == 'REC':
            cache.wallpaper_list = os.listdir(os.path.join('static', 'wallpaper'))
        else:
            cache.wallpaper_list = [name]
        return redirect('/wallpaper')
    else:
        return redirect('/')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
