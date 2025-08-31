import re

_PT_STOP = {
    "a","o","e","é","de","do","da","dos","das","um","uma","uns","umas",
    "para","por","com","sem","em","no","na","nos","nas","ao","à","às",
    "que","se","são","ser","foi","era","as","os","lo","la","lhe","eles","elas",
    "eu","tu","você","vocês","nós","meu","minha","meus","minhas","seu","sua",
    "seus","suas","este","esta","isso","aquele","aquela","isto","aquilo",
    "depois","antes","então","também","não","sim","mais","menos","muito",
    "pouco","já","ainda"
}

def preprocess_text(text: str):
    text = (text or "").lower()
    text = re.sub(r"[^a-z0-9á-úà-ùâ-ûã-õç\s]", " ", text)
    tokens = [t for t in text.split() if t not in _PT_STOP and len(t) > 2]
    return tokens