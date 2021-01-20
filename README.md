# rpi-envsys

本项目为树莓派家庭环境管理系统，使用了自制传感器集成板+外接屏幕+Arduino 开发板实现，够让用户直观的了解居住环境中挥发性有机化合物、温度、湿度、光强、二氧化碳等排量等信息以保障居住者居住环境的安全。

项目基于 B/S 架构，采用了 Python、PHP、HTML5、Bootstrap、jQuery、Vue.js 等技术，使用树莓派和 Arduino 平台，实现了一个多功能的家庭环境监控系统。该系统能让用户随时了解家庭环境的实时状况，能在环境不安全时控制一些设备，并能对居住者进行提醒，还有一些实用性的功能。产品具有界面美观，实用性强、后续扩展性好等特点。

本项目为综合项目，需要自己定制 PCB 板和购买相关零件进行焊接，具体见`doc/README.pdf`

### 项目截图

![1](https://github.com/LemoFire/rpi-envsys/raw/master/doc/1.png)

![2](https://github.com/LemoFire/rpi-envsys/raw/master/doc/2.png)

![3](https://github.com/LemoFire/rpi-envsys/raw/master/doc/3.png)

### 文件夹及基本说明

- arduino

  arduino 代码，直接烧入 arduino 即可

- python

  树莓派端主程序，配置好 config.conf 后直接使用 python3 运行 main.py 即可

- schematics

  电路图及 PCB 板，使用立创 EDA 打开即可

### Demo

（Demo 只展示前端部分）
[https://proj.ito.fun/rpiEnvSys/](https://proj.ito.fun/rpiEnvSys/)
