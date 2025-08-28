from transformers import pipeline
import torch

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
            