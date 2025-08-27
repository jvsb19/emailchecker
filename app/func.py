from nlp_utils import preprocess_text

def email_classify(text: str) -> str:
    tokens = preprocess_text(text)
    print(tokens)
    produtivo_keywords = ["acesso", "ajuda", "atualização", "chamado", "contrato", "erro", "problema", "suporte"]
    improdutivo_keywords = ["abraço", "feliz", "obrigado", "parabéns"]

    if any(word in tokens for word in produtivo_keywords):
        return "Produtivo"
    elif any(word in tokens for word in improdutivo_keywords):
        return "Improdutivo"
    return "Indefinido"

def email_response(category: str) -> str:
    if category == "Produtivo":
        return "Email categorizado como Produtivo"
    return "Email categorizado como Improdutivo"

    