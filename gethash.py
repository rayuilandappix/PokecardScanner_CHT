from PIL import Image
import imagehash
import os
import numpy as np

# 图片哈希表建立工具，请把卡图放到这个文件夹里
fnames = os.listdir("db_download")
#allhash = []
allhash = np.load("ImageRecognitionData/ptcgtcn.npy", allow_pickle=True).tolist()

for image in fnames:
    try:
        with Image.open(os.path.join("db_download", image)) as img:
            img = img.resize((300, 417))
            img = img.crop((25, 50, 280, 200))
            hash2 = imagehash.average_hash(img, 10)
            allhash.append([image,hash2.hash])
    except Exception as e:
        print(f"Error processing {image}: {e}")

# 将allhash列表转换为NumPy数组
allhash_array = np.array(allhash, dtype=object)  # 使用dtype=object以允许不同的数据类型
np.save("ptcgtcn.npy", allhash_array)
