# FGO_Bluetooth_Helper

这是一个基于蓝牙模块操作手机的FGO 游戏助手。可实现重复战斗，定制3T脚本，友情池抽取，无限池抽取，
搓丸子等功能。 生活不易，享受游戏。

###### 此项目为重构与功能定制需要，项目来源为[MacLauren12345](https://github.com/McLaren12345/FGO_Bluetooth_Assistant/)

## Getting Started

以下为部署和运行需求

### Prerequisites

1. window PC机 测试通过环境为win10.
2. 安装anaconda 64位windows运行环境.
3. 为了速度可添加国内源
```
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/

```
4. 机型为非曲面屏机型。 测试机型iPhone 6/6s.版本12以上可支持蓝牙鼠标。
5. tb搜索 蓝牙鼠标模块，价格在30-50不等。标准模块是一个连接模块和蓝牙模块。
一定和店家确认是要连接电脑的，问清楚少了部件。
插上usb口后能手机搜索到即可，


### Installing

##### 安装步骤 
- 项目根目录下有conda 移植环境配置文件
requirement.txt. 执行命令

```
conda create --name <fgo> --file requirement.txt
```

此命令将会创建 conda环境 name=fgo,并安装所有需要的package.

- 运行方法为：
1. 通过 Airplayer 将手机投影到PC 
2. 打开 Anaconda Prompt
```
cd 项目根目录
conda activate fgo
python main_function.py
```
- 脚本在/script/下，大家可以参照示例脚本更改做自己的战斗流程。
基本流程为角色技能,服装技能(充能服 换人等),释放宝具。
```
    # 1号角色使用技能2
    character_skill(mouse_instance=mouse_instance, character_number=1, skill_number=2)
    # 2号角色使用技能1,作用目标为角色1
    character_skill(mouse_instance=mouse_instance, character_number=2, skill_number=1, skill_target=1)
    character_skill(mouse_instance=mouse_instance, character_number=3, skill_number=1, skill_target=1)
    # 充能服充能1号位置
    cast_master_skill(mouse_instance=mouse_instance, skill_number=4, swap_target_1=1, swap_target_2=None)
    # 使用换人技能，交换(1,4)号角色
    cast_master_skill(mouse_instance=mouse_instance, skill_number=3, swap_target_1=2, swap_target_2=4)
    # 1号角色使用宝具 
    act_and_use_ultimate_skill(mouse_instance=mouse_instance, ultimate_skill=1)
```

## 自己定制？
通过截取游戏内的标志性图片，你也可以定制自己的功能。
流程为 
1. 识别图片-> 
2. 成功识别代表进入状态—> 
3. 使用BlueToothMouse 操作鼠标进行操作

运行 /util/CVModule.py 在/output 下会有当前屏幕截图。截取自己需要的图标后利用CVModule 调整坐标，
就可以获取需要点击的坐标了。


## Versioning

1.0.0
## Authors

* **guihehans** 

## Acknowledgments

* 感谢 [MacLauren的项目启发](https://github.com/McLaren12345/FGO_Bluetooth_Assistant/)
