import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import numpy as np

# Initialize main window
root = tk.Tk()
root.title("Image Encryption")
root.geometry("400x300")
root.configure(bg="lightblue")

# Global variables
image_path = ""

def select_image():
    global image_path
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if image_path:
        messagebox.showinfo("Image Selected", f"Selected: {os.path.basename(image_path)}")

def encrypt_image():
    global image_path
    if not image_path:
        messagebox.showerror("Error", "Please select an image first.")
        return

    img = cv2.imread(image_path)
    msg = message_entry.get()
    password = password_entry.get()

    if not msg or not password:
        messagebox.showerror("Error", "Enter both message and password.")
        return

    pixels = np.array(img, dtype=np.uint8)
    binary_message = ''.join(format(ord(i), '08b') for i in msg)
    message_length = len(binary_message)
    binary_length = format(message_length, '032b')

    data_index = 0
    for i in binary_length + binary_message:
        x = data_index // img.shape[1]
        y = data_index % img.shape[1]

        original_pixel_value = pixels[x, y, 0]
        lsb = int(i) #get the bit to set
        new_pixel_value = (original_pixel_value & 254) | lsb 

        pixels[x, y, 0] = np.uint8(new_pixel_value)
        data_index += 1

    encrypted_filepath = "encryptedImage.png"
    cv2.imwrite(encrypted_filepath, pixels)
    messagebox.showinfo("Success", "Image Encrypted Successfully!")
    os.startfile(encrypted_filepath)

# UI Components
style = ttk.Style()
style.configure("TButton", padding=6, relief="raised", font=("Consolas", 12, "bold"))
style.configure("TLabel", font=("Consolas", 12, "bold"))

ttk.Button(root, text="Select Image", command=select_image).pack(pady=5)
ttk.Label(root, text="Enter Secret Message:").pack()
message_entry = ttk.Entry(root)
message_entry.pack(pady=2)
ttk.Label(root, text="Enter Password:").pack()
password_entry = ttk.Entry(root, show="*")
password_entry.pack(pady=2)

encrypt_button = tk.Button(root, text="Encrypt Image", command=encrypt_image, font=("Consolas", 12, "bold"), bg="red", fg="white")
encrypt_button.pack(pady=5)

# Run the GUI
root.mainloop()
