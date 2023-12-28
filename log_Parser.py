from urllib.parse import unquote
import base64
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
import gzip
from io import BytesIO
import csv
filepath = "logfile.log"

def log_Parser(filepath):
    result={}
    try:
        with open(filepath):
            pass
    except:
        print("unable to open the file :",filepath)

    tree = ET.parse(filepath)
    root = tree.getroot()
    for request in root.findall('item'):
            raw_req=request.find('request').text
            raw_req = unquote(raw_req)
            raw_res=request.find('response').text
            result[raw_req]=raw_req
    return result

def builder(rawreq):
    try:
        raw = rawreq.decode(encoding='utf-8')
    
       
        
    except:
        raw = rawreq
    global headers,body,methode,path
    headers={}
    sp=raw.split('\n\n',1)
    if len(sp) > 1:
            head=sp[0]
            body=sp[1]
    else:
            head=sp[0]
            body=""
    c1 = head.split('\n', head.count('\n'))
    
    # Print the content of c1 for debugging
    print("c1:", c1)
    
    if c1:
        method = c1[0].split(' ', 2)[0]
        
        # Print the content of c1[0] for debugging
        
        # Check if there are enough elements after the split
        if len(c1[0].split(' ', 2)) > 1:
            path = c1[0].split(' ', 2)[1]
        else:
            path = ""
        
        # Print the content of path for debugging
        print("path:", path)
        
        for i in range(1, len(c1)):
            slice1 = c1[i].split(': ', 1)
            if slice1[0] != "":
                try:
                    headers[slice1[0]] = slice1[1]
                except:
                    pass
    return(headers,method,body,path)
f=open("httplogfile.csv","w")
c=csv.writer(f)
c.writerow(["methode","body","path","headers"])
f.close()
            
result = log_Parser(filepath)

for item in result:
    data=[]
    decoded_request = base64.b64decode(item)

    # Check if the response is gzip compressed
    if result[item].startswith('\x1f\x8b'):
        compressed_response = base64.b64decode(result[item])
        decompressed_response = gzip.decompress(compressed_response).decode('utf-8')
    else:
        # If not compressed, assume it's a regular base64-encoded string
        decompressed_response = base64.b64decode(result[item])
    # Parse HTML response using BeautifulSoup
    soup = BeautifulSoup(decompressed_response, 'html.parser')
    formatted_response = soup.prettify()
    headers,method,body,path= builder(decoded_request)

    data.append(method)
    data.append(body)
    data.append(path)
    data.append(headers)
    f=open("httplogfile.csv","a")
    c=csv.writer(f)
    c.writerow(data)
    f.close
