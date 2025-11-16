#******************************
#CS 1026 - Assignment 3 – Youtube Emotions
#Code by: Mark Ziza
#Student ID: mziza
#File created: November 18, 2024
#******************************
#This program imports emotions.py and uses its functions to print the results
#(more info in emotions.py summary) found for overall sentiment in specific
#countrys (or all) comment section.
#This program also guards against varius user inputs that would otherwise
#make the program crash.

import os.path
from emotions import *

#options of countries user can type
VALID_COUNTRIES = ['bangladesh', 'brazil', 'canada', 'china', 'egypt',
                   'france', 'germany', 'india', 'iran', 'japan', 'mexico',
                   'nigeria', 'pakistan', 'russia', 'south korea', 'turkey',
                   'united kingdom',  'united states','all']

#function asks user for varius file names going to be used in later functions (guards against bad inputs)
def ask_user_for_input():
    #guarding for the user entered file name for the keywords
    keyword_filename = input("Input keyword file (ending in .tsv):")
    if not keyword_filename.endswith(".tsv"):
        raise ValueError("Keyword file does not end in .tsv!")
    elif not os.path.exists(keyword_filename):
        raise FileNotFoundError(keyword_filename + " does not exist!")

    # guarding for the user entered file name for the commenters info
    comment_filename = input("Input comment file (ending in .csv):")
    if not comment_filename.endswith(".csv"):
        raise ValueError("Comments file does not end in .csv!")
    elif not os.path.exists(comment_filename):
        raise FileNotFoundError(comment_filename + " does not exist!")

    # guarding for the user entered country name
    country_name = input('Input a country to analyze (or "all" for all countries):')
    country_name = country_name.lower()
    if not country_name in VALID_COUNTRIES:
        raise ValueError(country_name + " is not a valid country to filter by!")

    # guarding for the user entered file name for the report file they will make
    report_filename = input("Input the name of the report file (ending in .txt):")
    if not report_filename.endswith(".txt"):
        raise ValueError("Report file does not end in .txt!")
    elif os.path.exists(report_filename):
        raise FileNotFoundError(report_filename + " already exists!")

    #making tuple of all names collected
    key_info = (keyword_filename, comment_filename, country_name, report_filename)
    #returning tuple
    return key_info

#main function that uses all other functions in unison
def main():
    try:
        #using function above to look for invalid inputs (if there is user enters info again)
        total_info = ask_user_for_input()
    except ValueError as Error:
        print(Error)
        main()
    except FileNotFoundError as Error2:
        print(Error2)
        main()
    else:
        #calling function from emotions.py
            key_dict = make_keyword_dict(total_info[0])
            comment_list = make_comments_list(total_info[2], total_info[1])
            try:
                #checking for runtime error in make_report function
                if not comment_list:
                    raise RuntimeError("No comments in the dataset!")
                total_max_emotion = make_report(comment_list, key_dict, total_info[3])
                print("Most common emotion is: " + total_max_emotion)
            except RuntimeError as Error3:
                print(str(Error3))

#calling main function
if __name__ == "__main__":
    main()