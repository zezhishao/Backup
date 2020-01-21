# _*_ coding: utf-8 _*_
# @Time   : 2020/1/21 1:42 下午 
# @Author : 邵泽志 
# @File   : Test.py
# @Desc   :
import numpy as np
import torch
from PIL import Image
from torchvision import transforms
from torchvision.transforms.functional import to_tensor

from dataloader import DigitalRecognizer



def normalize(tensor, mean, std, inplace=False):
    if not _is_tensor_image(tensor):
        raise TypeError('tensor is not a torch image.')

    if not inplace:
        tensor = tensor.clone()

    dtype = tensor.dtype
    mean = torch.as_tensor(mean, dtype=dtype, device=tensor.device)
    std = torch.as_tensor(std, dtype=dtype, device=tensor.device)
    tensor.sub_(mean).div_(std)
    return tensor


def _is_tensor_image(img):
    return torch.is_tensor(img) and img.ndimension() == 3




train_dataset = DigitalRecognizer(train=True, transform=transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,)),
]))
test_dataset = DigitalRecognizer(train=False, transform=transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,)),
]))


###############
train_db, val_db = torch.utils.data.random_split(train_dataset, [30000, 12000])
print('train:', len(train_db), 'validation:', len(val_db))

tra_loader = torch.utils.data.DataLoader(
    train_db,
    batch_size=64, shuffle=True)
val_loader = torch.utils.data.DataLoader(
    val_db,
    batch_size=64, shuffle=True)

###############


train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=64, shuffle=False)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=64, shuffle=False)

# img1 = train_dataset.train_data[0]
# # im1 = img1.numpy().astype(np.uint8)
# im1 = img1.numpy()
# img1 = Image.fromarray(im1, mode='L')
# img1.show()
# img1 = to_tensor(img1)
# img1 = normalize(img1, 0.1307, 0.3081)
# im11 = img1.numpy()
# a = 1


for t, (data, target) in enumerate(tra_loader):
    data_1 = (data[0][0]*0.3081 + 0.1307) * 255.0
    im = data_1.numpy()
    img = Image.fromarray(im, mode='L')
    img.show()
    img.save('new_lena.png')
    a = 1
    pass



a = 1
