from youtube_transcript_api import YouTubeTranscriptApi

import pydub

import youtube_dl
import os
import subprocess

import num2words

def textnum2str(text):

    strarr = text.split()
    for i in range(len(strarr)):
        if is_number(strarr[i]):
            strarr[i] = num2words.num2words(strarr[i])


    formatted = ""
    for str in strarr:
        formatted = formatted + str + " "

    return formatted

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

url = "https://www.youtube.com/watch?v="
ids = []

text = ""
while text != "done":
    text = input("enter video id; type \"done\" to move on")
    if text != "done":
        ids.append(text)

print("%d videos loaded" % len(ids))

for id in ids:
    print(id + "\n")



f = open("dataset/" + "metadata" + ".csv", "w", encoding="utf-8")

videonum = 1
textid = 1
for id in ids:
    transcript = YouTubeTranscriptApi.get_transcript(id)


    ydl_opts = {'noplaylist' : True,
                'format' : 'bestaudio/best',
                'outtmpl': 'tempaudio/%(id)s.%(ext)s'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:


        #info = ydl.extract_info(url+id, download=False)

        #ydl.list_formats(info)

        ydl.download([url + id])

    filename = "tempaudio/" + id + ".webm"
    newfile = "tempaudio/" + id + ".wav"

    subprocess.run(
        (['ffmpeg', '-y', '-i', filename, newfile]))

    os.remove(filename)

    audio = pydub.AudioSegment.from_wav(newfile)

    lastitem = False
    for i in range(len(transcript)):

        item = transcript[i]

        futureitem = item




        if i != len(transcript)-1:
            futureitem = transcript[i+1]
        else:
            lastitem = True


        id_tag = "video-" + str(videonum) + "-" + str(textid)

        if len(item['text']) > 20:
            start = int(item['start']*1000) #converting to milliseconds

            if lastitem:
                end = start + int(futureitem['duration'] * 1000)
            else:
                end = int(futureitem['start'] * 1000 + 400)


            audioselection = audio[start:end]

            audioselection.export("dataset/wavs/"+ id_tag+".wav", format="wav")

            formattedtext = textnum2str(item['text'])

            linewrite = id_tag + "|" + formattedtext + "|" + formattedtext + "\n"

            f.write(linewrite)

            textid += 1

    os.remove(newfile)
    videonum += 1
    textid = 1



f.close()


