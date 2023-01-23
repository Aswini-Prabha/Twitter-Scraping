import json
import requests
import streamlit as st
from streamlit_lottie import st_lottie 
import snscrape.modules.twitter as snt
import pymongo
from pymongo import MongoClient
client = MongoClient("localhost", 27017) 
import pandas as pd
import datetime
from PIL import Image

st.set_page_config(page_title="Twitter data scraping webpage",page_icon=":sunglasses:",layout="wide")
st.title(" :large_blue_circle: Twitter Scraping :large_blue_circle:")

def load_lottiefile(filepath:str):
    with open(filepath,"r")as f:
        return json.load(f)
lottie_s=load_lottiefile(r"C:\Users\Aswini Praba\Desktop\simple_streamlit_app\scrape.json")

with st.container():
    st.write("---")
    left_column,right_column=st.columns(2)
    with left_column:
        st.write(
            """
            :large_blue_circle: In this page you can scrape the TWITTER SEARCH RESULTS!
            Give the keyword in Search box :arrow_right: Set the limit and date :arrow_right:
            Get the output! :arrow_right:
            Download it in required(csv/json) format!
            """
            )
        x=st.text_input('Type the keyword below:point_down:', '')
        feed=[]
        limit=st.number_input('Enter the limit:point_down:')
        since=st.date_input("Enter from date:date::point_down:")
        until=st.date_input("Enter end date:date::point_down:")

        s=st.button('Submit')

    with right_column:
        st_lottie(
            lottie_s,
            speed=0.2,
            reverse=False,
            loop=True,
            quality="low",
            height=500,
            width=None,
            key=None
)

if s:
    st.write('please wait for few seconds.....')

    for tweet in snt.TwitterSearchScraper('x since until').get_items():
        if len(feed)==limit:
            break
        else:
            y={'Date':tweet.date,
               'ID':tweet.id,
               'URL':tweet.url,
               'User Name':tweet.user.username,
               'Content':tweet.rawContent,
               'Retweet count':tweet.retweetCount,
               'Reply count':tweet.replyCount,
               'Language':tweet.lang,
               'Source':tweet.source,
               'Like count':tweet.likeCount}
            feed.append(y)
    show =pd.DataFrame(feed)
    show.to_csv('tweet_data.csv',mode='w')
    df=pd.read_csv("tweet_data.csv",index_col=[0])
    st.write(df)
    data=df.to_dict(orient="records")
    db=client["ML"]
    db.twitter.insert_many(data)
    def convert_df(show):
        return show.to_csv(index=False).encode('utf-8')
    csv=convert_df(show)
    st.download_button(
        "Click to Download the data in csv format:arrow_down:",
        csv,
        "file.csv"
        "text/csv",
        key='download-csv'
    )
    data=df.to_dict(orient="records")
    jsf=json.dumps(data)
    st.download_button(
        label="Click to Download the data in json format:arrow_down:",
        file_name="data.json",
        mime="application/json",
        data=jsf,
    )

with st.container():
    st.write('---')
    st.subheader("Hope you enjoyed using this webpage!!!:thumbsup:")
    st.write("Please provide your valuable Feedback!!!:speech_balloon:")
    st.write("##")
    contact_form="""
    <form action="https://formsubmit.co/aswiniprabha22@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">      
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here" required></textarea>
        <button type="submit">Send</button>
    </form>
    """
    left_column,right_column=st.columns(2)
    with left_column:
        st.markdown(contact_form,unsafe_allow_html=True)
    with right_column:
        st.empty()
