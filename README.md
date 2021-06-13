# ImageSegmentation
My Frame work for Image Semantic Segmentation with pytorch Lightning + Albumentations
## Overview
I organizize the object detection algorithms proposed in recent years, and focused on **`Cityscapes`**, **`COCO`** , **`Pascal VOC`** and **`BDD100K`** Dataset.
This frame work also include **`EarlyStopping mechanism`**.


## Datasets:

I used 3 different datases: **`Cityscapes`, `COCO`, `Pascal VOC`** and **`BDD100K`**. Statistics of datasets I used for experiments is shown below

- **VOC**:
  Download the voc images and annotations from [VOC2007](http://host.robots.ox.ac.uk/pascal/VOC/voc2007) or [VOC2012](http://host.robots.ox.ac.uk/pascal/VOC/voc2012). Make sure to put the files as the following structure:

-- VOC2007
![](https://i.imgur.com/wncA2wC.png)

-- VOC2012
![](https://i.imgur.com/v3AQelB.png)

  
  
| Dataset                | Classes | #Train images/objects | #Validation images/objects |
|------------------------|:---------:|:-----------------------:|:----------------------------:|
| VOC2007                |    20   |      209/633       |          213/582        |
| VOC2012                |    20   |      1464/3507     |         1449/3422       |

  ```
  VOCDevkit
  ├── VOC2007
  │   ├── JPEGImages  
  │   ├── SegmentationClass
  │   ├── ...
  │   └── ...
  └── VOC2012
      ├── JPEGImages  
      ├── SegmentationClass
      ├── ...
      └── ...
  ```
  
- **COCO**:
  Download the coco images and annotations from [coco website](http://cocodataset.org/#download). Make sure to put the files as the following structure:

| Dataset                | Classes | #Train images/objects | #Validation images/objects |
|------------------------|:---------:|:-----------------------:|:----------------------------:|
| COCO2014               |    21   |         64k/-         |            31k/-           |
| COCO2017               |    21   |         92k/-        |             3k/-           |
```
  COCO
  ├── annotations
  │   ├── instances_train2014.json
  │   ├── instances_train2017.json
  │   ├── instances_val2014.json
  │   └── instances_val2017.json
  │── images
  │   ├── train2014
  │   ├── train2017
  │   ├── val2014
  │   └── val2017
  └── mask
      ├── train2014
      ├── train2017
      ├── val2014
      └── val2017
```

- **Cityscapes**:
The Cityscapes Dataset focuses on semantic understanding of urban street scenes. In the following, we give an overview on the design choices that were made to target the dataset’s focus.

![](https://i.imgur.com/Dgi4K9S.png)



  Download the container images and annotations from [cityscapes](https://www.cityscapes-dataset.com/downloads/). Make sure to put the files as the following structure:
 ![](https://i.imgur.com/rRJSIYQ.png)
![](https://i.imgur.com/L3bVJFM.png)  

```
  Cityscapes
  ├── leftImg8bit
  │   ├── train
  │   ├── val
  │   ├── test  
  │     
  │── gtFine_trainvaltest
      ├── gtFine
          ├── train
          ├── val
          ├── test 
```



## Semantic Segmentation Models - based on LightningModule
- **FPN**
- **FCN**
- **DeConvNet**
- **UNet**
- **SegNet**
- **PSPNet**
- **DeepLabV3**
- **DeepLabv3_plus**

## Prerequisites
* **Windows 10**
* **CUDA 10.2**
* **NVIDIA GPU 1660 + CuDNN v7.605**
* **python 3.6.9**
* **pytorch 1.81**
* **opencv-python 4.1.1.26**
* **numpy 1.19.5**
* **torchvision 0.9**
* **torchsummary 1.5.1**
* **Pillow 7.2.0**
* **dlib==19.21**
* **tensorflow-gpu 2.2.0**
* **tensorboard 2.5.0** 
* **pytorch-lightning 1.2.6**

## Usage
### 0. Prepare the dataset
* **Download custom dataset in the  `data_paths`.** 
* **And create custom dataset `custom_dataset.py` in the `dataset`.**

### Execute (Train/Val + Test)

#### Cityscape
```python
python run.py --use CityscapeModule --model DeepLabv3_plus
```
#### VOC
```python
python run.py --use VOCModule --model DeepLabv3_plus
```
#### COCO
```python
python run.py --use COCOModule --model DeepLabv3_plus
```
#### BDD100K
```python
python run.py --use BDD100KModule --model DeepLabv3_plus
```


## Reference
- U-Net :  https://github.com/milesial/Pytorch-UNet/blob/master/unet/unet_model.py
- SegNet : https://github.com/Charmve/Semantic-Segmentation-PyTorch/blob/7095051118c79c322df8b98ab4e59caeb61c57a0/models/seg_net.py
- DeconvNet:   https://github.com/renkexinmay/SemanticSegmentation-FCN-DeconvNet/blob/master/model.py
- FCN: https://github.com/pochih/FCN-pytorch/blob/master/python/fcn.py
- PSPNet: https://github.com/Lextal/pspnet-pytorch/blob/4eb6ab61287e837f5e2d8c1ae09fadeaa0e31e37/pspnet.py
- DeepLabV3: https://github.com/fregu856/deeplabv3/blob/master/model/deeplabv3.py
- DeepLabv3_plus : https://github.com/MLearing/Pytorch-DeepLab-v3-plus/blob/master/networks/deeplab_resnet.py
- Dataset Preprare: https://github.com/jfzhang95/pytorch-deeplab-xception/tree/master/dataloaders/datasets
https://towardsdatascience.com/master-the-coco-dataset-for-semantic-image-segmentation-part-1-of-2-732712631047
- Frame & FPN : https://github.com/Andy-zhujunwen/FPN-Semantic-segmentation
- cityscapes: https://www.cityscapes-dataset.com/dataset-overview/#features
- VOC2007: https://pjreddie.com/media/files/VOC2007_doc.pdf
- VOC2012: https://pjreddie.com/media/files/VOC2012_doc.pdf
- Albumentations : https://albumentations.ai/docs/examples/pytorch_classification/
- pytorch-lightning : https://pytorch-lightning.readthedocs.io/en/latest/
