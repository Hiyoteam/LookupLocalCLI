import requests
import tqdm
import os
import time

def stream_download(url,file):
    with open(file,"wb+") as f:
        progress=tqdm.tqdm(unit="B",unit_scale=True,unit_divisor=1024,miniters=1,desc="Downloading",ncols=100)
        for chunk in requests.get(url,stream=True).iter_content(chunk_size=1024):
            if chunk:
                progress.update(len(chunk))
                f.write(chunk)

def format_message(message):
    if message[3] and message[3] != "NONE":
        result=f"[{message[3]}]{message[2]}:\t{time.ctime(message[1])}\t#{message[0]}"
    else:
        result=f"{message[2]}:\t{time.ctime(message[1])}\t#{message[0]}"
    result+="\n"+message[5]
    return result+"\n"

def query(db,query):
    print("Initing cursor...",end="",flush=True)
    cursor=db.cursor()
    print("\rExecuting command...",end="",flush=True)
    cursor.execute(query)
    print("\rFetching executing results...")
    result=cursor.fetchall()
    print()
    return result