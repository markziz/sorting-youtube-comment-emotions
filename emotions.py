#******************************
#CS 1026 - Assignment 3 – Youtube Emotions
#Code by: Mark Ziza
#Student ID: mziza
#File created: November 18, 2024
#******************************
#This program takes a csv file with organized youtube comments by country
#and a tsv file of keywords and their emotions associated with them. The
#program makes a report on a new txt file of the most frequent emotions
#and the proportion of other emotions associated with a given country
#for each youtube comment in that region.

#establishing all emotions we are looking at
EMOTIONS = ['anger', 'joy', 'fear', 'trust', 'sadness', 'anticipation']

#function makes youtube comment all lowercase and removes non-alphabetical
def clean_text(comment):
    for letter in comment:
        if not letter.isalpha():
            comment = comment.replace(letter," ")
    comment = comment.lower()
    return comment

#function makes a dictionary that contains all emotion keywords and if that keyword contains each emotion
#1 = yes, 0 = no
def make_keyword_dict(keyword_file_name):
    #making primary dictionary
    keyword_dict = {}
    #opening file that contains all keywords and emotions associated
    keyword_infile = open(keyword_file_name, "r")
    keyword_line = keyword_infile.readline()
    while keyword_line != "":
        #making inner dictionary that will get added to primary
        emotions_dict = {}
        keyword_line = keyword_line.strip("\n")
        keyword_split_line = keyword_line.split("\t")
        for i in range(len(EMOTIONS)):
            #adding keyword and emotion score to inner dictionary
            emotions_dict[EMOTIONS[i]] = int(keyword_split_line[i+1])
        #adding inner dictionary to primary dictionary before inner is reset for next word
        keyword_dict[keyword_split_line[0]] = emotions_dict
        keyword_line = keyword_infile.readline()
    keyword_infile.close()
    #returning the primary dictionary
    return keyword_dict

#function finds the most apparent emotion in a comment using keywords dictionary
def classify_comment_emotion(comment, keywords):
    #cleaning comment with clean_text function
    comment = clean_text(comment)
    comment = comment.split()
    #making list counting each emotion(order same as order in EMOTIONS)
    emotion_count = [0,0,0,0,0,0]
    #adding each value of emotion from each keyword in comment
    for word in comment:
        if word in keywords:
            emotion_count[0] = emotion_count[0] + int(keywords[word]['anger'])
            emotion_count[1] = emotion_count[1] + int(keywords[word]['joy'])
            emotion_count[2] = emotion_count[2] + int(keywords[word]['fear'])
            emotion_count[3] = emotion_count[3] + int(keywords[word]['trust'])
            emotion_count[4] = emotion_count[4] + int(keywords[word]['sadness'])
            emotion_count[5] = emotion_count[5] + int(keywords[word]['anticipation'])
    #finding which emotion had the highest value and what index it is
    max_emotion_count = max(emotion_count)
    max_index = emotion_count.index(max_emotion_count)
    max_emotion = EMOTIONS[max_index]
    #returning string of the highest emotion
    return max_emotion

#Function makes a list of all commenters information in given region
def make_comments_list(filter_country, comments_file_name):
    #making main list
    comment_list = []
    comment_infile = open(comments_file_name, "r")
    comment_line = comment_infile.readline()
    #if user types specific country
    if filter_country != "all":
        while comment_line != "":
            #adding to inner dictionary all of commenters info from file
            comment_dict = {}
            comment_line = comment_line.strip()
            comment_split_line = comment_line.split(",")
            #only adding commenters from specific country
            if comment_split_line[2] == filter_country:
                comment_dict['comment_id'] = int(comment_split_line[0])
                comment_dict['username'] = comment_split_line[1]
                comment_dict['country'] = comment_split_line[2]
                comment_dict['text'] = comment_split_line[3].strip()
                #adding to main list
                comment_list.append(comment_dict)
            comment_line = comment_infile.readline()
    else:
        # if user wants all comments
        while comment_line != "":
            # adding to inner dictionary all of commenters info from file
            comment_dict = {}
            comment_line = comment_line.strip()
            comment_split_line = comment_line.split(",")
            #adding commenters from any country
            comment_dict['comment_id'] = int(comment_split_line[0])
            comment_dict['username'] = comment_split_line[1]
            comment_dict['country'] = comment_split_line[2]
            comment_dict['text'] = comment_split_line[3]
            comment_line = comment_infile.readline()
            # adding to main list
            comment_list.append(comment_dict)
    comment_infile.close()
    #returning main list
    return comment_list

#function prints total comments sentiment to file and main, reports proportions to selected file
def make_report(comment_list, keywords, report_filename):
    try:
        # checking for runtime error (if comment_list is empty)
        if not comment_list:
            raise RuntimeError("No comments in the dataset!")
        # making list counting each total sentiment from comments (order same as order in EMOTIONS)
        total_emotion_count = [0,0,0,0,0,0]
        #counter counting grand total of comments
        counter = 0
        for index in range(len(comment_list)):
            #classifying each comments emotion and adding 1 to main list depending on what emotion it is
            common_emotion = classify_comment_emotion(comment_list[index]['text'], keywords)
            emotion_index = EMOTIONS.index(common_emotion)
            total_emotion_count[emotion_index] += 1
            counter += 1
        # finding which emotion had the highest value and what index it is
        max_total_emotion_count = max(total_emotion_count)
        max_total_index = total_emotion_count.index(max_total_emotion_count)
        #finding out which emotion (string) it is
        max_total_emotion_string = EMOTIONS[max_total_index]
        #printing findings to a file user created
        emotion_outfile = open(report_filename, "w")
        emotion_outfile.write("Most common emotion: " + max_total_emotion_string + "\n\n")
        emotion_outfile.write("Emotion Totals\n")
        emotion_outfile.write("anger: " + str(total_emotion_count[0]) + " (%.2f%%)\n" %((total_emotion_count[0]/counter)*100))
        emotion_outfile.write("joy: " + str(total_emotion_count[1]) + " (%.2f%%)\n" % ((total_emotion_count[1] / counter) * 100))
        emotion_outfile.write("fear: " + str(total_emotion_count[2]) + " (%.2f%%)\n" % ((total_emotion_count[2] / counter) * 100))
        emotion_outfile.write("trust: " + str(total_emotion_count[3]) + " (%.2f%%)\n" % ((total_emotion_count[3] / counter) * 100))
        emotion_outfile.write("sadness: " + str(total_emotion_count[4]) + " (%.2f%%)\n" % ((total_emotion_count[4] / counter) * 100))
        emotion_outfile.write("anticipation: " + str(total_emotion_count[5]) + " (%.2f%%)" % ((total_emotion_count[5] / counter) * 100))
        emotion_outfile.close()
        #returning max emotion (string)
        return max_total_emotion_string
    #printing error if runtime error raised
    except RuntimeError as Error3:
        print(str(Error3))
        raise