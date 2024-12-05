import os
import json
import random
import time
import requests
from urllib.parse import urljoin
from PIL import Image
from gtts import gTTS
from moviepy.editor import (
    VideoClip,
    concatenate_videoclips,
    AudioFileClip,
    ImageClip,
    TextClip,
    CompositeVideoClip,
    concatenate_audioclips,
    CompositeAudioClip,
)
from bs4 import BeautifulSoup
import google.generativeai as genai
import fitz

# Initialize the Generative Model
model = genai.GenerativeModel('gemini-pro')
genai.configure(api_key="AIzaSyClYtEsgE50UkGLOc_HzJ_tNxbYB4N-0lg")


def extract_text_from_pdf(pdf_path):
    """Extract text from PDF."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


def delete_files_in_folder(folder_path):
    """Delete files in the specified folder."""
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")


def text_transform(text):
    """Remove unwanted characters from text."""
    return ''.join(char for char in text if char.isalnum())


def text_to_audio(text, lang):
    """Convert text to audio and save it as an MP3 file."""
    tts = gTTS(text=text, lang=lang, slow=False)
    audio_path = f'./audio/{text_transform(text)}.mp3'
    tts.save(audio_path)
    return tts


def webscraping(val):
    """Scrape images from Bing based on the query text."""
    querytext = val.replace(' ', '+')
    url = f"https://www.bing.com/images/search?q={querytext}+india&qft=+filterui:license-L2_L3_L5_L6&form=IRFLTR&first=1"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to retrieve the page: {e}")
        return
      
    soup = BeautifulSoup(response.text, 'html.parser')
    img_cont_divs = soup.find_all('div', class_='img_cont hoff')

    if img_cont_divs:
        img_tag = img_cont_divs[0].find('img')
        if img_tag:
            image_url = urljoin(url, img_tag.get('src'))
            image_content = requests.get(image_url).content
            with open('./images/temp.png', 'wb') as image_file:
                image_file.write(image_content)
            resize_images()
            os.remove('./images/temp.png')


def resize_images(image_folder='./images', output_folder='./images2', size=(640, 480)):
    """Resize images and save them to a specified folder."""
    img_path = os.path.join(image_folder, 'temp.png')
    with Image.open(img_path) as img:
        img_resized = img.resize(size)
        img_resized.save(os.path.join(output_folder, 'temp.png'))


def createText(article):
    """Summarize the article into 10 lines."""
    prompt = f"{article}\nsummarize this into 15 lines and give numbering for each line"
    response = model.generate_content(prompt)
    answer = response.text.strip().split('\n')
    return list(dict.fromkeys(line.split(' ', 1)[1].strip() for line in answer))


def translateLang(lang, sentences):
    """Translate a list of sentences into the specified language."""
    api_url = "http://127.0.0.1:8000/api/translate/"
    translated_texts = {}

    for sent in sentences:
        data = {'language': lang, 'text': sent}
        try:
            response = requests.post(api_url, json=data)
            response.raise_for_status()
            result = response.json()
            translated_texts[sent] = result['translated_text']
        except requests.RequestException as e:
            print(f"Error: {e}")
    
    return translated_texts


def subtitle(title, duration, lang):
    """Create a subtitle video clip."""
    image_path = "./images2/temp.png"
    image_clip = ImageClip(image_path, duration=duration)
    text_clip = TextClip(title, fontsize=20, color='white', bg_color='black',
                         font='./MANGAL.ttf' if lang in ['mr', 'hi'] else './Nirmala.ttf').set_duration(duration)

    text_clip = text_clip.set_position(('center', 'bottom'))
    return CompositeVideoClip([image_clip, text_clip])


def createIntro():
    """Create a white intro image."""
    white_image = Image.new("RGB", (640, 480), "white")
    white_image.save("./intro.png")


def title(title_text, img_path, duration):
    """Create a title video clip."""
    image_clip = ImageClip(img_path, duration=duration)
    text_clip = TextClip(title_text, fontsize=50, color='white', size=(image_clip.w, image_clip.h)).set_duration(duration).set_position('center')
    return CompositeVideoClip([image_clip, text_clip])


def generate_subtitles(sentences):
    """Generate subtitles for the given sentences."""
    subs = {}
    for sentence in sentences:
        result = sentence.replace(',', ',##').split('##')
        x = []
        s = ''
        for r in result:
            q = r.split()
            if len(q) < 3:
                s = r
            else:
                if s:
                    r = s + r
                    s = ''
                if len(q) > 8:
                    s = " ".join(q[8:])
                    r = " ".join(q[:8])
                x.append(r)
        if s:
            x.append(s)
        subs[sentence] = x
    return subs


def generateVideos(a, b, title_, filename='final_output.mp4'):
    """Generate videos from audio and subtitles."""
    all_audios = []
    all_videos = []
    
    delay_audio = AudioFileClip("./silence.mp3").set_duration(2)
    all_audios.append(delay_audio)
    
    createIntro()
    intro = title(title_, "./outro.jpeg", 2)
    all_videos.append(intro)
    
    background_music = AudioFileClip('./bg_music.mp3')
    bl = [background_music] * 10

    for sentence, all_subs in b.items():
        duration = 0
        webscraping(sentence)

        for sub in all_subs:
            text_to_audio(sub, 'mr')
            audio = AudioFileClip(f"./audio/{text_transform(sub)}.mp3")
            all_audios.append(audio)
            duration += audio.duration
            vid = subtitle(sub, audio.duration, 'en')
            all_videos.append(vid)

    final_audio_clip = concatenate_audioclips(all_audios)
    final_bg_audio_clip = concatenate_audioclips(bl)

    final_audio_clip = final_audio_clip.volumex(2.0)
    final_bg_audio_clip = final_bg_audio_clip.volumex(0.3).subclip(0, final_audio_clip.duration)

    final_audio_clip = CompositeAudioClip([final_bg_audio_clip, final_audio_clip])
    final_video_clip = concatenate_videoclips(all_videos).set_audio(final_audio_clip).set_duration(final_audio_clip.duration).speedx(1.1)

    return final_video_clip


def createall(article):
    """Create the entire video from the article."""
    a = createText(article=article)
    print(a)
    languages = ['en', 'mr', 'hi', 'gu', 'bn', 'te', 'ta', 'ml', 'kn', 'ur']
    for lang in languages[1:2]:
        tran = translateLang(lang, a)
        b = generate_subtitles(list(tran.values()))
        print(b)
        generateVideos(a, b, lang, f"output_{lang}")
