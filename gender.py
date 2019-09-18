# -*- coding: utf-8 -*-
"""3주차 과제.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RljepKXOryeIRRTXrer3sql0avmdgSOD
"""

import sys
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision.transforms as transforms
import torchvision.datasets as dset
from torchsummary import summary

print("--sys.version--")
print(sys.version)

print("\n--torch.__version__--")
print(torch.__version__)

batch_size = 20
total_epoch = 100
learning_rate = 0.01
use_cuda = torch.cuda.is_available()
criterion = nn.CrossEntropyLoss()

from google.colab import drive
drive.mount('/content/gdrive')

train_dataset = dset.ImageFolder(root="/content/gdrive/My Drive/Colab Notebooks/pytorch/gender classification/train", transform=transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]))
test_dataset = dset.ImageFolder(root="/content/gdrive/My Drive/Colab Notebooks/pytorch/gender classification/test", transform=transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]))

train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False)

def train(model, train_loader):
  model.train()
  
  optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
  losses = []
  for i, (image, label) in enumerate(train_loader):
    
    if use_cuda:
      image = image.cuda()
      label = label.cuda()
      
    pred_label = model(image)
    loss = criterion(pred_label, label)
    losses.append(loss.item())
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
  avg_loss = sum(losses)/len(losses)
  return avg_loss

def eval(model, test_loader):
  model.eval()
  device = next(model.parameters()).device.index
  
  total_cnt = 0
  correct_cnt = 0
  
  for i, (image, label) in enumerate(test_loader):
    if use_cuda:
      image = image.cuda()
      label = label.cuda()
      
      out = model(image)
      _, pred_label = torch.max(out.data, 1)
      total_cnt += image.data.size()[0]
      correct_cnt += (pred_label == label.data).sum().item()
      
    return correct_cnt / total_cnt

class SimpleMLP(nn.Module):
  def __init__(self):
    super(SimpleMLP, self).__init__()
    self.fc1 = nn.Linear(3*32*32, 8*28*28) 
    self.act1 = nn.ReLU()
    self.fc2 = nn.Linear(8*28*28, 8*24*24)
    self.act2 = nn.ReLU()    
    self.fc3 = nn.Linear(8*24*24, 16*8*8)
    self.act3 = nn.ReLU()
    self.fc4 = nn.Linear(16*8*8, 16*4*4)
    self.act4 = nn.ReLU()
    
    # Output layer
    self.out = nn.Linear(16*4*4, 10)
    
  def forward(self, x):
    x = x.view(-1, 3*32*32)
    x = self.act1(self.fc1(x))
    x = self.act2(self.fc2(x))
    x = self.act3(self.fc3(x))
    x = self.act4(self.fc4(x))
    
    out = self.out(x)
    return out

class SimpleMLP_Sigmoid(nn.Module):
  def __init__(self):
    super(SimpleMLP_Sigmoid, self).__init__()
    self.fc1 = nn.Linear(3*32*32, 8*28*28) 
    self.act1 = nn.Sigmoid()
    self.fc2 = nn.Linear(8*28*28, 8*24*24)
    self.act2 = nn.Sigmoid()    
    self.fc3 = nn.Linear(8*24*24, 16*8*8)
    self.act3 = nn.Sigmoid()
    self.fc4 = nn.Linear(16*8*8, 16*4*4)
    self.act4 = nn.Sigmoid()
    
    # Output layer
    self.out = nn.Linear(16*4*4, 10)
    
  def forward(self, x):
    x = x.view(-1, 3*32*32)
    x = self.act1(self.fc1(x))
    x = self.act2(self.fc2(x))
    x = self.act3(self.fc3(x))
    x = self.act4(self.fc4(x))
    
    out = self.out(x)
    return out

class SimpleCNN(nn.Module):
  def __init__(self):
    super(SimpleCNN, self).__init__()
    # Convolution layer
    self.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=2, padding=1)
    self.act1 = nn.ReLU()
    self.pool1 = nn.MaxPool2d(kernel_size=2)
    
    self.conv2 = nn.Conv2d(64, 192, kernel_size=3, padding=1)
    self.act2 = nn.ReLU()
    self.pool2 = nn.MaxPool2d(kernel_size=2)
    
    self.conv3 = nn.Conv2d(192, 384, kernel_size=3, padding=1)
    self.act3 = nn.ReLU()
    
    self.conv4 = nn.Conv2d(384, 256, kernel_size=3, padding=1)
    self.act4 = nn.ReLU()
    self.pool3 = nn.MaxPool2d(kernel_size=2)
    
    # Fully-Connected layer
    self.fc1 = nn.Linear(256 * 2 * 2, 1000)
    self.act5 = nn.ReLU()
    self.output = nn.Linear(1000, 10)
    
    
  def forward(self, x):
    x = self.pool1(self.act1(self.conv1(x)))
    x = self.pool2(self.act2(self.conv2(x)))
    x = self.act3(self.conv3(x))
    x = self.act4(self.conv4(x))
    x = self.pool3(x)
    
    x = x.view(-1, 256 * 2 * 2)
    
    x = self.act5(self.fc1(x))
    out = self.output(x)
    return out

class SimpleVGG(nn.Module):
  def __init__(self):
    super(SimpleVGG, self).__init__()
    self.conv1 = nn.Conv2d(3, 64, kernel_size=(3,3), padding=(1,1))
    self.act1 = nn.ReLU()
    self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
    
    
    self.conv2 = nn.Conv2d(64, 128, kernel_size=(3,3), padding=(1,1))
    self.act2 = nn.ReLU()
    self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
    
    self.conv3_1 = nn.Conv2d(128, 256, kernel_size=(3,3), padding=(1,1))
    self.act3_1 = nn.ReLU()
    self.conv3_2 = nn.Conv2d(256, 256, kernel_size=(3,3), padding=(1,1))
    self.act3_2 = nn.ReLU()
    self.conv3_3 = nn.Conv2d(256, 256, kernel_size=(3,3), padding=(1,1))
    self.act3_3 = nn.ReLU()
    self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2)
    
    self.conv4_1 = nn.Conv2d(256, 512, kernel_size=(3,3), padding=(1,1))
    self.act4_1 = nn.ReLU()
    self.conv4_2 = nn.Conv2d(512, 512, kernel_size=(3,3), padding=(1,1))
    self.act4_2 = nn.ReLU()
    self.conv4_3 = nn.Conv2d(512, 512, kernel_size=(3,3), padding=(1,1))
    self.act4_3 = nn.ReLU()
    self.pool4 = nn.AvgPool2d(kernel_size=2, stride=2)
    
    # Output layer
    self.fc1 = nn.Linear(512 * 2 * 2, 512)
    self.act5 = nn.ReLU()
    self.out = nn.Linear(512, 10)
    
  def forward(self, x):
    x1 = x
    x2 = self.act1(self.conv1(x1))
    x3 = self.pool1(x2)
    
    x4 = self.act2(self.conv2(x3))
    x5 = self.pool2(x4)
    
    x6 = self.act3_1(self.conv3_1(x5))
    x7 = self.act3_2(self.conv3_2(x6))
    x8 = self.act3_3(self.conv3_3(x7))
    x9 = self.pool3(x8)
    
    x10 = self.act4_1(self.conv4_1(x9))
    x11 = self.act4_2(self.conv4_2(x10))
    x12 = self.act4_3(self.conv4_3(x11))
    x13 = self.pool4(x12)
    
    x14 = x13.view(-1, 512 * 2 * 2)
    
    x15 = self.act5(self.fc1(x14))
    
    out = self.out(x15)
    return out

class SimpleResNet(nn.Module):
  def __init__(self):
    super(SimpleResNet, self).__init__()
    self.conv1 = nn.Conv2d(3, 64, kernel_size=(3,3), padding=(1,1))
    self.act1 = nn.ReLU()
    self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
    
    
    self.conv2 = nn.Conv2d(64, 128, kernel_size=(3,3),padding=(1,1))
    self.act2 = nn.ReLU()
    self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
    
    self.conv3_1 = nn.Conv2d(128, 256, kernel_size=(3,3), padding=(1,1))
    self.act3_1 = nn.ReLU()
    self.conv3_2 = nn.Conv2d(256, 256, kernel_size=(3,3), padding=(1,1))
    self.act3_2 = nn.ReLU()
    self.conv3_3 = nn.Conv2d(256, 256, kernel_size=(3,3), padding=(1,1))
    self.act3_3 = nn.ReLU()
    self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2)
    
    self.conv4_1 = nn.Conv2d(256, 512, kernel_size=(3,3), padding=(1,1))
    self.act4_1 = nn.ReLU()
    self.conv4_2 = nn.Conv2d(512, 512, kernel_size=(3,3), padding=(1,1))
    self.act4_2 = nn.ReLU()
    self.conv4_3 = nn.Conv2d(512, 512, kernel_size=(3,3), padding=(1,1))
    self.act4_3 = nn.ReLU()
    self.pool4 = nn.AvgPool2d(kernel_size=2, stride=2)
    
    # Output layer
    self.fc1 = nn.Linear(512 * 2 * 2, 512)
    self.act5 = nn.ReLU()
    self.out = nn.Linear(512, 10)
  
  def forward(self, x):
    x1 = x
    x2 = self.act1(self.conv1(x1))
    x3 = self.pool1(x2)
    
    x4 = self.act2(self.conv2(x3))
    x5 = self.pool2(x4)
    
    x6 = self.act3_1(self.conv3_1(x5))
    x7 = self.act3_2(self.conv3_2(x6))
    x8 = self.act3_3(self.conv3_3(x7) + x6)
    x9 = self.pool3(x8)
    
    x10 = self.act4_1(self.conv4_1(x9))
    x11 = self.act4_1(self.conv4_2(x10))
    x12 = self.act4_1(self.conv4_3(x11) + x10)
    x13 = self.pool4(x12)
    
    x14 = x13.view(-1, 512 * 2 * 2)
    
    x15 = self.act5(self.fc1(x14))
    
    out = self.out(x15)
    return out

mlp_model = SimpleMLP().cuda()
train_loss_lst = []
test_accuracy_lst = []
for epoch in range(total_epoch):
  train_loss = train(mlp_model, train_loader)
  train_loss_lst.append(train_loss)
  test_accuracy = eval(mlp_model, test_loader)
  test_accuracy_lst.append(test_accuracy)
  
  print(epoch+1, "loss :", train_loss)
  print("Accuracy :", test_accuracy)
  
summary(mlp_model, input_size = (3, 32, 32))

mlp_model2 = SimpleMLP_Sigmoid().cuda()
train_loss_lst = []
test_accuracy_lst = []
for epoch in range(total_epoch):
  train_loss = train(mlp_model, train_loader)
  train_loss_lst.append(train_loss)
  test_accuracy = eval(mlp_model, test_loader)
  test_accuracy_lst.append(test_accuracy)
  
  print(epoch+1, "loss :", train_loss)
  print("Accuracy :", test_accuracy)
  
summary(mlp_model2, input_size = (3, 32, 32))

cnn_model = SimpleCNN().cuda()
train_loss_lst = []
test_accuracy_lst = []
for epoch in range(total_epoch):
  train_loss = train(cnn_model, train_loader)
  train_loss_lst.append(train_loss)
  test_accuracy = eval(cnn_model, test_loader)
  test_accuracy_lst.append(test_accuracy)
  
  print(epoch+1, "loss :", train_loss)
  print("Accuracy :", test_accuracy)
  
summary(cnn_model, input_size = (3,32,32))

vgg_model = SimpleVGG().cuda()
train_loss_lst = []
test_accuracy_lst = []
for epoch in range(total_epoch):
  train_loss = train(vgg_model, train_loader)
  train_loss_lst.append(train_loss)
  test_accuracy = eval(vgg_model, test_loader)
  test_accuracy_lst.append(test_accuracy)
  
  print(epoch+1, "loss :", train_loss)
  print("Accuracy :", test_accuracy)
  
summary(vgg_model, input_size = (3,32,32))

resnet_model = SimpleResNet().cuda()
train_loss_lst = []
test_accuracy_lst = []
for epoch in range(total_epoch):
  train_loss = train(resnet_model, train_loader)
  train_loss_lst.append(train_loss)
  test_accuracy = eval(resnet_model, test_loader)
  test_accuracy_lst.append(test_accuracy)
  
  print(epoch+1, "loss :", train_loss)
  print("Accuracy :", test_accuracy)
  
summary(resnet_model, input_size = (3,32,32))