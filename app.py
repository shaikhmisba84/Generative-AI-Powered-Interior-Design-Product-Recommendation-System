import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
from string import punctuation
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
nltk.download("averaged_perceptron_tagger")
import pandas as pd
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route('/api/data', methods=['GET'])
@cross_origin()
def get_data():
    return jsonify({'message': 'This is a protected API endpoint'})


df = pd.read_csv("product_data.csv")
english_stopwords = stopwords.words('english')
lemmatizer = WordNetLemmatizer()

def clean_text(input_tags):
    tokens = word_tokenize(input_tags.lower())
    clean_tokens = [token for token in tokens if token not in english_stopwords and token not in punctuation]
    clean_tokens = [lemmatizer.lemmatize(token, pos="n") for token in clean_tokens]
    clean_tokens = [lemmatizer.lemmatize(token, pos="v") for token in clean_tokens]
    clean_tokens = [lemmatizer.lemmatize(token, pos="a") for token in clean_tokens]
    return ", ".join(clean_tokens)


def get_product_recommendations(tags):
    recommendations = [
        product for product in df.to_dict(orient='records') if any(tag in product["Product Tags"] for tag in tags)
    ]
    return recommendations

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input_tags = request.form.get("tags")
        cleaned_tags = clean_text(input_tags)
        tags_list = cleaned_tags.split(", ")
        recommendations = get_product_recommendations(tags_list)
        return render_template("results.html", recommendations=recommendations)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
