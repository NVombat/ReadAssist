#Import Libraries and functions
from fastapi import FastAPI
import uvicorn
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from models.savedtext import (
    get_text
)

from models.summ import (
    insert, getq
)

import time
from gtts import gTTS 
import os
import sqlite3
import re
# from sendemail import (
#     send_mail_summ, send_mail_ques
# )

from ML.wrapper import customwrapper
transformer = customwrapper()
app = FastAPI()

#SUMMARY
@app.get('/summ')
async def S(user : str):
    #Gets text from database
    text = get_text(user, "app.db")[-1][0]
    max_len = int(len(text.split(" "))*0.8)
    min_len = int(len(text.split(" "))*0.2)
    #Creates summary and limits min and max length
    summary = transformer.summarize(text, min_length=min_len, max_lenght=max_len)
    
    #Sends email with summary
    #send_mail_summ(user,summary[0]["summary_text"])
    #Inserts summary into database
    insert(user, summary[0]["summary_text"])
    #Redirects to display
    response = RedirectResponse(url='http://localhost:5000/display')
    
    return response

#Questions
@app.get('/ques')
async def Q(user : str):
    #Gets text from database
    quest = get_text(user, "app.db")[-1][0]
    templist = []
    
    quest = quest.split(" ")
    qlist = []
    fqlist = []
    li = []
    q = None
    #Runs through the text and generates every 20 words
    for i in range(len(quest)):
        templist.append(quest[i])
        if i % 20 == 0 and i != 0:
            try:
                print(' '.join(templist))
                #Generates questions and then appends to list
                q = transformer.question(' '.join(templist))
                qlist.append(q)
                
            except Exception as e:
                #Longest list of questions
                fqlist=qlist.pop()
                for di in fqlist:
                    li.append(di["question"])
                #Inserts questions into database
                insert(user, "\n".join(li))
                print(20*'-')
                templist = []
                qlist = []
                break
    #Gets questions from database
    qu = getq(user)
    #Sends mail with questions
    #send_mail_ques(user, qu[0])
    #Redirects to the DISPLAY
    response = RedirectResponse(url='http://localhost:5000/display')
    
    return response

#Converts para to speech
def convertpts(para : list):
    #For each para in the list of paragraphs
    #runs for each paragraph
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

#Voice
@app.get('/voic')
async def V(user : str):
    #Get text from database 
    text = str(get_text(user, "app.db")[-1][0])
    #Convert text to paragraphs
    para = list(filter(lambda x: x != "" and len(re.sub(r" ", "", x)) != 0, text.split('\n')))

    #Converts the text (received in paragraphs) to speech
    convertpts(para)
    #Redirects to DASHBOARD
    response = RedirectResponse(url='http://localhost:5000/dashboard')
    
    return response

if __name__ == '__main__':
    uvicorn.run(app, port=2222)