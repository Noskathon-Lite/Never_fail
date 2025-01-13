import tkinter as tk
from tkinter import scrolledtext, messagebox
from pymongo import MongoClient
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# MongoDB connection
def get_db_connection():
    """
    Connect to the MongoDB database.
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["plagchecker"]  # Replace with your database name
    return db

def check_plagiarism(user_input, collection):
    """
    Check plagiarism of the user input against documents in the database.

    Args:
        user_input (str): The text entered by the user.
        collection: The MongoDB collection to fetch saved texts.

    Returns:
        float: The highest plagiarism percentage found in the database.
    """
    # Fetch all saved texts from the database
    saved_texts = [doc['text'] for doc in collection.find()]
    
    # Include user input with the saved texts for comparison
    all_texts = saved_texts + [user_input]
    
    # Compute TF-IDF vectorization
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    # Compute cosine similarity
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    # Extract the last row (user input similarity with other texts)
    user_similarity = similarity_matrix[-1][:-1]
    
    # Calculate the highest similarity percentage
    max_similarity = max(user_similarity) * 100 if user_similarity.size > 0 else 0
    return max_similarity

def on_check_plagiarism():
    """
    Handle the 'Check Plagiarism' button click event.
    """
    user_input = text_input.get("1.0", tk.END).strip()
    if not user_input:
        messagebox.showwarning("Input Error", "Please enter some text to check plagiarism.")
        return
    
    db = get_db_connection()
    collection = db["testdata"]  # Replace with your collection name
    
    # Check plagiarism
    max_similarity = check_plagiarism(user_input, collection)
    messagebox.showinfo("Plagiarism Result", f"Plagiarism detected: {max_similarity:.2f}%")
    
    # Optionally save user input to the database
    collection.insert_one({"text": user_input})

# UI Setup
app = tk.Tk()
app.title("Plagiarism Checker")
app.geometry("600x400")

# Label
label = tk.Label(app, text="Enter text below to check for plagiarism:", font=("Arial", 14))
label.pack(pady=10)

# Text Input
text_input = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=70, height=10, font=("Arial", 12))
text_input.pack(pady=10)

# Check Button
check_button = tk.Button(app, text="Check Plagiarism", command=on_check_plagiarism, font=("Arial", 12), bg="blue", fg="white")
check_button.pack(pady=20)

# Start the UI loop
app.mainloop()
