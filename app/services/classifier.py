<<<<<<< HEAD
from transformers import pipeline 
import torch

classifier = pipeline( 
    "zero-shot-classification", 
    model="facebook/bart-large-mnli", 
    device=0 if torch.cuda.is_available() else -1 
) 

produtivo_labels = {
    "work", "help", "urgency", "refund", "technical support", "system acess", "system problem", "work budget", "error"
}

improdutivo_labels = {
    "non-work","congratulations", "joke", "automatic", "invitation", "personal", "greet", "vacation", "break", "checklist", "spam", "thank", "opinion"
}

def email_classify(text): 
    text_lower = text.lower() 

    resultado = classifier( 
        text_lower, 
        candidate_labels=list(produtivo_labels | improdutivo_labels), 
        hypothesis_template="This email is about {}."
    )

    if resultado["labels"][0] in produtivo_labels:
        return "Produtivo"
    return "Improdutivo"

def email_response(category): 
    if category == "Produtivo": 
        return "Esse e-mail requer uma ação ou resposta imediata." 
    elif category == "Improdutivo": 
        return "Esse e-mail não requer uma ação ou resposta imediata." 
    return "Indefinido"
=======
from dotenv import load_dotenv
from transformers import pipeline
import torch

load_dotenv()
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    device=0 if torch.cuda.is_available() else -1
)

def email_classify(text):
    
    text_lower = text.lower()
    
    resultado = classifier(
        text_lower,
        candidate_labels=["urgente", "não urgente"],
        hypothesis_template="This email is {}."
        )

    if resultado["labels"][0] == "urgente":
        return "Produtivo"
    return "Improdutivo"
            
>>>>>>> 63b72b2 (classifier funcional)
