import os 
import subprocess

files  = os.listdir('video')

for file in files:
    tutorial_number  = file.split('(360')[0].split('Tutorial _')[1]
    file_name = file.split(' _ Sigma')[0]
    print(tutorial_number , file_name)
    subprocess.run(["ffmpeg","-i",f"video/{file}",f"Audios/{tutorial_number}_{file_name}.mp3"]) # Convert videos to Audio (mp3) 