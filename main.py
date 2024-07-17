import sys
from PyQt5.QtWidgets import QApplication
from ui.login_dialog import LoginDialog

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 加载样式
    with open('ui/style.qss', 'r') as f:
        style = f.read()
        app.setStyleSheet(style)

    # TODO
    '''
    来讲一下现在最头疼的配置问题：
        在 Interface 里新增 connect_to_database() 函数
        试图获取当前设备的 mysql 配置并连接
        这个应该放在整个程序的开头运行
        
        读配置文件：用户要自己去填写配置文件（或者读取失败了再返回来调窗口让用户填）
                    这里如果出现读取失败会 raise ConfigNotFoundException
                    这个异常类博大精深(
                    里面有一个函数可以返回枚举的列表，列表里是所有需要但缺失的数据名称
                    可以根据这个调前端的窗口让用户填
                    ***注意：
                        成功读入之后，再接下来的所有数据库操作均有可能返回异常
                        均为 pymysql.MySQLError
        
        现在这个函数在 Interface 初始化的时候运行
        但如果配置文件读取失败就还得反复调用
        所以位置不太合理
        以后放在哪就交给前端了
    '''
    login_window = LoginDialog()
    login_window.show()
    sys.exit(app.exec_())
