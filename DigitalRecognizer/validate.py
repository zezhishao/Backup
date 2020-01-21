# _*_ coding: utf-8 _*_
# @Time   : 2020/1/21 4:30 下午 
# @Author : 邵泽志 
# @File   : validate.py
# @Desc   :
import torch


def validate(model, valid_loader, max_acc):
    correct = 0
    for t, (data, target) in enumerate(valid_loader):
        with torch.no_grad():
            data, target = data.cuda(), target.cuda()
        pred = model(data)
        # get the index of the max log-probability
        pred = pred.data.max(1, keepdim=True)[1]
        correct += pred.eq(target.data.view_as(pred)).cpu().sum()
    print('{:.3f}%\n'.format(
        100. * correct / len(valid_loader.dataset)))

    acc = 100. * correct / len(valid_loader.dataset)
    if acc > max_acc:
        torch.save(model.state_dict(), "model.pkl")

        max_acc = acc
    return max_acc

