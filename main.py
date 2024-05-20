import tkinter as tk
import random
from generate import *
from sort import *
import time


class SortingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Visualization")

        # self.entry_num_elements = tk.Entry(root)
        # self.entry_num_elements.pack()

        self.selected_num_elements = tk.IntVar()
        self.selected_num_elements.set(20)  # Default value

        self.checkbox_values = [10, 20, 50, 100, 200, 500, 1000, 10000]

        # self.optionmenu_num = tk.OptionMenu(root, self.selected_num_elements, *self.checkbox_values)
        # self.optionmenu_num.grid(row=0, column=1, padx=5, pady=5)
        
        self.num_checkboxes_frame = tk.Frame(root)
        self.num_checkboxes_frame.grid(row=0, column=0, columnspan=3, pady=5)
        
        self.label_num_elements = tk.Label(self.num_checkboxes_frame, text="Select Number of Elements:")
        self.label_num_elements.grid(row=0, column=0,  pady=5)

        self.num_checkboxes = []
        for i, value in enumerate(self.checkbox_values):
            checkbox = tk.Checkbutton(self.num_checkboxes_frame, text=str(value), variable=self.selected_num_elements, onvalue=value)
            row = 0 #i>=(len(self.checkbox_values)/2)
            checkbox.grid(row=row, column=int(i+1 - row * len(self.checkbox_values)/2), padx=5, pady=5)
            self.num_checkboxes.append(checkbox)

        self.button_generate = tk.Button(root, text="Generate", command=self.generate)
        self.button_generate.grid(row=0, column=3, padx=5, pady=5)

        
        self.algorithm_frame = tk.Frame(root)
        self.algorithm_frame.grid(row=1, column=0, columnspan=2, pady=5)

        self.label_algorithm = tk.Label(self.algorithm_frame, text="Select Sorting Algorithm:")
        self.label_algorithm.grid(row=0, column=0, padx=5, pady=5)

        self.selected_algorithm = tk.StringVar(root)
        self.selected_algorithm.set("Bubble Sort")  # Default value
        
        # self.sort_checkboxes_frame = tk.Frame(root)
        # self.sort_checkboxes_frame.grid(row=1, column=1, columnspan=1, pady=5)

        # self.sort_checkboxes = []
        # for i, value in enumerate(sorting_algorithms):
        #     checkbox = tk.Checkbutton(self.sort_checkboxes_frame, text=str(value), variable=self.selected_algorithm, onvalue=value)
        #     row = i>=(len(sorting_algorithms)/2)
        #     checkbox.grid(row=row, column=int(i - row * len(sorting_algorithms)/2), padx=5, pady=5)
        #     self.sort_checkboxes.append(checkbox)

        self.optionmenu_algorithm = tk.OptionMenu(self.algorithm_frame, self.selected_algorithm, *sorting_algorithms)
        self.optionmenu_algorithm.grid(row=0, column=1, padx=5, pady=5)

        self.sort_buttoms_frame = tk.Frame(root)
        self.sort_buttoms_frame.grid(row=1, column=2, columnspan=2, padx=5, pady=5)

        self.button_gensort = tk.Button(self.sort_buttoms_frame, text="Generate & Sort", command=self.gensort)
        self.button_gensort.grid(row=0, column=0, columnspan=1, padx=5, pady=5)

        self.button_sort = tk.Button(self.sort_buttoms_frame, text="Sort", command=self.sort)
        self.button_sort.grid(row=0, column=1, columnspan=1, padx=5, pady=5)

        self.button_instasort = tk.Button(self.sort_buttoms_frame, text="Instant Sort", command=self.instasort)
        self.button_instasort.grid(row=0, column=3, columnspan=1, padx=5, pady=5)

        self.button_skip = tk.Button(self.sort_buttoms_frame, text="Skip", command=self.skip)
        self.button_skip.grid(row=0, column=4, columnspan=1, padx=5, pady=5)

        self.button_pause = tk.Button(self.sort_buttoms_frame, text="Pause", command=self.pause)
        self.button_pause.grid(row=0, column=5, columnspan=1, padx=5, pady=5)

        self.button_stop = tk.Button(self.sort_buttoms_frame, text="Stop", command=self.stop)
        self.button_stop.grid(row=0, column=6, columnspan=1, padx=5, pady=5)

        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

        self.data = []
        self.number_to_color = []
        self.is_sorting = False
        self.is_paused = False
        self.skipping = False

        self.generate()

    def generate(self):
        self.is_sorting = False
        num_elements = self.selected_num_elements.get()
        self.data,colors,self.number_to_color = generate_num_to_color(num_elements)
        self.draw(self.data)

    def sort(self, skip=False):
        if self.is_sorting:
            self.stop()
            self.root.update()
            time.sleep(0.1)  # Polling interval

        algorithm = self.selected_algorithm.get()
        print(algorithm)
        print("Sorting...")
        self.is_sorting = True
        self.is_paused = False

        data = self.data.copy()
        step = 0
        start_time = time.time()  # Start time
        
        gen = get_sorting_generator(algorithm,data)
        for sorted_data in gen:
            if self.is_paused:
                while self.is_paused:
                    if not self.is_sorting:  # Check if the sorting process needs to be stopped
                        break
                    self.root.update()
                    time.sleep(0.1)  # Polling interval
            step += 1
            if not skip and not self.skipping:
                self.draw(sorted_data,algorithm,step)
                self.canvas.update()
            # self.root.after(1)
            if not self.is_sorting:  # Check if the sorting process needs to be stopped
                break

        if skip or self.skipping:
            self.draw(sorted_data,algorithm,step)
            self.canvas.update()
        self.skipping = False

        end_time = time.time()  # End time
        time_taken = end_time - start_time

        self.draw_time_taken(time_taken)
        # Add other sorting algorithms here

    def gensort(self):
        self.generate()
        self.sort()

    def instasort(self):
        self.sort(True)

    def pause(self):
        self.is_paused = not self.is_paused

    def stop(self):
        self.is_sorting = False
        
    def skip(self):
        self.skipping = True

    def draw(self, data, algorithm=False, step=0):
        self.canvas.delete("all")
        bar_width = 800 / len(data)
        for i, height in enumerate(data):
            x0 = i * bar_width
            y0 = 600
            x1 = (i + 1) * bar_width
            y1 = 600 - height
            color = self.number_to_color[height]  # Assuming self.number_to_color is a dictionary mapping height to color
            rgb_color = "#%02x%02x%02x" % tuple(int(c * 255) for c in color)  # Convert RGB tuple to hexadecimal color code
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=rgb_color)
        if (algorithm):
            self.canvas.create_text(400, 20, text=f"Algorithm: {algorithm}", fill="black", font=("Helvetica", 16))
            self.canvas.create_text(400, 40, text=f"Step: {step}", fill="black", font=("Helvetica", 16))

    def draw_time_taken(self, time_taken):
        self.canvas.create_text(400, 60, text=f"Time taken: {time_taken:.4f} seconds", fill="black", font=("Helvetica", 16))


if __name__ == "__main__":
    root = tk.Tk()
    app = SortingApp(root)
    root.mainloop()