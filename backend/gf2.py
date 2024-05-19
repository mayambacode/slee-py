import librosa
import numpy as np

#filename = 'audio.wav'
#filename = librosa.example('nutcracker')

# Load the audio file
#filename = 'nutcracker'

def get_characteristics(filename):
    # Load the audio file
    y, sr = librosa.load(filename)
    
    
    index_20 = int(20 * sr)
    index_last_20 = max(0, len(y) - index_20)  # start of the last 20 seconds

    # Extract tempo for the whole song, first 20% and last 20%
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    tempo_first_20, _ = librosa.beat.beat_track(y=y[:index_20], sr=sr)
    tempo_last_20, _ = librosa.beat.beat_track(y=y[index_last_20:], sr=sr)
    
    # Calculate the pitch
    # pitch = calculate_pitch(y, sr)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    #  Extract pitch values
    pitch_values = []
    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        if pitch > 0:
            pitch_values.append(pitch)
    
    # Convert the list to a numpy array
    pitch_values = np.array(pitch_values)

    # Calculate the average pitch
    pitch = np.mean(pitch_values)

    # Define duration for analysis (20 seconds)
    duration = 20  # seconds

    # Calculate the number of samples for 20 seconds
    num_samples = duration * sr

    # Extract the first 20 seconds
    y_first_20s = y[:num_samples]

    # Extract the last 20 seconds
    y_last_20s = y[-num_samples:]

    def average_pitch(y_segment, sr):
        pitches, magnitudes = librosa.piptrack(y=y_segment, sr=sr)
        pitch_values = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:
                pitch_values.append(pitch)
        pitch_values = np.array(pitch_values)
        return np.mean(pitch_values)

# Calculate the average pitch of the first 20 seconds
    pitch_first_20 = average_pitch(y_first_20s, sr)

# Calculate the average pitch of the last 20 seconds
    pitch_last_20 = average_pitch(y_last_20s, sr)

    # Get length of the song
    length = librosa.get_duration(y=y, sr=sr)
    
    # Append all values to a list
    characteristics = [tempo, tempo_first_20, tempo_last_20, length,  pitch_first_20, pitch_last_20, pitch ] 
    
    return characteristics

# Test the function
#characteristics = get_characteristics(filename)
#print(characteristics)
#print(type(filename))