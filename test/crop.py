import os
from PIL import Image
#from skimage import io
import tifffile as tif
import cv2
import matplotlib.pyplot as plt
import numpy as np


def read_tif( imgpath ):
    img = tif.imread(imgpath)#读取图片 imgpath为图片所在位置
    img = img/img.max()
    img =img*255-0.001#减去0.001防止变成负整型
    img =img.astype(np.uint8)
    print(img.shape)#显示图片大小和通道数  通道数为4
    b = img[:, :, 0]#蓝通道
    g = img[:, :, 1]#绿通道
    r = img[:, :, 2]#红通道
    nir = img[:, :, 3]#近红外通道，不可以用imshow直接查看
    
    #通道拼接  两种方法
    bgr = cv2.merge([b, g, r])
    rgb=  np.dstack([r,g,b])
    #cv2.imshow('bgr',bgr)
    #plt.matshow(rgb)
    #cv2.imshow('近红外灰度图',nir)
    cv2.imwrite("oilpalm.png", rgb)

    
 
def splitimage(src,rownum,colnum,dstpath,overlap_pix):
    """
    The image is cut to a fixed size and the overlap rate can be set; if overlap_pix = 0 Each image will not overlap
    Args:
        src: image file  path.
        rownum,colnum:The size of each image after cutting
        dstpath: save slice path
        overlap_pix:  Overlapping pixels
       
   
   
    """
    if os.path.exists(src) :
        print('文件存在')
    else:
        print('文件不存在')
        return
   
    if  os.path.isdir(dstpath) :
        print('文件夹不存在，则创建')
        pass
    else:
        os.mkdir(dstpath)
   
   
    img = Image.open(src)
   
    w, h = img.size
   
    if rownum <= h and colnum <= w:
        print('Original image info: %sx%s, %s, %s' % (w, h, img.format, img.mode))
        print('开始处理图片切割, 请稍候...')
 
        s = os.path.split(src)
        if dstpath == '':
            dstpath = s[0]
        fn = s[1].split('.')
      
        ext = fn[-1]
 
        num = 0
       
        rowheight = h // (rownum-overlap_pix) 
        colwidth = w // (colnum -overlap_pix) 
       
       
        for r in range(rowheight):
            for c in range(colwidth):
               
                Lx = (c * colnum) - overlap_pix * c
                Ly = (r * rownum) - overlap_pix * r
               
                if(Lx<=0 ):
                    Lx = 0
                   
                if( Ly <= 0):
                    Ly = 0
                   
                Rx = Lx + colnum
                Ry = Ly + rownum   
                   
                  
                box = (Lx,Ly, Rx,Ry)
                img.crop(box).save(os.path.join(dstpath,str(Lx)+'_'+str(Ly) + '_' + str(num) + '.' + ext))
                # crop(left, upper, right, lower) 名字中带有图像坐标
                num = num + 1
 
        print('图片切割完毕，共生成 %s 张小图片。' % num)
    else:
        print('不合法的行列切割参数！')
 
     
def main():
#    read_tif('oilpalm.tif')
    jpg_image_path = r'oilpalm.png'
    save_path =  r'crop_img'
    row = 600
    col = 600
    overlap_pix = 100
    splitimage(jpg_image_path,row, col, save_path,overlap_pix)
              
   
   
if __name__=='__main__':
    main()