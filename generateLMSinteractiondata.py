import random
import csv
import os
from numpy.random import randn
from scipy.stats import pearsonr
from numpy.random import seed
from numpy import mean
seed(1)

#learningDuration,numberOfPosts,numberOfMessagesSentToTeacher
#[professor,execise,slide]
very_lazy_students =  [[[80, 100], [0, 0], [0, 10]], [0, 0], [150]]
middle_lazy_students =  [[[60, 80], [0, 10], [10, 30]], [0, 1], [250]]
medium_students    =  [[[40, 60], [50, 60], [50, 80]], [1, 2], [400]]
good_students      =  [[[10, 20], [0, 100], [20, 100]], [1, 2], [200]]

profiles=[good_students, very_lazy_students, middle_lazy_students, medium_students]
#1-6,7-12,12-17,18-25
scene_list=[]
output_file=""

def read_csv(dir):
    files = os.listdir(dir)
    for file in files:
        if file.endswith(".csv"):
            input_file = os.path.join(dir, file)
            break
    with open(input_file, newline='') as incsvfile:
        reader = csv.DictReader(incsvfile)
        reader.fieldnames = ['sceneId','start frame', 'end frame', 'duration in s', 'scene class']
        next(reader)
        for row in reader:
            scene_list.append(row)


def get_output_file_name(dir):
    files = os.listdir(dir)
    for file in files:
       if file.endswith(".csv"):
           input_file = os.path.join(dir, file)
           break
    input_file = os.path.splitext(input_file)[0] + '_ratings.csv'
    return input_file

def generate_users_and_data(input_dir):
    read_csv(input_dir)
    output_file = get_output_file_name(input_dir)
    with open(output_file, 'w', newline='') as outcsvfile:
        fieldnames = ['userId', 'sceneId', 'learningDuration in %','numberOfPosts']
        writer = csv.DictWriter(outcsvfile, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()
        user_id=0
        values_learningDuration = []
        values_numberOfPost = []
        for i in range(len(profiles)):
            for j in range(profiles[i][2][0]):
                user_id+= 1
                if j == 0:
                    learningDuration=0
                    numberOfPosts=0
                    for x in range(0,len(scene_list)):
                        if scene_list[x].get("type") == "Professor":
                            learningDuration = random.randint(profiles[i][0][0][0], profiles[i][0][0][1])
                        elif scene_list[x].get("type") == "Slides":
                            learningDuration = random.randint(profiles[i][0][1][0], profiles[i][0][1][1])
                        else:
                            learningDuration = random.randint(profiles[i][0][2][0], profiles[i][0][2][1])
                        values_learningDuration.append(learningDuration)
                        numberOfPosts = random.randint(profiles[i][1][0], profiles[i][1][1]);
                        values_numberOfPost.append(numberOfPosts)

                        #print("{0},{1},{2},{3}".format(learningDuration,numberOfPosts,numberOfMessagesToTeachter))

                    first_record_learning_duration = values_learningDuration
                    first_record_number_posts = values_numberOfPost
                    #first_record_number_messages_to_teacter = 1 * randn(len(scene_list)) + mean(values_numberOfMessagesToTeatcher)

                    #print(first_record_learning_duration)
                    #print(first_record_number_posts)

                    for x in range(0, len(scene_list)):
                        writer.writerow({fieldnames[0]: user_id,
                                         fieldnames[1]: scene_list[x].get("sceneId"),
                                         fieldnames[2]: int(first_record_learning_duration[x]),
                                         fieldnames[3]: int(first_record_number_posts[x]),
                                         })
                else:
                    err_rec_learning_duration = 10 * randn(len(scene_list)) + 1
                    err_rec_rec_post = 0.5 * randn(len(scene_list)) + 1
                    record_learning_duration = first_record_learning_duration + err_rec_learning_duration
                    record_number_post = first_record_number_posts + err_rec_rec_post
                    #print(record_learning_duration)
                    corr, _ = pearsonr(first_record_learning_duration, record_learning_duration)
                    #print('Pearsons correlation: %.3f' % corr)
                    #print(err_rec_learning_duration)
                    #print(record_learning_duration)
                    for y in range(0,len(record_learning_duration)):
                        if record_learning_duration[y]<0:
                            record_learning_duration[y]=0
                        elif record_learning_duration[y]>100:
                            record_learning_duration[y] = 100
                        if record_number_post[y]<0:
                            record_number_post[y]=0

                    for x in range(0,len(scene_list)):
                        writer.writerow({fieldnames[0]: user_id,
                                     fieldnames[1]: scene_list[x].get("sceneId"),
                                     fieldnames[2]: int(record_learning_duration[x]),
                                     fieldnames[3]: int(record_number_post[x]),
                                         })
                if j == profiles[i][2][0] - 1:
                    first_record_number_posts=[]
                    first_record_learning_duration=[]

                    values_numberOfPost=[]
                    values_learningDuration=[]
                    #print("##########")
def main():
    generate_users_and_data("test")

if __name__ == '__main__':
    main()