import json
import os
from ShazamAPI import Shazam
from colored import fore, back, style
from termcolor import colored
import argparse

# Create an ArgumentParser object to handle command-line arguments
parser = argparse.ArgumentParser()

# Define the path argument for the script
parser.add_argument('-p', '--path', help='Complete folder path of the audio files.')

# Parse the command-line arguments
args = parser.parse_args()

# Get the audio folder path and add a '/' at the end
audio_folder = str(args.path)+'/' 

def check_copyright():
    # Print a message to indicate the start of the copyright verification process
    print(colored(" [ Verifying copyrighted materials ... ] ",'blue'))

    # Remove any .DS_Store files in the audio folder
    os.system("rm -rf "+audio_folder+'.DS_Store')
    
    # Iterate through each file in the audio folder
    for filename in os.listdir(audio_folder):
        # Read the content of the mp3 file
        mp3_file_content_to_recognize = open(audio_folder+filename, 'rb').read()
        # Use the ShazamAPI to recognize the song in the mp3 file
        shazam = Shazam(mp3_file_content_to_recognize)
        recognize_generator = shazam.recognizeSong()

        copyrighted = []
        # Iterate through the results of the song recognition
        for _,entry in recognize_generator:
            # Get the title and subtitle of the recognized song
            title = entry.get("track",{}).get("title","unknown")
            subtitle = entry.get("track",{}).get("subtitle","unknown")
            copyrighted.append(title + ' - ' + subtitle)

        if len(copyrighted) != 0:
            # Print a message indicating that the file is copyrighted and the title of the song
            print(fore.RED+ " [ Copyright : " + fore.WHITE + filename + fore.RED +" ] ")
            for i in list(dict.fromkeys(copyrighted)):
                print(fore.RED + " [ Title : " + fore.WHITE + i + fore.RED + " ] ")

    # Print a message to indicate the end of the copyright verification process
    print(colored(" [ Copyright verification finished. ",'blue'))

# Call the check_copyright function to start the copyright verification process
check_copyright()
