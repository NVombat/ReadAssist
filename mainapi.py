from fastapi import FastAPI 
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from models.savedtext import (
    getsummary

)

from models.summ import (
    insert
)

import time
from gtts import gTTS 
import os
import sqlite3
import re
from sendemail import (
    send_mail_summ, send_mail_ques
)

from ML.wrapper import customwrapper
transformer = customwrapper()
app = FastAPI()


@app.get('/summ')
async def S(user : str):

    text = getsummary(user, "app.db")[-1][0]
    max_len = int(len(text.split(" "))*0.5)
    min_len = int(len(text.split(" "))*0.2)
    summary = transformer.summarize(text, min_length=min_len, max_lenght=max_len)
    
    send_mail_summ(user,summary[0]["summary_text"])
    insert(user, summary[0]["summary_text"])
    response = RedirectResponse(url='http://localhost:5000/display')
    
    return response

@app.get('/ques')
async def Q(user : str):
    quest = getsummary(user, "app.db")[-1][0]
    templist = []
    
    quest = quest.split(" ")
    qlist = []
    fqlist = []
    li = []
    q = None
    for i in range(len(quest)):
        templist.append(quest[i])
        if i % 20 == 0 and i != 0:
            try:
                print(' '.join(templist))
                q = transformer.question(' '.join(templist))
                print(q)
                qlist.append(q)
                
            except Exception as e:
                fqlist=qlist.pop()
                print("THIS IS THE LONGEST SET OF Q/A: ", fqlist)
                for di in fqlist:
                    #print(di["question"])
                    li.append(di["question"])
                #print("TYPE - FQLIST: ", type(fqlist))
                insert(user, "\n".join(li))
                print(20*'-')
                templist = []
                qlist = []
                break
    
    #send_mail_ques(user, )
    response = RedirectResponse(url='http://localhost:5000/display')
    
    return response


def convertpts(para : list):
    #For each para in the list of paragraphs
    for p in para:
        #Convert the paragraph to an audio file which gets overwritten for each para
        language = 'en'
        myobj = gTTS(text=p, lang=language, slow=False) 
        myobj.save("testaudio.mp3")
        #Play it from system
        os.system("mplayer testaudio.mp3")

        #Pause before next paragraph and ask if it should continue
        np = "Next Paragraph... Should I continue?"
        myobj1 = gTTS(text=np, lang=language, slow=False) 
        myobj1.save("next.mp3")
        os.system("mplayer next.mp3")
        #Wait for 2.5 seconds
        time.sleep(2.5)


@app.get('/voic')
async def V(user : str):
    text = str(getsummary(user, "app.db")[-1][0])
    #print(text)
    para = list(filter(lambda x: x != "" and len(re.sub(r" ", "", x)) != 0, text.split("\n\n")))

    #Converts the text (received in paragraphs) to speech
    convertpts(para)

    response = RedirectResponse(url='http://localhost:5000/dashboard')
    
    return response