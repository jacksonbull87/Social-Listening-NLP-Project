import threading
import tornado.ioloop
import tornado.web
from tornado import gen
import asyncio
import nest_asyncio
from pyppeteer import launch

import twint
import nest_asyncio
# nest_asyncio.apply()
import numpy as np
import nltk
from nltk.corpus import stopwords
import re
from nltk.stem import WordNetLemmatizer
from string import punctuation
from nltk.tokenize import sent_tokenize, word_tokenize
import sklearn
import gensim
import gensim.corpora as corpora
import pyLDAvis.gensim
import streamlit as st
import pandas as pd
import pyLDAvis



 

def get_twitter_data(keyword):
    c = twint.Config()
    c.Search = keyword
    c.Lang = 'en'
    c.Pandas_clean = True
    c.Since = '2020-04-12'
    c.Store_csv = True
    c.Output = 'test.csv'
    c.Hide_output = True
    twint.run.Search(c)
    
    return pd.read_csv('test.csv')

def text_preprocessing(dataframe, keyword):

    #remove handles
    def remove_pattern(input_txt, pattern):
        r = re.findall(pattern, input_txt)
        for i in r:
            input_txt = re.sub(i, '', input_txt)

        return input_txt

    dataframe['tidy_tweet'] = dataframe['tweet'].apply(lambda x: remove_pattern(x, "@[/w]*"))
    #removeURLs

    dataframe['tidy_tweet'] = np.vectorize(remove_pattern)(dataframe['tidy_tweet'], "http([/S]*)?")
    dataframe['tidy_tweet'] = np.vectorize(remove_pattern)(dataframe['tidy_tweet'], "pic.twitter.com([/w]*)?")

    #Remove Punctuations, special characters, numbers

    dataframe['tidy_tweet'] = dataframe['tidy_tweet'].str.replace("[^a-zA-Z#]", " ")


    #Remove short Words
    dataframe['tidy_tweet'] = dataframe['tidy_tweet'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>3]))
    #Lemmatize Tweet
    lemmatizer = WordNetLemmatizer()
    dataframe['lemmatized_tweets'] = dataframe['tidy_tweet'].apply(lambda x: ' '.join([lemmatizer.lemmatize(word.lower()) for word in x.split()]))

    #remove stopwords

    stop_words = list(set(stopwords.words('english')))

    #adding stopwords that include search term and song titles
    stop_words = list(set(stopwords.words('english')))
    if len(keyword.split()) > 1:
        keyword = keyword.split()
        stop_words.extend(keyword)
    else:
        stop_words.append(keyword)

    non_stopword_tweets = []
    for i in dataframe['lemmatized_tweets']:

        word_tokens = word_tokenize(i) 
        non_stopword_tweets.append(' '.join([word for word in word_tokens if word not in stop_words]))


    dataframe['lemmatized_tweets'] = non_stopword_tweets
    
    return dataframe['lemmatized_tweets']

#run LDA model and create clusters
def create_topics(processed_data, num_of_topics):
    def sent_to_words(sentences):
        for sentence in sentences:
            yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

        
    data = processed_data.values.tolist()
    data_words = list(sent_to_words(data))

    bigrams = gensim.models.Phrases(data_words, min_count=50)
    for idx in range(len(processed_data)):
        for token in bigrams[processed_data[idx]]:
            if '_' in token:
                # Token is a bigram, add to document.
                processed_data[idx].append(token)

    # Create Dictionary
    id2word = corpora.Dictionary(data_words)
    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in data_words]

    # Build LDA model
    lda_model_bigram = gensim.models.LdaMulticore(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=num_of_topics, 
                                           random_state=100,
                                           chunksize=100,
                                           passes=5,
                                           per_word_topics=True)
    pyLDA_bigram_vis = pyLDAvis.gensim.prepare(lda_model_bigram, corpus, id2word)
    return pyLDA_bigram_vis





#Project Title
st.title("Social Listening For Artists")

#text input 
keyword = st.text_input("", "Type Here")
if st.button("Submit"):
    st.text("We're currently getting all the tweets that mention {}, so this might take a while. Meanwhile, go take te dog for a walk.".format(keyword))
    result = get_twitter_data(keyword)
    processed_data = text_preprocessing(result, keyword)
    pyLDA_bigram_vis = create_topics(processed_data, 4)
    st.success(pyLDAvis.display(pyLDA_bigram_vis))



