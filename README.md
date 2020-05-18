# Social-Listening-NLP-Project

## Project Goals
    -Social media is a vast ocean of content. Trying to catch anything useful or meaningful from it can be a daunting task, 
    especially if you're an a creative professional who just wants to create--sifting through thousands and 
    even millions of posts can be a tedious task and a major buzzkill when trying to be creative. 
    The goal of this project was to use NLP to help analyize online conversations in order to cluster audiences 
    based on popular topics.


## Data Collection
    -Search Term: 'billie eilish'
    -Social Platform: Twitter
    -Technology: Twint
    -Date Range: March 30 - April 1st
    -Total Tweets: 14,000



## Data Preprocessing
    Before analyzing the documents, I needed to clean the text so that 
    I can tokenize each term into meaningful words. I created a preprocessing function that 
    eliminated URL links, non-alpha characters, words less than 3 letters, and English stopwords provided by NLTK.
    
    Custom Stopwords: In addition to the standard stopwords that the NLTK library provides,
    I also included the search term and any words that are in popular song titles (if the search
    term is an artist).



## EDA

![](/visualizations/wordcloud_popular_tweets.png)

    Looking at the most common words for tweets with over 50 retweets, one can infer that proper nouns
    such as names, events, special guest appearances create the most buzz.


![](/visualizations/top_bigrams-popular_tweets.png)

    Another visual indicating bigrams are essential to extracting key terms/topics from my subject,
    I will use bigrams in my final LDA model


## Modeling/Topic Results (MVP)
    I ran my processed data through a Gensim LDA model with 4 topics as one of my parameters 
    and a minimum term frequency of 50. 
    You can click on the link below
    for an interactive visualization of the topic distribution for each cluster.

[INTERACTIVE VISUALIZATION](http://localhost:8888/view/pyvisual.html)


Topic 1: Papa Mochi aka James Corden/Youtube

Topic 2: iHeart Living Room Concert for America/Coronavirus

Topic 3: Album/Quarantine

Topic 4: BillieCoin, Saving The Planet

## Short-Term Improvements
    -Revise Data Scraper function using Selenium
    -Create a data pipeline (collection, preprocessing, cluster output)
    -Development frontend that integrates the pipeline
    
## Long-Term Improvements
    -Additional Insights and Features for Frontend Development
        -Artists Most Mentioned With: What other artists do I share the most fans with?
    -Flexible Search Capabilities
        -Adjust Date Range for Return Data
        -Include Stopwords for More Defined Topics/CLusters

