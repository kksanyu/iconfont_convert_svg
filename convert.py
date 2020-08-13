#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import xml
from svgpathtools.parser import parse_path

def main():

    parser = argparse.ArgumentParser(description='iconfont convert svg')
    parser.add_argument('-f', '--file', metavar='iconfont SVG文件', required=True)
    parser.add_argument('-o', '--output', metavar='输出目录', required=True)
    args = parser.parse_args()

    if not os.path.exists(args.file):
        raise Exception('SVG文件不存在')


    # 创建临时目录
    outputPath = args.output.strip('/') + '/'
    if not os.path.isdir(outputPath):
        os.makedirs(outputPath)


    DOMTree = xml.dom.minidom.parse(args.file)
    svg = DOMTree.documentElement

    ascent = 0
    descent = 0
    horizontalAdv = 0
    glyphCount = 0

    tags = svg.getElementsByTagName('*')
    for tag in tags:
        if 'font' == tag.tagName:
            if tag.hasAttribute('horiz-adv-x'):
                horizontalAdv = float(tag.getAttribute('horiz-adv-x'))

        if 'font-face' == tag.tagName:
            if tag.hasAttribute('ascent'):
                ascent = float(tag.getAttribute('ascent'))
            if tag.hasAttribute('descent'):
                descent = float(tag.getAttribute('ascent'))

        if 'glyph' == tag.tagName:
            metadata = {
                'name': '',
                'codepoint': '',
                'width': horizontalAdv,
                'height': abs(descent) + ascent
            }

            if tag.hasAttribute('glyph-name'):
                metadata['name'] = tag.getAttribute('glyph-name')
            else:
                glyphCount = glyphCount + 1
                metadata['name'] = 'icon%d' % glyphCount

            if tag.hasAttribute('horiz-adv-x'):
                metadata['width'] = float(tag.getAttribute('horiz-adv-x'))
            
            if tag.hasAttribute('unicode'):
                metadata['unicode'] = tag.getAttribute('unicode')

            # 过滤无path的节点
            if not tag.hasAttribute('d'):
                continue

            print('-------------------------------------')
            print('正在解析 {}'.format(metadata['name']))

            # 获取路径
            path = parse_path(tag.getAttribute('d')) if tag.hasAttribute('d') else ''
            xmin, xmax, ymin, ymax = path.bbox()
            width = int(xmax - xmin)
            height = int(ymax - ymin)
            print('图标宽度: {} x {}'.format(width, height))

            # 计算缩放整体倍数
            scale = 1
            if width > height:
                scale = 896 / width if width > 896 else 896 / width
            else:
                scale = 896 / height if height > 896 else 896 / height

            fixWidth = int(width * scale)
            fixHeight = int(height * scale)

            # 修复由于精度问题导致不满足896像素的情况
            if abs(fixWidth - 896) < 5:
                fixWidth = 896
            
            if abs(fixHeight - 896) < 5:
                fixHeight = 896

            print('修正尺寸: {} x {}'.format(fixWidth, fixHeight))

            # 对于缩放比例保留4位小数
            scaleX = int(fixWidth / width * 10000 + 0.5) / 10000
            scaleY = int(fixHeight / height * 10000 + 0.5) / 10000
            print('修复比例: {}  {}'.format(scaleX, scaleY))
        
            # 将图标移动到0,0位置
            path = path.translated(complex('{}{}j'.format(-1 * xmin, -1 * ymax)))

            # 计算最终的偏移量, 保留2位小数, 将图标移动到画板的中心位置
            translateX = int((1024 - fixWidth) / 2 / scaleX * 100 + 0.5) / 100
            translateY = int(-1 * (1024 - fixHeight) / 2 / scaleY * 100 + 0.5) / 100
            print('translateX', translateX, 'translateY', translateY)

            # 生成图标文件
            svgContentFormat = '<?xml version="1.0" encoding="UTF-8" standalone="no"?><svg xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg" version="1.1" width="1024" height="1024" viewBox="0 0 1024 1024"> <path d="{}" id="{}" transform="scale({} {}) scale(1 -1) translate({} {})"/></svg>'
            svgContent = svgContentFormat.format(path.d(), metadata['name'], scaleX, scaleY, translateX, translateY)
            with open('{}{}.svg'.format(outputPath, metadata['name']), mode='w', encoding='utf-8') as f:
                f.write(svgContent)

if __name__ == '__main__':
    main()
