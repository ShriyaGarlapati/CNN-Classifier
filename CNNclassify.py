# -*- coding: utf-8 -*-
"""CNNclassify.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1J1H09naNM50YA0dJNTnIcyJKyKKGme2T
"""

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import numpy as np
import matplotlib.pyplot as plt
import time

import cv2
import os
import argparse
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from resnet20_cifar import resnet20

import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from thop import profile, clever_format
from resnet20_cifar import resnet20
import time
import torch
import torchvision.transforms as transforms
from torchvision.datasets import CIFAR10
from PIL import Image









class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=5, stride=1)
        self.bn1 = nn.BatchNorm2d(32)  

        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1)
        self.bn2 = nn.BatchNorm2d(64)  

        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc1 = nn.Linear(64 * 6 * 6, 512)
        self.fc2 = nn.Linear(512, 128)
        self.fc3 = nn.Linear(128, 10)
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        x = self.pool(torch.relu(self.bn1(self.conv1(x))))  
        x = self.pool(torch.relu(self.bn2(self.conv2(x))))  

        x = x.view(-1, 64 * 6 * 6)
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

def train(seed):
    transform_train = transforms.Compose([
      transforms.RandomHorizontalFlip(),  
      transforms.RandomCrop(32, padding=4),  
      transforms.ToTensor(),
      transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))  
      ])
    trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform_train)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=128, shuffle=True, num_workers=2)


    torch.manual_seed(seed)
    np.random.seed(seed)

    model = CNN().to(device)
    criterion = nn.CrossEntropyLoss()
    
    optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9, weight_decay=5e-4)  
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)  
    train_acc_list, test_acc_list = [], []

    for epoch in range(12):  
        model.train()
        correct, total = 0, 0
        running_loss = 0.0

        for i, data in enumerate(trainloader, 0):
            inputs, labels = data
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()

            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        train_acc = 100 * correct / total
        train_acc_list.append(train_acc)

        test_acc = test(model)
        test_acc_list.append(test_acc)

        print(f"Epoch {epoch+1}, Training Accuracy: {train_acc:.2f}%, Test Accuracy: {test_acc:.2f}%")
        scheduler.step()

    torch.save(model.state_dict(), './model/cnn_model.pth')

    plt.plot(train_acc_list, label="Training Accuracy")
    plt.plot(test_acc_list, label="Testing Accuracy")
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()

def test(model=None, img_path=None):
    transform_test = transforms.Compose([
      transforms.ToTensor(),
      transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
      ])
    testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform_test)
    testloader = torch.utils.data.DataLoader(testset, batch_size=100, shuffle=False, num_workers=2)
    if model is None:
        model = CNN().to(device)
        model.load_state_dict(torch.load('./model/cnn_model.pth'))  

    

    model.eval()  
    correct, total = 0, 0

    with torch.no_grad():  
      for data in testloader:  
        images, labels = data
        images, labels = images.to(device), labels.to(device)  

        outputs = model(images)  
        _, predicted = torch.max(outputs.data, 1)  

        total += labels.size(0)  
        correct += (predicted == labels).sum().item()  

    accuracy = 100 * correct / total  
    print(f"Test Accuracy on CIFAR-10 dataset: {accuracy:.2f}%")
    return accuracy



def test_image(img_path):
  transform = transforms.Compose([
    transforms.ToPILImage(),  
    transforms.ToTensor(),  
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))  
    ])

  img = cv2.imread(img_path)  
  img = cv2.resize(img, (32, 32))  

  
  img = transform(img).unsqueeze(0).to(device)  
  model=None
  if model is None:
    model = CNN().to(device)
    model.load_state_dict(torch.load('./model/cnn_model.pth'))  
  model.eval()  
  with torch.no_grad():  
    outputs = model(img)  
    _, predicted = torch.max(outputs.data, 1)  

  print(f"Predicted class: {predicted.item()}")

  conv1_output = model.conv1(img)  
  conv1_output = conv1_output.cpu().detach()  

  fig, axs = plt.subplots(4, 8, figsize=(10, 5))  
  for i in range(32):  
    axs[i // 8, i % 8].imshow(conv1_output[0, i], cmap='gray') 
    axs[i // 8, i % 8].axis('off')  
  plt.tight_layout()  
  plt.savefig('CONV_rslt.png')  
  plt.show()  
























def test_resnet20():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    transform_test = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])

    test_dataset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                                download=True, transform=transform_test)
    test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=100,
                                              shuffle=False, num_workers=2)

    model = resnet20()
    model_path = "./resnet20_cifar10_pretrained.pt"  
    model.load_state_dict(torch.load(model_path, map_location=device))  
    model = model.to(device)  

    model.eval()

    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)

            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = 100 * correct / total
    print(f'Test Accuracy of ResNet-20 on CIFAR-10 test dataset: {accuracy:.2f}%')













def compute_flops_and_params(model, input_size):
    model.eval()  
    input_tensor = torch.randn(input_size)  
    macs, params = profile(model, inputs=(input_tensor,))  
    macs, params = clever_format([macs, params], "%.3f")  
    return macs, params


def MACParameters():

  cnn_model = CNN()
  resnet_model = resnet20()
  cnn_macs, cnn_params = compute_flops_and_params(cnn_model, (1, 3, 32, 32))  
  print(f"CNN Model - MACs: {cnn_macs}, Parameters: {cnn_params}")
  resnet_macs, resnet_params = compute_flops_and_params(resnet_model, (1, 3, 32, 32))  
  print(f"ResNet-20 Model - MACs: {resnet_macs}, Parameters: {resnet_params}")





def inferencespeed(model, input_tensor, num_iterations=1000, warmup_iterations=100):
    model.eval()

    for _ in range(warmup_iterations):
        with torch.no_grad():
            model(input_tensor)

    start_time = time.time()
    for _ in range(num_iterations):
        with torch.no_grad():
            model(input_tensor)
    total_time = time.time() - start_time

    average_time = total_time / num_iterations
    return average_time

def preprocess_cnn_image(image_path):
    transform = transforms.Compose([
        transforms.Resize((32, 32)),  
        transforms.RandomCrop(32, padding=4),  
        transforms.ToTensor(),         
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))  
    ])
    image = Image.open("HORSE.png")  # Open the image file
    image_tensor = transform(image)  # Apply the transformations
    image_tensor = image_tensor.unsqueeze(0)  # Add batch dimension
    return image_tensor

# Preprocessing function for ResNet-20 model
def preprocess_resnet_image(image_path):
    transform = transforms.Compose([
        transforms.Resize((32, 32)),  # Resize to 32x32 for CIFAR-10
        transforms.ToTensor(),         # Convert image to tensor
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))  # Normalize for ResNet-20
    ])
    image = Image.open("HORSE.png")  # Open the image file
    image_tensor = transform(image)  # Apply the transformations
    image_tensor = image_tensor.unsqueeze(0)  # Add batch dimension
    return image_tensor

# Example usage of the function with the custom CNN model and ResNet-20
def inference_speed_test():
    # Specify the path to the actual image you want to test
    image_path = '"HORSE.png"'  # Update this path

    # Preprocess the image for CNN
    cnn_input_tensor = preprocess_cnn_image(image_path).to(device)

    # Preprocess the image for ResNet-20
    resnet_input_tensor = preprocess_resnet_image(image_path).to(device)

    # Load the models
    cnn_model = CNN().to(device)
    cnn_model.load_state_dict(torch.load('./model/cnn_model.pth'))

    from resnet20_cifar import resnet20
    resnet20_model = resnet20().to(device)
    resnet20_model.load_state_dict(torch.load("./resnet20_cifar10_pretrained.pt", map_location=device))

    # Test inference speed for the CNN model
    cnn_inference_time = inferencespeed(cnn_model, cnn_input_tensor)
    print(f"Average Inference Time for CNN Model: {cnn_inference_time * 1000:.4f} ms")

    # Test inference speed for the ResNet-20 model
    resnet_inference_time = inference_speed_test(resnet20_model, resnet_input_tensor)
    print(f"Average Inference Time for ResNet-20 Model: {resnet_inference_time * 1000:.4f} ms")





# Main Function to handle command line arguments
if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(torch.cuda.is_available())
    os.makedirs('./model', exist_ok=True)
    parser = argparse.ArgumentParser(description='CNN Classifier for CIFAR-10')
    parser.add_argument('command', choices=['train', 'test', 'resnet20'], help='command to execute')
    parser.add_argument('image', nargs='?', help='image path for testing')
    args = parser.parse_args()

    if args.command == 'train':
        random_seeds = [189, 173, 200]  # Example seeds
        for seed in random_seeds:
            print(f"Training with seed: {seed}")
            train(seed)
    elif args.command == 'test' and args.image:
        test_image(args.image)
    elif args.command == 'resnet20':
        test_resnet20()
