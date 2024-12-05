from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .web import getAllurls, getText
from .main import extract_text_from_pdf, createText, generate_subtitles, generateVideos
from .models import PibVideo

from .forms import VideoDescriptionForm
from django.core.files.storage import default_storage
import os
import time
import requests

def index(request):
    return render(request, 'index.html')

def ApprovedVideo(request):
    return render(request, 'ApprovedVideo.html')

def edit(request):
    return render(request, 'Edit.html')

def PendingVideo(request):
    link_dict = getAllurls()
    return render(request, 'PendingVideo.html', {'videos': link_dict})

def Register(request):
    return render(request, 'Register.html')

def Login(request):
    return render(request, 'Login.html')

# Modified video_list to show only the latest video
def video_list(request):
    # Get the latest video based on the date field (assuming your model has a 'date' field)
    latest_video = PibVideo.objects.filter(status=0).order_by('-date').first()  # Show only the most recent video with status 0
    return render(request, 'video_list.html', {'latest_video': latest_video})

def InputPage(request):
    if request.method == 'POST':
        try:
            if 'input_text' in request.POST:
                link = str(request.POST["input_text"])
                return handle_text_input(request, link)
            elif 'pdf_file' in request.FILES:
                pdf_file = request.FILES['pdf_file']
                return handle_pdf_upload(request, pdf_file)
        except Exception as e:
            print("Error in InputPage:", str(e))
            return render(request, 'InputPage.html', {'error': str(e)})
    return render(request, 'InputPage.html')

def handle_text_input(request, link):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print("Processing link:", link)
            text = getText(link)
            print("Text extracted:", text)
            a = createText(text)
            print("Text created:", a)
            b = generate_subtitles(a)
            print("Subtitles generated:", b)
            final_clip = generateVideos(a, b, "mr", "output_en.mp4")
            print("Video generated:", final_clip)
            return save_video(request, final_clip)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retrying
            else:
                return render(request, 'InputPage.html', {'error': str(e)})

def handle_pdf_upload(request, pdf_file):
    try:
        print("Processing PDF upload:", pdf_file)
        
        # Save the uploaded PDF file
        file_name = default_storage.save(pdf_file.name, pdf_file)
        file_path = os.path.join(default_storage.location, file_name)
        
        # Extract text from the PDF
        text = extract_text_from_pdf(file_path)
        print("Text extracted from PDF:", text)
        
        # Create text and generate subtitles and video
        a = createText(text)
        print("Text created:", a)
        b = generate_subtitles(a)
        print("Subtitles generated:", b)
        final_clip = generateVideos(a, b, "mr", "output_en.mp4")
        print("Video generated:", final_clip)
        
        return save_video(request, final_clip)
        
    except Exception as e:
        print("Error in handle_pdf_upload:", str(e))
        return render(request, 'InputPage.html', {'error': str(e)})

def save_video(request, final_clip):
    try:
        video_file_path = 'videos/generated_video.mp4'
        video_file_full_path = os.path.join(default_storage.location, video_file_path)
        print("Saving video at:", video_file_full_path)
        final_clip.write_videofile(video_file_full_path, codec="libx264", audio_codec="aac", fps=24)
        
        new_video = PibVideo(
            title='Generated Video',
            caption='Generated Caption',
            description='Video description here',
            video=video_file_path
        )
        new_video.save()
        print("Video saved successfully.")
        return render(request, 'InputPage.html', {'success': 'Video generated successfully!'})
    
    except Exception as e:
        print("Error during video save:", str(e))
        return render(request, 'InputPage.html', {'error': str(e)})

def approve_video(request, video_id):
    video = get_object_or_404(PibVideo, id=video_id)
    video.status = True
    video.save()
    return redirect('video_list')

def edit_video(request, video_id):
    video = get_object_or_404(PibVideo, id=video_id)
    if request.method == 'POST':
        form = VideoDescriptionForm(request.POST, instance=video)
        if form.is_valid():
            form.save()
            return redirect('video_list')
    else:
        form = VideoDescriptionForm(instance=video)
    return render(request, 'Edit.html', {'form': form, 'video': video})
