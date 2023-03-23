import os
import customtkinter
import tkinter as tk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import datetime

import get_measurements


WIDTH = 1000
HEIGTH = 600
PLOT_EKG = False


customtkinter.set_default_color_theme("green")
customtkinter.set_appearance_mode('Light')


def start_EKG():
    global PLOT_EKG
    PLOT_EKG = True


def stop_EKG():
    global PLOT_EKG
    PLOT_EKG = False




class LiveBPMFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # create the label
        self.time_label = customtkinter.CTkLabel(self, text="", font=("Segoe UI", 30))
        self.time_label.pack()

        # update the label every second
        self.update_BPM()
        self.after(1000, self.update_BPM)

    def update_BPM(self):
        BPM_data = get_measurements.get_oximeter_data()
        current_BPM = BPM_data[2]
        BPM_valid = BPM_data[3]

        if BPM_valid:
            BPM_str = 'Utrip:   ' + str(current_BPM) + ' BPM'
        else:
            BPM_str = 'Utrip:   -- BPM'

        self.time_label.configure(text=BPM_str)
        self.after(1000, self.update_BPM)



class LiveSpO2Frame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # create the label
        self.time_label = customtkinter.CTkLabel(self, text="", font=("Segoe UI", 30))
        self.time_label.pack()

        # update the label every second
        self.update_SpO2()
        self.after(1000, self.update_SpO2)

    def update_SpO2(self):
        SpO2_data = get_measurements.get_oximeter_data()
        current_SpO2 = SpO2_data[0]
        SpO2_valid = SpO2_data[1]

        if SpO2_valid:
            SpO2_str = 'SpO2:   ' + str(current_SpO2) + '%'
        else:
            SpO2_str = 'SpO2:   --%'
        
        self.time_label.configure(text=SpO2_str)
        self.after(1000, self.update_SpO2)



class LiveTimeFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # create the label
        self.time_label = customtkinter.CTkLabel(self, text="", font=("Segoe UI", 18))
        self.time_label.pack()

        # update the label every second
        self.update_time()
        self.after(1000, self.update_time)

    def update_time(self):
        now = datetime.datetime.now()
        time_str = now.strftime("%H:%M:%S")
        self.time_label.configure(text=time_str)
        self.after(1000, self.update_time)



class LiveDateFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # create the label
        self.time_label = customtkinter.CTkLabel(self, text="", font=("Segoe UI", 18))
        self.time_label.pack()

        # update the label every second
        self.update_date()
        self.after(1000, self.update_date)

    def update_date(self):
        today = datetime.date.today()
        time_str = today.strftime("%d.%m.%Y")
        self.time_label.configure(text=time_str)
        self.after(1000, self.update_date)



class LivePlotFrame(customtkinter.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Create a Figure object and add a subplot
        self.fig = plt.Figure(facecolor='#242424', figsize=(12,4))
        self.ax = self.fig.add_subplot(111)

        # Create a Tkinter canvas that can display the Figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Create a function to update the plot data
        def update_plot(_):
            global PLOT_EKG
            # Generate a random value to plot
            if PLOT_EKG == True:
                y = get_measurements.get_ECG_data()

                # Append the new value to the data list
                self.data.append(y)
  
            # Limit the data to the last few values
            self.data = self.data[-25:]

            # Clear the plot and plot the updated data
            self.ax.clear()
            self.ax.plot(self.data, linewidth=3)

            # Appearance of the plot
            self.ax.grid()
            self.ax.set_facecolor("#444444")
            self.ax.set_xlim(0, 25)
            # self.ax.set_ylim(0, 10)

            self.ax.spines['bottom'].set_color('#c0c0c0')
            self.ax.spines['top'].set_color('#c0c0c0')
            self.ax.spines['right'].set_color('#c0c0c0')
            self.ax.spines['left'].set_color('#c0c0c0')

            self.ax.xaxis.label.set_color('#c0c0c0')
            self.ax.yaxis.label.set_color('#c0c0c0')
            self.ax.tick_params(axis='x', colors='#c0c0c0')
            self.ax.tick_params(axis='y', colors='#c0c0c0')

            # Set the plot title and axis labels
            self.ax.set_title("EKG Live Plot", color='#c0c0c0')
            self.ax.set_xlabel("Time")
            self.ax.set_ylabel("Value")

            # Redraw the canvas
            self.canvas.draw()

        # Create a list to store the plot data
        self.data = []

        # Create an animation that calls the update_plot function every second
        PLOT_INTERVAL = 500
        self.anim = FuncAnimation(self.fig, update_plot, interval=PLOT_INTERVAL)

        # Start the animation
        # self.anim.running = True



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("EKG in Pulzni Oksimeter")
        self.geometry(f'{WIDTH}x{HEIGTH}')

        # Set grid layout 1 x 2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Slike")

        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "icon_white.png")), size=(50, 50))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.EKG_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "EKG.png")),
                                                dark_image=Image.open(os.path.join(image_path, "EKG_2_white.png")), size=(20, 20))
        self.SpO2_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "SPO2.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "SPO2_white.png")), size=(20, 20))


        # Create navigation frame -------------------------------------------------------
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  EKG in SpO2", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Domov",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="EKG",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.EKG_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Pulzni Oksimeter",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.SpO2_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        # Display time
        self.time_frame = LiveTimeFrame(self.navigation_frame)
        self.time_frame.grid(row=4, column=0, padx=20, pady=10, sticky="sew")

        # Display date
        self.date_frame = LiveDateFrame(self.navigation_frame)
        self.date_frame.grid(row=5, column=0, padx=20, pady=10, sticky="nsew")

    

        # Appearance mode - dark/light mode
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")


        # Create home frame -------------------------------------------------------------
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)



        # Create second frame - EKG -----------------------------------------------------
        self.EKG_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.EKG_frame.grid_columnconfigure(0, weight=1)

        # Create the LivePlotFrame and add it to the EKG frame
        self.live_plot_frame = LivePlotFrame(self.EKG_frame)
        self.live_plot_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=30)

        # Button to start the live-plotting
        self.stop_button = customtkinter.CTkButton(self.EKG_frame, text="START", command=start_EKG)
        self.stop_button.grid(row=1, column=0, padx=20, pady=10)
        # Button to stop the live-plotting
        self.stop_button = customtkinter.CTkButton(self.EKG_frame, text="STOP", command=stop_EKG)
        self.stop_button.grid(row=2, column=0, padx=20, pady=10)



        # Create third frame - SpO2 -----------------------------------------------------
        self.SpO2_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.SpO2_frame.columnconfigure(0, weight=1)

        self.SpO2_frame_large_image_label = customtkinter.CTkLabel(self.SpO2_frame, text="", image=self.large_test_image)
        self.SpO2_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.SpO2_current = LiveSpO2Frame(self.SpO2_frame)
        self.SpO2_current.grid(row=1, column=0, padx=20, pady=10, sticky='ew')

        self.BPM_current = LiveBPMFrame(self.SpO2_frame)
        self.BPM_current.grid(row=2, column=0, padx=20, pady=10, sticky='ew')


        # Create changing image frame ---------------------------------------------------
        # self.change_image = MyFrame(self.SpO2_frame)
        # self.change_image.grid(row=3, column=0, padx=20, pady=10, sticky='ew')



        # Select default frame
        self.select_frame_by_name("home")



    def select_frame_by_name(self, name):
        # Set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # Show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
            
        if name == "frame_2":
            self.EKG_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.EKG_frame.grid_forget()

        if name == "frame_3":
            self.SpO2_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.SpO2_frame.grid_forget()


    def home_button_event(self):
        self.select_frame_by_name("home")


    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")


    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")


    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)




if __name__ == "__main__":
    app = App()
    app.mainloop()
