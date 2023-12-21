import tkinter as tk
import subprocess

def run_facial_req():
    subprocess.run(["python3", "facial_req.py"])

def run_facial_req_twilio():
    subprocess.run(["python3", "facial_req_twilio.py"])

def run_headshots():
    subprocess.run(["python3", "headshots.py"])

def run_train_mode():
    subprocess.run(["python3", "train_model.py"])

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Select Script to Run")

    # Create buttons for each script
    btn_facial_req = tk.Button(root, text="Run facial_req.py", command=run_facial_req)
    btn_facial_req_twilio = tk.Button(root, text="Run facial_req_twilio.py", command=run_facial_req_twilio)
    btn_headshots = tk.Button(root, text="Run headshots.py", command=run_headshots)
    btn_train_mode = tk.Button(root, text="Run train_model.py", command=run_train_mode)

    # Place the buttons on the window
    btn_facial_req.pack(pady=10)
    btn_facial_req_twilio.pack(pady=10)
    btn_headshots.pack(pady=10)
    btn_train_mode.pack(pady=10)

    # Start the GUI loop
    root.mainloop()

if __name__ == "__main__":
    main()
