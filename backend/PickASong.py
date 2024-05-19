#The purpose of this file is that is scans all files within the music folder
#that is hardcoded, gets the characteristics, runs the prediction, then picks the best song
#the input for this function is the current heart rate

from gf2 import get_characteristics
import os
#get the directory we are currently in 
script_dir = os.path.dirname(os.path.abspath(__file__))
MUSICISHERE = os.path.join(script_dir, "Music")


import torch
from ModelDefinition import SimpleNN  # Import your model class

# Define the model
input_size = 9  # Number of input values is equal to that number
#was determined earlier.
#10 is a working number, I don't know why
hidden_size = 10 # Number of neurons in the hidden layer (you can change this, but don't. It's working)
#remember, our good little model only return one output. 
output_size = 1  # Number of output values (I don't think heartbeat will exceed 200)
#0.01 is a good learning rate, DO NOT MESS WITH IT. I KNOW YOU ARE TEMPTED TO.
learning_rate = 0.01 
#10% probability of dropping any given connection for the purposes of reducing
#overiffing
dropout_prob = 0.1

print("Load the saved model definition")
# Define the file path to the saved model

script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "HBModel.pth")


# Instantiate the model
model = SimpleNN(input_size, hidden_size, output_size, dropout_prob) # Ensure to provide the required arguments


# Load the model state dict
model.load_state_dict(torch.load(model_path))

# Set the model to evaluation mode
model.eval()

#this scans the selected directory
def find_mp3_files(directory):
    #print("The directory I am looking in is: ", directory)
    mp3_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.mp3'):
                mp3_files.append(os.path.join(root, file))
    #print("The names of the files relative to myself are:" , mp3_files)
    return mp3_files

def pickASong(heartRate, restingHR):
    print("It's time to pick a song")
    mp3filelist = find_mp3_files(MUSICISHERE)
    currentminsong = [mp3filelist[0], 0]
    for song in mp3filelist:
        print("I am considering the song: ", song)
        tempprediction = 3
        print("I am getting the characteristics of this song")
        songcharacteristics = get_characteristics(song)
        print(songcharacteristics)
        songcharacteristics.append(heartRate)
        songcharacteristics.append(restingHR)
        songcharacteristics = songcharacteristics
        print("I am appending the heart rate passed to me to the list")
        print(songcharacteristics)
        songcharacteristics = torch.tensor(songcharacteristics,dtype=torch.float32)
        
        #songcharacteristics = torch.unsqueeze(songcharacteristics,1)
        print("I have attempted to make the thing I'm feeding in look correct")
        print(songcharacteristics)
        tempprediction = model(songcharacteristics)
        tempprediction = tempprediction.tolist()
        tempprediction = tempprediction[0]
        print("The prediction for: ", song, " is: ", tempprediction)
        #if the next song will slow down your heart rate more, then it is the best choice
        if tempprediction < currentminsong[-1]:
            currentminsong[0] = song
            currentminsong[-1] = tempprediction
    return currentminsong[0]

pickASong(100,79)