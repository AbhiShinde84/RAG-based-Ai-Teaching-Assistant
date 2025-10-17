# How to use this RAG AI Teaching assistant on your own data
## Step 1 - Collect your videos
Move all your video files to the video folder

## Step 2 - Convert to mp3
Convert all the video files to mp3 by ruunning process_video

## Step 3 - Convert mp3 to json 
Convert all the mp3 files to json by ruunning mp3_to_json

## Step 4 - Merge json chunks 
For efficiency combine the json chunks by running merge_chunks
Here you will get newjsons folder containing all new chunk_merged json files 

## Step 5 - Convert the json files to Vectors
Use the file preprocessing_json to convert the json files to a dataframe with Embeddings and save it as a joblib pickle

## Step 6 - Prompt generation and feeding to LLM

Read the joblib file and load it into the memory. Then create a relevant prompt as per the user query and feed it to the LLM


# Note : 
    for ffmpeg (to convert mp4 to mp3) : 
    https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl-shared.zip

    copy the extracted ffmpeg folder in the c drive in programfiles 
    then add the bin folder path in the environment variables : 
    for example : "C:\Program Files (x86)\ffmpeg\bin"

    for whisper :
    pip install git+https://github.com/openai/whisper.git

    for using ollama :
    download link : https://ollama.com/download/OllamaSetup.exe

    For ollama bge-m3 Run this command in terminal : "ollama pull bge-m3"

    for using lamma 3.2 llm model run  : "ollama run llama3.2"
    
    

