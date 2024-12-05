import math
from gtts import gTTS
from moviepy.editor import VideoClip, concatenate_videoclips, AudioFileClip, ImageSequenceClip, TextClip, CompositeVideoClip, vfx
from PIL import Image
import os
# from googletrans import Translator
import nltk
from moviepy.editor import concatenate_audioclips

from pydub import AudioSegment


# def translate_text(text_path, target_language='hi'):
#     with open(text_path, 'r', encoding='utf-8') as file:
#         content = file.read()

#     translator = Translator()
#     translated_text = translator.translate(content, dest=target_language)

#     with open('translated_text_hi.txt', 'w', encoding='utf-8') as trans_file:
#         trans_file.write(translated_text.text)

#     return translated_text.text



def text_to_audio(text):

    # Create the gTTS object and save the audio file
    tts = gTTS(text=text, lang='en', slow=False)

    # tts = gTTS(text=translate_text(text_to_speak), lang='hi', slow=False)
    tts.save('./audio/'+text+".mp3")
    return tts

def resize_images(image_folder, output_folder, size=(1920, 1080)):
    print("here")
    os.makedirs(output_folder, exist_ok=True)

    for img_file in os.listdir(image_folder):
        if img_file.endswith(".jpg"):
            img_path = os.path.join(image_folder, img_file)
            img = Image.open(img_path)
            img_resized = img.resize(size)

            output_path = os.path.join(output_folder, img_file)
            img_resized.save(output_path)

def generate_subtitles(rawtext):
    rawtext = rawtext.replace('\n', ' ')

    # print(rawtext)

    sentences = nltk.sent_tokenize(rawtext)
    subs = dict()

    for sentence in sentences:
        s = sentence.replace(',', ',##')
        result = s.split('##')
        x = []
        s = ''
        for r in result:
            q = r.split()
            if len(q) < 3:
                s = r
            else:
                if s != '':
                    r = s + r
                    s = ''
                if len(q) > 8:
                    s = " ".join(q[8:])
                    r = " ".join(q[:8])
                x.append(r)
        if s != '':
            x.append(s)
        subs[sentence] = x
    # print(subs)
    return subs

def text_to_video(content):

    all_audios = []
    all_videos = []
    all_subtitles = []
    print("here")
    # with open(script_path, 'r', encoding='utf-8') as file:
    #     content = file.read()

    subtitles = generate_subtitles(content)

    image_files = sorted(os.listdir(resized_image_folder)) #dateaset
    img_index = 0
    img_path = './resized_images'

    for sentence, all_subs in subtitles.items():
        # print(sentence)
        # print(all_subs)

        duration = 0

        for sub in all_subs:
            text_to_audio(sub)
            audio = AudioFileClip("./audio/" +sub+".mp3")
            all_audios.append(audio)
            duration += audio.duration

            subtitle_text = sub
            subtitle_clip = TextClip(subtitle_text, fontsize=24, color='white', bg_color='black').set_position('center', 'center').set_duration(audio.duration)

            # subtitle_clip.write_videofile('./temp/'+sub+'.mp4', codec='libx264', audio_codec='aac', fps=24)
            all_subtitles.append(subtitle_clip)

        img_clip = ImageSequenceClip([os.path.join(img_path, image_files[img_index])], fps=24).set_duration(duration).fx(vfx.fadein, 0.1).fx(vfx.fadeout, 0.1)
        img_index += 1
        # subtitle_clip.write_videofile('./temp/' + sentence + '.mp4', codec='libx264', audio_codec='aac', fps=24)

        all_videos.append(img_clip)

    final_audio_clip = concatenate_audioclips(all_audios)
    final_video_clip = concatenate_videoclips(all_videos)
    final_sub_clip = concatenate_videoclips(all_subtitles)
    final_clip = CompositeVideoClip([final_video_clip, final_sub_clip])
    final_clip = final_clip.set_audio(final_audio_clip).set_duration(final_audio_clip.duration)
    print(type(final_clip))
    # final_clip.write_videofile('final_output.mp4', codec='libx264', audio_codec='aac', fps=24)


if __name__ == '__main__':

    original_image_folder = "./images"
    resized_image_folder = "./resized_images"
    resize_images(original_image_folder, resized_image_folder)
    content = "India is my country, all indians are my brothers and sisters. I love my country."
    text_to_video(content)
    # print(translate_text('input_text_en.txt'))