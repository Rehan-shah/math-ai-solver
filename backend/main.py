import os
from groq import Groq
from fastapi import FastAPI
import uvicorn
import json
from utilits import extract_code, ask_groq, get_video_length
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment
import subprocess
from fastapi.middleware.cors import CORSMiddleware
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, CompositeAudioClip, ColorClip, AudioClip
import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
load_dotenv(Path("./env"))
app = FastAPI()


client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root(problem: str):
    i = 0
    prompt = f"""Create a Manim video of 20 - 30 seconds , not more than that. that answers the following math question:

    Question : {problem}
    The video should:
    Use a copious amount of mathematical symbols.
    Make sure the text is wrapped if it does fit on the screen.
    Clear the board after a few points are made to maintain clarity.
    Contain no images, only text and mathematical symbols.
    THERE SHOULD BE NO OVERLAPPING TEXT OF SYMBOLS thus clear the text perodically .
    REPLY WITH A SINGLE CODE BLOCK
    The name of the scene should be S1S.
    ALSO ADD COLOR 
    answer in a code block starting with ```python
    DO NOT GIVE ANY OTHER CODE BLOCKS EXPECT ONE WITH MANIM CODE 
    """

    try:
        chat_completion = ask_groq(prompt)
        code = extract_code(chat_completion.choices[0].message.content)
        print(chat_completion.choices[0].message.content)
    except Exception as e:
        if i == 0:

            chat_completion = ask_groq(prompt)
            print(chat_completion.choices[0].message.content)
            code = extract_code(chat_completion.choices[0].message.content)
            i += 1
        else:
            return {
                "code": 1,
                "message": str(e)
            }


    with open("./scene.py", "w") as f:
        f.write(code)
    try:
        result = subprocess.run(["manim", "scene.py", "S1S"], capture_output=True, text=True, check=True)
        print("Manim output:", result.stdout)
    except subprocess.CalledProcessError as e:
        code = extract_code(ask_groq(f"""Slove this code error 
                 -----
                 CODE : {code}
                 -----
                 Error : {e.stderr}
                 ----
                 response in python code blocks , single file"""
                 ).choices[0].message.content)



        with open("./scene.py", "w") as f:
            f.write(code)

        result = subprocess.run(["manim", "scene.py", "S1S"], capture_output=True, text=True, check=True)
        print("Manim output:", result.stdout)


    video_path = "./media/videos/scene/1080p60/S1S.mp4"
    clip_duration = get_video_length(video_path)
    print(clip_duration , " seconds" , f"{clip_duration:.2f}")

    
    script_unformated = ask_groq(f"""CODE : {code}
    -------
    This voiceover is to be attached to the clip created from the above Manim code. The script should be concise and fit within {clip_duration:.2f} seconds, which is approximately {(clip_duration/60)*150 - 10} words. 
    Ensure the explanation is brief and directly related to the topic illustrated by the Manim animation.
    Do not start with pleasentaries or greetings.Do not start with here is the script just directly starting with the script.
    """
    )
    script = script_unformated.choices[0].message.content
    print(script)
    # Generate audio using Eleven Labs
    audio_stream = client.text_to_speech.convert(
        voice_id="pMsXgVXv3BLzUgSXRplE",
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=script,
        voice_settings=VoiceSettings(
            stability=0.1,
            similarity_boost=0.3,
            style=0.2,
        ),
    )

    # Save audio to file
    audio_path = "./voiceover.mp3"
    with open(audio_path, "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)

    try:
        # Check if files exist
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)

        # Set the fps attribute for the video clip
        if video.fps is None:
            video.fps = 60  # Default to 60 if fps information is not available

        # Determine the final duration (use the longer of video or audio)
        final_duration = max(video.duration, audio.duration)

        # Extend video if necessary
        if final_duration > video.duration:
            black_screen = ColorClip(size=video.size, color=(0, 0, 0), duration=final_duration - video.duration)
            final_video = CompositeVideoClip([video, black_screen.set_start(video.duration)])
        else:
            final_video = video

        # Safely extend audio if necessary
        if final_duration > audio.duration:
            # Create silence for the remaining duration
            silence_duration = final_duration - audio.duration
            silence = AudioClip(lambda t: 0, duration=silence_duration)
            extended_audio = CompositeAudioClip([audio, silence.set_start(audio.duration)])
        else:
            extended_audio = audio

        # Set the audio of the video clip
        final_clip = final_video.set_audio(extended_audio)

        # Ensure the final clip duration matches the longer of video or audio
        final_clip = final_clip.set_duration(final_duration)

        # Export the final video
        output_path = "../frontend/public/final_video.mp4"
        final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=video.fps)

        # Close the clips
        final_clip.close()
        video.close()
        audio.close()

        return {
            "code": 0,
            "message": f"Video with voiceover created successfully. Duration: {final_duration:.2f} seconds",
            "output_path": output_path
        }

    except FileNotFoundError as e:
        return {"code": 1, "message": str(e)}
    except Exception as e:
        return {"code": 2, "message": f"An error occurred: {str(e)}"}

# Usage

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
