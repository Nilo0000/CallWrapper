
from import_libary import *

def embed_content(content):

    ## Now embed it using openai
    embedded_final = openAI_Client.embeddings.create(
        input = content,
        model = "text-embedding-3-small"
    ) # This gets the embedding

    # Return that embedding
    return embedded_final.data[0].embedding

def textify_embed(embed_list):
            
    string_of = ", ".join(str(f) for f in embed_list)
    print(string_of)