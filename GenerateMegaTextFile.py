import re
import requests
import zipfile
import io
from datasets import load_dataset
import pickle
import os

MEGA_TEXT_PATH = "mega_text.txt"

#To remove XML tags from text
def removeXML(text):
    return re.sub(r"<[^>]+>", "", text)

#Create large text file of the English language through various mediums
def generateMegaText():
    with open(MEGA_TEXT_PATH, "w", encoding="utf-8") as outfile:
        #Segment 1: Enwik9
        print("Downloading enwik9")
        try:
            urlEnwik9 = "https://ia801809.us.archive.org/23/items/enwik9/enwik9.zip"
            response = requests.get(urlEnwik9)
            response.raise_for_status()
            #Extract enwik9 text from zip
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                with z.open("enwik9") as f:
                    enwik9Text = f.read().decode("utf-8", errors="ignore")
                    enwik9Text = removeXML(enwik9Text)
                    print("Added enwik9")
                    outfile.write(enwik9Text + "\n")
        except Exception as e:
            print("Error downloading or processing enwik9:", e)

        #Segment 2: Gutenberg books
        gutenbergIds = [84, 2701, 1342, 42, 2389, 4214, 1289, 1, 21, 123]
        #Loop through random list of Gutenberg book ids to be added
        for id in gutenbergIds:
            #Book url with id
            bookURL = f"https://www.gutenberg.org/files/{id}/{id}-0.txt"
            print(f"Downloading Gutenberg book {id} from {bookURL}")
            try:
                r = requests.get(bookURL)
                if r.status_code == 200:
                    print(f"Added Gutenberg book {id}")
                    outfile.write(r.text + "\n")
                else:
                    print(f"Gutenberg fail {id}. Status code: {r.status_code}")
            except Exception as e:
                print(f"Error gutenberg {id}:", e)

        #Segment 3: English langauge datasets
        datasetsData = [
            ("stanfordnlp/imdb", None),
            ("Yelp/yelp_review_full", None),
            ("sentence-transformers/agnews", None),
            ("nthngdy/ccnews_split", "plain_text")
        ]

        #Load and add each large language model from Huggingface
        for modelName, modelConfig in datasetsData:
            print(f"Loading dataset {modelName}")
            try:
                #Load dataset with config if config exists
                dataset = load_dataset(modelName, modelConfig, split="train") if modelConfig else load_dataset(modelName, split="train")

                #If 'text' (the standard column for the text data) does not exist, 
                textColExists = "text" if "text" in dataset.column_names else None
                for entry in dataset:
                    #If 'text' (the standard column for the text data) exists, append that
                    if textColExists:
                        text = entry.get(textColExists, "").strip()
                    #Otherwise, concatenate every column into a single string separated by ". "
                    else:
                        text = ". ".join(str(entry[col]) for col in dataset.column_names if entry.get(col)).strip()

                    #If data from columns found, add to file
                    if text and text != ".":
                        outfile.write(text + "\n")
            except Exception as e:
                print(f"Error loading {modelName}: {e}")

        print("Mega file complete")

#Serializers for average code (map)
def serializeAverageCode(data):
    filename = "averageCode.pickle"
    with open(filename, "wb") as file:
        pickle.dump(data, file)
    print(f"Map serialized to {filename}. Size: {os.path.getsize(filename)} bytes")

def deserializeAverageCode():
    filename = "averageCode.pickle"
    with open(filename, "rb") as file:
        data = pickle.load(file)
    return data




