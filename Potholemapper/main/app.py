import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from main import main

def select_directory(label):
    dir_path = filedialog.askdirectory(title="Select a Directory")
    label['text'] = dir_path  # update label text to selected directory path

def select_file(label):
    file_path = filedialog.askopenfilename(title="Select a File")
    label['text'] = file_path  # update label text to selected file path

def analyze(dashcam_video_dir, gpx_filepath, model_filepath):
    print(dashcam_video_dir)
    print(gpx_filepath)
    print(model_filepath)
    working_dir = "working_dir"
    output_html_filepath = "results.html"
    main(dashcam_video_dir, gpx_filepath, model_filepath, working_dir, output_html_filepath)
    root.quit()

root = tk.Tk()
root.title("Directory and File Selector")

# Apply some styling
style = ttk.Style()
style.configure('TButton', font=('Arial', 10), padding=5)
style.configure('TLabel', font=('Arial', 10), padding=5, background='#ececec')

# Use Frame to hold widgets and apply background color
frame = ttk.Frame(root, padding=10, style='TFrame')
frame.pack(fill='both', expand=True)

# First directory selection
label1 = ttk.Label(frame, text="Select Tesla Dashcam directory", width=50, anchor='w')
label1.pack(fill='x')
button1 = ttk.Button(frame, text="Browse", command=lambda: select_directory(label1))
button1.pack()

# Second directory selection
label2 = ttk.Label(frame, text="Select the .GPX file", width=50, anchor='w')
label2.pack(fill='x')
button2 = ttk.Button(frame, text="Browse", command=lambda: select_file(label2))
button2.pack()

# File selection
label3 = ttk.Label(frame, text="Select the Yolo model file", width=50, anchor='w')
label3.pack(fill='x')
button3 = ttk.Button(frame, text="Browse", command=lambda: select_file(label3))
button3.pack()

# Quit button
button_quit = ttk.Button(frame, text="Quit", command=root.quit)
button_quit.pack()

button_analyze = ttk.Button(frame, text="Analyze", command=lambda: analyze(label1['text'], label2['text'], label3['text']))
button_analyze.pack()

root.mainloop()