
from time import sleep
import json
import tkinter as tk
from urllib.request import urlopen
import requests as requests
from PIL import ImageTk

def get(url: str, max_retries: int = 3) -> requests.Response:
    retries_cnt = 0
    while (_req := requests.get(url)).status_code != 200 \
            and retries_cnt < max_retries:
        sleep(1 + 2 * retries_cnt)
    return _req


if __name__ == '__main__':

    req=get('https://www.varzesh3.com/')
    if req.status_code == 200:
        print(f'it\'s true. Our result:\n{req.headers}')
    else:
        print(f'{req.status_code=}')



    weather = ('http://api.openweathermap.org/data/2.5/weather?'
             'lat=35.69&'
             'lon=51.42&'
             'appid=7cdcfaa69a322e2c77fdf3043de45290&'
             'units=metric&'
             'lang=eng')
    res = requests.get(weather)
    data = res.json()
    print("\nWeather in Tehran:", data['weather'][0]['description'])
    print("temperature:", data['main']['temp'], "°C")
    print("pressure:", data['main']['pressure'], "hPa")
    print("humidity:", data['main']['humidity'], "%")


    IssPosition = get('http://api.open-notify.org/iss-now.json') \
        .json()["iss_position"]
    AstronautsInSpace = get('http://api.open-notify.org/astros.json').json()
    data = dict()
    NumberOfAstronauts = 0
    for Astrona_dic in AstronautsInSpace['people']:
        name, SpaceCraft = Astrona_dic['name'], Astrona_dic['craft']
        if SpaceCraft not in data:
            data[SpaceCraft] = [name]
        else:
            data[SpaceCraft].append(name)
        NumberOfAstronauts += 1
    print(f'\n\n There are currently  {len(data)} Spacecraft in space in which {NumberOfAstronauts} astronauts live!')
    for IssLoc in data:
        if IssLoc == 'ISS':
            print(f'ISS (located at {IssPosition["latitude"]} lat., {IssPosition["longitude"]} '
                  f'lon. right now)')
        else:
            print(IssLoc)
        for Astronauts in data[IssLoc]:
            print('\t' + Astronauts)


def refresh_picture():
    with urlopen(requests.get('https://randomfox.ca/floof/', timeout=5).json()['image']) as resp:
        img = ImageTk.PhotoImage(data=resp.read())
    lbl_picture.configure(image=img)
    lbl_picture.image = img
wndw = tk.Tk()
wndw.title('Cute Cats')
wndw.geometry('800x600')
PictureFrame = tk.Frame(wndw)
PictureFrame.place(relx=0.5, rely=0.5, anchor='c')  # type: ignore
with urlopen(requests.get('https://aws.random.cat/meow', timeout=5).json()['file']) as Res:
    Picture = ImageTk.PhotoImage(data=Res.read())
    lbl_picture = tk.Label(PictureFrame, image=Picture)
lbl_picture.grid(column=0, row=0, padx=10, pady=10)
lbl_picture.config(width=700, height=500)
btn_generate = tk.Button(PictureFrame, text='Next', font=('VK Sans Display', 12), command=refresh_picture)
btn_generate.grid(column=0, row=1, padx=20, pady=20)
wndw.mainloop()
