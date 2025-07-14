import tkinter as tk
from tkinter import filedialog, messagebox
import os
from process_video import process_video

input_path = ""
output_dir = ""

def select_input():
    global input_path
    input_path = filedialog.askopenfilename(
        title="Select input video",
        filetypes=[("MP4 files", "*.mp4")]
    )
    input_label.config(text=os.path.basename(input_path))

def select_output_dir():
    global output_dir
    output_dir = filedialog.askdirectory(title="Select output folder")
    output_label.config(text=output_dir)

def run_process():
    if not input_path or not output_dir:
        messagebox.showwarning("Missing Info", "Please select both input video and output folder.")
        return

    start = entry_start.get()
    end = entry_end.get()
    song_id = entry_id.get()

    try:
        output_path = os.path.join(output_dir, "output.mp4")
        process_video(start, end, song_id, input_path=input_path, output_path=output_path)
        messagebox.showinfo("Success", f"Video saved to:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

# GUI setup
root = tk.Tk()
root.title("BeatSyncer")

tk.Label(root, text="Video Start Time (HH:MM:SS):").grid(row=0, sticky='w')
entry_start = tk.Entry(root, width=20)
entry_start.grid(row=0, column=1)

tk.Label(root, text="Video End Time (HH:MM:SS):").grid(row=1, sticky='w')
entry_end = tk.Entry(root, width=20)
entry_end.grid(row=1, column=1)

tk.Label(root, text="BeatSaver ID:").grid(row=2, sticky='w')
entry_id = tk.Entry(root, width=20)
entry_id.grid(row=2, column=1)

tk.Button(root, text="Select Input Video", command=select_input).grid(row=3, column=0, pady=(10,0))
input_label = tk.Label(root, text="No file selected", anchor='w', width=40)
input_label.grid(row=3, column=1, sticky='w')

tk.Button(root, text="Select Output Folder", command=select_output_dir).grid(row=4, column=0)
output_label = tk.Label(root, text="No folder selected", anchor='w', width=40)
output_label.grid(row=4, column=1, sticky='w')

tk.Button(root, text="Process Video", command=run_process).grid(row=5, columnspan=2, pady=20)

root.mainloop()
