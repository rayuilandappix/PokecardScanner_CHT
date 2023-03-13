import imagehash
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import WIN_CLOSED
import requests
import numpy as np
from PIL import Image as pimg
from PIL import ImageGrab
from pynput import keyboard
import pyautogui as pag

#初始化
stax=0
stay=0
staix=0
staiy=0
stbx=0
stby=0
sglist=[]

#识别相似图片并给出列表
def findpic():
    lastlist=[]
    with pimg.open("sc.png") as imgs:
        hash1 = imagehash.average_hash(imgs, 10).hash
    rget=np.load("ptcgtcn.npy",allow_pickle=True)
    belike=50
    while belike<100:
            getlist=[]
            piclist=[]
            threshold = 1 - belike/100
            diff_limit = int(threshold*(10**2))
            for i in rget:
                hash2=i[1]
                #print(hash2)
                if np.count_nonzero(hash1 != hash2) <= diff_limit:
                    getlist.append(i[0].replace(".png",""))
                    piclist.append(i[0])
                    lastpic=i[0]

            if len(getlist)<10 and len(lastlist)==0:
                lastlist=getlist
            if(len(getlist)>1):
                belike+=1
            else:
                break
    if(len(piclist)==0):
        return lastpic,lastlist
    else:
        return piclist[0],lastlist


def downloadcard(cardnum):
    url="https://asia.pokemon-card.com/tw/card-img/tw"+cardnum.replace('.png','').zfill(8)+'.png'
    print(url)
    while True:
                try:
                    res=requests.get(url,timeout=5)
                    with open("downcard/downloadcard.png",'wb') as f:
                        f.write(res.content)
                    reimg=pimg.open('downcard/downloadcard.png').resize((300,417))
                    reimg.save('downcard/downloadcard.png')
                    break
                except:
                    pass

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
        print("捕获结束点")
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
#print(findpic())

#捕获框选区域图片
def getpic():
    try:
        im=ImageGrab.grab((staix,staiy,stbx,stby))
        im.save("sc.png")
        #print(findpic())
    except:
        print("错误")


#GUI初始化
sg.theme('LightGrey1')
layout=[
    [sg.Button("框选区域",key='getarea',font="黑体"),sg.Button("查询",key='find',font="黑体"),sg.Listbox(values=sglist,key='cardlist',enable_events=True,size=(35,5))],
    [sg.Image(key="showpic",filename="downcard/downloadcard.png")]
    ]
window= sg.Window('PTCG卡片助手', layout,size=(350,550),keep_on_top=True)
while True:
    event,value = window.Read(timeout=3000)
    if(event=="getarea"):
        with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
            listener.join()
        print("捕获结束") 
    if(event=="find"):
        getpic()
        outcard,outlist=findpic()
        downloadcard(outcard)
        getcard="downcard/downloadcard.png"
        window['showpic'].update(getcard)
        window['cardlist'].update(outlist)
    if(event=="cardlist"):
        try:
            outcard=window['cardlist'].get()
            downloadcard(outcard[0])
            getcard="downcard/downloadcard.png"
            window['showpic'].update(getcard)
        except Exception as e:
            print(e)
    if(event==WIN_CLOSED):
        break