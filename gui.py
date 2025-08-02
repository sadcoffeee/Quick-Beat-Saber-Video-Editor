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

def toggle_overlay_fields():
    if apply_overlay_var.get():
        entry_id.config(state='normal')
        label_id.config(fg='black')
    else:
        entry_id.config(state='disabled')
        label_id.config(fg='gray')

def run_process():
    if not input_path or not output_dir:
        messagebox.showwarning("Missing Info", "Please select both input video and output folder.")
        return

    overlay_enabled = apply_overlay_var.get()
    saturation = saturation_value.get()

    start = entry_start.get()
    end = entry_end.get()
    song_id = entry_id.get() if overlay_enabled else ""

    try:
        output_path = os.path.join(output_dir, "output.mp4")
        process_video(start, end, song_id,
                      input_path=input_path,
                      output_path=output_path,
                      apply_overlay=overlay_enabled,
                      saturation=saturation)
        messagebox.showinfo("Success", f"Video saved to:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")


# GUI setup
root = tk.Tk()
apply_overlay_var = tk.BooleanVar(value=True)
saturation_value = tk.DoubleVar(value=1.4)
root.title("BS Quick Video Editor")

tk.Label(root, text="Video Start Time (HH:MM:SS):").grid(row=0, sticky='w')
entry_start = tk.Entry(root, width=20)
entry_start.grid(row=0, column=1)

tk.Label(root, text="Video End Time (HH:MM:SS):").grid(row=1, sticky='w')
entry_end = tk.Entry(root, width=20)
entry_end.grid(row=1, column=1)

tk.Checkbutton(root, text="Show BeatSaver Overlay", variable=apply_overlay_var, command=toggle_overlay_fields).grid(row=4, columnspan=2, pady=(10, 0))

label_id = tk.Label(root, text="BeatSaver ID:")
label_id.grid(row=5, sticky='w')
entry_id = tk.Entry(root, width=20)
entry_id.grid(row=5, column=1)

tk.Label(root, text="Saturation Boost:").grid(row=6, sticky='w')
tk.Scale(root, from_=1.0, to=1.5, resolution=0.05, orient='horizontal',
         variable=saturation_value, length=150).grid(row=6, column=1, sticky='w')

tk.Button(root, text="Select Input Video", command=select_input).grid(row=2, column=0, pady=(10,0))
input_label = tk.Label(root, text="No file selected", anchor='w', width=40)
input_label.grid(row=2, column=1, sticky='w')

tk.Button(root, text="Select Output Folder", command=select_output_dir).grid(row=3, column=0)
output_label = tk.Label(root, text="No folder selected", anchor='w', width=40)
output_label.grid(row=3, column=1, sticky='w')

tk.Button(root, text="Process Video", command=run_process).grid(row=7, columnspan=2, pady=20)

root.mainloop()
