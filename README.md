# statsMenu
### NAS开始页
### 它能做什么?

###### 书签管理
###### 翻译
###### 性能监控

### 如何启动?

克隆项目到本地

```bash
git clone https://github.com/mekwenby/statsMenu.git
```

安装依赖

```bash
pip install -r requirements.txt
```

DeBUG启动

```bash
python app.py
```

正式启动

编辑run.py 文件第32行

Windows 使用 run(False)

Linux 使用 run(True)

```python
if __name__ == "__main__":
    # 单进程 + 协程 适应 Windows
    run(False)
    # 多进程 + 协程 适应 Linux
    #run(True)
```

```bash
python run.py
```

本项目支持 Docker-Compose

```
docker-compose up -d
```



### 配置百度翻译API

编辑config.yaml 文件

填写正确的Baidu_Translate_appid和Baidu_Translate_appkey

API申请:https://api.fanyi.baidu.com/

```yaml
Baidu_Translate_appid: '20230*********'
Baidu_Translate_appkey: '*************_qD'
```



### 设置锁屏密码和Cookie过期时间

编辑config.yaml 文件

```yaml
Lock_screen_password: '1324'	# 锁屏密码
Password_validity_period: 86400	# 过期时间
```