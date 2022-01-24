#Imports
from fastapi.responses import RedirectResponse
from ML.wrapper import customwrapper
from fastapi import FastAPI
from gtts import gTTS
import uvicorn
import time
import os
import re

from models.savedtext import (
    get_text
)
from models.summ import (
    insert,
    getq
)
# from sendemail import (
#     send_mail_summ,
#     send_mail_ques
# )

transformer = customwrapper()
app = FastAPI()

#SUMMARY
@app.get('/summ')
async def S(user : str):
    text = get_text(user, "app.db")[-1][0]
    max_len = int(len(text.split(" "))*0.8)
    min_len = int(len(text.split(" "))*0.2)

    summary = transformer.summarize(text, min_length=min_len, max_lenght=max_len)

    #Sends email with summary
    #send_mail_summ(user,summary[0]["summary_text"])
    insert(user, summary[0]["summary_text"])

    response = RedirectResponse(url='http://localhost:5000/display')
    return response

#Questions
@app.get('/ques')
async def Q(user : str):

    quest = get_text(user, "app.db")[-1][0]
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
                qlist.append(q)

            except Exception as e:

                fqlist=qlist.pop()
                for di in fqlist:
                    li.append(di["question"])

                insert(user, "\n".join(li))
                templist = []
                qlist = []
                break

    qu = getq(user)
    #send_mail_ques(user, qu[0])

    response = RedirectResponse(url='http://localhost:5000/display')
    return response

#Converts para to speech
def convertpts(para : list):
    for p in para:
        language = 'en'
        myobj = gTTS(text=p, lang=language, slow=False) 
        myobj.save("testaudio.mp3")
        os.system("mplayer testaudio.mp3")

        np = "Next Paragraph... Should I continue?"
        myobj1 = gTTS(text=np, lang=language, slow=False) 
        myobj1.save("next.mp3")
        os.system("mplayer next.mp3")
        time.sleep(2.5)

#Voice
@app.get('/voic')
async def V(user : str):
    text = str(get_text(user, "app.db")[-1][0])
    para = list(filter(lambda x: x != "" and len(re.sub(r" ", "", x)) != 0, text.split('\n')))

    convertpts(para)
    response = RedirectResponse(url='http://localhost:5000/dashboard')
    return response

if __name__ == '__main__':
    uvicorn.run(app, port=2222)