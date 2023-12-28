"""
项目启动脚本
build: 20231227
"""

from gevent import monkey
from gevent.pywsgi import WSGIServer

monkey.patch_all()

from multiprocessing import cpu_count
from multiprocessing import Process
from app import app


def run(MULTI_PROCESS):
    if MULTI_PROCESS == False:
        WSGIServer(('0.0.0.0', 12380), app).serve_forever()
    else:
        mulserver = WSGIServer(('0.0.0.0', 12380), app)
        mulserver.start()

        def server_forever():
            mulserver.start_accepting()
            mulserver._stop_event.wait()

        for i in range(cpu_count()):
            p = Process(target=server_forever)
            p.start()


if __name__ == "__main__":
    # 单进程 + 协程 适应 Windows
    run(False)
    # 多进程 + 协程 适应 Linux
    # run(True)
