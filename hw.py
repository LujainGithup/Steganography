import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import string

class security:
    def __init__(self, root):
        self.root = root
        self.text = ""
        self.bits = tk.StringVar(value="1")
        self.img = None
        self.GUI()

    def GUI(self):
        title = tk.Label(self.root, text="Steganography", font=("Arial", 18, "bold"), fg="black")
        title.grid(row=0, column=0, pady=10, columnspan=4)
        frame1 = tk.LabelFrame(self.root, text="Original Image")
        frame1.grid(row=1, column=0, padx=10, pady=10)

        self.title = tk.Label(frame1, text="", width=30, height=15)
        self.title.grid(row=0, column=0, columnspan=3)


        buttonimage = tk.Button(frame1, text="Select Image", command=self.selectimage, bg="black", fg="white")
        buttonimage.grid(row=1, column=0, padx=5, pady=5)

        buttonhide = tk.Button(frame1, text="Hide", bg="black", fg="white", command=self.hide)
        buttonhide.grid(row=1, column=1, padx=5, pady=5)

        buttonrestore = tk.Button(frame1, text="Restore", bg="black", fg="white", command=self.restore)
        buttonrestore.grid(row=1, column=2, padx=5, pady=5)

        frame2 = tk.LabelFrame(self.root, text="Secret Text")
        frame2.grid(row=1, column=1, padx=10, pady=10)
        self.box = tk.Text(frame2, height=15, width=30)
        self.box.pack()
        button2 = tk.Button(frame2, text="Select Text File", bg="black", fg="white" ,command=self.selecttext)
        button2.pack(pady=5)
        frame3 = tk.LabelFrame(self.root, text="Result Image")
        frame3.grid(row=1, column=2, padx=10, pady=10)
        self.result = tk.Label(frame3, text="", width=30, height=15)
        self.result.pack()
        buttonsave = tk.Button(frame3, text="Save Result",bg="black", fg="white", command=self.saveimage)
        buttonsave.pack(pady=5)
        frameout = tk.Frame(self.root)
        frameout.grid(row=1, column=3, padx=10, pady=10, sticky="n")
        tk.Label(frameout, text="Number of bits ").grid(row=0, column=0, padx=10)
        option = tk.OptionMenu(frameout, self.bits, "1", "2", "3")
        option.grid(row=0, column=1, padx=10)


    def selectimage(self):
        path = filedialog.askopenfilename(filetypes=[("image", "*.bmp")])
        if path:
            self.img = Image.open(path)
            width = 250
            height = 250
            display = ImageTk.PhotoImage(self.img.resize((width, height), Image.LANCZOS))
            self.title.config(image=display, width=width, height=height)
            self.title.image = display
            print(f"Loaded image: {path}")

    def selecttext(self):
        path = filedialog.askopenfilename(filetypes=[("text", "*.txt")])
        if path:
            with open(path, 'r') as file:
                self.text = file.read()
            self.box.delete(1.0, tk.END)
            self.box.insert(tk.END, self.text)
            print(f"Loaded text from file: {path}")
            print(f"Secret text: {self.text}")


    def hide(self):
        if not self.img or not self.text:
            return

        bits = int(self.bits.get())
        copyimage = self.img.copy()
        pixels = copyimage.load()


        tobinary = ''.join(format(ord(char), '08b') for char in self.text) + '00000000'
        length = len(tobinary)
        print(f"binary of secret text is: {tobinary}")

        i = 0
        for y in range(copyimage.height):
            for x in range(copyimage.width):
                if i >= length:
                    break
                r, g, b = pixels[x, y]


                r = (r >> bits) << bits
                g = (g >> bits) << bits
                b = (b >> bits) << bits


                if i < length:
                    r |= int(tobinary[i:i + bits], 2)
                    i += bits
                if i < length:
                    g |= int(tobinary[i:i + bits], 2)
                    i += bits
                if i < length:
                    b |= int(tobinary[i:i + bits], 2)
                    i += bits

                pixels[x, y] = (r, g, b)

            if i >= length:
                break


        width = 250
        height = 250
        resultimage = ImageTk.PhotoImage(copyimage.resize((width, height), Image.LANCZOS))
        self.result.config(image=resultimage, width=width, height=height)
        self.result.image = resultimage
        self.resultimgee = copyimage

    def restore(self):
        if not hasattr(self, 'img') or self.img is None:
            messagebox.showerror("Error", "You must select an original image first!")
            return
        numbits = int(self.bits.get())
        pixels = self.img.load()
        binary = ""
        for y in range(self.img.height):
            for x in range(self.img.width):
                r, g, b = pixels[x, y]
                binary += format(r & ((1 << numbits) - 1), '0' + str(numbits) + 'b')
                binary += format(g & ((1 << numbits) - 1), '0' + str(numbits) + 'b')
                binary += format(b & ((1 << numbits) - 1), '0' + str(numbits) + 'b')

        decoded_text = ""
        for i in range(0, len(binary), 8):
            byte = binary[i:i + 8]
            if len(byte) < 8:
                break
            if byte == '00000000':
                break
            decoded_text += chr(int(byte, 2))
        self.box.delete(1.0, tk.END)
        self.box.insert(tk.END, decoded_text)
        print(f"Decoded text: {decoded_text}")

    def saveimage(self):
        if hasattr(self, 'resultimgee'):
            path = filedialog.asksaveasfilename(defaultextension=".bmp", filetypes=[("image", "*.bmp")])
            if path:
                self.resultimgee.save(path)
                messagebox.showinfo("done", f"result image saved in  {path}")
                print(f"Result image saved in: {path}")



root = tk.Tk()
app = security(root)
root.mainloop()

