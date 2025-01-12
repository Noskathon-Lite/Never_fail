import os

def load_documents(path: str, file_extension: str = '.txt'):
    """
    Load text documents from the specified directory.
    Args:
        path (str): Path to the directory containing documents.
        file_extension (str): The file extension to filter by (default is .txt).
    Returns:
        List[str]: A list containing the contents of each document.
    """
    documents = []
    
    if not os.path.isdir(path):
        raise ValueError(f"The provided path '{path}' is not a valid directory.")
    
    for filename in os.listdir(path):
        if filename.endswith(file_extension):
            try:
                with open(os.path.join(path, filename), 'r', encoding='utf-8') as file:
                    documents.append(file.read())
            except Exception as e:
                print(f"Error reading file {filename}: {e}")
    
    return documents
