from openai import OpenAI
import fitz
import re
import time
from gtts import gTTS
from moviepy.editor import VideoClip, TextClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from web import getText
from moviepy.video.compositing.concatenate import concatenate_videoclips
import moviepy.editor as mp

# # Specify the path to the ImageMagick binary (replace "path/to/magick" with the actual path)
# mp.ImageSequenceClip.set_images_magick_path("C:/Program Files/ImageMagick-7.1.1-Q16-HDRI")


# OpenAI API key
def genTextSum():
    OPENAI_API_KEY = "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"

    # Initialize OpenAI client
    client = OpenAI(api_key=OPENAI_API_KEY)

    # Your prompt
    text = getText("https://pib.gov.in/PressReleasePage.aspx?PRID=1986133")
    # print(text)
    prompt = f"Sumerize the following news in 10 sentences and put each sentence in () like (sentence 1) (sentence 2)...  :\n{text} "
    # print(prompt)
    # prompt = "PRESIDENT OF INDIA GRACES 2ND CONVOCATION OF IIIT, LUCKNOW"
    print("================================")
    def get_completion(prompt, model="gpt-3.5-turbo"):
        messages = [{"role": "user", "content": prompt}]
        completion = client.chat.completions.create(
            model=model, messages=messages, temperature=0,
        )
        return completion.choices[0].message.content

    # Generate and print completion
    completion = get_completion(prompt)
    print(completion)
    return completion
genTextSum()
