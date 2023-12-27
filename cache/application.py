class Application:
    def __init__(self):
        """
        serial 序号,决定图标排列顺序
        name 应用名词
        genre 应用类型
        value 跳转路径

        ico_genre 图标类型
        ico_value 图标的值
        ico_size 应用磁贴大小 (1 or 2)

        genre: link(链接) wol(网络唤醒)
        ico_genre: text(文本) image(图标)

        """
        self.serial = 1
        self.name = None
        self.genre = None
        self.value = None
        self.ico_genre = None
        self.ico_value = None
        self.ico_size = 1


if __name__ == '__main__':
    app = Application()
    app.name = 'baidu'
    app.genre = 'link'
    app.value = 'https://www.baidu.com/'
    app.ico_genre = 'text'
    app.ico_value = 'Bai'
