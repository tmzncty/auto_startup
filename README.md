# auto_startup
一个自动添加当前进程到开机启动的工具，也可以用于单独设置开机启动项。感谢GPT-4！

我没写中文，需要的话自己改改代码就行。

![image](https://github.com/tmzncty/auto_startup/assets/72063145/1c4227b6-4b7d-48e8-9ebb-2f5efa795c26)

写了暗黑模式。

![image](https://github.com/tmzncty/auto_startup/assets/72063145/fd476de4-30d1-4ef1-b460-2bbb67c0d97f)

# 适用范围
WINDOWS
# 使用方法
## py文件
```
pip install -r requirements.txt
```
然后运行auto_startup_with_gui.py即可
## exe文件
直接双击即可。
# 注意事项
## 倒计时
我是因为懒得自己点所以设置的20秒，需要的话可以自己调整。具体看代码就行，几个数值，但是单位是毫秒。丢到GPT里面让他改改也行。
# 测试情况
Windows Server 2022 Datacenter测试通过，其他懒得弄，需要去问GPT就行。

# **下面可以不用看**







# 缘起
现在才是说背景的时候。我不好说是因为技嘉的MZ31-AR0问题还是7302问题。参看https://www.bilibili.com/read/cv26863982
PowerShell运行powercfg.exe /hibernate on报错
```
Hibernation failed with the following error: The request is not supported.

The following items are preventing hibernation on this system.
        The system firmware does not support hibernation.
休眠失败，出现以下错误：请求不受支持。

下列项目将阻止此系统的休眠。
系统固件不支持休眠
```
![bf609182bb19643f7e446910d4cf02c](https://github.com/tmzncty/auto_startup/assets/72063145/940ab5fd-429f-44eb-938e-e99084ba972d)
![995492e83f71ba7e176b8be6db75b73](https://github.com/tmzncty/auto_startup/assets/72063145/46df9073-6b7d-45ad-8071-3a04b77876e8)

死活就是不能休眠，那样的话就只能迫真休眠了。干脆自己记录我开机前有啥进程，然后下次开机的时候自动打开。（问就是学校断电不然没那么多事情）
而且我也调整过注册表内容和组策略内容，干脆就先这样吧。

