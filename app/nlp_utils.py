import re
import spacy

nlp = spacy.load("pt_core_news_sm")

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Zá-úÁ-Ú\s]", "", text)
    doc = nlp(text)
    
    tokens = [
    token.lemma_ for token in doc 
        if not token.is_stop and not token.is_punct and len(token.lemma_) > 2
    ]

    return tokens
