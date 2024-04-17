# PokecardScanner_CHT

## 简介

PokecardScanner_CHT 是一款基于imagehash技术的宝可梦卡牌图片搜索工具。通过截取图片，可以用任意语种卡牌来快速查找繁体中文版本的卡片图片和信息。

注意：繁体中文数据库中不包含高罕卡片，如需查询高罕卡片，可能会出现识别错误。

## 使用方法

1. **区域框选查询**（适用于观看宝可梦卡牌比赛）

   - 将鼠标移动到卡片左上角，按下Shift键，然后将鼠标移动到卡片右下角，松开Shift键，完成区域框选。
   - 点击“查询”按钮，自动截取框选区域的图片并查找对应的繁体中文卡片。
   - 勾选“自动”选项，工具将每3秒自动检索框选区域内的卡片。

2. **截图查询**（可以在玩宝可梦live、或是遇到卡表中不认识的牌时使用）

   - 使用其他软件进行截图。
   - 点击“搜索卡片”按钮，进行卡片识别。

## 问题与解决

- 如果搜索结果与实际卡片不符，请检查框选的区域是否正确。可以检查生成的“sc.png”文件是否截取到了完整的卡图，并确保没有大边框。如有问题，请重新框选。
- 对于双屏或多屏用户，请确保框选区域位于主屏幕上，否则“区域框选查询”功能将无法正常工作。
- 您可以使用“ImageRecognitionData\ptcgtcn.npy”数据开发更多图像识别应用。该数据会持续更新。
- 如何利用数据库查找最相似的卡牌可以查看main里的find_most_similar_images函数
- 可参考gethash.py来建立数据库

## 卡片收录说明

- 数据集当前更新至SV5a《绯红薄雾》。