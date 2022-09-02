# -*- coding: utf-8 -*-
# @Time   : 2022-08-30 11:59
# @Name   : GetDownloadvideoUrl.py

import json
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import sys
import os
import re
import signal

caps = {
    "browserName": "chrome",
    'goog:loggingPrefs': {'performance': 'ALL'}  # 开启日志性能监听
}
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")  # 指定端口为9527
e = dict() # 存储下载地址Map(filename, url)
#判断操作系统
def os_system():
    if sys.platform == 'linux':
        return 'linux'
    elif sys.platform == 'win32':
        return 'win'
    elif sys.platform == 'darwin':
        return 'mac'
    else:
        return 'other'  
print(os_system())
if os_system() == 'win':
    # 打开chrome浏览器
    res=subprocess.Popen("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9527 ",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    browser = webdriver.Chrome(desired_capabilities=caps, options=options,executable_path='chromedriver.exe')
elif os_system() == 'linux':
    print('linux Unsupported')
    sys.exit()
elif os_system() == 'mac':
     # 打开chrome浏览器
    res=subprocess.Popen("/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome -remote-debugging-port=9527 ",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    browser = webdriver.Chrome(desired_capabilities=caps, options=options,executable_path='./chromedriver')
else:
     sys.exit()
PID=res.pid

# 过滤文件
def filter_type(_type: str):
    types = [
        # 'application/javascript', 'application/x-javascript', 'text/css', 'webp', 'image/png', 'image/gif',#目标 
        # 'image/jpeg', 'image/x-icon', 'application/octet-stream','application/json','audio/mpeg','text/html','text/html','text/plain','text/javascript','video/mp2t'
        'application/vnd.apple.mpegurl'
    ]
    if _type not in types:
        return False
    return True
# 获取响应中m3u8地址 
def getUrl(filename):
    performance_log = browser.get_log('performance')  # 获取名称为 performance 的日志
    for packet in performance_log:
        message = json.loads(packet.get('message')).get('message')  # 获取message的数据
        if message.get('method') != 'Network.responseReceived':  # 如果method 不是 responseReceived 类型就不往下执行
            continue
        packet_type = message.get('params').get('response').get('mimeType')  # 获取该请求返回的type
        if not filter_type(_type=packet_type):  # 过滤非需要type
            continue
        url = message.get('params').get('response').get('url')  # 获取 该请求  url
        print(url)
        print()
        e[filename]=url #存入map
# 获取每天视频       
def playUrl(url):
    browser.get(url)
    time.sleep(1)
    videolink = browser.find_elements(By.PARTIAL_LINK_TEXT,'视频') # 播放列表关键字
    for i in videolink:
        print (i.text)
        i.click()
        time.sleep(1)
        fileName = i.text
        getUrl(fileName)
        time.sleep(3) 


# 输出到文件
def OutputFile():
    with open('videourl.json','a',encoding= 'utf-8') as file_read:
        json.dump(e, file_read,ensure_ascii=False)
    with open('script.bat','a',encoding='utf-8') as f:
        f.write("chcp 65001\n@echo off\n")
        for key in e:
            f.write("N_m3u8DL-CLI_v3.0.2.exe \""+e[key]+"\" --workDir \"%USERPROFILE%\Downloads\\tmooc\" --saveName \""+key+"\" --enableDelAfterDone --headers \"Referer:https://tts.tmooc.cn/\" --maxThreads \"32\"\n")
    with open('script.sh','a',encoding='utf-8') as f:
        f.write("#!/bin/bash\n")
        for key in e:
            f.write("./N_m3u8DL-RE \""+e[key]+"\" --save-dir \"Downloads/tmooc\" --save-name \""+key+"\" --del-after-done --header \"Referer:https://tts.tmooc.cn/\" --thread-count \"32\" --download-retry-count \"10\" --ffmpeg-binary-path \"/usr/local/Cellar/ffmpeg/5.1/bin/ffmpeg\"\n")
def splitStr(url:str):
    reg="https://tts.tmooc.cn/video/showVideo"
    if reg in url:
        data = re.split('=|\&',url)
        return data[1]
    else:
        print("url 不正确")
        return ""
def main():
    time.sleep(1)
    browser.get('https://tts.tmooc.cn/studentCenter/toMyttsPage')
    # 自动登录
    # time.sleep(1)
    # browser.find_element(By.ID,'login_xxw').click()
    # time.sleep(1)
    # browser.find_element(By.ID,'js_account_pm').send_keys('xxx@qq.com') #账号
    # browser.find_element(By.ID,'js_password').send_keys('xxx') #密码
    # browser.find_element(By.ID,'js_submit_login').click()
    time.sleep(1)
    print('请先登录账号再进行操作')
    startStr = input("请输入开始回放地址: ")
    try:
        SRART= (int)(splitStr(startStr))
    except ValueError:
        print("输入错误")
        return
    endStr = input("请输入结束回放地址: ")
    try:
        END = (int)(splitStr(endStr))
    except ValueError:
        print("输入错误")
        return
    print("START: "+str(SRART)+"---- END:"+str(END))
    if SRART<END:
        print("输入错误")
        return
    # 创建播放回放地址
    # 'https://tts.tmooc.cn/video/showVideo?menuId=99992&version=JSDXXXXXXX'
    for x in range(SRART,END-1,-1):
        basicUrl=startStr.replace(str(SRART),str(x)) # 创建播放回放地址
        playUrl(basicUrl) #播放视频获取m3u8地址
    OutputFile() #输出到文件
  

main()
os.kill(PID,signal.SIGINT)
