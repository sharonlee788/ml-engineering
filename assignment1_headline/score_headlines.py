import sys
from datetime import date
from sentence_transformers import SentenceTransformer
import joblib



#### get inputs ####

# expect:
# python score_headlines.py todaysheadlines.txt nyt

# error message if both text file and source are not given
if len(sys.argv) < 3:
    print("Usage: python score_headlines.py <input_file> <source>")
    sys.exit()

input_file = sys.argv[1]
source = sys.argv[2]

headlines = []
with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line != "":
            headlines.append(line)


#### convert to vectors ####
try:
    model = SentenceTransformer("/opt/huggingface_models/all-MiniLM-L6-v2")
except:
    model = SentenceTransformer("all-MiniLM-L6-v2")

vectors = model.encode(headlines)


#### feed vectors to SVM model and get outputs ####
svm_model = joblib.load("model/svm.joblib")
predictions = svm_model.predict(vectors)


#### write the results to file ####
today = date.today()
output_file = f"headline_scores_{source}_{today.year}_{today.month}_{today.day}.txt"

with open(output_file, "w", encoding="utf-8") as out:
    for headline, label in zip(headlines, predictions):
        out.write(str(label) + "," + headline + "\n")

print("Wrote: ", output_file)