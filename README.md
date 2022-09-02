# TMOOC 视频下载脚本
一键下载TMOOC视频脚本
**注意：对于付费资源需要有相应权限才能下载。另外，代码只做学习交流用途，请勿用于非法情景。**
## 依赖
python >= 3.7.2

pip >= 19.0.2

selenium >= 4.4.0
- 下载对应chrome版本的chromedriver 放在同级目录下
* [chromedriver](https://registry.npmmirror.com/binary.html?path=chromedriver/)
## 食用
1.执行下述命令。

```
python3 GetDownloadvideoUrl.py
```
2.登录视频的网址，把视频地址复制

```
如 https://tts.tmooc.cn/video/showVideo?menuId=981376&version=xxx
```

3.粘贴复制的网站

输入到控制台
```
请输入开始回放地址：https://tts.tmooc.cn/video/showVideo?menuId=981376&version=xxx
```
4.执行后效果
```
请输入开始回放地址: https://tts.tmooc.cn/video/showVideo?menuId=981376&version=xxx
请输入结束回放地址: https://tts.tmooc.cn/video/showVideo?menuId=981335&version=xxx
START: 981376---- END:981335

5.6上午视频
https://c.it211.com.cn/xxx/xxx.m3u8?_time=xxxx&sign=xxxx

5.6下午视频
https://c.it211.com.cn/xxx/xxxx.m3u8?_time=xxx&sign=xxxx
```
***注意如果解析不到下载地址，检查脚本的关键字是否和播放网站匹配默认为`视频`,也有可能是别的`视频回放`等,获取不到请多运行几次脚本
## 下载方法
- windows平台推荐
[N_m3u8DL-CLI](https://github.com/nilaoda/N_m3u8DL-CLI)
- mac平台推荐
[N_m3u8DL-RE](https://github.com/nilaoda/N_m3u8DL-RE)
* 别的m3u8下载工具支持aes加密的也可以下载
* 生成脚本默认就是使用这两个工具
* 工具和脚本脚步同一目录下执行即可