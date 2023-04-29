import torch
import torch.nn as nn

import time
from preprocess import *
#import keras
#from keras.models import Sequential
#from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, RNN
from keras.utils import to_categorical


# Second dimension of the feature is dim2
feature_dim_2 = 11

# Save data to array file first
save_data_to_array(max_len=feature_dim_2)

# # Loading train set and test set
X_train, X_test, y_train, y_test = get_train_test()

# # Feature dimension
feature_dim_1 = 20
channel = 1
epochs = 50
batch_size = 100
verbose = 1
num_classes = 2

# Reshaping to perform 2D convolution
X_train = X_train.reshape(X_train.shape[0], feature_dim_1, feature_dim_2, channel)
X_test = X_test.reshape(X_test.shape[0], feature_dim_1, feature_dim_2, channel)

y_train_hot = to_categorical(y_train)
y_test_hot = to_categorical(y_test)

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.conv1 = nn.Conv2d(channel, 32, kernel_size=2)
        self.conv2 = nn.Conv2d(32, 48, kernel_size=2)
        self.conv3 = nn.Conv2d(48, 120, kernel_size=2)
        self.maxpool = nn.MaxPool2d(kernel_size=2)
        self.dropout1 = nn.Dropout(p=0.25)
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(120*6*6, 128)
        self.dropout2 = nn.Dropout(p=0.25)
        self.fc2 = nn.Linear(128, 64)
        self.dropout3 = nn.Dropout(p=0.4)
        self.fc3 = nn.Linear(64, num_classes)
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x):
        x = nn.functional.relu(self.conv1(x))
        x = nn.functional.relu(self.conv2(x))
        x = nn.functional.relu(self.conv3(x))
        x = self.maxpool(x)
        x = self.dropout1(x)
        x = self.flatten(x)
        x = nn.functional.relu(self.fc1(x))
        x = self.dropout2(x)
        x = nn.functional.relu(self.fc2(x))
        x = self.dropout3(x)
        x = self.fc3(x)
        x = self.sigmoid(x)
        return x
        
model = Model()