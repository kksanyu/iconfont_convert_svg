iconfont_convert_svg
=====
[![License](https://img.shields.io/github/license/kksanyu/iconfont_convert_svg)](https://github.com/kksanyu/iconfont_convert_svg)

### 概述

可以将 `iconfont` 生成的 `svg` 拆分并还原成多个 `svg`, 拆分后的文件可直接上传 `iconfont` 官网。

[iconfont官网传送门](https://www.iconfont.cn/)

### 安装依赖

```shell
# svg路径解析工具
$ pip install svgpathtools
```

### 使用

```shell
# python convert.py --file 字体文件 --output 输出文件目录
$ python convert.py --file font_1323992_b66zu86ei89.svg --output out
```

### 相关查阅文档

- [理解SVG坐标系统和变换： transform属性](https://www.bbsmax.com/A/o75NOL4PdW/)

- [理解SVG transform坐标变换(转)](https://www.jianshu.com/p/bf8eb5502afa)

- [SVG翻转 --- ZC测试(1)](https://www.cnblogs.com/h5skill/p/6878849.html)

- [CSS3 transform 属性](https://www.w3school.com.cn/cssref/pr_transform.asp)

### License

The MIT License(http://opensource.org/licenses/MIT)

请自由地享受和参与开源

