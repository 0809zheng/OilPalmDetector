# OilPalmDetector
检测高分辨率、大尺寸的卫星图像中的棕榈树。

### 训练过程
1. 标注训练集：将训练集的标签文件放在路径`./VOCdevkit/VOC2007`下的**Annotation**文件夹中；将图片文件放在路径`./VOCdevkit/VOC2007`下的**JPEGImages**文件夹中。（可以使用辅助的训练集，如 https://github.com/rs-dl/CROPTD ）
2. 在`./VOCdevkit/VOC2007`路径下运行：`python voc2yolo4.py`
3. 在主路径下运行：`python voc_annotation.py`
4. 开始训练，在主路径下运行：`python train.py`（在**train.py**文件中可设置训练超参数），训练结果保存为文件`./model_data/model.pth`。

### 测试过程
1. [下载](https://pan.baidu.com/s/1DzySlv9znHBfadu3i5F5Zw)(提取码`abtm`)预训练模型和测试图像。预训练模型放在路径`./model_data/model.pth`下，测试图像放在路径`./test/oilpalm.png`下。
1. 在`./test`路径下运行，对测试图像进行格式转换和切割（500x500），预设了25%的重叠率：`python crop.py`
2. 开始测试，在主路径下运行：`python predict.py`

### 部分结果展示
![](https://github.com/0809zheng/OilPalmDetector/blob/main/test/part_of_result.png)
