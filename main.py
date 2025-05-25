import random
import datetime
import webbrowser
import pyttsx3
import wikipedia
from pygame import mixer
import speech_recognition as sr
import pyaudio
import streamlit as st
import threading
import requests
from bs4 import BeautifulSoup
import subprocess

from google_images_search import GoogleImagesSearch


import streamlit as st

# Load custom CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Create a sidebar for instructions
st.sidebar.title("Instructions For AuroraSphere")
st.sidebar.markdown("1. voice commands to control web sites.")
st.sidebar.markdown("(Open)browser, Spotify, Instagram,Youtube")
st.sidebar.markdown("2. Search somthing over youtube")
# st.sidebar.markdown("   Play Music")
st.sidebar.markdown("3. to check current time, say 'time' or 'what is the time?' ")
st.sidebar.markdown("4. To search for images, say 'show me images of [your query].'")
st.sidebar.markdown("5. Topic name to get information from Wikipedia")
st.sidebar.markdown("6. Check temperature")
st.sidebar.markdown("7. Top 5 news of india, say 'news'")

# st.sidebar.markdown("6. To open translator say (Majestic Translator)")
# Add more instructions and explanations as needed

# Main content in the main section
st.title('AuroraSphere')
mixer.init()
# Add your main content and functionality here

# Rest of your code


mixer.init()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
volume = engine.getProperty('volume')
engine.setProperty('volume', 10.0)
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 30)

x = 0

greetings = ['hey there', 'hello', 'hi', 'Hai', 'hey!', 'hey']
question = ['how are you', 'how are you doing']
responses = ['Okay', "I'm fine"]
var1 = ['who made you', 'who created you']
var2 = ['I was created by Ridhimaa Thakur, Abhinav Prashar and Deesha Devi right in this computer.', 'Ridhimaa Thakur']
var3 = ['what time is it', 'what is the time', 'time']
var4 = ['who are you', 'what is your name']
cmd1 = ['open browser', 'open google']
cmd2 = ['play music', 'play songs', 'play a song', 'open music player']
cmd2_1=['song']
cmd3 = ['tell a joke', 'tell me a joke', 'say something funny', 'tell something funny']
jokes = [
    'Can a kangaroo jump higher than a house? Of course, a house doesn’t jump at all.',
    'My dog used to chase people on a bike a lot. It got so bad, finally I had to take his bike away.',
    'Doctor: I\'m sorry but you suffer from a terminal illness and have only 10 to live. '
    'Patient: What do you mean, 10? 10 what? Months? Weeks?!" Doctor: Nine.'
] 
cmd4 = ['open youtube', 'I want to watch a video']
cmd5 = ['wikipedia', 'open wikipedia']
cmd6 = ['exit', 'shut up', 'close', 'goodbye', 'nothing']
cmd7 = ['what is your color', 'what is your colour', 'your color', 'your color?']
colrep = ['Right now it\'s rainbow', 'Right now it\'s transparent', 'Right now it\'s non-chromatic']
cmd8 = ['what is your favorite color', 'what is your favourite color']
cmd9 = ['thank you']
cmd10 = ['spotify', 'open spotify']
cmd11 = ['open instagram', 'instagram']
news = ['news']
cmd12 = ['temperature', 'current temperature','What is the temprature','what is the current temprature']

repfr9 = ['you\'re welcome', 'glad I could help you']

songs = [
    # 'C:/Users/HP/Desktop/projects/Neew/Keane_-_Somewhere_Only_We_Know_(Jesusful.com).wav',
    # 'C:/Users/HP/Desktop/Magestic Bot/Keane_-_Somewhere_Only_We_Know_(Jesusful.com).wav'
    'C:/Users/HP/Desktop/VVA/Keane_-_Somewhere_Only_We_Know_(Jesusful.com).wav'
    # 'C:/Users/HP/Desktop/projects/Neew/SALES_-_Pope_Is_a_Rockstar.wav',
    # 'C:/Users/HP/Desktop/projects/Neew/Olivia_Rodrigo_-_Drivers_License.wav',
    # 'C:/Users/HP/Desktop/projects/Neew/Sean Kingston  Justin Bieber - Eenie Meenie(audiosong.in).wav',
    # 'C:/Users/HP/Desktop/projects/Neew/Tattoo.wav'
]

song_played = False  # Flag to track if the song has been played

engine_loop_running = False
prev_recognized_text = ""
engine_lock = threading.Lock()

def open_new_script():
    try:
        # Replace 'new.py' with the actual path to your 'n.py' script
        subprocess.Popen(['streamlit', 'run', 'Translator.py'])
        say_response("Opening the new application.")
    except Exception as e:
        say_response(f"An error occurred while opening the new application: {str(e)}")

def say_response(response):
    global engine_loop_running
    with engine_lock:
        if not engine_loop_running:
            engine_loop_running = True
            engine.say(response)
            st.write(response)
            engine.runAndWait()
            engine_loop_running = False

def process_voice_input():
    global song_played
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Tell me something:")
        audio = r.listen(source)
        try:
            recognized_results = r.recognize_google(audio, show_all=True)
            if "alternative" in recognized_results:
                recognized_text = recognized_results["alternative"][0]["transcript"].lower()
            else:
                recognized_text = ""
            st.write("You said: " + recognized_text)
            return recognized_text
        except sr.UnknownValueError:
            st.write("Could not understand audio")
            return ""


# def get_youtube_search_results(search_url):
#     response = requests.get(search_url)
#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     video_links = []
    
#     for link in soup.find_all('a'):
#         href = link.get('href')
#         if href.startswith('/watch?'):
#             video_url = f'https://www.youtube.com{href}'
#             video_links.append(video_url)
    
#     return video_links


gis = GoogleImagesSearch('AIzaSyCATlRGShMUTYJJW6KD6qjuALZymRc5uOA', 'e5d0164a5984e4116')

# ... (Your other code)

# Function to search for images on Google and display them
def show_images_of(query):
    try:
        # Perform an image search on Google
        gis.search({'q': query, 'num': 5})

        # Display the images in your Streamlit app side by side
        if gis.results():
            st.write("<div style='display: flex; flex-wrap: wrap; justify-content: center;'>", unsafe_allow_html=True)
            for index, image in enumerate(gis.results()):
                st.image(image.url, caption=f"Image {index + 1}", width=200)  # Adjust the width as needed
            st.write("</div>", unsafe_allow_html=True)
        else:
            say_response("Sorry, I couldn't find any images for that query.")
    except Exception as e:
        # Log the error and report it to the user
        st.write(f"An error occurred while fetching images: {str(e)}")
        say_response(f"An error occurred while fetching images: {str(e)}")






def get_top_news(api_key):
    try:
        # Specify the News API endpoint and parameters
        news_url = f'https://newsapi.org/v2/top-headlines'
        params = {
            'apiKey': api_key,
            'country': 'us',  # You can change the country code as needed
            'pageSize': 5  # Fetch the top 5 headlines
        }

        # Send a GET request to the News API
        response = requests.get(news_url, params=params)
        data = response.json()

        if 'articles' in data:
            articles = data['articles']
            headlines = [article['title'] for article in articles]
            return headlines
        else:
            return ["No news headlines available."]

    except Exception as e:
        return [f"An error occurred while fetching news headlines: {str(e)}"]
# ... (Your other code)

# Initialize your text-to-speech engine and other settings here

# Replace 'YOUR_NEWS_API_KEY' with your actual News API key
news_api_key = '92de0d07895d447681dfee7f9c248772'

searching_youtube = False


while True:
    recognized_text = process_voice_input()

    if not song_played:
        if recognized_text.strip() != "":
            x = 0

    

    if recognized_text in greetings:
        random_greeting = random.choice(greetings)
        say_response(random_greeting)
        print(random_greeting)

    elif recognized_text.startswith("show me images of "):
        query = recognized_text[len("show me images of "):]
        show_images_of(query)

    elif recognized_text in cmd12:
        # Replace 'YOUR_API_KEY' with your actual weather API key
        api_key = 'f2b034a3dfb82f00da103586f91f992e'
        try:
        # Use a geolocation service to obtain your current latitude and longitude
            geolocation_url = 'http://ipinfo.io/json'
            response = requests.get(geolocation_url)
            location_data = response.json()
        
            # Extract the coordinates
            if 'loc' in location_data:
                coordinates = location_data['loc'].split(',')
                latitude, longitude = coordinates
                
                # Use the latitude and longitude to fetch the weather data
                weather_url = f'http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}'
                
                response = requests.get(weather_url)
                data = response.json()

                if data['cod'] == 200:
                    temperature = data['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
                    city = data['name']
                    say_response(f'The current temperature in {city} is approximately {temperature:.2f} degrees Celsius.')
                else:
                    say_response('Sorry, I couldn\'t retrieve the temperature at the moment.')
            else:
                say_response('I couldn\'t determine your current location.')
        except Exception as e:
            say_response(f'An error occurred while fetching the temperature: {str(e)}')

    
    elif recognized_text in question:
        say_response(random.choice(responses))


    elif recognized_text in news:

        news_headlines = get_top_news(news_api_key)
        if news_headlines:
            for index, headline in enumerate(news_headlines):
                say_response(f"News {index + 1}: {headline}")
        else:
            say_response("Sorry, I couldn't fetch any news headlines at the moment.")

    elif recognized_text in var1:
        say_response(random.choice(var2))

    elif recognized_text == 'majestic translator':
        open_new_script()

    elif recognized_text in cmd9:
        say_response(random.choice(repfr9))

    elif recognized_text in cmd7:
        say_response(random.choice(colrep))

    elif recognized_text in cmd8:
        say_response(random.choice(colrep))

    elif recognized_text in cmd2:
        mixer.init()
        x = random.choice(songs)
        mixer.music.load(x)
        mixer.music.play()
        song_played = True
        break

    elif recognized_text in var4:
        say_response('I am a AuroraSphere a Virtual Voice Assistant')

    elif recognized_text in cmd4:
        webbrowser.open('https://www.youtube.com')

        # Set the flag to indicate YouTube search mode
        searching_youtube = True
    
    elif searching_youtube:
    # If the bot is in YouTube search mode, treat recognized text as a search query
    # and perform a search on YouTube
        if recognized_text.strip() != "":
            youtube_search_url = f'https://www.youtube.com/results?search_query={recognized_text}'
            webbrowser.open(youtube_search_url)
            searching_youtube = False
    

    elif recognized_text in cmd11:
        webbrowser.open('www.instagram.com/')

    elif recognized_text in cmd6:
        say_response('Goodbye! See you later.')
        song_played = False
        mixer.music.stop()
        break


    elif recognized_text in cmd5:
        webbrowser.open('www.wikipedia.com')

    elif recognized_text in cmd10:
        webbrowser.open('www.spotify.com')

    elif recognized_text in var3:
        current_time = datetime.datetime.now().strftime("The time is %H:%M")
        say_response("Current time:\n" + current_time)

    elif recognized_text in cmd1:
        webbrowser.open('www.google.com')

    elif recognized_text == "print previous command":
        if prev_recognized_text:
            say_response("Your previous command was: " + prev_recognized_text)
        else:
            say_response("You haven't given any command yet.")
            
    elif recognized_text in cmd3:
        say_response(random.choice(jokes))

    elif x == 0 and recognized_text.strip() != "":
        try:
            search_result = wikipedia.summary(recognized_text, sentences=2)
            say_response("Here is what I found on Wikipedia:\n" + search_result)
        except wikipedia.exceptions.DisambiguationError as e:
            first_suggestion = e.options[0]
            search_result = wikipedia.summary(first_suggestion, sentences=2)
            say_response("Here is what I found on Wikipedia for " + first_suggestion + ":\n" + search_result)
        except wikipedia.exceptions.PageError:
            say_response("I'm sorry, I couldn't find any information on Wikipedia about that topic.")

    else:
        say_response("Sorry, I didn't understand.")

    prev_recognized_text = recognized_text