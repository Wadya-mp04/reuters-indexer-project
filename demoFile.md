Before running the demo, please ensure the following setup steps are completed:

Install dependencies

pip install nltk beautifulsoup4

Then initialize NLTK data (for word_tokenize, RegexpTokenizer, and stopwords):

import nltk
nltk.download('punkt')
nltk.download('stopwords')

Reuters dataset

Make sure you have the Reuters-21578 .sgm files downloaded and extracted.

Update the file path inside reuters_loader/**init**.py:

REUTERS_PATH = "PATH/TO/YOUR/reuters/sgm"

⚠️ Replace this with the local absolute path to the folder that contains your .sgm files.

Driver model

You don’t need to execute each file individually.

The project follows a driver-class structure, where main.py imports and orchestrates all components (tokenizer, indexers, compression, etc.).

You can reproduce all results (Naïve vs SPIMI, query processing, compression table) simply by running:

python main.py
