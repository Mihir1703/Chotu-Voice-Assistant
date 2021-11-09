import json  # for handling json data
import webbrowser  # open webpages on default browser
import pyttsx3  # python text to speech module
import datetime  # python datetime module
import speech_recognition as s  # google speech_recognition library
import requests  # This handles API requests
from utils.location import get_location  # importing location function from utils.location folder
import wikipedia  # Wikipedia module to find search results
from utils.spotifyAPI import play_sound  # importing sound playing function from utils.spotifyAPI folder
import os  # importing operating system modules
from googlesearch import search  # google search module provides relevant url using keywords
import mysql.connector  # connector for MySQL database
import time  # python time module

# python text to speech with inbuilt windows voices using Microsoft Speech api v5 (sapi5)
speak_engine = pyttsx3.init('sapi5')
# getting all voices present in windows machine as voices
voices = speak_engine.getProperty('voices')
# setting voice to particular sound as desired
speak_engine.setProperty('voice', voices[1].id)

# loading credentials from db.json file 
credentials = json.load(open('db.json'))
#  login credentials for MySQL database(this connects to database)
database = mysql.connector.connect(host=credentials['host'], user=credentials['user'], password=credentials['password'],database=credentials['database'])
#  name of table where data is stored
table_name = credentials['table']

# middleware function for handling all the queries in sql database
mycursor = database.cursor()


# Speak function for python to speak something
def speak(audio):
    # speaks the string audio
    speak_engine.say(audio)
    # runs and waits
    speak_engine.runAndWait()


# Wish me first
def wish_me():
    # first getting time
    hour = int(datetime.datetime.now().hour)
    # if time between 0 to 12 say Good Morning
    if 0 <= hour < 12:
        speak("Good Morning Bro")
    # if time between 12 to 18 say Good Afternoon
    elif 12 <= hour <= 18:
        speak("Good Afternoon Bro")
    # else say Good Evening
    else:
        speak("Good Evening Bro")
    speak("Tell me what i can do for you")


# End wish
def end_wish():
    hour = int(datetime.datetime.now().hour)
    # if night time say Good Night
    if 18 < hour < 24:
        speak("Good Night!!")
    # else say this
    else:
        speak("Have a nice day, bro")
    speak("Thank you for using me, see you soon")


# Get temperature
def get_temperature():
    global temp
    # search query and getting current location
    search = f'{get_location()}'
    # api key for authentication
    apikey = 'd6d1d3412b24cff7c6489a1447771f01'
    # getting url for requesting temperature
    url = 'https://api.openweathermap.org/data/2.5/weather'
    url = f'{url}?q={search}&appid={apikey}&units=metric'
    # get request to url
    response = requests.get(url)
    # extracting response from API
    x = response.json()
    # extracting temperature from data
    if x["cod"] != "404":
        y = x["main"]
        temp = y["temp"]
    # if 404( not found ) status code speak error
    else:
        speak("We got some error from server")
        return
    speak(f'current temperature in {search} is {temp} degree Celsius')


# Take command in form of voices and return back a string 
def get_command():
    # initialising speech recogniser
    listeners = s.Recognizer()
    # activating microphone as source
    with s.Microphone() as source:
        # adjusting noise level and sensitivity of microphone to recognize voice in noisy atmosphere
        listeners.adjust_for_ambient_noise(source)
        # listening to query made by user
        audio = listeners.listen(source)
        # if any error return None
        try:
            # get text from speech using google
            source_data = listeners.recognize_google(audio)
            # to lowercase
            lower_query = str(source_data).lower()
            # return query
            return lower_query
        except Exception as e:
            # if exception print it
            print(e)
            # if spoken nothing return none
            return None


# getting a non empty command from user
def get_not_empty_command():
    message = get_command()
    # while message is null retake input
    while message is None or message == '':
        message = get_command()
    # if message becomes not null return
    print(message)
    return message


# wikipedia search function using wikipedia module and speak first result 
def search_wiki():
    global result
    speak("What would you like to search")
    # getting query to search
    search = get_not_empty_command()
    # searching query via wikipedia module
    try:
        # if there is any error while processing use except block commands
        try:
            # getting data for keyword
            result = wikipedia.summary(search, sentences=5)
        # if multiple results found show the first one
        except wikipedia.DisambiguationError as e:
            result = wikipedia.summary(e.options[0], sentences=5)
        # providing information to user
        speak(f"According to wikipedia ,{result}")
        # wait for some time 
        time.sleep(0.5)
        speak(f"that's all about it.")
    except Exception as e:
        print(e)
        # if error occurs not to exit program and say error occur to user
        speak("Sorry, we got some error from the server")


# playing music from spotify using spotifyAPI module 
def play_music(query):
    # choice of user music
    choice = query.find('play music') + len('play music')
    #  getting song name
    song = query[choice::]  # (choice :: ) stores string from choice up to end
    # by chance if spotify api gives error we would prefer saying error occur besides exiting unusually
    try:
        # this function enables us to play sound
        play_sound(song)
        return
    except Exception as e:
        print(e)
        # if error occurs not to exit program and say error occur to user
        speak("Sorry, we got some error from the server")


# opening application in windows using windows shell commands 
def open_app(query):
    index = query.find('application') + len('application')
    # getting application name from query
    search = query[index::]
    if 'notepad' in search:  # if keyword exists in search run the command block
        speak('Opening Notepad')
        path = 'C:\\Windows\\system32\\notepad'
        # this will open the command line internally and process the path to start application
        os.startfile(path)
    elif 'command prompt' in search:
        speak('Opening command prompt')
        path = 'C:\\Windows\\system32\\cmd'
        os.startfile(path)
    elif 'calculator' in search:
        speak("Opening calculator")
        path = "C:\\Windows\\system32\\calc"
        os.startfile(path)
    elif 'word' in search:
        speak("Opening microsoft word")
        path = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Word.lnk"
        os.startfile(path)
    elif 'powerpoint' in search:
        speak("Opening microsoft powerpoint")
        path = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Powerpoint.lnk"
        os.startfile(path)
    elif 'excel' in search:
        speak("Opening microsoft excel")
        path = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Excel.lnk"
        os.startfile(path)
    elif 'onenote' in search:
        speak("Opening microsoft onenote")
        path = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\OneNote.lnk"
        os.startfile(path)
    elif 'chrome' in search:
        speak("Opening Google chrome")
        path = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Google Chrome.lnk"
        os.startfile(path)
    elif 'edge' in search:
        speak("Opening microsoft edge")
        path = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Edge.lnk"
        os.startfile(path)
    elif 'teams' in search:
        speak("Opening microsoft teams")
        path = "C:\\Users\\Administrator\\Desktop\\Microsoft Teams.lnk"
        os.startfile(path)
    elif 'yahoo mail' in search:
        speak("Opening yahoo mail")
        path = "C:\\Users\\Administrator\\Desktop\\Yahoo Mail.lnk"
        os.startfile(path)
    elif 'game' in search:
        speak("Opening Smash Karts")
        path = "C:\\Users\\Administrator\\Desktop\\Smash Karts.lnk"
        os.startfile(path)
    else:
        speak("Sorry sir, I couldn't find the application")


# search for a query in google and open first result in browser using webbrowser module
def open_web(query):
    # extracting query from user input and storing it in to_search variable
    index = query.find('open')
    index = index + len('open')
    # getting search keyword from query string
    to_search = query[index::]
    # search function from google search module provides us number of url and we are going to open the 1st one and
    # open function opens url in default browser
    try:
        # if there is any error while processing use except block commands
        webbrowser.open(search(to_search)[0])
    except:
        # if error occurs say user an error occurred
        speak("Please provide me a correct command, Bro")


# this helps in adding assignments record to MySQL database
def assign_rec():
    speak('please tell the subject name.')
    sub = get_not_empty_command()
    speak('after how many days do you have to submit it.')
    #  getting interval in integer
    interval = get_not_empty_command()
    #  getting today's date in specified format
    dt = datetime.date.today().strftime('''%Y-%m-%d''')
    # if database connection fails or interval is a string then error will be handled
    try:
        #  to deal with negative values
        if int(interval) < 0:
            speak("Negative values not allowed!!")
            return
        # executing following query on SQl
        mycursor.execute(f'insert into {table_name} values("{sub}",DATE_ADD("{dt}", INTERVAL {int(interval)} DAY))')
        # commit the changes to the MySQL
        database.commit()
        speak('your assignment is added successfully')
    except:
        speak("Some error occurred, please try again")


#  function to show assignments from database
def show_assign():
    #  getting today's date in specified format
    dt = datetime.date.today().strftime('''%Y-%m-%d''')
    # executing following query on SQl to retrieve pending assignments with submission in 7 days
    mycursor.execute(f'select subject from {table_name} where last_date between Date(now()) and Date_ADD(Date(now()), '
                     f'Interval 7 Day)')
    # declaring list to store pending assignments
    arr = []
    # storing data into list
    for i in mycursor:
        arr.append(i[0])
    # if no assignments pending say this
    if len(arr) == 0:
        speak("You have done all assignments now it's time to enjoy")
        return
    # converting list into a dictionary so that there should be no duplicate entry and duplicate entry would be
    # incremented in count
    data = {i: arr.count(i) for i in arr}
    speak("These are your pending assignments")
    # speak out all assignments pending
    for i in data:
        speak(f'{data[i]} {i} assignment')
        # wait for 0.5 seconds for better hearing
        time.sleep(0.5)


# if function is main run the following lines of code
if __name__ == "__main__":
    # wishing the user
    wish_me()
    when_to_close = True
    # if user said exit we will exit
    while when_to_close:
        query = get_not_empty_command()
        if 'thank you' in query:
            speak("Pleasure to help you bro")
            continue
        if 'chhotu' not in query:
            if 'chotu' not in query:
                continue
        # searching wikipedia
        if 'wikipedia' in query:
            search_wiki()
        # used this just for fun
        elif 'how are you' in query:
            speak("I am fine Bro, hope same for you")
        # to know temperature
        elif "today's temperature" in query:
            get_temperature()
        # for playing sound
        elif 'play music' in query:
            play_music(query)
        # to add assignments
        elif 'add assignment' in query:
            assign_rec()
        # to know pending assignments
        elif 'pending assignment' in query:
            show_assign()
        # opening application
        elif 'application' in query:
            open_app(query)
        # open websites
        elif 'open' in query:
            open_web(query)
        # exit program
        elif 'exit' in query:
            when_to_close = False
    # wish user good night if it is night else good day
    end_wish()
