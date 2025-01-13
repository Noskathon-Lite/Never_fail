from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import pytesseract

import io

app = Flask(__name__)

# MongoDB connection
def get_db_connection():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["plagchecker"]
    return db

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    data = request.json
    user_input = data.get("text", "").strip()
    if not user_input:
        return jsonify({"error": "Input text is required"}), 400

    db = get_db_connection()
    collection = db["testdata"]

    # Fetch saved texts
    saved_texts = [doc['text'] for doc in collection.find()]
    all_texts = saved_texts + [user_input]

    # TF-IDF and Cosine Similarity
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    similarity_matrix = cosine_similarity(tfidf_matrix)

    # Get user similarity
    user_similarity = similarity_matrix[-1][:-1]
    max_similarity = max(user_similarity) * 100 if user_similarity.size > 0 else 0

    # Save user input
    collection.insert_one({"text": user_input})
    return jsonify({"similarity": max_similarity})

@app.route('/extract-text', methods=['POST'])
def extract_text():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded."}), 400
    
    image_file = request.files['image']
    
    try:
        img = Image.open(io.BytesIO(image_file.read()))
        text = pytesseract.image_to_string(img)
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)