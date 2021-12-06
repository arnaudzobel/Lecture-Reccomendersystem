import cv2
import os
import numpy as np
import time as t
from sceneClassificator import executeSceneClassification
from audioFeaturesUtils import extract_audio_features
from utils import save_matrix, save_keyframes, save_to_csv
from visualFeaturesUtils import preprocess,getEntropy,getColorMoments,getEuclideanDistance,getRegionOfInterest
from cutVideo import cutVideo
from generateLMSinteractiondata import generate_users_and_data



min_scene_lenght = 2
skipFrames = 1
sampling_rate = 1
channel1 = []
channel2 = []
motionThreshold = 10
channels = []
totalFrames = 0
store_coordinate_points = []
fps=0

shotSifts = []
key_frames = []
key_frames_idx = []
min_scene_lenght=2
max_scene_lenght=15

def detectScenes(videofile, type):
    videoType1 = type
    entropy = []
    entropyDifference = []
    euclideanDistance = []
    colorDifference = []
    output_dir = os.path.split(videofile)[0]
    now = t.time()
    now_all = t.time()
    videoCap = cv2.VideoCapture(videofile)
    fps = videoCap.get(cv2.CAP_PROP_FPS)
    totalFrames = int(videoCap.get(cv2.CAP_PROP_FRAME_COUNT))
    success, image = videoCap.read()
    counter = -1

    while success:
            success, image = videoCap.read()
            if image is None:
                break
            #resize image to 50%
            scale_percent = 50
            width = int(image.shape[1] * scale_percent / 100)
            height = int(image.shape[0] * scale_percent / 100)
            dim = (width, height)
            image = cv2.resize(image, dim)

            # calculate the average color of each image frame
            avg_color_per_row = np.average(image, axis=0)
            avg_colors = np.average(avg_color_per_row, axis=0)
            int_averages = np.array(avg_colors, dtype=np.uint8)
            actualColor = sum(int_averages[:])
            counter = counter + 1
            print("frame "+str(counter))
            if videoType1:
                image = preprocess(getRegionOfInterest(image))
                #cv2.imshow('background ectraction', image)
                #cv2.waitKey(0)
                #cv2.destroyAllWindows()

            histogram = cv2.calcHist([image], [0], None, [256], [0, 256])
            totalPixels = width * height
            entropy.append(getEntropy(histogram, totalPixels))
            colorMoments = getColorMoments(histogram, totalPixels)
            if counter == 0:
                entropyDifference.append(0)
                euclideanDistance.append(0)
                colorDifference.append(0)
            else:
                entropyDifference.append(abs(entropy[counter] - entropy[counter - 1]))
                euclideanDistance.append(getEuclideanDistance(colorMoments, previousColorMoments))
                colorDifference.append(abs(actualColor - previousColor))
            previousColor = actualColor
            previousColorMoments = colorMoments
    print("Feature extraction completed")
    print(euclideanDistance)
    print(colorDifference)
    print()
    later = t.time()
    difference = int(later - now)
    print("t visuell ex %d" % difference)
    now=t.time()
    meanEuclideanDistance = sum(euclideanDistance[1:]) / float(len(euclideanDistance) - 1)
    thresholdEuclideanDistance = meanEuclideanDistance
    segments = []
    changeDetectionTimeline = []
    segments.append(0)
    transiton_index=0
    transitionDeteted=False

    #For all frames
    for i in range(totalFrames):
        cnt=-1
        #Index of last frame within the second
        if i % fps == 0:
            cnt += 1
            #Index of start frame within the second
            startIndex = i - int(fps)
            if startIndex < 0:
                startIndex = 0
            transitionDeteted = False
            #For all Frames within the second
            for j in range(startIndex, i):
                #Check if Euclidiean distance is higher than threshold
                if euclideanDistance[j] > thresholdEuclideanDistance:
                    a = euclideanDistance[j] - euclideanDistance[j + 1]
                    b = entropyDifference[j] - entropyDifference[j + 1]
                    if a > 1:
                        transitionDeteted = True
                        transiton_index = cnt*fps+j
                        break
            if transitionDeteted:
                #save index of transition frame
                key_frames_idx.append(transiton_index)
                changeDetectionTimeline.append(1)
            else:
                 changeDetectionTimeline.append(0)

    time = np.arange(totalFrames/ fps)
    print(key_frames_idx)
    print(changeDetectionTimeline)

    for i in range(0,len(key_frames_idx)+1):
        frame_1 = 0
        frame_2 = 0
        frame_3 = 0
        if i== 0:
            frame_1 = 1
            frame_2 = key_frames_idx[i]//2
            frame_3 = key_frames_idx[i]-1
        elif i == len(key_frames_idx):
            frame_1 = key_frames_idx[len(key_frames_idx)-1]+5
            frame_2 = totalFrames - (totalFrames - key_frames_idx[len(key_frames_idx)-1]) // 2
            frame_3 = totalFrames - 5
        else:
            frame_1 = key_frames_idx[i-1] + 5
            frame_2 = key_frames_idx[i] - (key_frames_idx[i] - key_frames_idx[i-1]) // 2
            frame_3 = key_frames_idx[i] - 1
        videoCap.set(1, frame_1)
        success, image = videoCap.read()
        key_frames.append(image)

        videoCap.set(1, frame_2)
        success, image = videoCap.read()
        key_frames.append(image)

        videoCap.set(1, frame_3)
        success, image = videoCap.read()
        key_frames.append(image)
    #save keyframes
    save_keyframes(key_frames,videofile)
    fileName = os.path.splitext(os.path.split(videofile)[1])[0]
    later = t.time()
    difference = int(later - now)
    print("t feat anal %d" % difference)
    now=t.time()
    #Execute scene classification
    result=executeSceneClassification(output_dir+"\\"+fileName)
    save_to_csv(output_dir+"\\"+fileName+"\keyframes",fileName,result,key_frames_idx,totalFrames,fps)
    later = t.time()
    difference = int(later - now)
    print("t scene classif %d" % difference)
    now = t.time()
    #extract audio features
    breakTimeLine = extract_audio_features(videofile,fps,output_dir+"\\"+fileName+"\\")
    later = t.time()
    difference = int(later - now)
    print("t aud ex %d " % difference)
    now = t.time()


    #Clean data. two consecutive slide change not allowed
    for i in range(0, len(changeDetectionTimeline)):
       if changeDetectionTimeline[i] == 1 and (changeDetectionTimeline[i-1] == 1 or changeDetectionTimeline[i-2] == 1):
           changeDetectionTimeline[i] = 0
    interestingChangesTimeLine=[]

    #Detect Topic change
    for i in range(0,len(changeDetectionTimeline)):
        if changeDetectionTimeline[i] == 1:
            print(str(i))
            if (i>0 and (breakTimeLine[i-1] == 1)) or (i<len(breakTimeLine)-1 and breakTimeLine[i+1] ==1):
                print("######### Interesting detected")
                interestingChangesTimeLine.append(1)
            else:
                interestingChangesTimeLine.append(0)
        else:
            interestingChangesTimeLine.append(0)

    print(result)
    print(key_frames_idx)

    # Save detected scenes
    save_matrix(time, breakTimeLine, changeDetectionTimeline, interestingChangesTimeLine,output_dir+"\\"+fileName+"\\")

    # Ignore fault slides
    counter = 0
    to_del=[]
    for k, v in result.items():
        if v == "Fault":
            key_frames_idx.pop(k - 1 - counter)
            counter = counter + 1
            to_del.append(k)
    for x in to_del:
           result.pop(x)
    dist = 0
    indices_cleaned = []

    #Ignore detected scene with duration under min_duration
    print(key_frames_idx)
    for i in range(0, len(key_frames_idx)+1):
        if i == 0:
            dist = key_frames_idx[i]
        elif i == len(key_frames_idx):
            dist = (totalFrames / float(fps)) - (key_frames_idx[i - 1] / float(fps))
        else:
            dist = (key_frames_idx[i] / float(fps)) - (key_frames_idx[i - 1] / float(fps))
        if dist < min_scene_lenght * 60:
            print("Skipp scene")
        else:
            if(i == len(key_frames_idx)):
                indices_cleaned.append(key_frames_idx[i-1])
            else:
                indices_cleaned.append(key_frames_idx[i])
    print(indices_cleaned)


    segments = indices_cleaned

    #save final scene detection result
    save_to_csv(output_dir+"\\"+fileName+"\distribution",fileName,result,segments,totalFrames,fps)
    distrib_path=output_dir+"\\"+fileName+"\distribution\\"
    later = t.time()
    difference = int(later - now)
    print("t detec int scene %d" % difference)
    now=t.time()
    generate_users_and_data(output_dir+"\\"+fileName+"\distribution")
    later = t.time()
    difference = int(later - now)
    print("t detec LMS %d" % difference)
    now=t.time()
    #Cut detected scenes
    cutVideo(videofile, segments, totalFrames, fps, distrib_path)
    later = t.time()
    difference = int(later - now)
    print("t cut vid %d" % difference)

    later = t.time()
    difference = int(later - now_all)
    print("t all %d" % difference)
    print("vid fps %d"%fps)
    cv2.destroyAllWindows()