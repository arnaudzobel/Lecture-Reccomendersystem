
import os
def cutVideo(fileName, segments, totalFrame,fps,output_dir):
    file = os.path.split(fileName)[1]
    scene_name = file.split(".")[0]

    if len(segments) > 0:
        if len(segments) == 1:
            cmd = "ffmpeg -ss 0 -i "+fileName+ " -to " + str(
                segments[0] / float(fps)) + " -c copy " + output_dir + scene_name + "-1" + ".mp4"
            os.system(cmd)
            print(cmd)

            cmd = "ffmpeg -ss " + str(
                (segments[0]) / float(fps)) + " -i "+fileName+ " -to " + str(totalFrame / float(
                fps)) + " -c copy " + output_dir + scene_name + "-2" + ".mp4"
            os.system(cmd)
            print(cmd)
        else:
            for x in range(0, len(segments)):
                index = x + 1
                if x == 0:
                    cmd = "ffmpeg -ss 0 -i "+fileName+" -to " + str(
                        segments[x + 1] / float(
                            fps)) + " -c copy " + output_dir + scene_name + "-%d" % index + ".mp4"
                elif x == len(segments) - 1:
                    cmd = "ffmpeg  -ss " + str(
                        (segments[x]) / float(fps)) +" -i "+fileName+ " -to " + str(totalFrame / float(
                        fps)) + " -c copy " + output_dir + scene_name + "-%d" % index + ".mp4"
                else:
                    endPos = str(segments[x + 1] / float(fps) - segments[x] / float(fps))
                    startPos = str(segments[x] / float(fps))
                    cmd = "ffmpeg -ss " + startPos +" -i "+fileName+ " -to " + endPos + " -c copy " + output_dir + scene_name + "-%d" % index + ".mp4"
                os.system(cmd)