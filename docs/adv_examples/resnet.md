## 简介 Introduction

### 图像分类与CNN

**图像分类**是指将图像信息中所反映的不同特征，把不同类别的目标区分开来的图像处理方法，是计算机视觉中其他任务，比如目标检测、语义分割、人脸识别等高层视觉任务的基础。

ImageNet大规模视觉识别挑战赛（ILSVRC），常称为ImageNet竞赛，包括图像分类、物体定位，以及物体检测等任务，是推动计算机视觉领域发展最重要的比赛之一。

在2012年的ImageNet竞赛中，深度卷积网络AlexNet横空出世。以超出第二名10%以上的top-5准确率，勇夺ImageNet2012比赛的冠军。从此，以**CNN（卷积神经网络）**为代表的深度学习方法开始在计算机视觉领域的应用开始大放异彩，更多的更深的CNN网络被提出，比如ImageNet2014比赛的冠军VGGNet, ImageNet2015比赛的冠军ResNet。



### ResNet

[ResNet](https://arxiv.org/abs/1512.03385) 是2015年ImageNet竞赛的冠军。目前，ResNet相对对于传统的机器学习分类算法而言，效果已经相当的出色，之后大量的检测，分割，识别等任务也都在ResNet基础上完成。

[OneFlow-Benchmark](xxx)中，提供ResNet50 v1.5的OneFlow实现。我们在ImageNet-2012数据集上训练90轮后，验证集上的准确率能够达到：77.318%(top1)，93.622%(top5)。

![resnet50_validation_acuracy](imgs/resnet50_validation_acuracy.png)



在训练速度上，OneFlow的实现与TensorFlow等框架相比，也有一定优势。

（TODO：补充图片，通过这个文件画图（ 金山云性能测试结果_0615.xlsx），画出resnet50和其他框架的速度对比图）





**关于ResNet50 v1.5的说明：**

> ResNet50 v1.5是原始[ResNet50 v1](https://arxiv.org/abs/1512.03385)的一个改进版本，相对于原始的模型，精度稍有提升 (~0.5% top1)，详细说明参见[这里](https://github.com/NVIDIA/DeepLearningExamples/tree/master/MxNet/Classification/RN50v1.5) 。
>



准备好亲自动手，复现上面的结果了吗？

下面，本文就以上面的ResNet50 为例，一步步展现如何使用OneFlow进行网络的训练和预测。



## 准备工作 Requirements

别担心，使用OneFlow非常容易，只要准备好下面三步，即可开始OneFlow的图像识别之旅。

- 安装OneFlow。 

  - 直接通过pip安装：`pip install oneflow`  （TODO：确定我们的pip源是否做好,问caishenghang）
  - 其他安装方式：参考[这里](XXX)（TOOD：待补充链接，链接到编译安装的文档说明） 。

- 下载[OneFlow-Benchmark](https://github.com/Oneflow-Inc/OneFlow-Benchmark/tree/of_develop_py3/cnn_benchmark)仓库。

  `git clone git@github.com:Oneflow-Inc/OneFlow-Benchmark.git`

- 准备数据集（可选）
  - 下载示例数据集：`wget https://oneflow-public.oss-cn-beijing.aliyuncs.com/datasets/imagenet_ofrecord_example/part-00000`（TOOD：后续确认这个链接，最好和readme打包）
  - 或者：制作完整OFRecord格式的ImageNet数据集（见下文进阶部分）
  - 再或者：直接使用“合成数据”。



**关于数据集的说明：**


> 1）本文的展示的代码中，使用OFRcord格式的数据集可以提高数据加载效率（但这非必须，参考XXX，oneflow支持直接加载numpy数据）。（TODO：补充mnist 文档链接）
>
> 2）为了使读者快速上手，我们提供了一个小的示例数据集。直接下载，即可快速开始训练过程。读者可以在熟悉了流程后，可以参考数据集制作部分，制作完整的数据集。
>
> 3）“合成数据”是指不通过磁盘加载数据，而是直接在内存中生成一些随机数据，作为网络的数据输入源。



## 快速开始 Quick Start

那么接下来，立马开始OneFlow的图像识别之旅吧！

先切换到代码目录：

```
cd OneFlow-Benchmark/Classification/resnet50v1.5
```



### 训练和验证（Train & Validation）

在命令行执行：

```
sh train.sh
```



若在屏幕上不断打印出类似下面的信息，则表明训练过程正常运行：

```
train: epoch 0, iter 200, loss: 7.024337, top_1: 0.000957, top_k: 0.005313, samples/s: 964.656
train: epoch 0, iter 400, loss: 6.849526, top_1: 0.003594, top_k: 0.012969, samples/s: 991.474
...
train: epoch 0, iter 5000, loss: 5.557458, top_1: 0.064590, top_k: 0.174648, samples/s: 935.390
Saving model to ./output/snapshots/model_save-20200629223546/snapshot_epoch_0.
validation: epoch 0, iter 100, top_1: 0.074620, top_k: 0.194120, samples/s: 2014.683
```



可以看到：

- 随着训练的进行，loss不断下降，而训练的top_1/top_k准确率不断提高（其中top_k默认为top_5准确率，可自定义）。
- 每个epoch结束时，会做另外两个工作：1）执行一次验证，并打印出验证集上的top_1/top_k准确率；2）保存模型。
- samples/s 用来指示训练/验证的执行速度，即每秒钟能处理的图片数量。



**复现实验的说明：**

> Q1. 多久能够完成训练？
>
> 在GPU环境下，使用单机8卡（NVIDIA TITAN V），完成90个epoch的完整训练过程，大概需要15小时。
>
> 
>
> Q2. 在ImageNet-2012数据集上训练90个epoch后，准确率能达到多少？
>
> 训练集：80.57%（top1）
>
> 验证集：77.318%（top1），93.622%（top5）



### 预测（Inference）

恭喜，到这里，您已经知道如何用OneFlow训练模型。

接下来，试试用训练好的模型对新图片进行分类预测吧！



**关于模型，您可以选择：**

- 使用刚才训练出的模型进行预测。
- 或者，下载已训练好的模型：[resnet_v1.5_model](https://oneflow-public.oss-cn-beijing.aliyuncs.com/model_zoo/resnet_v15_of_best_model_val_top1_77318.tgz ) (validation accuracy: 77.318% top1，93.622% top5 )。
- 再或者，将其他框架已有的模型转换成OneFlow模型，见下面模型转换的部分。（TODO：模型转换内容补充后，怎加这里的跳转链接）



准备好模型后，将模型目录填入`inference.sh` 脚本的`MODEL_LOAD_DIR`变量中，然后执行以下命令，对开始预测：

```
sh inference.sh
```



若输出下面的内容，则表示预测成功：

```
image_demo/tiger.jpg
0.81120294 tiger, Panthera tigris
```




## 更详细的说明 Details
### 训练 Train

####  从单卡训练到多卡训练，训练超参数如何调整？

TODO：待补充；

更进一步介绍链接：
模型准备
数据加载
Optimizer  配置

####  多机分布式训练如何配置？

TODO：待补充，多机的配置方式，补充多机的脚本；

更进一步介绍链接：
分布式策略



#### 训练过程可视化？如何得到训练的中间状态？

TODO：shengjian，先略。

更多问题补充。








### 验证 Validation

#### 如何进行独立的验证过程？

略，脚本有问题，待删除；



### 预测 Inference

可以使用训练好的模型对图片进行分类，下面程序展示了如何加载已经训练好的网络和参数进行推断。




### 半精度训练与预测

Oneflow原生支持半精度(fp16)模型的训练。这里的半精度训练是指使用float32和float16格式存储数据的混合精度模型训练，训练时候参数以fp16格式存储和训练，同时保留fp32权重文件用作梯度更新和计算过程。

由于参数的存储减半（fp32 >> fp16），会带来训练过程的加速，在oneflow中开启半精度模式后，resnet50的训练通常能达到1.7倍的加速。不过由于精度的降低，模型的精度也会有略微的下降。

在Oneflow中开启fp16半精度模型的训练很简单，您只需要在train.sh脚本中指定参数：--use_fp16 True即可。

完整的脚本如下：
```shell
DATA_ROOT=/DATA/disk1/ImageNet/ofrecord
#gdb --args \
  python3 of_cnn_train_val.py \
    --num_epochs=100 \
    --train_data_dir=$DATA_ROOT/train \
    --train_data_part_num=256 \
    --val_data_dir=$DATA_ROOT/validation \
    --val_data_part_num=256 \
    --num_nodes=1 \
    --gpu_num_per_node=4 \
    --optimizer="momentum" \
    --learning_rate=0.256 \
    --loss_print_every_n_iter=200 \
    --batch_size_per_device=32 \
    --val_batch_size_per_device=100 \
    --use_new_dataloader=True \
    --model="resnet50" \
    --use_fp16 true \
    --label-smoothing=0.1 \
    --use_boxing_v2 True
```

除了指定--use_fp16以外，半精度模型的训练、输出、测试过程与之前正常的resnet50模型的训练过程完全一致。

这里，我们提供一个训练好半精度模型供您使用：

[resnet_v1.5_fp16_model](https://oneflow-public.oss-cn-beijing.aliyuncs.com/model_zoo/resnet_v15_of_best_fp16_model_val_top1_77229.tgz ) (validation accuracy: 77.229% top1，93.550% top5 )





## 进阶 Advanced

###  数据集制作

#### 用于图像分类数据集简介

用于图像分类的公开数据集有CIFAR，ImageNet等等，这些数据集中，是以jpeg的格式提供原始的图片。

- [CIFAR](http://www.cs.toronto.edu/~kriz/cifar.html)
  是由Hinton 的学生Alex Krizhevsky 和Ilya Sutskever 整理的一个用于识别普适物体的小型数据集。包括CIFAR-10和CIFAR-100。

- [ImageNet](http://image-net.org/index) 
	ImageNet数据集，一般是指2010-2017年间大规模视觉识别竞赛(ILSVRC)的所使用的数据集的统称。ImageNet数据从2010年来稍有变化，常用ImageNet-2012数据集包含1000个类别，其中训练集包含1,281,167张图片，每个类别数据732至1300张不等，验证集包含50,000张图片，平均每个类别50张图片。



#### OFRecord提高IO效率

**原始的数据集：**

往往是由成千上万的图片或文本等文件组成，这些文件被散列存储在不同的文件夹中，一个个读取的时候会非常慢，并且占用大量内存空间。

**OFRecord：**

内部借助“Protocol Buffer”二进制数据编码方案，它只占用一个内存块，只需要一次性加载一个二进制文件的方式即可，简单，快速，尤其对大型训练数据很友好。另外，当我们的训练数据量比较大的时候，可以将数据分成多个OFRecord文件，来提高处理效率。

关于OFRecord的详细说明请参考：[OFRecord数据格式](http://183.81.182.202:8000/extended_topics/ofrecord.html) （TODO：确定这个链接）



#### 将ImageNet转换成OFRecord

TODO：后续将脚本放在：OneFlow-Benchmark/Classification/tools目录
https://github.com/Oneflow-Inc/OneFlow-Benchmark



在OneFlow中，提供了将原始ImageNet-2012数据集文件转换成OFRecord格式的脚本。如果您已经准备好了ImageNet-2012数据集(训练集和验证集)，并且训练集/验证集的格式如下：

```shell
│   ├── train
│   │   ├── n01440764
│   │   └── n01443537
                                 ...
│   └── validation
│       ├── n01440764
│       └── n01443537
                                 ...
```

那么，一键执行以下脚本即可完成训练集和验证集 > OFRecord的转换：
**转换训练集**

```shell
python3 imagenet_ofrecord.py  \
--train_directory ../data/imagenet/train  \
--output_directory ../data/imagenet/ofrecord/train   \
--label_file imagenet_lsvrc_2015_synsets.txt   \
--shards 256  --num_threads 8 --name train  \
--bounding_box_file imagenet_2012_bounding_boxes.csv   \
--height 224 --width 224
```

**转换验证集**

```shell
python3 imagenet_ofrecord.py  \
--validation_directory ../data/imagenet/validation  \
--output_directory ../data/imagenet/ofrecord/validation  \
--label_file imagenet_lsvrc_2015_synsets.txt --name validation  \
--shards 256 --num_threads 8 --name validation \
--bounding_box_file imagenet_2012_bounding_boxes.csv  \
--height 224 --width 224
```

**参数说明：**

```shell
--train_directory
# 指定待转换的训练集文件夹路径
--validation_directory
# 指定待转换的验证集文件夹路径
--name
# 指定转换的是训练集还是验证集
--output_directory
# 指定转换后的ofrecord存储位置
 --num_threads
# 任务运行线程数
--shards
# 指定ofrecord分片数量，建议shards = 256
#（shards数量越大，则转换后的每个ofrecord分片数据量就越少）
--bounding_box_file
# 该参数指定的csv文件中标记了所有目标box的坐标，使转换后的ofrecord同时支持分类和目标检测任务
```

运行以上脚本后，你可以在../data/imagenet/ofrecord/validation、../data/imagenet/ofrecord/train下看到转换好的ofrecord文件：

```shell
.
├── train
│   ├── part-00000
│   └── part-00001
                             ...
└── validation
    ├── part-00000
    └── part-00001
                             ...
```



如果您尚未下载过Imagenet数据集，请自行下载和准备以下文件：

- ILSVRC2012_img_train.tar

- ILSVRC2012_img_val.tar

我们将用以下两个步骤，帮您完成数据集的预处理。之后，您就可以使用上面介绍的转换脚本进行OFReciord的转换了。下面假设您已经下载好了原始数据集，并存放在data/imagenet目录下：

```shell
├── data
│   └── imagenet
│       ├── ILSVRC2012_img_train.tar
│       ├── ILSVRC2012_img_val.tar
├── imagenet_utils
│   ├── extract_trainval.sh
│   ├── imagenet_2012_bounding_boxes.csv
│   ├── imagenet_2012_validation_synset_labels.txt
│   ├── imagenet_lsvrc_2015_synsets.txt
│   ├── imagenet_metadata.txt
│   ├── imagenet_ofrecord.py
│   └── preprocess_imagenet_validation_data.py
```

**步骤一：extract imagenet**

这一步主要是将ILSVRC2012_img_train.tar和ILSVRC2012_img_val.tar解压缩，生成train、validation文件夹。train文件夹下是1000个虚拟lebel分类文件夹(如：n01443537)，训练集图片解压后根据分类放入这些label文件夹中；validation文件夹下是解压后的原图。

```shell
sh extract_trainval.sh ../data/imagenet # 参数指定存放imagenet元素数据的文件夹路径
```
```shell
解压后，文件夹结构示意如下：
.
├── extract_trainval.sh
├── imagenet
│   ├── ILSVRC2012_img_train.tar
│   ├── ILSVRC2012_img_val.tar
│   ├── train
│   │   ├── n01440764
│   │   │   ├── n01440764_10026.JPEG
│   │   │   ├── n01440764_10027.JPEG 
                                               ...
│   │   └── n01443537
│   │       ├── n01443537_10007.JPEG
│   │       ├── n01443537_10014.JPEG
											 ...
│   └── validation
│       ├── ILSVRC2012_val_00000236.JPEG
│       ├── ILSVRC2012_val_00000262.JPEG        
											...
```

**步骤二：validation数据处理**

经过上一步，train数据集已经放入了1000个分类label文件夹中形成了规整的格式，而验证集部分的图片还全部堆放在validation文件夹中，这一步，我们就用preprocess_imagenet_validation_data.py对其进行处理，使其也按类别存放到label文件夹下。
```shell
python3 preprocess_imagenet_validation_data.py  ../data/imagenet/validation
# 参数 ../data/imagenet/validation为ILSVRC2012_img_val.tar解压后验证集图像存放的路径。
```
处理后项目文件夹格式如下：
```shell
.
├── extract_trainval.sh
├── imagenet
│   ├── ILSVRC2012_img_train.tar
│   ├── ILSVRC2012_img_val.tar
│   ├── train
│   │   ├── n01440764
│   │   └── n01443537
                                ...
│   └── validation
│       ├── n01440764
│       └── n01443537
                               ...
```

至此，已经完成了全部的数据预处理，您可以直接跳转至**转换训练集**和**转换验证集**，轻松完成ImageNet-2012数据集到OFRecord的转换过程了。



### 模型转换

从tf转of，或者是从ONNX转of，这部分待补充。
TODO: 联系Jianhao Zhang 补充ONNX转of


## 结果 Results
速度测试结果

和tf的对比



```

```