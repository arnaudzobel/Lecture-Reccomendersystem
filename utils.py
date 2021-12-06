import os
import cv2
import csv
import numpy as np
from numpy.linalg import norm
def save_matrix(timeLine, breaks, slideChanges, topicChanges,path):
    out_file = open(path+"matrix.txt", 'w')
    out_file.write("TimeLine:     ")
    for idx in timeLine:
        out_file.write(str(idx)+"  ")
    out_file.write("\n")

    out_file.write("BreaksTimeLine:       ")
    for idx in breaks:
            out_file.write(str(idx)+"  ")
    out_file.write("\n")

    out_file.write("SceneChanges: ")
    for idx in slideChanges:
        out_file.write(str(idx)+"  ")

    out_file.write("\n")

    out_file.write("TopicChanges: ")
    for idx in topicChanges:
        out_file.write(str(idx)+"  ")

def save_keyframes(key_frames, videofile):
    folderName=os.path.split(videofile)[0]
    scene_name=os.path.splitext(os.path.split(videofile)[1])[0]
    cmd = "rd /Q /S " + folderName + "\\"+scene_name
    os.system(cmd)
    cmd = "mkdir " + folderName + "\\"+scene_name
    os.system(cmd)
    cmd = "mkdir " + folderName + "\\"+scene_name+"\keyframes"
    os.system(cmd)
    cmd = "mkdir " + folderName + "\\"+scene_name+"\distribution"
    os.system(cmd)
    sceneCounter=0
    sceneIndex=0
    for i, frame in enumerate(key_frames):
        if i % 3 == 0:
            sceneCounter+=1
            sceneIndex=0
        cv2.imwrite(str(folderName) + "\\"+scene_name+"\keyframes/"+scene_name+"-%d-%d.jpg"%(sceneCounter, sceneIndex), frame)
        sceneIndex+=1
    print("key frames saved")

def getbrightness(img):
    if len(img.shape) == 3:
        # Colored RGB or BGR (*Do Not* use HSV images with this function)
        # create brightness with euclidean norm
        return np.average(norm(img, axis=2)) / np.sqrt(3)
    else:
        # Grayscale
        return np.average(img)

def save_to_csv(dir,fileName, prediction,scene,totalFrame,fps):

    output_file = dir+"\\"+fileName.split(".")[0] + '.csv'
    with open(output_file, 'w', newline='') as outcsvfile:
            fieldnames = ['sceneId', 'start frame', 'end frame', 'duration in s', 'scene class']
            writer = csv.DictWriter(outcsvfile, delimiter=',', fieldnames=fieldnames)
            writer.writeheader()
            start=0
            end=0
            duration=0
            name=""
            for index in range(0,len(scene)+1):
                if index == 0:
                    start=0
                    end = scene[index]/float(fps)
                    duration = scene[index]/float(fps)
                elif index == len(scene):
                    start = scene[index-1]/float(fps)
                    end = totalFrame / float(fps)
                    duration = (totalFrame / float(fps))-(scene[index-1]/float(fps))
                else:
                    start = scene[index - 1] / float(fps)
                    end = scene[index] / float(fps)
                    duration = (scene[index] / float(fps)) - (scene[index - 1] / float(fps))
                writer.writerow({fieldnames[0]: "%d" % (index + 1),
                                 fieldnames[1]: int(start),
                                 fieldnames[2]: int(end),
                                 fieldnames[3]: "{:.2f}".format(duration),
                                 fieldnames[4]: prediction.get(index+1)
                                 })