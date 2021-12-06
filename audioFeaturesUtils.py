import scipy.io.wavfile
import moviepy.editor

channel1 = []
channel2 = []
channels = []
breakTimeLine = []

def extract_audio_features(videoFile,fps, path):

    video = moviepy.editor.VideoFileClip(videoFile)
    audiodata = video.audio
    audiodata.write_audiofile(path+"audio.wav")
    # get raw audio data as a bytestring
    rate, audio = scipy.io.wavfile.read(path+"audio.wav")
    print("fps audio %d"%rate)
    channel1 = audio[:, 0]  # left
    channel2 = audio[:, 1]  # Right
    for i in range(0, len(channel1)):
        if i % (rate / fps) == 0:
            channels.append(channel1[i])

    for i in range(0, len(channels)):
        if i % fps == 0:
            breakCounter = 0
            index = i - int(fps)
            if index < 0:
                index = 0
            for j in range(index, i):
                if (channels[j] >= -6) and (channels[j] <= 6):
                    breakCounter += 1
            #one second break
            if breakCounter > (int(fps) - 5):
                breakTimeLine.append(1)
            else:
                breakTimeLine.append(0)
    return breakTimeLine