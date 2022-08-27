import pickle
import pandas as pd
from nltk import word_tokenize, PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
import re
import contractions

## models and  path
Y_LABEL_ENCODER_PATH = "./y_label_encoder.pkl"
PRODUCT_PREDICTION_MODEL_PATH = "./model.pkl"
COUNT_VECTORIZER_PATH = "./countVectorizer.pkl"
TF_IDF_TRANSFORMER_PATH = "./tfidf_transformer.pkl"

## loading models and encoders
Y_LABEL_ENCODER = pickle.load(open(Y_LABEL_ENCODER_PATH , "rb"))
PRODUCT_PREDICTION_MODEL = pickle.load(open(PRODUCT_PREDICTION_MODEL_PATH , "rb"))
COUNT_VECTORIZER = pickle.load(open(COUNT_VECTORIZER_PATH , "rb"))
TF_IDF_TRANSFORMER = pickle.load(open(TF_IDF_TRANSFORMER_PATH , "rb"))


stemmer = PorterStemmer()
stop_words = stopwords.words('english')


class TextPreprocessing:
    def __init__(self, countVectorizer , tfidf_transformer, y_label_encoder) -> None:
        self.countVectorizer = countVectorizer
        self.tfidf_transformer = tfidf_transformer
        self.y_label_encoder = y_label_encoder


    def preprocess(self, data):
        X = data["Consumer complaint narrative"].apply(self.text_cleaning)
        X = self.countVectorizer.transform(X)
        X = self.tfidf_transformer.transform(X)
        X = X.toarray()
        
        return X


    def text_cleaning(self, text : str) -> str:
        '''
        description:
            it clean the text
            - change to lower case
            - remove the numerical numbers
            - remove newline symbols , special symbols, whitespace
            - transforming every tokens into it's stem form
            - expanding the contractions
        '''
        text = text.lower()
        
        # change numerical money to 'money' 
        text = re.sub("\$[0-9.]+","dollar money",text)
        # removing the newline symbols '\n'
        text = re.sub("\n"," ",text)

        #changing format of dates
        text = re.sub("[0-9x]+/[0-9x]+/[0-9x]+"," date ",text)

        text = re.sub(r"[0-9]+","number",text)
        text = re.sub(r"xx+", "", text)
        text = re.sub(r"[^a-zA-Z ]+"," ",text)
        text = re.sub(r"\s+"," ",text)
        text = text.lstrip().rstrip()
        tokens = self.tokenizer(sentance=text)
        #
        tokens = [stemmer.stem(contractions.fix(token)) for token in tokens if token not in stop_words ]
        text = " ".join(tokens).lstrip().rstrip()

        return text

    def tokenizer(self, sentance):
        return word_tokenize(sentance)
    

    def y_label_decode(self, class_id : int) -> str:
        res = self.y_label_encoder.classes_[class_id]

        return res



class Model:
    def __init__(self, model, preprocessor) -> None:
        self.model = model
        self.text_preprocessor = preprocessor

    def predict(self, data : str) -> str:
        X = self.text_preprocessor.preprocess(data)
        prediction = self.model.predict(X)
        prediction = self.text_preprocessor.y_label_decode(class_id = int(prediction[0]))

        return prediction


def predict(complaint : str) -> str:
    '''
    description:
        it predict the results
    '''
    # converting into dataframe 
    data = {"Consumer complaint narrative" : str(complaint)}
    data = pd.DataFrame(data,index=[0])
    
    prediction = model.predict(data = data)
    return prediction
   

textPreprocessor = TextPreprocessing(countVectorizer=COUNT_VECTORIZER, tfidf_transformer=TF_IDF_TRANSFORMER, y_label_encoder=Y_LABEL_ENCODER)
model = Model(model = PRODUCT_PREDICTION_MODEL, preprocessor=textPreprocessor)


if __name__ == "__main__":

     complaint = input("enter the complaint : ")
     data = {"Consumer complaint narrative" : str(complaint),}
     data = pd.DataFrame(data,index=[0])
     prediction = model.predict(data = data)

     print(f"\npredicted product : {prediction}")
