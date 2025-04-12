import time
from utils import *

import time
from utils import *
from turtle import st
import cmd  # 新增导入

class Aria2cShell(cmd.Cmd):
    intro = '欢迎使用aria2c管理控制台(输入help获取帮助)'
    prompt = '(aria2c) '
    
    def do_status(self, arg):
        """查看aria2c状态"""
        if check_aria2c_rpc():
            print("aria2c正在运行")
        else:
            print("aria2c未运行")
    
    def do_start(self, arg):
        """启动aria2c服务"""
        start_aria2c_rpc()
    
    def do_stop(self, arg):
        """停止aria2c服务"""
        stop_aria2c_rpc()
    
    def do_exit(self, arg):
        """退出程序"""
        print("正在退出...")
        return True



def main():
    print("Hello from aria2c-mcp!")
    print("check if have aria2c")
    auto_download_aria2c()
    auto_download_ariang()
    create_default_config()

    if not check_aria2c_rpc():
        print("not found aria2c-rpc, start it")
        start_aria2c_rpc()
    else:
        print("found aria2c-rpc, stop it")
        stop_aria2c_rpc()
        start_aria2c_rpc()
    
    time.sleep(1)
    start_ariang()

    Aria2cShell().cmdloop()




if __name__ == "__main__":
    main()
