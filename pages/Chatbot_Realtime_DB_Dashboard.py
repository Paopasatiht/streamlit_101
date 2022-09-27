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
from crate import client
import datetime

def convert_milli_to_datetime(time_in_millis):
    dt = datetime.datetime.fromtimestamp(time_in_millis / 1000.0, tz=datetime.timezone.utc)
    return dt

def query_crate():
    crate_client = client.connect("http://110.78.211.35:4200/", timeout = 3)
    cursor = crate_client.cursor()

    query_string = """
    SELECT timestamp, intents, question, answer, probability, status
    FROM "doc"."demo"
    LIMIT 100;
    """
    cursor.execute(query_string)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['time', 'intent', 'question', 'answer'
                                    ,'probability','status'])
    return df



st.title('🎈 Chatbot Realtime Database Dashboard')

st.sidebar.subheader('Input')
url_input = st.sidebar.text_input('Select URL', 'https://raw.githubusercontent.com/Paopasatiht/iarepus-chat-bot/main/configs/data_corpus_v2.csv')
# intent_input = st.sidebar.text_input('Select Type of Sentence', 'ทักทาย')
if url_input=='https://raw.githubusercontent.com/Paopasatiht/iarepus-chat-bot/main/configs/data_corpus_v2.csv':
    try: 
        df = query_crate()
        st.subheader('Output')
        st.info(f'The dataframe that you want to see is : from the CrateDB ')
    except:
        st.warning('The Query Doesn\'t work ')
        df = pd.read_csv('https://raw.githubusercontent.com/Paopasatiht/iarepus-chat-bot/main/data_corpus.csv')

        st.subheader('Output')
        st.info(f'The dataframe that you want to see is : {url_input} ')

    word_list = df.question.to_list()

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


@st.cache
def convert_df(df):
   return df.to_csv().encode('utf-8')


if url_input:
    # df = pd.read_csv(url_input)
    # preprocess
    df.time = df.time.apply(lambda x: convert_milli_to_datetime(x))
    list_columns = ['status', 'time', 'intent', 'question', 'answer'
                    ,'probability']


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

            csv = convert_df(df)
            st.download_button(
            label="Press to Download",
            data=csv,
            file_name="all_data.csv",
            mime="text/csv",
            )
        else:
            st.write('The Dataframe')
            filter_df = df[df[genre]==full_table]
            st.dataframe(filter_df)
            csv = convert_df(filter_df)
            st.download_button(
            label="Press to Download",
            data=csv,
            file_name="filter_data.csv",
            mime="text/csv",
            )

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