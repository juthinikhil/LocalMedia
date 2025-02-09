import os
import ftplib
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

class FTPUploaderApp:
    def __init__(self, master):
        self.master = master
        master.title("FTP Photo Uploader")
        master.geometry("400x300")
        master.configure(bg="#f0f0f0")

        self.label = ttk.Label(master, text="Enter FTP Server Details:", font=("Arial", 14))
        self.label.pack(pady=10)

        self.server_label = ttk.Label(master, text="FTP Server:")
        self.server_label.pack(pady=5)
        self.server_entry = ttk.Entry(master, width=40)
        self.server_entry.pack(pady=5)

        self.user_label = ttk.Label(master, text="Username:")
        self.user_label.pack(pady=5)
        self.user_entry = ttk.Entry(master, width=40)
        self.user_entry.pack(pady=5)

        self.pass_label = ttk.Label(master, text="Password:")
        self.pass_label.pack(pady=5)
        self.pass_entry = ttk.Entry(master, show='*', width=40)
        self.pass_entry.pack(pady=5)

        self.connect_button = ttk.Button(master, text="Connect", command=self.connect_to_ftp)
        self.connect_button.pack(pady=20)

        self.file_path = ""
        self.ftp = None

    def connect_to_ftp(self):
        server = self.server_entry.get()
        user = self.user_entry.get()
        password = self.pass_entry.get()

        try:
            self.ftp = ftplib.FTP(server)
            self.ftp.login(user, password)
            messagebox.showinfo("Success", "Connected to FTP server!")
            self.show_file_browser()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect: {e}")

    def show_file_browser(self):
        self.clear_widgets()

        self.label.config(text="Select a photo to upload:")
        self.upload_button = ttk.Button(self.master, text="Browse", command=self.browse_file)
        self.upload_button.pack(pady=10)

        self.upload_button = ttk.Button(self.master, text="Upload", command=self.upload_file)
        self.upload_button.pack(pady=10)

    def clear_widgets(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def browse_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
        if self.file_path:
            self.label.config(text=os.path.basename(self.file_path))

    def upload_file(self):
        if not self.file_path:
            messagebox.showwarning("Warning", "Please select a file to upload.")
            return

        try:
            with open(self.file_path, 'rb') as file:
                self.ftp.storbinary(f'STOR {os.path.basename(self.file_path)}', file)
            messagebox.showinfo("Success", "File uploaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload file: {e}")

    def on_closing(self):
        if self.ftp:
            self.ftp.quit()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FTPUploaderApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()