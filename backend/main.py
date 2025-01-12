import tkinter as tk
from tkinter import filedialog
from PIL import Image
import pytesseract
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Set the path for Tesseract executable (if required)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust this path for your system

# Function to extract text from image
def extract_text_from_image():
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        text_box1.delete(1.0, tk.END)  # Clear existing text
        text_box1.insert(tk.END, text)  # Insert extracted text

# Function to check plagiarism
def check_plagiarism():
    text1 = text_box1.get(1.0, tk.END).strip()
    text2 = text_box2.get(1.0, tk.END).strip()
    
    if not text1 or not text2:
        result_label.config(text="Please enter text in both boxes", fg="red")
        return
    
    # Use Cosine Similarity to check similarity
    vectorizer = CountVectorizer().fit_transform([text1, text2])
    similarity_matrix = cosine_similarity(vectorizer[0:1], vectorizer[1:2])
    
    similarity_percentage = similarity_matrix[0][0] * 100  # Convert to percentage
    if similarity_percentage > 80:
        result_label.config(text=f"Similarity: {similarity_percentage:.2f}% - High Plagiarism", fg="red")
    elif similarity_percentage > 50:
        result_label.config(text=f"Similarity: {similarity_percentage:.2f}% - Moderate Plagiarism", fg="orange")
    else:
        result_label.config(text=f"Similarity: {similarity_percentage:.2f}% - Low Plagiarism", fg="green")

# Create Tkinter window
root = tk.Tk()
root.title("Plagiarism Checker")

# Set window size
root.geometry("600x600")

# Create Text Boxes for input
text_box1_label = tk.Label(root, text="Enter text or upload an image for text extraction:")
text_box1_label.pack(pady=5)

text_box1 = tk.Text(root, height=6, width=50)
text_box1.pack(pady=10)

# Add Image Upload Button
image_upload_button = tk.Button(root, text="Upload Image", command=extract_text_from_image)
image_upload_button.pack(pady=5)

# Create Second Text Box for comparison text
text_box2_label = tk.Label(root, text="Enter second text to check plagiarism against:")
text_box2_label.pack(pady=5)

text_box2 = tk.Text(root, height=6, width=50)
text_box2.pack(pady=10)

# Create Check Plagiarism Button
check_button = tk.Button(root, text="Check Plagiarism", command=check_plagiarism)
check_button.pack(pady=20)

# Create Result Label
result_label = tk.Label(root, text="Result will appear here", font=("Arial", 14))
result_label.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
