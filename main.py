import imagehash
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import WIN_CLOSED
import requests
import numpy as np
from PIL import Image as pimg
from PIL import ImageGrab
from pynput import keyboard
import pyautogui as pag
from requests_html import HTMLSession
import configparser
import os
#加了这个pyinstaller打包有问题
#import zhconv

cf=configparser.ConfigParser()
cf.read("config.ini",encoding="utf-8-sig")
autosizew=int(cf.get("Size","width"))
autosizeh=int(cf.get("Size","high"))
#初始化
stax=0
stay=0
staix=0
staiy=0
stbx=0
stby=0
sglist=[]
oldcard=""

# 保存剪切板内的图片
def get_cut_image():
    clipboard_image = ImageGrab.grabclipboard()  
    if isinstance(clipboard_image, pimg.Image):  
        clipboard_image.save("sc.png")

# 寻找最相似的图片
def find_most_similar_images():
    # 读取图片并调整大小和裁剪，计算目标图片哈希值1
    similar_images=[]
    with pimg.open("sc.png") as imgs:
        imgs=imgs.resize((300,417))
        imgs=imgs.crop((25,50,280,200))
        hash1 = imagehash.average_hash(imgs, 10).hash

    # 加载图片数据
    image_data=np.load("ImageRecognitionData/ptcgtcn.npy",allow_pickle=True)

    # 初始化相似度阈值
    similarity=50
    # 遍历每个相似度阈值，检查剩余相似的图片
    while similarity<100:  
            pic_number_list=[]
            pic_name_list=[]
            threshold = 1 - similarity/100
            diff_limit = int(threshold*(10**2))
            for i in image_data:
                #获取一张卡的哈希值为哈希2
                hash2=i[1]
                #print(i)
                #print(type(hash2))
                #比较哈希1，哈希2的相似度，如果高于阈值，加入列表
                if np.count_nonzero(hash1 != hash2) <= diff_limit:
                    pic_number_list.append(i[0].replace(".png",""))
                    pic_name_list.append(i[0])
                    most_similar_pic=i[0]
            #如果相似的图片小于10种且不为0，输出相似列表
            if len(pic_number_list)<10 and len(similar_images)==0:
                similar_images=pic_number_list

            if(len(pic_number_list)>1):
                #缩小比较范围
                similarity+=1
            else:
                #超过100时停止循环
                break
    
    #如果最后一轮不再有相似的图片，返回上一轮最相似的结果
    if(len(pic_number_list)==0):
        return most_similar_pic,similar_images
    #如果最后一轮仍有相似的图片，返回最可能的结果和列表
    else:
        return pic_number_list[0],similar_images



def downloadcard(cardnum):
    #检查是否有缓存文件
    if os.path.exists("download_cards/"+cardnum.replace('.png','').zfill(8)+'.png'):
        img_cache=pimg.open("download_cards/"+cardnum.replace('.png','').zfill(8)+'.png')
        img_cache.save("download_cards/downloadcard.png")
    #没有缓存的文件则下载他们
    else:
        url="https://asia.pokemon-card.com/tw/card-img/tw"+cardnum.replace('.png','').zfill(8)+'.png'
        print(url)
        while True:
            try:
                res=requests.get(url,timeout=15)
                with open("download_cards/downloadcard.png",'wb') as f:
                    f.write(res.content)
                reimg=pimg.open('download_cards/downloadcard.png').resize((300,417),pimg.BICUBIC)
                reimg.save('download_cards/downloadcard.png',subsampling=0,quality=95,dpi=(300,300))
                break
            except Exception as e: 
                print(e)
                break
        #缓存文件
        img_cache=pimg.open("download_cards/downloadcard.png")
        img_cache.save("download_cards/"+cardnum.replace('.png','').zfill(8)+'.png')
    url="https://asia.pokemon-card.com/tw/card-search/detail/"+cardnum
    try:
        session=HTMLSession()
        r=session.get(url)
        e=r.html.find('.skill')
        #print(e)
        out=""
        for i in e:
            if(out==""):
                 out=i.text
            else:
                out=out+'\n'+i.text
        #不需要转简体可以注释掉
        #out=zhconv.convert(out,'zh-cn')
        window['cardinfo'].update(out)
    except Exception as e:
        print(e)



#键盘按下检测
def on_press(key):
    global stax,stay,stbx,stby
    #框选区域开始点
    if key==keyboard.Key.shift_l and stax==0 and stay==0:
        print("======================")
        mousex,mousey=pag.position()
        print("框选开始点")
        print(mousex,mousey)
        stax=mousex
        stay=mousey

#键盘释放检测
def on_release(key):
    #框选区域结束点
    global stax,stay,stbx,stby,staix,staiy
    if key==keyboard.Key.shift_l:
        print("框选结束点")
        mousex,mousey=pag.position()
        print(mousex,mousey)    
        try:
            if mousex-stax>20 and mousey-stay>20:
                staix=stax
                staiy=stay
                stbx=mousex
                stby=mousey
                stax=0
                stay=0
                return False
            else:
                print("无法识别范围")
        except Exception as e:
            print(e)
    stax=0
    stay=0

#捕获框选区域图片
def getpic():
    try:
        im=ImageGrab.grab((staix,staiy,stbx,stby))
        im.save("sc.png")
    except:
        print("错误")

#GUI部分
sg.theme('LightGrey1')
layout=[
    [sg.Button("框选区域",key='getarea',font="黑体"),sg.Button("查询",key='find',font="黑体"),sg.Button("截图查询",key='findcut',font="黑体"),sg.Checkbox(key='autostart',text='自动',default=False)],
    #[sg.Button("查询",key='findcut',font="黑体")],
    [sg.Image(key="showpic",filename="download_cards/downloadcard.png")],
    [sg.ML(key='cardinfo',font="黑体",size=(350,200))]
    ]
window= sg.Window('PTCG截图卡查助手', layout,size=(autosizew,autosizeh),keep_on_top=True)
while True:
    event,value = window.Read(timeout=3000)
    if(event=="getarea"):
        print("鼠标移动到卡片左上角，按住左Shift键，直到把鼠标移动到卡片右下角松开Shift，即可完成框选")
        with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
            listener.join()
        print("完成框选") 
    if(event=="find"):
        getpic()
        outcard,outlist=find_most_similar_images()
        downloadcard(outcard)
        getcard="download_cards/downloadcard.png"
        window['showpic'].update(getcard)
    if(event=="findcut"):
        get_cut_image()
        outcard,outlist=find_most_similar_images()
        downloadcard(outcard)
        getcard="download_cards/downloadcard.png"
        window['showpic'].update(getcard)
    if(event=="cardlist"):
        try:
            outcard=window['cardlist'].get()
            downloadcard(outcard[0])
            getcard="download_cards/downloadcard.png"
            window['showpic'].update(getcard)
        except Exception as e:
            print(e)
    if(event==WIN_CLOSED):
        break
    try:
        if value['autostart']==True:
            getpic()
            outcard,outlist=find_most_similar_images()
            if(outcard!=oldcard):
                downloadcard(outcard)
                oldcard=outcard
            getcard="download_cards/downloadcard.png"
            window['showpic'].update(getcard)
    except Exception as e:
        print(e)