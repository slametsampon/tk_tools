import tkinter as tk
import cmath


class Dial(tk.Frame):
    def __init__(self, parent, **options):
        tk.Frame.__init__(self, parent, padx=3, pady=3, borderwidth=2, **options)


class Compass(tk.Frame):
    def __init__(self, parent, **options):
        tk.Frame.__init__(self, parent, padx=3, pady=3, borderwidth=2, **options)


class RotaryScale(tk.Frame):
    def __init__(self, parent, range=100.0, size=100, **options):
        tk.Frame.__init__(self, parent, padx=3, pady=3, borderwidth=2, **options)

        self.range = range
        self.size = size

        self.canvas = tk.Canvas(self, width=self.size, height=self.size)
        self.canvas.grid()

        initial_value = 0.0
        self.arrow(initial_value)

    def to_absolute(self, x, y):
        return x + self.size/2, y + self.size/2

    def arrow(self, number: float):
        self.canvas.delete('all')

        number = number if number <= self.range else self.range
        number = 0.0 if number < 0.0 else number
        self.draw_scale()

        radius = 0.9 * self.size/2.0
        angle_in_radians = (2.0 * cmath.pi / 3.0) + number / self.range * (5.0 * cmath.pi / 3.0)

        center = cmath.rect(0, 0)
        outer = cmath.rect(radius, angle_in_radians)

        self.canvas.create_line(
            *self.to_absolute(center.real, center.imag),
            *self.to_absolute(outer.real, outer.imag),
            width=5
        )

    def draw_scale(self, divisions=10):
        self.canvas.create_arc(2, 2, self.size-2, self.size-2, style=tk.PIESLICE, start=-60, extent=30, fill='red')
        self.canvas.create_arc(2, 2, self.size-2, self.size-2, style=tk.PIESLICE, start=-30, extent=60, fill='yellow')
        self.canvas.create_arc(2, 2, self.size-2, self.size-2, style=tk.PIESLICE, start=30, extent=210, fill='green')

        # find the distance between the center and the inner tick radius
        inner_tick_radius = int(self.size * 0.4)
        outer_tick_radius = int(self.size * 0.5)

        for tick in range(divisions):
            angle_in_radians = (2.0 * cmath.pi / 3.0) + tick/divisions * (5.0 * cmath.pi / 3.0)
            inner_point = cmath.rect(inner_tick_radius, angle_in_radians)
            outer_point = cmath.rect(outer_tick_radius, angle_in_radians)

            self.canvas.create_line(
                *self.to_absolute(inner_point.real, inner_point.imag),
                *self.to_absolute(outer_point.real, outer_point.imag),
                width=1
            )


class Graph(tk.Frame):
    def __init__(self, parent, x_min, x_max, y_min, y_max, x_scale, y_scale, **options):
        tk.Frame.__init__(parent)

        self.canvas = tk.Canvas(**options)
        self.canvas.grid()

        self.w = float(self.canvas.config('width')[4])
        self.h = float(self.canvas.config('height')[4])
        self.x_min = x_min
        self.x_max = x_max
        self.x_scale = x_scale
        self.y_min = y_min
        self.y_max = y_max
        self.y_scale = y_scale
        self.px_x = (self.w - 100) / ((x_max - x_min) / x_scale)
        self.px_y = (self.h - 100) / ((y_max - y_min) / y_scale)

        self.draw_axes()

    def draw_axes(self):
        rect = 50, 50, self.w - 50, self.h - 50

        self.canvas.create_rectangle(rect, outline="black")

        for x in self.frange(0, self.x_max - self.x_min + 1, self.x_scale):
            x_step = (self.px_x * x) / self.x_scale
            coord = 50 + x_step, self.h - 50, 50 + x_step, self.h - 45
            self.canvas.create_line(coord, fill="black")
            coord = 50 + x_step, self.h - 40
            self.canvas.create_text(coord, fill="black", text=str(self.x_min + x))

        for y in self.frange(0, self.y_max - self.y_min + 1, self.y_scale):
            y_step = (self.px_y * y) / self.y_scale
            coord = 45, 50 + y_step, 50, 50 + y_step
            self.canvas.create_line(coord, fill="black")
            coord = 35, 50 + y_step
            self.canvas.create_text(coord, fill="black", text=str(self.y_max - y))

    def plot_point(self, x, y):
        xp = (self.px_x * (x - self.x_min)) / self.x_scale
        yp = (self.px_y * (self.y_max - y)) / self.y_scale
        coord = 50 + xp, 50 + yp
        # self.canvas.create_text(coord, fill="white", text="x")
        return coord

    def plot_line(self, points):
        last_point = ()
        for point in points:
            this_point = self.plot_point(point[0], point[1])

            if last_point:
                self.canvas.create_line(last_point + this_point, fill="black")
            last_point = this_point
            # print last_point

    @staticmethod
    def frange(x, y, jump, digits_to_round=3):
        while x < y:
            yield round(x, digits_to_round)
            x += jump


if __name__ == '__main__':
    root = tk.Tk()

    p = RotaryScale(root, range=20.0)
    p.grid(row=0, column=0)

    increment = 1.0
    value = 0.0

    def inc():
        global value
        value += increment
        p.arrow(value)
        print(value)

    zero_btn = tk.Button(root, text='increment by {}'.format(increment), command=inc)
    zero_btn.grid(row=1, column=0)



    root.mainloop()

