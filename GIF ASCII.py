import subprocess
import time
from PIL import Image, ImageSequence
import tkinter as tk
from tkinter import filedialog
import requests
import io

# Function to get user choice (File or URL)
def get_user_choice():
    while True:
        print("Choose an option:")
        print("1. Display from a GIF file")
        print("2. Display from a URL")
        choice = input("Enter the option number (1/2): ")
        if choice in ['1', '2']:
            return choice
        else:
            print("Invalid option. Please choose 1 or 2.")

# Function to display a GIF from a file
def display_gif_from_file():
    root = tk.Tk()
    root.withdraw()
    gif_path = filedialog.askopenfilename(
        title="Select a GIF file",
        filetypes=[("GIF files", "*.gif")]
    )
    root.destroy()

    if not gif_path:
        print("No file selected. The program will exit.")
        exit()

    display_gif_in_cmd(gif_path)

# Function to display a GIF from a URL
def display_gif_from_url():
    url = input("Enter the URL of the GIF: ")
    display_gif_as_ascii(url)

# Function to get the aspect ratio of the GIF
def get_aspect_ratio(image):
    width, height = image.size
    return height / width

# Function to resize the image for ASCII rendering
def resize_image(image, new_width):
    aspect_ratio = get_aspect_ratio(image)
    new_height = int(new_width * aspect_ratio * 0.55)
    resized_image = image.resize((new_width, new_height)).convert('L')
    return resized_image

# Function to convert a frame to ASCII
def frame_to_ascii(image):
    ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
    ascii_image = ""
    for pixel in image.getdata():
        ascii_image += ASCII_CHARS[pixel // 25]
    return ascii_image

# Function to display ASCII animation in the CMD
def display_gif_in_cmd(gif_path, width=120):
    with Image.open(gif_path) as gif:
        aspect_ratio = get_aspect_ratio(gif)
        cmd_height = int(width * aspect_ratio * 0.55)
        subprocess.run(f"mode con cols={width} lines={cmd_height}", shell=True)

        frames = [frame_to_ascii(resize_image(frame, width)) for frame in ImageSequence.Iterator(gif)]
        try:
            while True:
                for frame in frames:
                    subprocess.run("cls", shell=True)
                    print("\n".join(frame[i:(i+width)] for i in range(0, len(frame), width)))
                    time.sleep(gif.info['duration'] / 1000)
        except KeyboardInterrupt:
            pass

# Function to display a GIF from a URL
def display_gif_as_ascii(url, width=120):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Unable to download the GIF. Status Code: {response.status_code}")
        return

    gif = Image.open(io.BytesIO(response.content))

    aspect_ratio = get_aspect_ratio(gif)
    cmd_height = int(width * aspect_ratio * 0.55)
    subprocess.run(f"mode con cols={width} lines={cmd_height}", shell=True)

    frames = [frame_to_ascii(resize_image(frame, width)) for frame in ImageSequence.Iterator(gif)]
    try:
        while True:
            for frame in frames:
                subprocess.run("cls", shell=True)
                print("\n".join(frame[i:(i+width)] for i in range(0, len(frame), width)))
                time.sleep(gif.info['duration'] / 1000)
    except KeyboardInterrupt:
        pass

# Main menu
choice = get_user_choice()

if choice == '1':
    display_gif_from_file()
elif choice == '2':
    display_gif_from_url()
