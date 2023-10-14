![DQ(SZI}DE_T%@{KS2F{OMRH](https://github.com/wdy-pursue/rha/assets/57004624/54020a86-82d0-42d3-8443-d61efcfbd275)# 介绍
利用Stable-Diffution API去除图片ai感

使用Stable-Diffution API进行自动化跑图的测试过程中，我们发现一个特性，通过调整重绘幅度，可以逐渐去除图片上的阴影，从而达到去除ai感的结果。我们猜测这可能是tile的预处理器的模糊化导致的。

编写程序的初衷是节省人力劳动，批量出图，最初是为我们自己的工作室项目而创建的，但由于种种原因，我们未能将其投入实际生产环境。因此，我们决定将其分享出来，以便更多的开发者能够受益并继续研究和优化这一特性。



# 效果
![}QX(VNPE)R}XG4NOG(VJI(V](https://github.com/wdy-pursue/rha/assets/57004624/c7880b23-b13e-48c6-9e7b-1cf32002c49f)
![%2P~JCMSGYADC RSUY8}8_M](https://github.com/wdy-pursue/rha/assets/57004624/f32ac04c-1ddd-4848-97fe-6412045e21b0)



# 使用
配置python地址，双击bat文件即可，通过修改config目录下的json文件内容来修改参数。
