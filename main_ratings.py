"""
auth: AJ Boyd (aboyd3@umbc.edu)
date: 11/1/24
desc: this script processes the cornell movie dialog dataset and organizes it in a json format. 
the json file has each key refer to a rating range and each value is an array of movies within that rating range
"""
import datasets, json
  
# import the Cornell movie dialog dataset
dataset = datasets.load_dataset(trust_remote_code=True, path="cornell_movie_dialog")
dialog = list(dataset['train']) # gotta cast dis as a list to manipulate it 

# since the dataset uses ID markers instead of plaintext strings for its dialog, we have to do a lil bit of parsing
movie_lines_filepath = "corpus_files/movie_lines.txt" # filepath to plaintext movie lines
DELIMITER = ' +++$+++ '
line_text = {} # a dictionary where the key is the Line ID and the value is the text associated with it

# populate line_text dictionary
with open(movie_lines_filepath, 'r') as f:
    for line in f:
        fields = line.split(DELIMITER)
        if len(fields) == 5:
            line_id = fields[0].strip()
            text = fields[4].strip()
            line_text[line_id] = text

# once we get the dialog associated with the IDs, we update each instance of the dataset
for d in dialog:
    dialog_lines = [line_text.get(line_id, "xxx") for line_id in d['utterance']['LineID']]
    d['utterance']['text'] = dialog_lines

print("finished updating dialog text")
# analysis 1: examine the correlation of movie genre to the proportion of emotions in its dialog 
# for now, we analyze each line of dialog separately. later, we might do some sort of overlap to get the sentiment of back-and-forth conversation

# first, we organize each movie by rating range
# a dictionary where the key is the movie rating and the key is a list of movies that are a part of it
# Bad = 0-4.9, Average = 5-7.9, Good:8-10
ranges = {"bad": [], "average": [], "good": []} 
print(f"reading through {len(dialog)} conversations")
i = 0
for d in dialog:
    movie_rating = float(d["movieIMDBRating"])
    if movie_rating >= 0 and movie_rating < 4:
        ranges['bad'].append(d)
    elif movie_rating >= 4 and movie_rating < 7.5:
        ranges['average'].append(d)
    elif movie_rating >= 7.5:
        ranges['good'].append(d)

try:
    # write the data to a file
    with open("ratings_dict.txt", "w", encoding="utf-8") as f:
        json.dump(ranges, f, ensure_ascii=False, indent=1)
except Exception as e:
    print(f"error: {e}")
