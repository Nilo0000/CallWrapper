
# Imports
from Main.helpers.import_libary import *

def getContents(url):
    # Retrieve HTML information
    response = requests.get(url)
    html_text = response.text ## Gets the entire HTML text of the website (inspect element)
    
    soup_version = BeautifulSoup(html_text, "html.parser") #All information of the text

    return soup_version.get_text(separator="", strip = True)

'''
    -- Possible new way of structuring the database
        Perhaps, we can create a few types of collections and chatgpt can decide which
        collection may be most relevant and then look through there
'''

def update_data():
    #Go to the pages collection, check if content exists and if it doesn't create a content characteristic for it
    no_content_indexes = pages_collection.find( {"content_exists" : False} ) # O(log n ) execution time

    # O(n) execution time, total is n + log(n)
    #Loop through everything, and add a "content" section with its contents
    for spec_index in no_content_indexes:
        index_url = spec_index.get("url")
        index_id = spec_index.get("_id")

        webpage_contents = getContents(index_url)
        #Now Append the contents to the spec_index characteristics
        #Now add the contents to the index
        pages_collection.update_one(    
            {"url" : index_url},
            {"$set": {"contents":webpage_contents}},
            upsert = True
        ) #end of updateOne

        #Now update the boolean
        pages_collection.update_one(    
            {"url" : index_url},
            {"$set": {"content_exists":True}},
            upsert = False
        ) #end of updateOne

        #Update the content_exists definition

def add_data_site(url):

    # Get the name (header)
    response = requests.get(url).text
    html_reader = BeautifulSoup(response, "html.parser")
    name_header = html_reader.find("h1").text

    webpage_contents = getContents(url)

    # Embeddings
    embeding_information = embed_content(webpage_contents)
    
    # Full format string
    format_string = {
        "header" : name_header,
        "url" : url,
        "content_exists" : True,
        "contents" : webpage_contents,
        "embedding" : embeding_information
    }

    # Now to insert to database
    pages_collection.insert_one(format_string)
