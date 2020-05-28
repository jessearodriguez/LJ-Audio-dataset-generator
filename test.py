import os
import pydub


for wav in os.listdir("dataset/wavs"):
    print(wav)
    audio = pydub.AudioSegment.from_wav("dataset/wavs/" + wav)

    audio = audio.set_frame_rate(22050)  # sample rate used in the lj dataset
    audio = audio.set_channels(1)  # stereo to mono conversion

    audio.export("dataset/temp/" + wav, format="wav")
