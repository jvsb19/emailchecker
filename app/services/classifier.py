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
        candidate_labels=["social", "opiniativo", "festivo", #Improdutivos
                        "urgente", "manutenção", "problema"],#Produtivos
        hypothesis_template="This email is {}."
        )
    print(resultado)

    if resultado["labels"][0] == "urgente" or resultado["labels"][0] == "manutenção" or resultado["labels"][0] == "problema" or resultado["labels"][0] == "reunião":
        return "Produtivo"
    return "Improdutivo"
            