import os
from sceneDetector import detectScenes
from generateLMSinteractiondata import generate_users_and_data
#path = sys.argv[1]
#videoType1 = sys.argv[2]

path = "test"
videoType1 = True
def load_video_records(path):
    files = []
    for file in os.listdir(path):
        if file.endswith(".mp4"):
            files.append(os.path.abspath(os.path.join(path,file)))
    return files

def main():
    files = load_video_records(path)
    for file in files:
        detectScenes(file, videoType1)
        ##generate_users_and_data(os.path.abspath("test/rec/"))

if __name__ == '__main__':
    main()