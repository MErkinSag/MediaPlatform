import time

import streamlit as st
from streamlit_option_menu import option_menu
import requests

# 1. as sidebar menu
with st.sidebar:
    content_type = option_menu("Media Contents", ['Movies', 'Games', 'Music'],
         menu_icon="cast", default_index=1)


# 2. horizontal menu
action = option_menu(None, ["All", "Upload", "Edit", "Categorize"],
    icons=['home', 'cloud-upload', 'gear', "list-task"],
    menu_icon="cast", default_index=0, orientation="horizontal")


def divide_section_into_columns():
    col1, col2, col3, col4 = st.columns(4)
    layout = {0: col1, 1: col2, 2: col3, 3: col4}
    return layout


def edit_movie_name(movie_id):
    if "edited_name" in st.session_state:
        # send request to fast api
        # if the status is 200:

        st.session_state["movies"][movie_id]["name"] = st.session_state["edited_name"]

        # else:
        #   st.write("Server error, please try again later")
        #   log
        del st.session_state["edited_name"]


def remove_movie(movie_id):
    del st.session_state["movies"][movie_id]


def display_movies(layout):
    for i, movie_id in enumerate(st.session_state["movies"]):
        # determine which columnar line does this movie belong
        pos = i % 4

        review = st.session_state["movies"][movie_id]["review"]
        name = st.session_state["movies"][movie_id]["name"]

        text_placeholder = layout[pos].empty()
        text_placeholder.text(f"Movie: {name}")

        text_placeholder = layout[pos].empty()
        text_placeholder.text(f"Review: {review}")

        button_placeholder = layout[pos].empty()
        button_placeholder.button(f"Remove", key=f"button{movie_id}", on_click=remove_movie, args=(movie_id,))

        # if the edit button was pressed
        if f"edit{movie_id}" in st.session_state and st.session_state[f"edit{movie_id}"]:
            layout[pos].text_input("Please enter new name for the movie", key="edited_name", on_change=edit_movie_name,
                                   args=(movie_id,))
        else:
            button_placeholder = layout[pos].empty()
            button_placeholder.button(f"Edit", key=f"edit{movie_id}")


def display():
    load_init_data()
    layout = divide_section_into_columns()
    if content_type == 'Movies':
        display_movies(layout)


def load_init_data():
    if "init" not in st.session_state:
        print("loading initial data")
        data = requests.get("http://localhost:8000/data")

        st.session_state["movies"] = data.json()["movies"]
        print(f"movie data:\n{st.session_state['movies']}")

        st.session_state["init"] = True


if __name__ == "__main__":
    # print(f"ss keys: {st.session_state}")
    
    display()
    