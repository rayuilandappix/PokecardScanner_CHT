from PIL import Image
import imagehash
import os
import numpy as np
import pandas as pd

#图片哈希表建立工具，请把卡图放到这个文件夹里
fnames = os.listdir("db_download")
allhash=[]
for image in fnames:
    try:
        with Image.open(os.path.join("db_download",image)) as img:
                    img=img.resize((300,417))
                    img=img.crop((25,50,280,200))
                    hash2 = imagehash.average_hash(img,10).hash
                    allhash.append([image,hash2])
    except:
        pass
np.save("ptcgtcn.npy",allhash)
