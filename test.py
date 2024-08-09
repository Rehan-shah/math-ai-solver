from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, CompositeAudioClip, ColorClip, AudioClip
import os

def create_video_with_voiceover(video_path, audio_path):

# Usage
result = create_video_with_voiceover("./media/videos/scene/1080p60/S1S.mp4", "./voiceover.mp3")
print(result)
