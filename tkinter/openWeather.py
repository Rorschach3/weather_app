import tkinter as tk
from tkinter import Menu, Canvas, PhotoImage, Label, Frame, Entry, Button, OptionMenu, Text
from PIL import Image, ImageTk
import requests
import os
import threading
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the environment variables
OPEN_WEATHER_API_KEY = os.getenv('OPEN_WEATHER_API_KEY')

HEIGHT = 400
WIDTH = 800


def weather(city):
    show['text'] = 'Please wait . . . .'
    try:
        # Correctly constructing the API request
        source = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q={city}&units=imperial&appid={OPEN_WEATHER_API_KEY}')
        data = source.json()

        if data['cod'] != '200':
            show['text'] = "Error! Please try again"
            return

        # Accessing the forecast data (for the first forecast entry)
        forecast = data['list'][0]
        a = "City: " + data['city']['name'] + '\n'
        b = "Weather: " + forecast['weather'][0]['description'] + '\n'
        c = "Temperature: " + str(forecast['main']['temp']) + '°F\n'
        d = "Feels Like: " + str(forecast['main']['feels_like']) + '°F\n'
        e = "Low: " + str(forecast['main']['temp_min']) + '°F\n'
        f = "High: " + str(forecast['main']['temp_max']) + '°F\n'
        g = "Humidity: " + str(forecast['main']['humidity']) + '%\n'

        show['text'] = a + b + c + d + e + f + g
    except Exception as e:
        show['text'] = f"Error! Please try again. \n{str(e)}"
        return


def start_thread():
    threading.Thread(target=lambda: weather(entry.get())).start()


root = tk.Tk()

root.title("Weather App")
root.configure(background="black")

# Menu bar setup
m = Menu(root)
menubar = Menu(m, tearoff=0)
menubar.add_command(label="Home")
menubar.add_command(label="Info")
menubar.add_command(label="Exit", command=root.destroy)

root.config(menu=menubar)

# Main window setup
canvas = Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

background_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "pic.png"))
Label(root, image=background_img).place(relx=0, rely=0, relwidth=1, relheight=1)

upper_frame = Frame(root, bg='gray')
upper_frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor="n")

entry = Entry(upper_frame, bg="white", bd=0)
entry.place(relx=0, rely=0, relwidth=0.7, relheight=1)

Button(upper_frame, text="Search", font=40, bd=0, bg="#f2f2f2", command=start_thread).place(relx=0.7, rely=0, relwidth=0.30, relheight=1)

lower_frame = Frame(root, bg="black", bd=3)
lower_frame.place(relx=0.5, rely=0.3, relwidth=0.75, relheight=0.65, anchor="n")

show = Label(lower_frame, bg="#f2f2f2", font=40)
show.place(relx=0, rely=0, relwidth=1, relheight=1)

if __name__ == "__main__":
    root.mainloop()
