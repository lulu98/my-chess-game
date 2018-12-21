import speech_recognition as sr

#issue: if you say a number which is bigger than 10 than it will only check single digit at once
def get_row_col(voice_input):
    row = None
    col = None
    for i in voice_input:
        i = i.lower()
        if ("eins" in voice_input.lower()):
            row = 7
        elif ("zwei" in voice_input.lower()):
            row = 6
        elif ("drei" in voice_input.lower()):
            row = 5
        elif ("vier" in voice_input.lower()):
            row = 4
        elif ("fünf" in voice_input.lower()):
            row = 3
        elif ("sechs" in voice_input.lower() or "sex" in voice_input.lower()):
            row = 2
        elif ("sieben" in voice_input.lower()):
            row = 1
        elif ("acht" in voice_input.lower()):
            row = 0
        if (i == '1' or i == '2' or i == '3' or i == '4' or i == '5' or i == '6' or i == '7' or i == '8'):
            if(row == None):
                row = 8-int(i)
        if(i == 'a' or i == 'b' or i == 'c' or i == 'd' or i == 'e' or i == 'f' or i == 'g' or i == 'h'):
            if(col == None):
                col = ord(i)-97
    return row,col

def get_position():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # Speech recognition using Google Speech Recognition
    try:
        text = r.recognize_google(audio, language="de-DE")
        print("You said: " + text)
        return get_row_col(text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None,None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

#print(get_position())