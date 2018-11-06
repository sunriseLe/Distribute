#coding=utf-8

import os

import requests


class ServerInterface:
    def __init__(self, workDir, server):
        self.workDir = workDir
        self.server = server
        self.token = ''

    # 获取绝对路径
    def getAbsolutePath(self, path):
        return os.path.join(self.workDir, path)

    # 切换当前工作目录
    def cd(self, dirPath):
        if dirPath != '.':
            if dirPath == '..':
                if self.workDir != '/': # workDir不是根目录，获取当前运行脚本的绝对路径
                    self.workDir = os.path.dirname(self.workDir)
            elif os.path.isabs(dirPath): # 判断是否为绝对路径,形式类似/home/..或/home
                self.workDir = dirPath # 绝对路径直接赋值
            else: #将目录和文件名合成一个路径
                self.workDir = os.path.join(self.workDir, dirPath)
        print(self.workDir)

    # 创建目录
    def mkdir(self, dirPath):
        response = requests.post(self.server + '/file/createDir', # 访问路径http://localhost:80/file/createDir
                                 {'dirPath': self.getAbsolutePath(dirPath), 'token': self.token}) # 客户端向服务器端回传token，验证身份
        return response.json()

    # 显示文件列表，默认显示当前工作目录
    def ls(self, dirPath=None):
        response = requests.post(self.server + '/file/list', # 访问路径http://localhost:80/file/list
                                 {'dirPath': self.getAbsolutePath(dirPath or self.workDir), 'token': self.token})
        return response.json()

    # 上传本地文件
    def up(self, localFilePath, destDirPath): # 将本地文件上传到云盘中某一目录
        if os.path.exists(localFilePath) and not os.path.isdir(localFilePath): # 判断本地文件是否存在
            response = requests.post(self.server + '/file/upload', # 访问路径http://localhost:80/file/upload
                                     {'destDirPath': self.getAbsolutePath(destDirPath), 'token': self.token},
                                     files={'file': open(localFilePath, 'rb')})#以二进制读模式打开本地文件
            return response.json()
        else:
            print('本地文件不存在，请检查路径')

    # 将云盘文件保存为本地某一文件
    def down(self, filePath, localFilePath):
        if not os.path.exists(localFilePath): # 本地文件不存在
            response = requests.post(self.server + '/file/download', # 访问路径http://localhost:80/file/download
                                     {'filePath': self.getAbsolutePath(filePath), 'token': self.token})
            if str(response.headers['Content-Type']).find('application/json') == -1:
                with open(localFilePath, 'wb') as f:
                    f.write(response.content)
                    print('下载成功')
            else:
                return response.json()
        else:
            print('本地文件已存在，请检查路径')

    # 重命名文件或目录
    def re(self, oldPath, newPath):
        response = requests.post(self.server + '/file/rename', # 访问路径http://localhost:80/file/rename
                                 {'oldPath': self.getAbsolutePath(oldPath), 'newPath': self.getAbsolutePath(newPath),
                                  'token': self.token})
        return response.json()

    #移动文件或目录
    def mv(self, oldPath, newPath):
        response = requests.post(self.server + '/file/move', # 访问路径http://localhost:80/file/move
                                 {'oldPath': self.getAbsolutePath(oldPath), 'newPath': self.getAbsolutePath(newPath),
                                  'token': self.token})
        return response.json()

    # 永久删除文件或目录
    def rm(self, path):
        response = requests.post(self.server + '/file/delete', # 访问路径http://localhost:80/file/delete
                                 {'path': self.getAbsolutePath(path), 'token': self.token})
        return response.json()

    #用户注册
    def signup(self, username, password):
        response = requests.post(self.server + '/user/signup', # 访问路径http://localhost:80/user/signup
                                 {'username': username, 'password': password})
        return response.json()

    #用户登录
    def login(self, username, password): # 访问路径http://localhost:80/user/login
        response = requests.post(self.server + '/user/login', {'username': username, 'password': password})
        result = response.json()
        if result['status'] == 200:
            self.token = result['token']
        return result

    #登出
    def logout(self): # 访问路径http://localhost:80/user/logout
        response = requests.post(self.server + '/user/logout', {'token': self.token})
        return response.json()
