from youtube_transcript_api import YouTubeTranscriptApi


transcript = YouTubeTranscriptApi.get_transcript("oG2MIqhYYHg")


len(transcript)

for i in range(len(transcript)):
    print(transcript[i])