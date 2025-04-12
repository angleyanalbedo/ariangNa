import os
import platform
import subprocess
import requests
import zipfile
import tarfile
import shutil
import atexit  # 新增导入

# 检查有没有aria2NG
def check_aria2NG():
    """检查当前目录下是否存在 AriaNg"""
    return os.path.exists("AriaNg") or os.path.exists("AriaNg/index.html")
def download_ariang():
    """下载 AriaNg"""
    url = "https://github.com/mayswind/AriaNg/releases/download/1.3.10/AriaNg-1.3.10-AllInOne.zip"
    filename = "AriaNg.zip"

    print(f"正在下载 AriaNg 到当前目录...")
    response = requests.get(url, stream=True)
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall("AriaNg")

    os.remove(filename)
    print("AriaNg 下载完成")

def check_aria2c():
    """检查当前目录下是否存在 aria2c"""
    return os.path.exists("aria2c") or os.path.exists("aria2c.exe")


def download_aria2c():
    """根据系统类型下载 aria2c"""
    system = platform.system()
    if system == "Windows":
        url = "https://github.com/aria2/aria2/releases/download/release-1.36.0/aria2-1.36.0-win-64bit-build1.zip"
        filename = "aria2.zip"
    elif system == "Linux":
        url = "https://github.com/aria2/aria2/releases/download/release-1.36.0/aria2-1.36.0-linux-glibc228-x86_64.tar.bz2"
        filename = "aria2.tar.bz2"
    elif system == "Darwin":  # macOS
        url = "https://github.com/aria2/aria2/releases/download/release-1.36.0/aria2-1.36.0-osx-darwin.dmg"
        filename = "aria2.dmg"
    else:
        print("不支持的操作系统")
        return

    print(f"正在下载 aria2c 到当前目录...")
    response = requests.get(url, stream=True)
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    if system == "Windows":
        with zipfile.ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall(".")
        os.rename("aria2-1.36.0-win-64bit-build1/aria2c.exe", "aria2c.exe")
        shutil.rmtree("aria2-1.36.0-win-64bit-build1")
    elif system == "Linux":
        with tarfile.open(filename, "r:bz2") as tar_ref:
            tar_ref.extractall(".")
        os.rename("aria2-1.36.0-linux-glibc228-x86_64/aria2c", "aria2c")
        shutil.rmtree("aria2-1.36.0-linux-glibc228-x86_64")
    elif system == "Darwin":
        print("macOS 下载完成后需要手动挂载 DMG 文件并安装")

    os.remove(filename)
    print("aria2c 下载完成")

def auto_download_aria2c():
    if check_aria2c():
        print("当前目录下已存在 aria2c，无需下载")
    else:
        download_aria2c()
        if not check_aria2c():
            print("下载失败")
            exit(1)
        print("下载成功")


def auto_download_ariang():
    if check_aria2NG():
        print("当前目录下已存在 AriaNg，无需下载")
    else:
        download_ariang()
        if not check_aria2NG():
            print("下载失败")
            exit(1)
        print("下载成功")
# 创建默认配置文件
def create_default_config():
    if not os.path.exists("aria2.conf"):
        with open("aria2.conf", "w") as f:
            f.write("enable-rpc=true\n"
                   "rpc-listen-all=true\n"
                   "rpc-listen-port=16800\n"
                   "rpc-allow-origin-all=true\n"
                   "dir=./Downloads")
        print("创建默认配置文件成功")
    else:
        print("配置文件已存在")

# 启动aria2c的rpc
def start_aria2c_rpc(config_file="aria2.conf"):
    log_file = open("aria2c.log", "a")  # 追加模式打开日志文件
    if platform.system() == "Windows":
        subprocess.Popen(["aria2c", "--conf-path=" + config_file],
                        stdout=log_file,  # 输出重定向到文件
                        stderr=log_file)  # 错误重定向到文件
    else:
        subprocess.Popen(["aria2c", "--conf-path=" + config_file, "--daemon=true"],
                        stdout=log_file,
                        stderr=log_file)
    print("aria2c started, 输出已重定向到aria2c.log")

# 检查aria2c是否有进程
def check_aria2c_rpc():
    if platform.system() == "Windows":
        result = subprocess.run(["tasklist", "/FI", "IMENAME eq aria2c.exe"], capture_output=True, text=True)
        return "aria2c.exe" in result.stdout
    else:
        result = subprocess.run(["ps", "-ef"], capture_output=True, text=True)
        return "aria2c" in result.stdout


# 停止aria2c的rpc
def stop_aria2c_rpc():
    if platform.system() == "Windows":
        subprocess.Popen(["taskkill", "/F", "/IM", "aria2c.exe"])
    else:
        subprocess.Popen(["pkill", "aria2c"])

def start_ariang():
    if platform.system() == "Windows":
        subprocess.Popen(["start", "", "AriaNg/index.html"], shell=True)  # Windows使用start命令
    else:
        subprocess.Popen(["xdg-open", "AriaNg/index.html"])  # Linux/Mac使用xdg-open
# 注册退出处理函数
atexit.register(stop_aria2c_rpc)

