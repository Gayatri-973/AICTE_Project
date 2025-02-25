import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
import numpy as np

# Initialize main window
root = tk.Tk()
root.title("Image Decryption")
root.geometry("400x250")
root.configure(bg="lightblue")

# Global variables
encrypted_image_path = ""

def select_encrypted_image():
    global encrypted_image_path
    encrypted_image_path = filedialog.askopenfilename(title="Select Encrypted Image", filetypes=[("Image files", "*.png")])
    if encrypted_image_path:
        messagebox.showinfo("Encrypted Image Selected", f"Selected: {os.path.basename(encrypted_image_path)}")

def decrypt_image():
    global encrypted_image_path
    if not encrypted_image_path:
        messagebox.showerror("Error", "Select an encrypted image first.")
        return

    img = cv2.imread(encrypted_image_path)
    pixels = np.array(img, dtype=np.uint8)
    password = password_entry.get()

    if password != password_entry.get():
        messagebox.showerror("Error", "Incorrect password.")
        return

    total_pixels = pixels.size
    if total_pixels < 32:
        messagebox.showerror("Error", "Invalid image or no hidden message found!")
        return

    binary_data = "".join(str(pixels[i // img.shape[1], i % img.shape[1], 0] & 1) for i in range(32))

    try:
        message_length = int(binary_data, 2)
        print(f"Decoded message length: {message_length}")
        
    except ValueError:
        messagebox.showerror("Error", "Failed to decode message length!")
        return

    if message_length <= 0 or message_length * 8 > total_pixels - 32:
        messagebox.showerror("Error", "Invalid message length detected!")
        return

    binary_message = "".join(str(pixels[(32 + i) // img.shape[1], (32 + i) % img.shape[1], 0] & 1) for i in range(message_length * 8))

    try:
        decrypted_text = ""
        for i in range(0, message_length, 8):
            byte = binary_message[i:i + 8]
            print(f"Binary byte: {byte}") 
            char_code = int(byte, 2)
            print(f"Character code: {char_code}") 
            char = chr(char_code)
            print(f"Character: {char}")
            decrypted_text += char
        decrypted_text = decrypted_text.rstrip("\x00")
    except Exception as e:
        messagebox.showerror("Error", f"Error in decoding message: {str(e)}")
        return

    messagebox.showinfo("Decryption Successful", f"Decrypted message:\n\n{decrypted_text}")

# UI Components
style = ttk.Style()
style.configure("TButton", padding=6, relief="raised", font=("Consolas", 12, "bold"))
style.configure("TLabel", font=("Consolas", 12, "bold"))

ttk.Button(root, text="Select Encrypted Image", command=select_encrypted_image).pack(pady=5)

ttk.Label(root, text="Enter Password:").pack()
password_entry = ttk.Entry(root, show="*")
password_entry.pack(pady=2)

decrypt_button = tk.Button(root, text="Decrypt Image", command=decrypt_image, font=("Consolas", 12, "bold"), bg="green", fg="white")
decrypt_button.pack(pady=5)

# Run the GUI
root.mainloop()
