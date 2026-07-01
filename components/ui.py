import streamlit as st

def page_title(title, subtitle=None):

    st.title(title)

    if subtitle:
        st.write(subtitle)

    st.divider()