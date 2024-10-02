import os
from moviepy.editor import *

def create_video(image_folder, audio_file, output_file, aud_minutes, aud_seconds):
    # Load images
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    image_files.sort()  # Ensure images are in order
    
    # Calculate duration for each image
    total_duration = aud_minutes * 60 + aud_seconds  # 6 minutes and 6 seconds
    image_duration = total_duration / len(image_files)
    
    # Create clips for each image
    clips = [ImageClip(os.path.join(image_folder, img)).set_duration(image_duration) for img in image_files]
    
    # Concatenate all image clips
    video = concatenate_videoclips(clips, method="compose")
    
    # Load audio and set its duration to match the video
    audio = AudioFileClip(audio_file).set_duration(total_duration)
    
    # Set the audio of the video
    final_video = video.set_audio(audio)
    
    # Write the result to a file
    final_video.write_videofile(output_file, fps=24)

# Usage

image_folder = "../../crime_and_punishment"
audio_file = "../../cnp_dostoevsky.wav"
output_file = "output_video_cnp.mp4"

create_video(image_folder, audio_file, output_file, aud_minutes=7, aud_seconds=44)