# 介绍
利用Stable-Diffution API去除图片ai感

使用Stable-Diffution API进行自动化跑图的测试过程中，我们发现一个特性，通过调整重绘幅度，可以逐渐去除图片上的阴影，从而达到去除ai感的结果。我们猜测这可能是tile的预处理器的模糊化导致的。

编写程序的初衷是节省人力劳动，批量出图，最初是为我们自己的工作室项目而创建的，但由于种种原因，我们未能将其投入实际生产环境。因此，我们决定将其分享出来，以便更多的开发者能够受益并继续研究和优化这一特性。



# 效果
处理前：
![}QX(VNPE)R}XG4NOG(VJI(V](https://github.com/wdy-pursue/rha/assets/57004624/6fa727df-1aac-41bd-abc6-914dc4fa0ea7)
处理后是经过脚本处理后TD TV直接放大的版本：
![%2P~JCMSGYADC RSUY8}8_M](https://github.com/wdy-pursue/rha/assets/57004624/7dcee974-4116-4bac-82ef-e63e9d91b85d)
处理前：
![DQ(SZI}DE_T%@{KS2F{OMRH](https://github.com/wdy-pursue/rha/assets/57004624/e0b9ed82-3119-4c78-a0df-bb233b0c983f)
处理后是经过脚本处理后TD TV直接放大的版本：
![Q_S V{306%LP1A77KYGIVF8](https://github.com/wdy-pursue/rha/assets/57004624/7ccb4525-f5d6-4430-95cc-a26a80be9fd7)
处理前：
![RU}UREG_ )}CG1Q9{0N`KAK](https://github.com/wdy-pursue/rha/assets/57004624/9b08d3dd-3d42-4303-b48f-74f63bc25d83)
处理后是经过脚本处理后TD TV直接放大的版本：

![%E@SK@_`V0 UW)9 6GXX{D6](https://github.com/wdy-pursue/rha/assets/57004624/926e68e6-bcb0-4faa-8757-a8422efd0dd0)




# 使用
配置python地址，双击bat文件即可，通过修改config目录下的json文件内容来修改参数。

对于json文件中的秘钥部分，如果使用的是秋叶大佬的版本，设置一下 ![C6JI7D$Z4UTP3KDBV(EYUNG](https://github.com/wdy-pursue/rha/assets/57004624/162b2113-f935-4822-a2e5-4327c53d0184) 
不会找秘钥位置的朋友直接设置账号密码为123,123，秘钥为 Basic d2R5OndkeQ== 

如果使用的是原版sd，启动时添加这个参数即可： --api --autolaunch --api-auth 123:123 
