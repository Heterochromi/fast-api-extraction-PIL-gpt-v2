from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from extractUtils import remove_extra_spaces


model_name = "silma-ai/silma-embeddding-matryoshka-0.1"
model_ar = SentenceTransformer(model_name)

# model_name = "BAAI/bge-large-en-v1.5"
model_name = "BAAI/bge-small-en-v1.5"
model_en = SentenceTransformer(model_name)

def semantic_similarity(query, sentence , lang = "en" or "ar"):
    query = remove_extra_spaces(query).lower()
    sentence = remove_extra_spaces(sentence).lower()
    if lang == "en":
        score = cos_sim(model_en.encode(query), model_en.encode(sentence))[0][0].tolist()
    else:
        score = cos_sim(model_ar.encode(query)[:768], model_ar.encode(sentence)[:768])[0][0].tolist()
    return score



