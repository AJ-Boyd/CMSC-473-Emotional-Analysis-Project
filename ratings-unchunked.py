"""
auth: AJ Boyd
desc: once you've got a json file, we can start our emotional analysis. 
this script iterates through each movie dialogue in each genre then records the emotion evoked from that dialogue.
this data is recorded and stored in a different json file. the data can be visuallized with a graph.
WARNING: this stuff takes a loooooooong time.
"""

from transformers import AutoTokenizer, AutoModelWithLMHead, AutoModelForCausalLM
import json

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

with open("ratings_dict.txt", "r", encoding="utf-8") as f:
    rating_dict = json.load(f)
print('dictionary loaded in')

emotions_by_rating = []
i = 0

for rating in rating_dict:
    # build a dictionary that holds the counts for every emotion per genre    
    emotion_dict = {'rating': rating, 'joy': 0, 'sadness': 0, 'anger': 0, 'surprise': 0, 'fear': 0, 'love': 0}

    # get every text interaction for the genre
    for dialog_dict in rating_dict[rating]:
        try:
            # text = "\n".join(dialog_dict['utterance']['text'])
            # get every single line of dialog (with more than 3 words)
            for t in dialog_dict['utterance']['text']:
                if len(t.split()) > 3:
                    emotion = get_emotion(t) # get the analyzed emotion from that interaction
                    emotion_dict[emotion] += 1 # increase the count of that emotion by 1   
                    i += 1
                    print(f"{i}--{t}")
        except Exception as e:
            print(f"error getting sentiment \ntext: {t}\nerror: {e}") 
    
    
    emotions_by_rating.append(emotion_dict)


# write to file
try:
    with open("genre-unchunked.txt", "w", encoding="utf-8") as f:
        json.dumps(emotions_by_rating, f, ensure_ascii=False, indent=1)
except Exception as e:
    print(f"error: {e}")
   
        