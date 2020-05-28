from youtube_transcript_api import YouTubeTranscriptApi

import pydub

import youtube_dl
import os
import subprocess

import num2words
import random


def textnum2str(text): # converts a sentence containing numbers to a sentence with those numbers converted to strings

    strarr = text.split()
    for i in range(len(strarr)):
        if is_number(strarr[i]):
            strarr[i] = num2words.num2words(strarr[i])


    formatted = ""
    for str in strarr:
        formatted = formatted + str + " "

    return formatted


def is_number(s): # determines if input is a number or not
    try:
        float(s)
        return True
    except ValueError:
        return False


def randomConcat(transcript):  # randomly concatenates the transcript and returns it in a similar format
    newtranscript = []


    newitem = {}
    i = 0
    while i < len(transcript):

        concated = False

        if len(transcript[i]['text']) > 15: #check if the sentence meets minimum length requirements, useful to filter out "[music]" type subtittles

            if i == len(transcript) - 1: #is the last item in the list
                newitem = transcript[i]
                i += 1

            else: # there's probably a cleaner way to do this

                try: # to catch the last few index out of bounds errors from trying to access i+x approaching towards the end of the list

                    if random.random() < 0.75: #1 random chance concatination

                        if random.random() < 0.5:#2 random chance concationation

                            if random.random() < 0.5:#3 random concatination
                                j = 0
                                newtext = ""
                                start =transcript[i]['start']
                                duration = transcript[i]['duration']
                                while j < 3:

                                    if len(transcript[i]['text']) > 15:
                                        newtext += transcript[i]['text'] + " "
                                        j += 1
                                    i += 1



                                newitem = {
                                    "text": newtext,
                                    "start": start,
                                    "duration": duration,
                                    }
                                concated = True

                            if not concated:
                                j = 0
                                newtext = ""
                                start = transcript[i]['start']
                                duration = transcript[i]['duration']
                                while j < 2:

                                    if len(transcript[i]['text']) > 15:
                                        newtext += transcript[i]['text'] + " "
                                        j += 1
                                    i += 1

                                newitem = {
                                    "text": newtext,
                                    "start": start,
                                    "duration": duration,
                                }
                                concated = True
                        if not concated:
                            j = 0
                            newtext = ""
                            start = transcript[i]['start']
                            duration = transcript[i]['duration']
                            while j < 1:

                                if len(transcript[i]['text']) > 15:
                                    newtext += transcript[i]['text'] + " "
                                    j += 1
                                i += 1

                            newitem = {
                                "text": newtext,
                                "start": start,
                                "duration": duration,
                            }
                            concated = True

                    else:
                        newitem = transcript[i]
                        i += 1

                except IndexError:
                    try:
                        newitem = transcript[i]
                        i += 1
                    except:
                        pass



            newtranscript.append(newitem)
        else:
            i += 1


    return newtranscript


url = "https://www.youtube.com/watch?v="
ids = []

text = ""

while text != "done": # loop to get all video ids
    text = input("enter video id; type \"done\" to move on")
    if text != "done":
        ids.append(text)

print("%d videos loaded" % len(ids))

for id in ids:
    print(id + "\n")



f = open("dataset/" + "metadata" + ".csv", "w", encoding="utf-8") #create the metadata cvs file for the dataset

videonum = 1
textid = 1
for id in ids:

    transcript = YouTubeTranscriptApi.get_transcript(id) #get the video transcript

    transcript = randomConcat(transcript)

    ydl_opts = {'noplaylist' : True,
                'format' : 'bestaudio/best',
                'outtmpl': 'tempaudio/%(id)s.%(ext)s'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:


        #info = ydl.extract_info(url+id, download=False)

        #ydl.list_formats(info)

        ydl.download([url + id]) #downloads video audio as a webm

    filename = "tempaudio/" + id + ".webm"
    newfile = "tempaudio/" + id + ".wav"

    subprocess.run( #converts the webm to wav using ffmpeg
        (['ffmpeg', '-y', '-i', filename, newfile]))

    os.remove(filename)




    audio = pydub.AudioSegment.from_wav(newfile)

    audio = audio.set_frame_rate(22050) #sample rate used in the lj dataset
    audio = audio.set_channels(1) #stereo to mono conversion

    lastitem = False

    for i in range(len(transcript)): #generates audio splices based off of transcript start times

        if i > len(transcript)-3: #stops the inclusion of the last 3 lines (these tend to be broken from youtube transcripts)
            continue
        item = transcript[i]

        futureitem = item




        if i != len(transcript)-1:
            futureitem = transcript[i+1]
        else:
            lastitem = True


        id_tag = "video-" + str(videonum) + "-" + str(textid)

        if len(item['text']) > 20:
            start = int(item['start']*1000+ 150) #converting to milliseconds
            #the addition of 150 ms and 300 ms helps out the time youtube's transcripts to a more correct value
            if lastitem:
                end = start + int(futureitem['duration'] * 1000 )
            else:
                end = int(futureitem['start'] * 1000 + 300)


            audioselection = audio[start:end]

            audioselection.export("dataset/wavs/"+ id_tag+".wav", format="wav")

            formattedtext = textnum2str(item['text'])

            linewrite = id_tag + "|" + item['text'] + "|" + formattedtext + "\n"

            f.write(linewrite)

            textid += 1

    os.remove(newfile)
    videonum += 1
    textid = 1



f.close()


