#EZ trainer : get HR data
import csv
import pygame
import gf2
import tkinter as tk
from tkinter import filedialog 

# Initialize Pygame mixer
pygame.mixer.init()

# Create a new window
root = tk.Tk()

# Create a label widget
heading = tk.Label(root, text="Heart Rate Trainer").pack()

# Define selected_filename here
selected_filename = None

browselbl = tk.Label(root, text="Browse for file").pack()
# Function to open the file dialog
def browse_file():
    global selected_filename
    selected_filename = filedialog.askopenfilename(
        filetypes=[("MP3 files", "*.mp3 *.wav")],
        title="Select an audio file"
    )
    if selected_filename:
        print(f"Selected file: {selected_filename}")
        # You can add any additional functionality you need here
        label.config(text=f"Selected file: {selected_filename}")

# Function to play the selected music file
def play_music():
    global selected_filename
    if selected_filename:
        pygame.mixer.music.load(selected_filename)
        pygame.mixer.music.play()

# Function to stop the music
def stop_music():
    pygame.mixer.music.stop()

# Create a button to browse files
browse_button = tk.Button(root, bg="gray", text="Browse", command=browse_file)
browse_button.pack()

# Create a label to display the selected file path
label = tk.Label(root, text="No file selected")
label.pack()


# Create buttons to play and stop the music
play_button = tk.Button(root, text="Play Music", command=play_music)
play_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Music", command=stop_music)
stop_button.pack(pady=10)


r_hr_lbl = tk.Label(root, text="Please enter your resting Heart Rate").pack()
r_hr_entry = tk.Entry(
    fg="black",
    bg="white",
    width=12
)
r_hr_entry.pack()




start_hr_lbl = tk.Label(root, text="Please enter starting heart rate").pack()

start_hr_entry = tk.Entry(
    fg="black",
    bg="white",
    width=12
)
start_hr_entry.pack()



end_hr_lbl = tk.Label(root, text="Please enter ending heart rate").pack()

end_hr_entry = tk.Entry(
    fg="black",
    bg="white",
    width=12
)
end_hr_entry.pack()



hr_list = []

def calculate_and_save():
    global selected_filename
    hr_list = (gf2.get_characteristics(selected_filename))

    start_hr = int (start_hr_entry.get())
    r_hr = int (r_hr_entry.get())
    end_hr = int(end_hr_entry.get())

    difference =  end_hr-start_hr
    hr_list.append(start_hr)
    hr_list.append(r_hr)
    hr_list.append(difference)

    print(hr_list)
    
    csv_filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    with open(csv_filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(hr_list)
    print("I have saved the following list:")
    print(hr_list)
    start_hr_entry.delete(0, tk.END)
    r_hr_entry.delete(0, tk.END)
    end_hr_entry.delete(0, tk.END)
    

calculate_button = tk.Button(root, text="Save", command=calculate_and_save)
calculate_button.pack(pady=10)

# Start the event loop
root.mainloop()

pygame.quit()