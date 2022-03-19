import pyttsx3
import datetime
import wikipedia
import webbrowser
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.font_manager as fm

font = fm.FontProperties(fname='Acme-Regular.ttf')

data = pd.read_csv('big-mac-adjusted-index.csv')
data = data.drop(['USD', 'EUR', 'GBP', 'JPY', 'CNY'], axis=1)
data['date'] = data['date'].apply(lambda x: x.split("-")[0])
data = data.groupby(['date', 'iso_a3', 'name'])[['local_price', 'dollar_price', 'GDP_dollar']].mean().reset_index()
data['date'] = pd.to_numeric(data['date'])
data.head(5)

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def online():
    speak('Starting all system applications')
    print('Starting all system applications')
    speak('Installing all drivers')
    print('Installing all drivers')
    speak('Every driver is installed')
    print('Every driver is installed')
    speak('All systems have been started')
    print('All systems have been started')
    speak('Good to go')
    print('Good to go')


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
        print("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
        print("Good Afternoon!")

    else:
        speak("Good Evening!")
        print("Good Evening!")

    online()
    speak("Please enter your name:")
    n = input("Please enter your name:")
    speak("Hi, I am Jarvis. Please tell me how may I help you")
    speak(n)
    print("Hi, I am Jarvis. Please tell me how may I help you", n)


if __name__ == "__main__":
    wishMe()
    while True:

        speak("Enter your query: ")
        query = input("Enter your query: ")
        query = query.lower()

        if 'who is' in query:
            speak('Searching Wikipedia...')
            print('Searching Wikipedia...')
            query = query.replace("who is", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open google' in query:
            speak("Opening Google")
            print("Opening Google")
            webbrowser.get('chrome').open_new_tab("google.com")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
            print(f"The time is {strTime}")

        elif "global average price of big mac" in query:
            price_history = dict(data.groupby('date')['dollar_price'].mean())

            fig, ax = plt.subplots(figsize=(25, 13), facecolor="white")
            plt.plot(price_history.keys(), price_history.values(), lw=10, color='#FFE68A')
            plt.scatter(x=price_history.keys(), y=price_history.values(), s=400, color='#FFE68A')
            ax.axhspan(ymin=3.0, ymax=3.25, fc='#FA6A5E', alpha=0.8)
            ax.text(s="The global average price of Big Mac. (Dollar) ", x=2016, y=3.1, font=font, fontsize=50,
                    color='white', va='center', ha='center')
            ax.axis('off')
            ax.set_ylim(3., 4)

            for_text = price_history.items()
            for year, value in for_text:
                plt.text(s=f"{round(value, 1)}", x=year + 0.05, y=value + 0.02, font=font, color='#FA6A5E', fontsize=20)
                plt.text(s=year, x=year, y=3.25, font=font, color='#FA6A5E', fontsize=30, va='bottom', ha='center')
                plt.text(s=year, x=year, y=3.25, font=font, color='#FA6A5E', fontsize=30, va='bottom', ha='center')
                plt.axvline(x=year, ymin=1.3 / 4, ymax=(value - 3), color='#FFE68A', linestyle='--', linewidth=3)

            plt.show()

        elif "is big mac's price and gdp related?" in query:
            data_2021 = data[data['date'] == 2021]
            data_2021 = data_2021.copy()
            data_2021['group'] = data_2021['GDP_dollar'].apply(lambda x: int(x // 10000))
            average = data_2021.groupby('group').mean()
            fig, ax = plt.subplots(figsize=(20, 13), facecolor="white")
            plt.scatter(x=average['GDP_dollar'], y=average['dollar_price'], s=1200, alpha=0.8, color='#FA6A5E')
            plt.scatter(x=data_2021['GDP_dollar'], y=data_2021['dollar_price'], s=100, color='#FFE68A')

            for i in range(9):
                ax.axvline(x=(i + 1) * 10000, color='#FA6A5E', linestyle='--', linewidth=1, alpha=0.5)
                ax.text(s=f"{(i + 1) * 10000}", x=(i + 1) * 10000, y=1.75, color='#FA6A5E', ha='center', va='top',
                        fontsize=20, font=font)

            for i in range(2, 8):
                #     ax.axhline(y=i, color='#FA6A5E', linestyle='--', linewidth=1)
                ax.text(s=f"{i} dollar", x=-1000, y=i, color='#FA6A5E', ha='right', va='center', fontsize=20, font=font)

            ax.set_xlim(0, 90000)

            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)

            ax.spines['bottom'].set_color('#FA6A5E')
            ax.spines['left'].set_color('#FA6A5E')

            ax.set_xticks([])
            ax.set_yticks([])

            plt.text(s="The relationship between GDP(per Capita) and Big Mac prices.", x=0, y=7.8, font=font,
                     fontsize=30)

            plt.show()

        elif "which country is the most expensive and which country is the cheapest?" in query:
            data_2021 = data[data['date'] == 2021]
            data_2021 = data_2021.copy()
            data_2021['group'] = data_2021['GDP_dollar'].apply(lambda x: int(x // 10000))
            average = data_2021.groupby('group').mean()

            sort_price = data_2021.sort_values(by='dollar_price')
            high = sort_price.tail(4)
            low = sort_price.head(4)

            fig, ax = plt.subplots(figsize=(20, 13), facecolor="white")

            plt.bar(x=[*range(10, 6, -1)], height=low['dollar_price'], color='#FFE68A')
            plt.scatter([5, 5.5, 6], y=[3] * 3, s=400, color='#FFE68A')
            plt.bar(x=[*range(4, 0, -1)], height=high['dollar_price'], color='#FFE68A')

            for i, value in enumerate(zip(high['dollar_price'], high['name'])):
                plt.text(s=f"{round(value[0], 2)} dollar", x=(4 - i), y=value[0], va='bottom', ha='center', font=font,
                         fontsize=15)
                plt.text(s=f"{value[1]}", x=(4 - i), y=value[0] + 0.3, va='bottom', ha='center', font=font, fontsize=20)

            for i, value in enumerate(zip(low['dollar_price'], low['name'])):
                plt.text(s=f"{round(value[0], 2)} dollar", x=(10 - i), y=value[0], va='bottom', ha='center', font=font,
                         fontsize=15)
                plt.text(s=f"{value[1]}", x=(10 - i), y=value[0] + 0.3, va='bottom', ha='center', font=font,
                         fontsize=20)

            ax.axhspan(ymin=8.5, ymax=10, fc='#FA6A5E', alpha=0.8)
            ax.text(s="Top 4 countries where Big Mac is the cheapest and most expensive.", x=0.5, y=9.2, font=font,
                    fontsize=30, color='white', va='center', ha='left')

            plt.axis("off")

            plt.ylim(0, 10)
            plt.show()

        elif "history of big mac price in switzerland, russia" in query:
            swit = data[data['name'] == 'Switzerland']
            swit = swit.copy()
            swit['ad_loc'] = swit['local_price'].apply(lambda x: x / 6.5)
            swit['ad_dol'] = swit['dollar_price'].apply(lambda x: x / 8.063016)

            rus = data[data['name'] == 'Russia']
            rus = rus.copy()
            rus['ad_loc'] = rus['local_price'].apply(lambda x: x / 75)
            rus['ad_dol'] = rus['dollar_price'].apply(lambda x: x / 2.702459)

            fig, ax = plt.subplots(figsize=(12, 10), facecolor="white")
            spec = gridspec.GridSpec(ncols=1, nrows=19, figure=fig)

            spec = gridspec.GridSpec(ncols=1, nrows=19, figure=fig)
            ax1 = fig.add_subplot(spec[:9, 0])
            ax2 = fig.add_subplot(spec[10:, 0])

            ax1.plot(swit['date'], swit['ad_dol'], lw=5, color='#FFE68A')
            ax1.scatter(swit['date'], swit['ad_dol'], s=200, color='#FFE68A')
            ax1.plot(swit['date'], swit['ad_loc'], lw=5, color='#FA6A5E')
            ax1.scatter(swit['date'], swit['ad_loc'], s=200, color='#FA6A5E')

            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)

            ax1.set_xticks([])
            ax1.set_yticks([])

            for i in swit['date']:
                ax1.text(s=i, x=i, y=0.8, font=font, fontsize=20, va='top', ha='center')
                ax2.text(s=i, x=i, y=0.54, font=font, fontsize=20, va='top', ha='center')

            for i, value in enumerate(zip(swit['date'], swit['local_price'], swit['ad_loc'])):
                ax1.text(s=f"{value[1]}", x=value[0], y=value[2] + 0.01, font=font, fontsize=30, va='bottom',
                         ha='center', color='#FA6A5E')

            for i, value in enumerate(zip(swit['date'], swit['dollar_price'], swit['ad_dol'])):
                if i == 0:
                    continue
                ax1.text(s=f"{round(value[1], 1)} dollar", x=value[0], y=value[2] + 0.01, font=font, fontsize=20,
                         va='bottom', ha='center', color='#FFE68A')

            for i in range(-4, 1):
                ax1.text(s=f"{round((i * 0.05) * 100)} %", x=2010.3, y=1 + i * 0.05, font=font, fontsize=20,
                         va='center', ha='center')

            ax2.plot(rus['date'], rus['ad_dol'], lw=5, color='#FFE68A')
            ax2.scatter(rus['date'], rus['ad_dol'], s=200, color='#FFE68A')
            ax2.plot(rus['date'], rus['ad_loc'], lw=5, color='#FA6A5E')
            ax2.scatter(rus['date'], rus['ad_loc'], s=200, color='#FA6A5E')

            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)

            for i in range(-2, 6):
                ax2.text(s=f"{round((i * 0.2) * 100)} %", x=2010.3, y=1 + i * 0.2, font=font, fontsize=20, va='center',
                         ha='center')

            for i, value in enumerate(zip(rus['date'], rus['local_price'], rus['ad_loc'])):
                ax2.text(s=f"{round(value[1])}", x=value[0], y=value[2] + 0.01, font=font, fontsize=30, va='bottom',
                         ha='center', color='#FA6A5E')

            for i, value in enumerate(zip(rus['date'], rus['dollar_price'], rus['ad_dol'])):
                if i < 3:
                    continue
                ax2.text(s=f"{round(value[1], 1)} dollar", x=value[0], y=value[2] + 0.05, font=font, fontsize=20,
                         va='bottom', ha='center', color='#FFE68A')

            ax2.set_xticks([])
            ax2.set_yticks([])

            ax1.text(s="Switzerland (The most expensive)", x=2011, y=1.05, font=font, fontsize=20)
            ax1.text(s="Local price", x=2019, y=1.05, font=font, fontsize=20, color='#FA6A5E')

            ax2.text(s="Russia (The Cheapest)", x=2011, y=2, font=font, fontsize=20)
            ax2.text(s="Local price", x=2019, y=1.4, font=font, fontsize=20, color='#FA6A5E')

            ax.axis('off')
            plt.show()
        elif "current price of big mac" in query:
            data_2021 = data[data['date'] == 2021]
            print("Current price of Big Mac all over the world:")
            speak("Current price of Big Mac all over the world:")
            print(data_2021)

        elif "history of big mac price in india" in query:
            ind = data[data['name'] == 'India']
            print(ind)

        elif "history of big mac price in usa" in query:
            usa = data[data['name'] == 'United States']
            print(usa)

        elif "history of big mac price in south korea" in query:
            sk = data[data['name'] == 'South Korea']
            print(sk)

        elif "history of big mac price in europe" in query:
            ea = data[data['name'] == 'Euro area']
            print(ea)

        elif "history of big mac price in china" in query:
            ch = data[data['name'] == 'China']
            print(ch)

        elif "exit" in query:
            speak("Good bye. Have a nice day.")
            print("Good bye. Have a nice day.")
            break

        else:
            speak('We will send your query to our voice analyst and he or she will be contacting you shortly.')
            speak('Please enter your mail and phone number for contact.')
            print("We will send your query to our voice analyst and he or she will be contacting you shortly.")
            mailid = input("Enter your mail: ")
            phno = input("Enter your phone number: ")
