"""
auth: AJ Boyd (aboyd3@umbc.edu)
date: 11/1/24
desc: this script processes the cornell movie dialog dataset and organizes it in a json format. the json file has each key refer to a genre and each value is an array of movies within that genre
"""
import datasets, json
from transformers import AutoTokenizer, AutoModelWithLMHead, AutoModelForCausalLM
  
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

# download the model fine-tuned for emotional analysis
tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-emotion")
model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-emotion")

# helper function predicts the sentiment from a given string
# returns one of six emotions: joy, anger, sadness, surprise, anger, or love
def get_emotion(text):
  input_ids = tokenizer.encode(text + '</s>', return_tensors='pt')
  output = model.generate(input_ids=input_ids, max_length=2)
  dec = [tokenizer.decode(ids) for ids in output]
  label = dec[0]
  return label.split()[-1]

print("finished loading in model for emotional analysis")

genre_dict = {}
for d in dialog:
    movie_genres = d['movieGenres']
    
    for g in movie_genres:
        # if this genre, g, isn't in the genres dictionary, add it as a new key
        if g not in genre_dict:
            genre_dict[g.strip()] = {'genre': g, 'joy': 0, 'sadness': 0, 'anger': 0, 'surprise': 0, 'fear': 0, 'love': 0}
            print(f"adding {g}.")
            
print("finished adding all genres")

i = 0
for d in dialog:
    text = d['utterance']['text']
    
    # for every line of text, if that line has more than 3 words, get the emotion from that line
    for line in text:
        if len(line.split()) > 3:
            emotion = get_emotion(line)
            i += 1
            print(f"{i} -- {line} -- {emotion}")
            
            try:
                # for every genre this line of dialog belongs to, increment that emotion's frequency
                for g in d['movieGenres']:
                    genre_dict[g][emotion] += 1
            except Exception as e:
                print(f"unknown emotion {e}")
try:
    # write the data to a file, you may need to change the encoding
    with open("genre-unchunked.txt", "w", encoding="utf-8") as f:
        print(genre_dict)
        json.dump(genre_dict, f, ensure_ascii=False, indent=1)
except Exception as e:
    print(f"error: {e}")