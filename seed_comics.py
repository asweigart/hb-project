from model import Publisher, Book, connect_to_db, db
from server import app
from datetime import datetime
import os
import re
import json

# root_dir = raw_input("Enter File Path: ")
# root_dir = "C:\Users\Paola\Desktop\Comic Test"
root_dir=""




def walk_files(root_dir):
    """walk the specified directory and get the file names within that directory"""

    data_files ={}

    name=""
    year=""
    issue=""
    ext=""
    end = ('.db','.jpg','.png') #EXTENSIONS TO IGNORE


    for root, dirs, files in os.walk(root_dir):
        print "Root Directory: ",root 
        print "Directories in Root: ",dirs
        data_files['root'] = root
        data_files['comics'] = []
        # data_files[key]=files
        for counter, i in enumerate(files):
            """
            # USE REGEX TO GET name, year, issue, file extension from file name.
            FIX ME:: Don't include parens in year

            FIX ME: REMOVE _ and - from name etc.
            """
            print "A file: ",counter, i
            n = re.compile(r'([a-zA-Z-:_(\s)]+)')
            y = re.compile(r'(\(\d\d\d\d\))')
            iss = re.compile(r'(.art\s\d)|(.art\d)|(.art_\d)|(\d\d\d)|(\d\d)|(\d)')
            e = re.compile(r'(.cb.)')
            #CHECK FOR non-comic file formats and ignore
            if i.endswith(end):
                print "not a comic file"
                name=""
                year=""
                issue=""
                ext=""
            else:
                """
                #TRY TO RETRIEVE THE group from regex
                #ELSE  print not enough data. 
                FIX ME:: Retrieve what data can be found, give empty strings for the rest
                """
                try:
                    name = n.search(i).group()
                    year = y.search(i).group()
                    issue = iss.search(i).group()
                    ext = e.search(i).group()
                    data_files['comics'].append({
                            'name':name,
                            'issue_number':issue,
                            'year':year,
                            'extension':ext,
                            'file':i})
                    # import pdb; pdb.set_trace()
                except AttributeError:
                   print "not enough data"

            print " "
            print "Title: ",name, "Issue: ",issue,"Year: ",year,"FileType: ",ext
            print " "

    return data_files


def seed_publishers():
    pub_file = open("seed_data/comic_publishers.txt") # Open file

    for line in pub_file:
        #split into strings
        line = line.rstrip()
        publisher = Publisher(name=line)

        db.session.add(publisher)
    db.session.commit()

    print "Publishers seeded "
    pub_file.close()


if __name__ == "__main__":
    connect_to_db(app)
    print "Connected to db"


    # walk_files(root_dir)
    seed_publishers()




#MATCHES THE ISSUE NUMBER
# (.art\s\d)|(.art\d)|(\d\d\d)|(\d\d)|(\d)

   # m = re.search('([a-zA-Z-:_(\s)]+)','\(\d\d\d\d\)','\(.*\)','(.cb.)')
