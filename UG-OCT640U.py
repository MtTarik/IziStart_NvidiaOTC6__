#ubuntu 20.04
#python3.8 -HULE

import os
import subprocess
import signal
import threading
import tkinter as tk
from tkinter import messagebox, filedialog, Listbox, END
from datetime import datetime

pipeline_proc = None
record_proc = None
SERIAL = ""

def start_pipeline(serial):
    global pipeline_proc
    cmd = [
        "sudo", "gst-launch-1.0",
        f"oct640usrc serial={serial}", "exposure-mode=auto_minmax",
        "!", "tee", "name=t",
        "t.", "!", "queue", "!", "videoconvert", "!", "xvimagesink", "sync=false",
        "t.", "!", "queue", "!", "fakesink"
    ]
    pipeline_proc = subprocess.Popen(" ".join(cmd), shell=True, preexec_fn=os.setsid)

def stop_pipeline():
    global pipeline_proc
    if pipeline_proc:
        os.killpg(os.getpgid(pipeline_proc.pid), signal.SIGINT)
        pipeline_proc = None

def start_record(serial):
    global record_proc
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filename = f"oct640u_{timestamp}.raw"
    cmd = [
        "sudo", "gst-launch-1.0",
        f"oct640usrc serial={serial}", "exposure-mode=auto_minmax",
        "!", "filesink", f"location={filename}"
    ]
    record_proc = subprocess.Popen(" ".join(cmd), shell=True, preexec_fn=os.setsid)

def stop_record():
    global record_proc
    if record_proc:
        os.killpg(os.getpgid(record_proc.pid), signal.SIGINT)
        record_proc = None

def on_start_stream():
    global SERIAL
    SERIAL = serial_entry.get().strip()
    if not SERIAL:
        messagebox.showerror("Error", "Enter the camera serial number!")
        return
    threading.Thread(target=start_pipeline, args=(SERIAL,)).start()

def on_start_record():
    if not SERIAL:
        messagebox.showerror("Error", "First start the flow!")
        return
    threading.Thread(target=start_record, args=(SERIAL,)).start()

def on_stop_record():
    stop_record()

def on_stop_stream():
    stop_pipeline()

def on_open_videos():
    viewer = tk.Toplevel(root)
    viewer.title("Recorded videos")
    listbox = Listbox(viewer, width=60)
    listbox.pack(padx=10, pady=10)

    files = sorted([f for f in os.listdir() if f.startswith("oct640u_") and f.endswith(".raw")])
    for f in files:
        listbox.insert(END, f)

    def play_selected():
        selected = listbox.get(listbox.curselection())
        cmd = f"ffplay -f rawvideo -pixel_format yuv420p -video_size 1280x720 {selected}"
        subprocess.Popen(cmd, shell=True)

    play_btn = tk.Button(viewer, text="▶️ Review ", command=play_selected)
    play_btn.pack(pady=5)

# GUI Setup
root = tk.Tk()
root.title("OCT640U")

tk.Label(root, text="serial ID Camera:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
serial_entry = tk.Entry(root)
serial_entry.insert(0, "25010760")
serial_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Button(root, text="▶️ Start", command=on_start_stream).grid(row=1, column=0, padx=5, pady=5)
tk.Button(root, text="START_RECORD", command=on_start_record).grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="⏹️ STOP", command=on_stop_record).grid(row=2, column=0, padx=5, pady=5)
tk.Button(root, text="✖️ END ", command=on_stop_stream).grid(row=2, column=1, padx=5, pady=5)
tk.Button(root, text="📂 PLAY FILE VIDEO", command=on_open_videos).grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()





# ResourceWarning : Enable tracemalloc to get the object allocation traceback
# # Windows version (not tested, but should work with the same logic as the Linux version)

# Windows version Facking sorse code) - do not run until there is a version of the gs plugin for windows

# import os
# import subprocess
# import signal
# import threading
# import tkinter as tk
# from tkinter import messagebox, Listbox, END
# from datetime import datetime

# pipeline_proc = None
# record_proc = None
# SERIAL = ""

# def start_pipeline(serial):
#     global pipeline_proc
#     cmd = [
#         "gst-launch-1.0",
#         f"oct640usrc serial={serial}", "exposure-mode=auto_minmax",
#         "!", "tee", "name=t",
#         "t.", "!", "queue", "!", "videoconvert", "!", "autovideosink", "sync=false",
#         "t.", "!", "queue", "!", "fakesink"
#     ]
#     pipeline_proc = subprocess.Popen(" ".join(cmd), shell=True,
#                                      creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)

# def stop_pipeline():
#     global pipeline_proc
#     if pipeline_proc:
#         pipeline_proc.send_signal(signal.CTRL_BREAK_EVENT)
#         pipeline_proc = None

# def start_record(serial):
#     global record_proc
#     timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
#     filename = f"oct640u_{timestamp}.raw"
#     cmd = [
#         "gst-launch-1.0",
#         f"oct640usrc serial={serial}", "exposure-mode=auto_minmax",
#         "!", "filesink", f"location={filename}"
#     ]
#     record_proc = subprocess.Popen(" ".join(cmd), shell=True,
#                                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)

# def stop_record():
#     global record_proc
#     if record_proc:
#         record_proc.send_signal(signal.CTRL_BREAK_EVENT)
#         record_proc = None

# def on_start_stream():
#     global SERIAL
#     SERIAL = serial_entry.get().strip()
#     if not SERIAL:
#         messagebox.showerror("Error", "Enter the camera serial number!")
#         return
#     threading.Thread(target=start_pipeline, args=(SERIAL,), daemon=True).start()

# def on_start_record():
#     if not SERIAL:
#         messagebox.showerror("Error", "Start the stream first!")
#         return
#     threading.Thread(target=start_record, args=(SERIAL,), daemon=True).start()

# def on_stop_record():
#     stop_record()

# def on_stop_stream():
#     stop_pipeline()

# def on_open_videos():
#     viewer = tk.Toplevel(root)
#     viewer.title("Recorded Videos")
#     listbox = Listbox(viewer, width=60)
#     listbox.pack(padx=10, pady=10)

#     files = sorted([f for f in os.listdir() if f.startswith("oct640u_") and f.endswith(".raw")])
#     for f in files:
#         listbox.insert(END, f)

#     def play_selected():
#         try:
#             selected = listbox.get(listbox.curselection())
#             cmd = f"ffplay -f rawvideo -pixel_format yuv420p -video_size 1280x720 {selected}"
#             subprocess.Popen(cmd, shell=True)
#         except:
#             messagebox.showerror("Error", "No file selected")

#     tk.Button(viewer, text="▶️ Play", command=play_selected).pack(pady=5)

# # GUI Setup
# root = tk.Tk()
# root.title("OCT640U GUI - Windows")

# # Serial input
# tk.Label(root, text="Camera Serial:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
# serial_entry = tk.Entry(root)
# serial_entry.insert(0, "25010760")
# serial_entry.grid(row=0, column=1, padx=5, pady=5)

# # Buttons
# tk.Button(root, text="▶️ Start", command=on_start_stream).grid(row=1, column=0, padx=5, pady=5)
# tk.Button(root, text="⏺ Record", command=on_start_record).grid(row=1, column=1, padx=5, pady=5)
# tk.Button(root, text="⏹ Stop Record", command=on_stop_record).grid(row=2, column=0, padx=5, pady=5)
# tk.Button(root, text="❌ Stop Stream", command=on_stop_stream).grid(row=2, column=1, padx=5, pady=5)
# tk.Button(root, text="📂 Open Videos", command=on_open_videos).grid(row=3, column=0, columnspan=2, pady=10)

# root.mainloop()
