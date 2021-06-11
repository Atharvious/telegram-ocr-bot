import torch
import torch.nn as nn

# Img sizes width -- 128, 64, 32, 16, 8, 4
# Img sizes height - 32, 16, , 8,  8, 8, 8
class HandwritingModel(nn.Module):
    def __init__(self, num_classes, in_channels=1, img_size=(32,128)):
        super(HandwritingModel, self).__init__()
        self.img_size = img_size

        self.conv_kernels = [5, 5, 3, 3, 3]
        self.features = [in_channels, 32, 64, 128, 128, 256]
        self.pool_kernels = [(2,2),(2,2),(2,1),(2,1),(2,1)]
        self.num_conv_layers = len(self.conv_kernels)
        self.num_rnn_layers = 2
        layers = []
        for i in range(self.num_conv_layers):
            layers.append(
                self.cnn_block(self.features[i],
                          self.features[i+1],
                          self.conv_kernels[i],
                          1,
                          2 if i < 2 else 1,
                          self.pool_kernels[i]
                )
            )
        self.cnn = nn.Sequential(*layers)


        rnn_in_channels = 256

        rnn_hidden_channels = 256
        
        self.lstm = nn.LSTM(rnn_in_channels, rnn_hidden_channels, self.num_rnn_layers, bidirectional= True, batch_first= True)

        self.linear = nn.Sequential(
                nn.Linear(2*rnn_hidden_channels, 512),
                nn.ReLU(),
                nn.Linear(512, num_classes)
            )

    def cnn_block(self, in_channels, out_channels, kernel_size, stride, padding, pool_size):
        return nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding, bias = True),
            nn.BatchNorm2d(out_channels, momentum = 0.5),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size = pool_size,
                           stride= pool_size),
        )

    def forward(self, x):
        x = self.cnn(x)
        try:
            assert x.size(2) == 1
        except AssertionError:
            print(f"CNNout Size:\t{x.size(2)}")

        x = torch.squeeze(x, dim=2).permute(0,2,1)

        x = self.lstm(x)[0]

        return self.linear(x)

def test():
    x = torch.randn(1,1,32,128)
    model = HandwritingModel(num_classes = 36, in_channels = 1, img_size = (32,128))
    print(model)
    print(model(x).size())

if __name__ == '__main__':
    test()