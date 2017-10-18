import base64
import os
from io import FileIO
import tkinter as tk


def create_image_string(img_path):
    with open(img_path, 'rb') as f:
        encoded_string = base64.b64encode(f.read())

    file_name = os.path.basename(img_path).split('.')[0]
    file_name = file_name.replace('-', '_')

    return file_name, encoded_string


def archive_image_files():
    destination_path = "tk_tools"
    py_file = ''

    for root, dirs, files in os.walk("images"):
        for name in files:
            img_path = os.path.join(root, name)
            file_name, file_string = create_image_string(img_path)

            py_file += '{} = {}\n'.format(file_name, file_string)

    py_file += '\n'

    with open(os.path.join(destination_path, 'images.py'), 'w') as f:
        f.write(py_file)

if __name__ == '__main__':
    #archive_image_files()

    root = tk.Tk()
    c = tk.Canvas(root)
    c.grid()

    # read and execute the image file from within
    exec(open('tk_tools/images.py').read())
    print(led_green)

    img = tk.PhotoImage(data=led_green)
    c.create_image(0, 0, image=img, anchor='nw')

    root.mainloop()

