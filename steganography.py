import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import numpy as np

# Initialize main window
root = tk.Tk()
root.title("Image Steganography")
root.geometry("400x450")  # Increased window height
root.configure(bg="lightblue")

# Global variables
image_path = ""
encrypted_image_path = ""

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
    password = encrypt_password_entry.get()  # Use the correct password entry

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
        lsb = int(i)
        new_pixel_value = (original_pixel_value & 254) | lsb

        pixels[x, y, 0] = np.uint8(new_pixel_value)
        data_index += 1

    encrypted_filepath = "encryptedImage.png"
    cv2.imwrite(encrypted_filepath, pixels)
    messagebox.showinfo("Success", "Image Encrypted Successfully!")
    os.startfile(encrypted_filepath)

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
    password = decrypt_password_entry.get()  # Use the correct password entry

    if password != decrypt_password_entry.get(): # Check against the correct entry
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

# Encryption Section
ttk.Button(root, text="Select Image", command=select_image).pack(pady=5)
ttk.Label(root, text="Enter Secret Message:").pack()
message_entry = ttk.Entry(root)
message_entry.pack(pady=2)
ttk.Label(root, text="Enter Password:").pack()
encrypt_password_entry = ttk.Entry(root, show="*") # Create encrypt password entry
encrypt_password_entry.pack(pady=2)
encrypt_button = tk.Button(root, text="Encrypt Image", command=encrypt_image, font=("Consolas", 12, "bold"), bg="red", fg="white")
encrypt_button.pack(pady=5)

# Decryption Section
ttk.Button(root, text="Select Encrypted Image", command=select_encrypted_image).pack(pady=5)
ttk.Label(root, text="Enter Password:").pack()
decrypt_password_entry = ttk.Entry(root, show="*") # Create decrypt password entry
decrypt_password_entry.pack(pady=2)
decrypt_button = tk.Button(root, text="Decrypt Image", command=decrypt_image, font=("Consolas", 12, "bold"), bg="green", fg="white")
decrypt_button.pack(pady=5)

# Run the GUI
root.mainloop()
