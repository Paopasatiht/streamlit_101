import streamlit as st
import pandas as pd
import numpy as np
import pythainlp
from pythainlp import word_tokenize
from pythainlp.corpus import get_corpus # for getting stopwords
import wordcloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

st.title('🎈 Chatbot\'s Intelligent Dashboard')



st.sidebar.subheader('Input')
url_input = st.sidebar.text_input('Select URL', 'https://raw.githubusercontent.com/Paopasatiht/iarepus-chat-bot/main/configs/data_corpus_v2.csv')
# intent_input = st.sidebar.text_input('Select Type of Sentence', 'ทักทาย')
if url_input=='https://raw.githubusercontent.com/Paopasatiht/iarepus-chat-bot/main/configs/data_corpus_v2.csv':
    df = pd.read_csv(url_input)

    word_list = df.Keys.to_list()

    s = " ".join(word_list)

    words = word_tokenize(s)
    all_words = ' '.join(words).lower().strip()
    all_word = re.sub('(\n|\s{2})', '', all_words)

    stopwords=pythainlp.corpus.thai_stopwords()
    stopwords=set(list(stopwords)).union({'นี้', 'อัน', 'แต่', 'ไม่'})

    wordcloud = WordCloud(
        font_path='./assets/fonts/THSarabunNew.ttf',
        regexp='[ก-๙]+',

        stopwords=stopwords,
        width=2000, height=1000,

        prefer_horizontal=1,
        max_words=50, 

    #     colormap='viridis', # default matplotlib colormap
        colormap='tab20c',
    #     colormap='plasma',
        background_color = 'white').generate(all_words)

    plt.figure(figsize = (10, 9))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.tight_layout(pad=0)

if url_input:
    st.subheader('Output')
    st.info(f'The dataframe that you want to see is : {url_input} ')

    df = pd.read_csv(url_input)
    list_columns = df.columns.to_list()
    tuple_columns = tuple(col for col in list_columns)

    with st.container():
        col1, col2 = st.columns(2)

        genre = col1.radio(
            "What's your interest group ( reccomend 'Intents' ) ",
            tuple_columns)


        list_visuailize_df = np.append(df[genre].unique(), 'All Category')
        tuple_visualize_columns = tuple(list_visuailize_df)

        full_table = col2.radio(
            "What's your intrest dataframe ",
            tuple_visualize_columns)

        if full_table=='All Category':
            st.dataframe(df)
        else:
            st.write('The Dataframe')
            st.dataframe(df[df[genre]==full_table])

    with st.container():
        col3, col4 = st.columns(2)
        col3.subheader('Bar Chart Visualization')
        col3.info(f'this bar is showing according to the genre: {genre} ')
        df_ratio = df.groupby(genre).count()
        col3.write(df_ratio)
        col3.bar_chart(df_ratio)


        col4.subheader("Word Cloud Chart")
        plt.show()
        col4.pyplot(plt)
else:
    st.subheader('Enter Your Input')
    st.warning('👈 Avaiting your input !!!')