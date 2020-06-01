


import os
import pydub


for wav in os.listdir("dataset/wavs/macro-output"):
    print(wav)
    audio = pydub.AudioSegment.from_wav("dataset/wavs/macro-output/" + wav)

    audio = audio.set_frame_rate(22050)  # sample rate used in the lj dataset
    audio = audio.set_channels(1)  # stereo to mono conversion

    audio.export("dataset/temp/" + wav, format="wav")

'''



import youtube_dl

ydl_opts = {'noplaylist' : True,
                'outtmpl': 'tempaudio/%(id)s.%(ext)s'}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:

    url = "https://www.youtube.com/watch?v="
    info = ydl.extract_info(url+"qy6bHvHooQc", download=False)

    ydl.list_formats(info)
'''