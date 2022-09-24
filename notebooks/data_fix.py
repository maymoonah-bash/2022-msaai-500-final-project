import re
import tkinter as tk
from tkinter import filedialog


def init(root):
    root = tk.Tk()
    root.withdraw()


def scrub_txt_file(root):
    # init windows stuff
    # get the file path
    file_path = filedialog.askopenfilename()
    bad_string = open(file_path, encoding="utf8").read()
    # create regex that only gets basic characters
    regex = "[^a-zA-Z0-9\n\.\,\-]"
    clean_str = re.sub(regex, ' ', bad_string)
    # write out sanitized file
    save_file(clean_str, root)


def save_file(out_string,root):
    fd = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if fd is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    fd.write(out_string)
    fd.close() # `()` was missing.

def main():
    root = tk.Tk()
    root.withdraw()
    scrub_txt_file(root)


if __name__ == "__main__":
    main()