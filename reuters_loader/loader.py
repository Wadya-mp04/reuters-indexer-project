import os
from bs4 import BeautifulSoup
import re

#function i had my gen AI create to remove junk from parsed text
def clean_text(s: str) -> str:
    if not s:
        return ""
    # Remove control characters
    s = re.sub(r"[\x00-\x1F\x7F]", " ", s)
    # Remove the “Reuter” signature and trailing symbols like \x03
    s = re.sub(r"\bReuter\b", " ", s, flags=re.IGNORECASE)
    # Collapse newlines and extra spaces
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def loadReutersFiles(dir : str):
    allDocs = {}
    for fileName in sorted(os.listdir(dir)):
        if not fileName.lower().endswith((".sgm", ".sgml")):       #check and skip non-sgm files
            continue
        filePath = dir + '/' + fileName
        docs = parseFiles(filePath)                             #parse sgm files into docs 
        allDocs.update(docs)                                    #add new docs into complete doc dictionary
    return allDocs

def parseFiles(path:str):
    docs = {}                                                   #this dictionary will hold all 1000 docs in each sgm file and return it to the load func
    with open(path,'r',encoding = 'latin-1') as f:                #gen AI recommended that i encode the sgm files in latin-1
        parsedFile = BeautifulSoup(f.read(),'html.parser')      #parse the sgm file
    
    for r in parsedFile.find_all("reuters"):                          #will iterate through all reuter tags and add them to a list
        newID = r.get("newid")
        if newID is None:
            continue                                            #skip tags with no newID
        doc_id = int(newID)                                     
        text_tag = r.find('text')                                   #text tag contains title and body
        title = body = ""                        
        if text_tag:                                            #check if body or title are null
            t = text_tag.find("title")
            d = text_tag.find("dateline")
            b = text_tag.find("body")
            if t:
                title = t.get_text()
                title = clean_text(title)
            else:
                title = ""
            if b:
                body = b.get_text()
                body  = clean_text(body)
            else:
                body = ""
        else: 
            continue 
        docs[doc_id] = {                                          #create dictionary with docID as key and title/body as attributes
            "title": title,
            "body": body
        }
    return docs


