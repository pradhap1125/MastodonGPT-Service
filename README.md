#Install Ollama first to run this project :
#https://ollama.com/download

#Pull llama3 and paraphrase-multilingual model 
    #ollama pull llama3
#ollama pull paraphrase-multilingual-MiniLM-L12-v2

#To install all required dependencies:
#pip install -r requirements.txt

# To refresh the app with new dependencies:
#poetry lock
#poetry update
#poetry sync

# Update the poetry.lock and pyproject.toml files to include any other dependencies if needed

#To build : 
#poetry build

# To run the application locally using waitress after installing whl file:
# waitress-serve --port=5000 mastodongpt.app:app

# To run the application from an IDE:
# app.py


