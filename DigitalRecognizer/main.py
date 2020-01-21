# _*_ coding: utf-8 _*_
# @Time   : 2020/1/21 1:54 下午 
# @Author : 邵泽志 
# @File   : main.py
# @Desc   :
import pandas as pd
import torch
from torch import nn
from LeNet import Net
from dataloader import My_Data_loader
from validate import validate
from tqdm import tqdm

Train = False

train_loader, valid_loader, test_loader = My_Data_loader()

model = Net().cuda()

loss_fn = nn.NLLLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=1e-2, momentum=0.5)
max_acc = -1

if Train:
    for epoch in range(20):
        for data, target in tqdm(train_loader):
            with torch.no_grad():
                data, target = data.cuda(), target.cuda()
            pred = model(data)
            loss = loss_fn(pred, target)
            # print(epoch, t, loss.data.item())
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        max_acc = validate(model, valid_loader, max_acc)
else:
    model = Net().cuda()
    model.load_state_dict(torch.load("./model.pkl"))
    model.eval()

label_list = []
output_list = []

i = 1

for data, target in test_loader:
    with torch.no_grad():
        data, target = data.cuda(), target.cuda()
    output = model(data)
    pred = output.data.max(1, keepdim=True)[1].reshape(-1).cpu().numpy().tolist()
    label_list += list(range(i, i + len(data)))
    output_list += pred
    i += len(data)

pd.DataFrame({'ImageId': label_list, 'Label': output_list}).to_csv("result.csv", index=False, sep=',')
