import torch
from ModelDefinition import RNN  # Import your model class

numinputvariables = 9
hiddensize = 10
numlayers = 1 #this is the number of layers of the LSTM model
shuffleBool = True #should we shuffle while training, yes or no?
batchsize = 10 #this is the batch size for training our model
classes = 30 #this is the hidden layer size for the fc model
learningrate = 0.4


# Define the file path to the saved model
model_path = 'RNN_model.pth'


# Instantiate the model
model = RNN(numinputvariables, hiddensize, numlayers, classes)  # Ensure to provide the required arguments

# Load the model state dict
model.load_state_dict(torch.load(model_path))

# Set the model to evaluation mode
model.eval()

def predict_Heart_Beat(datain):
    return model(datain)
