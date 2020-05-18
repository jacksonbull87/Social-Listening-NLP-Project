

#get the tweet data
def get_tweets_by_keyword(keyword, since_date):
    c = twint.Config()
    c.Search = keyword
    c.Lang = 'en'
    c.Since = since_date
    c.Format = "Tweet ID: {id} | Date: {date} | Username: {username} | Tweet: {tweet} | #Replies: {replies} | #Retweets: {retweets} | #Likes: {likes}"
    c.Store_csv = True
    c.Output = 'keywordtwitterdata.csv'
    c.Hide_output = True
    twint.run.Search(c)

#function take in 3 inputs: username, number of tweets, and since date as inputs and saves as a csv file
def get_tweets_by_user(username, limit, since_date):
    import twint
    c = twint.Config()
    c.Username = username
    c.Limit = limit
    c.Since = since_date
    c.Format = "Tweet ID: {id} | Date: {date} | Username: {username} | Tweet: {tweet} | #Replies: {replies} | #Retweets: {retweets} | #Likes: {likes}"
    c.Store_csv = True
    c.Hide_output = True
    c.Output = 'usertweetdata.csv'
    twint.run.Search(c) 

#clean and preprocess text
def text_preprocessing(dataframe, keyword):

    #remove handles
    def remove_pattern(input_txt, pattern):
        r = re.findall(pattern, input_txt)
        for i in r:
            input_txt = re.sub(i, '', input_txt)

        return input_txt

    dataframe['tidy_tweet'] = dataframe['tweet'].apply(lambda x: remove_pattern(x, "@[\w]*"))
    #removeURLs

    dataframe['tidy_tweet'] = np.vectorize(remove_pattern)(dataframe['tidy_tweet'], "http\/\/[\S]*")
    dataframe['tidy_tweet'] = np.vectorize(remove_pattern)(dataframe['tidy_tweet'], "pic.twitter.com/[\w]*")

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

    bigrams = gensim.models.Phrases(data_words, min_count=10)
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
                                           passes=10,
                                           per_word_topics=True)
    pyLDA_bigram_vis = pyLDAvis.gensim.prepare(lda_model_bigram, corpus, id2word)
    return pyLDA_bigram_vis