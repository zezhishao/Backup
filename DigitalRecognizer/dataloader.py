# _*_ coding: utf-8 _*_
# @Time   : 2020/1/21 1:04 下午 
# @Author : 邵泽志 
# @File   : dataloader.py
# @Desc   : 


import os
import numpy as np
import pandas as pd
import torch
from PIL import Image
from torchvision import transforms


def _check_exists():
    return os.path.exists("./data/test.csv") and os.path.exists("./data/train.csv") and os.path.exists(
        "./data/test.pt") and os.path.exists("./data/train.pt")


class DigitalRecognizer(torch.utils.data.Dataset):  # 需要继承data.Dataset
    """
    dataset类的设置非常自由，主要是Init、__getitem__、__len__三个函数。
    当数据集不是很大的时候，可以直接加载到内存中。这个数据可能是raw data，也可以是已经被预处理好的文件。例如pt文件，npy文件等。
    当数据集很大的时候，也可以只设置好读取路径和读取方式。在__getitem__里面设置好读取一个的方式。
    读取的速度肯定比内存读取慢，所以要设置好多线程读取。在Dataloader中的多线程不知道是否就是针对__getitem__的多线程。
    """

    def __init__(self, train=True, transform=None, target_transform=None, download=False):
        """
        init作为初始化函数，在实例化这个类的时候是会被运行的！
        而下面的那些函数
        """
        self.root_path = "./data/"
        self.training_file = "train.pt"
        self.test_file = "test.pt"
        self.transform = transform
        self.target_transform = target_transform
        self.train = train  # training set or test set

        """
        在这里先转成tensor会大幅度提高后面数据加载的速度。假如在__getitem__里面再提取、转换，会变得慢很多。
        """
        if self.train:
            self.train_data, self.train_label = torch.load("./data/train.pt")
        else:
            self.test_data = torch.load("./data/test.pt")

    def __getitem__(self, index):
        if self.train:
            img, target = self.train_data[index], int(self.train_label[index])
        else:
            img, target = self.test_data[index], -1
        im = img.numpy().astype(np.uint8)
        img = Image.fromarray(im, mode='L')
        if self.transform is not None:
            img = self.transform(img)
        im1 = img.numpy()
        a = 1
        if self.target_transform is not None:
            target = self.target_transform(target)
        return img, target

    def __len__(self):
        if self.train:
            return len(self.train_data)
        else:
            return len(self.test_data)


def My_Data_loader():
    train_dataset = DigitalRecognizer(train=True, transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,)),
    ]))
    test_dataset = DigitalRecognizer(train=False, transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,)),
    ]))
    train_db, val_db = torch.utils.data.random_split(train_dataset, [35000, 7000])
    print('train:', len(train_db), 'validation:', len(val_db))
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=64, shuffle=False)

    tra_loader = torch.utils.data.DataLoader(
        train_db,
        batch_size=64, shuffle=True)
    val_loader = torch.utils.data.DataLoader(
        val_db,
        batch_size=64, shuffle=True)
    return tra_loader, val_loader, test_loader


if __name__ == "__main__":
    pass
