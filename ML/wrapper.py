#Encapsulates all models
#Caches the models and uses the preexisting model instead of reloading it
from .OCR import get_text
from .ptt import get_pdf
import pytesseract 
from .question import secondary_pipeline
from transformers import pipeline

class customwrapper():
    def __init__(self):
        self.questionmodel = None
        self.summarizemodel = None
        self.tessearct = None
        self.generatemodel = None
        
    def question(self, text : str):
        if self.questionmodel == None:
            self.questionmodel = secondary_pipeline('question-generation')

        return self.questionmodel(text)

    def summarize(self, text : str, min_length, max_lenght ):
        if self.summarizemodel == None:
            self.summarizemodel = pipeline('summarization')
        return self.summarizemodel(text, min_length=min_length, max_lenght=max_lenght)

    def generate_text(self, text : str):
        
        if self.generatemodel == None:
            self.generatemodel = pipeline('text2text-generation')
        return self.generatemodel(text)

if __name__ == '__main__':
    # gpt = pipeline('text-generation', model='gpt')
    trans = cutomwrapper()
    text = '''
    The physical nature of time is addressed by general relativity with respect to events in space-time. Examples of events are the collision or two particles, the explosion of a supernova, or the arrival of a rocket ship. Every event can be assigned four numbers representing its time and position (the event's coordinates). However, the numerical values are different for different observers. In general relativity, the question of what time it is now only has meaning relative to a particular observer. Distance and time are intimately related and the time required for light to travel a specific distance is the same for all observers, as first publicly demonstrated by Michelson and Morley. General relativity does not address the nature of time for extremely small intervals where quantum mechanics holds. At this time, there is no generally accepted theory of quantum general relativity.
    '''
    print(trans.question(text=text))