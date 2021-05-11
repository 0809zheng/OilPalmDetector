from yolo import YOLO
from PIL import Image, ImageDraw
import os

def IoU(c1, c2):
    assert type(c1) == tuple
    assert type(c2) == tuple
    
    x00, y00, x10, y10, _ = c1
    x01, y01, x11, y11, _ = c2
    
    if min(x10, x11)-max(x00, x01) <= 0 or min(y10, y11)-max(y00, y01) <= 0:
        return 0
    
    INTERSECTION = (min(x10, x11)-max(x00, x01)) * (min(y10, y11)-max(y00, y01))   
    UNION = (x10-x00)*(y10-y00) + (x11-x01)*(y11-y01) - INTERSECTION
    return INTERSECTION/(UNION+1e-8)


def globalNMS(coords):
    threshold_area = 2000
    threshold_conf = 0.85
    threshold_iou = 0.22
    final_coords = []
    
    n = len(coords)
    coords.append((0,0,0,0,0))
    visited = [n]
    print('There are totally %d propose objects.' %n)
    
    for i in range(n):
        if i in visited:
            continue
        visited.append(i)
        
        temp_coords = [coords[i]]
        for j in range(i+1, n+1):
            if j in visited:
                continue
            if IoU(coords[i], coords[j]) >= threshold_iou:
                visited.append(j)
                temp_coords.append(coords[j])
                
        max_index = -1
        max_area = 0
        for k in range(len(temp_coords)):
            tx0, ty0, tx1, ty1, ts = temp_coords[k]
            if (tx1-tx0)*(ty1-ty0) > max_area:
                max_area = (tx1-tx0)*(ty1-ty0)
                max_index = k
        tx0, ty0, tx1, ty1, ts = temp_coords[max_index]
        if ts >= threshold_conf and (tx1-tx0)*(ty1-ty0) >= threshold_area:
            final_coords.append(temp_coords[max_index])
        
    return final_coords



yolo = YOLO()

# 分别检测每一张子图像
print('All crop images predict begin.')
name = os.listdir('./test/crop_img/')
global_coords = []

for img in name:
    image = Image.open('./test/crop_img/'+img)
    r_image, local_coords = yolo.detect_image(image)
    if local_coords == []:
        continue
    r_image.save('./test/crop_result/'+img)
    
    dx, dy = int(img.split('_')[0]), int(img.split('_')[1])
    for (x0, y0 ,x1, y1, s) in local_coords:
        x0, y0 ,x1, y1 = x0+dx, y0+dy ,x1+dx, y1+dy
        height, width = x1-x0, y1-y0
        if height < width:
            y0 += (width-height)//2
            y1 -= (width-height)//2
        else:
            x0 += (height-width)//2
            x1 -= (height-width)//2
        global_coords.append((x0, y0 ,x1, y1, s))
print('All crop images predict finish.')


# 在原图中展示结果
print('The whole image produce begin.')
gimg = Image.open('./test/oilpalm.png')

draw = ImageDraw.Draw(gimg)
final_coords = globalNMS(global_coords)
print('Totally find %d oil palm trees.' % len(final_coords))

for (x0, y0 ,x1, y1, s) in final_coords:
    draw.ellipse([x0, y0 ,x1, y1])
del draw
#gimg.show()
gimg.save('./test/result.png')
print('The whole image produce finish.')
