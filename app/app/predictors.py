import joblib
import re
import string

#preprocessor for sentiment analysis
def preprocessor(text, resolve_contractions=True):
    text = text.lower()
    contractions = { "ain't": "am not","aren't": "are not","can't": "cannot","can't've": "cannot have","'cause": "because","could've": "could have",
                "couldn't": "could not","couldn't've": "could not have","didn't": "did not","doesn't": "does not","don't": "do not",
                "hadn't": "had not","hadn't've": "had not have","hasn't": "has not","haven't": "have not","he'd": "he would",
                "he'd've": "he would have","he'll": "he will","he's": "he is","how'd": "how did","how'll": "how will","how's": "how is",
                "i'd": "i would","i'll": "i will","i'm": "i am","i've": "i have","isn't": "is not","it'd": "it would","it'll": "it will",
                "it's": "it is","let's": "let us","ma'am": "madam","mayn't": "may not","might've": "might have","mightn't": "might not",
                "must've": "must have","mustn't": "must not","needn't": "need not","oughtn't": "ought not","shan't": "shall not",
                "sha'n't": "shall not","she'd": "she would","she'll": "she will","she's": "she is","should've": "should have",
                "shouldn't": "should not","that'd": "that would","that's": "that is","there'd": "there had","there's": "there is",
                "they'd": "they would","they'll": "they will","they're": "they are","they've": "they have","wasn't": "was not",
                "we'd": "we would","we'll": "we will","we're": "we are","we've": "we have","weren't": "were not","what'll": "what will",
                "what're": "what are","what's": "what is","what've": "what have","where'd": "where did","where's": "where is","who'll": "who will",
                "who's": "who is","won't": "will not","would've":"would have","wouldn't": "would not","you'd": "you would","you'll": "you will",
                "you're": "you are"}
    if(resolve_contractions):
        text = text.split()
        new_text = []
        for word in text:
            if word.lower() in contractions:
                if(word[0] in string.ascii_uppercase):
                    resolved = contractions[word.lower()].split(" ")
                    resolved[0] = resolved[0].title()
                    new_text.append(" ".join(resolved))
                else:
                    new_text.append(contractions[word.lower()])
            else:
                new_text.append(word)
        text = " ".join(new_text)
    
    text = re.sub(r"@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+", " ", text)
    text = re.sub(r' yr ', ' year ', text)
    text = re.sub(r"<br />", " ", text)
    text = re.sub(r' ₹ ', ' rs ', text)
    text = re.sub(r"[~@\]%\{\\*#\)\(+:<.=>'$;\[!^&_/\}-]", " ", text)
    return text


def SentimentIntensityClassifier():
    return joblib.load("./models/sentiment_model.joblib")

def StockLowRegressor():
    return joblib.load("./models/low.pkl")

def StockHighRegressor():
    return joblib.load("./models/high.pkl")

def __testStockRegressors(test_high, test_low):
    high = StockHighRegressor()
    low = StockLowRegressor()
    print("Accuracy of high price predictions:", round(high.score(test_high[0], test_high[1])*100, 2), "%")
    print("Accuracy of low price predictions:", round(low.score(test_low[0], test_low[1])*100, 2), "%")  

def __testSentiementIntensityClassifier(headlines, predictions):
    sic = SentimentIntensityClassifier()
    print("Accuracy of Sentiment Intensity Classifier", round(sic.score(headlines, predictions)*100, 2), "%")
