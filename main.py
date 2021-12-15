import os
import sys
from sceneDetector import detectScenes
from generateLMSinteractiondata import generate_users_and_data
path = sys.argv[1]
WHITEBOARD_PROF_IN_FULL_SCREEN = sys.argv[2]

def load_video_records(path):
    files = []
    for file in os.listdir(path):
        if file.endswith(".mp4"):
            files.append(os.path.abspath(os.path.join(path,file)))
    return files

def main():
    files = load_video_records(path)
    for file in files:
        detectScenes(file, WHITEBOARD_PROF_IN_FULL_SCREEN)
if __name__ == '__main__':
    main()