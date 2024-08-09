import re
import os
from groq import Groq
from pathlib import Path
from moviepy.editor import VideoFileClip
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
load_dotenv(Path("./env"))

def get_video_length(file_path):
    clip = VideoFileClip(file_path)
    duration = clip.duration
    clip.close()
    return duration



def extract_code(text):
    # Regex pattern to match code blocks
    print(text)
    pattern = r'```(?:\w+)?\n(.*?)```'
    
    # Find all matches
    matches = re.findall(pattern, text, re.DOTALL)

    if len(matches) == 1:
        return matches[0]
    else:
        raise ValueError("No code block found or mutlipel code block found")


def ask_groq(prompt: str):

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-70b-8192",
    )
    with open("./print.txt", "w") as f:
        f.write(chat_completion.choices[0].message.content)

    return chat_completion
