import torch.nn as nn
from torch.nn import init

class myNet(nn.Module):
    def __init__(self, imtype):
        super(myNet, self).__init__()
        if imtype == 'bit':
            n = 1
        elif imtype == 'rgb':
            n = 3

        self.conv1_1 = nn.Sequential(     # input_size=(1*28*28)
            nn.Conv2d(
                in_channels=n,
                out_channels=16,
                kernel_size=3,
                padding=1
            ),   # padding=2保证输入输出尺寸相同
        )
        self.BN = nn.BatchNorm2d(1, momentum=0.5)
        self.conv1_2 = nn.Sequential(  # input_size=(16*28*28)
            nn.Conv2d(
                in_channels=16,
                out_channels=16,
                kernel_size=3,
                padding=1
            ),  # padding=2保证输入输出尺寸相同
            nn.ReLU(),  # input_size=(16*28*28)
            nn.MaxPool2d(kernel_size=2, stride=2)  # output_size=(16*14*14)
        )
        self.conv2_1 = nn.Sequential(
            nn.Conv2d(
                in_channels=16,
                out_channels=32,
                kernel_size=3),
        )  # output 32*12*12
        self.conv2_2 = nn.Sequential(
            nn.Conv2d(
                in_channels=32,
                out_channels=32,
                kernel_size=3),
            nn.ReLU(),  # input_size=(32*10*10)
            nn.MaxPool2d(2, 2)  # output_size=(8*5*5)
        )
        self.fc1 = nn.Linear(32 * 5 * 5, 128)
        self.relu1 = nn.ReLU()
        self.dropout = nn.Dropout(0.2)
        self._set_init(self.fc1)
        self.fc2 = nn.Linear(128, 11)
        self._set_init(self.fc2)
        self.softmax = nn.LogSoftmax(dim=1)

    def _set_init(self, layer):  # 参数初始化
        init.normal_(layer.weight, mean=0., std=.1)

    # 定义前向传播过程，输入为x
    def forward(self, x):
        # x = x.view(-1, 28, 28)
        # x = self.BN(x)
        # x = x.view(-1, 1, 28, 28)
        x = self.conv1_1(x)
        x = self.conv1_2(x)
        x = self.conv2_1(x)
        x = self.conv2_2(x)
        x = x.view(x.size()[0], -1)
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.dropout(x)
        x = self.fc2(x)
        return self.softmax(x)


class tryNet(nn.Module):
    def __init__(self, imtype):
        super(tryNet, self).__init__()
        if imtype == 'bit':
            n = 1
        elif imtype == 'rgb':
            n = 3

        self.conv1_1 = nn.Sequential(     # input_size=(1*28*28)
            nn.Conv2d(
                in_channels=n,
                out_channels=32,
                kernel_size=3,
                padding=1
            ),   # padding=2保证输入输出尺寸相同
        )
        self.BN = nn.BatchNorm2d(1, momentum=0.5)
        self.conv1_2 = nn.Sequential(  # input_size=(16*28*28)
            nn.Conv2d(
                in_channels=32,
                out_channels=64,
                kernel_size=3,
                padding=1
            ),  # padding=2保证输入输出尺寸相同
            nn.ReLU(),  # input_size=(16*28*28)
            nn.MaxPool2d(kernel_size=2, stride=2)  # output_size=(16*14*14)
        )
        self.conv2_1 = nn.Sequential(
            nn.Conv2d(
                in_channels=64,
                out_channels=128,
                kernel_size=3),
        )  # output 32*12*12
        self.conv2_2 = nn.Sequential(
            nn.Conv2d(
                in_channels=128,
                out_channels=256,
                kernel_size=3),
            nn.ReLU(),  # input_size=(32*10*10)
            nn.MaxPool2d(2, 2)  # output_size=(8*5*5)
        )
        self.gap = nn.AdaptiveAvgPool2d((5, 5))
        self.fc1 = nn.Linear(256*25, 128)
        self.relu1 = nn.PReLU()
        self.dropout = nn.Dropout(0.4)
        self._set_init(self.fc1)
        self.fc2 = nn.Linear(128, 11)
        self.relu2 = nn.PReLU()
        self.softmax = nn.LogSoftmax(dim=1)

    def _set_init(self, layer):  # 参数初始化
        init.normal_(layer.weight, mean=0., std=.1)

    # 定义前向传播过程，输入为x
    def forward(self, x):
        # x = x.view(-1, 28, 28)
        # x = self.BN(x)
        # x = x.view(-1, 1, 28, 28)
        x = self.conv1_1(x)
        x = self.conv1_2(x)
        x = self.conv2_1(x)
        x = self.conv2_2(x)
        x = self.gap(x)
        x = x.view(x.size()[0], -1)
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.dropout(x)
        x = self.fc2(x)
        return self.softmax(x)
