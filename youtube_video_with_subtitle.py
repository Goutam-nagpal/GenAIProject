from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_url):
    # Extract the video ID from the YouTube URL
    if 'youtu.be' in video_url:
        video_id = video_url.split('/')[-1]
    else:
      video_id = video_url.split("v=")[1]
    print(video_id)
    
    # Retrieve transcript using the YouTubeTranscriptApi
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    
    # Formatting the transcript into a readable form
    transcript_text = " ".join([item['text'] for item in transcript])
    
    return transcript_text


# # Example usage
# video_url = 'https://youtu.be/6v8djXa-IPQ?si=wc-TX8UAiRLZs51i'
# transcript = get_transcript(video_url)
# print(transcript)