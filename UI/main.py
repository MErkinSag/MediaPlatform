import time
from typing import List, Dict
import streamlit as st
from streamlit_option_menu import option_menu
import requests


def divide_section_into_columns():
    col1, col2, col3, col4 = st.columns(4)
    layout = {0: col1, 1: col2, 2: col3, 3: col4}
    return layout


def edit_movie_name(movie_id):
    if "edited_name" in st.session_state:

        old_movie_name = st.session_state["movies"][movie_id]["name"]

        new_movie_name = st.session_state["edited_name"]
        imdb_rating = st.session_state["movies"][movie_id]["imdb_rating"]

        movie_data = {"content": {"id": movie_id, "name": new_movie_name, "imdb_rating": imdb_rating}, "update_columns": ["name"]}
        response = requests.put("http://backend_api:8000/contents/movies", json=movie_data)

        if response.status_code == 200:
            st.session_state["movies"][movie_id]["name"] = st.session_state["edited_name"]
            st.write(f"Movie {old_movie_name} name has changed into {new_movie_name}")
        else:
            st.write(f"Movie {old_movie_name} name could not be changed.")

        del st.session_state["edited_name"]


def edit_video_name(video_id):
    if "edited_name" in st.session_state:

        old_video_name = st.session_state["videos"][video_id]["name"]
        new_video_name = st.session_state["edited_name"]
        video_year = st.session_state["videos"][video_id]["year"]

        video_data = {"content": {"id": video_id, "name": new_video_name, "year": video_year}, "update_columns": ["name"]}
        print(f"GAME DATA: {video_data}")
        response = requests.put("http://backend_api:8000/contents/videos", json=video_data)

        if response.status_code == 200:
            st.session_state["videos"][video_id]["name"] = st.session_state["edited_name"]
            st.write(f"Video {old_video_name} name has changed into {new_video_name}.")
        else:
            st.write(f"Video {old_video_name} name could not be changed.")

        del st.session_state["edited_name"]


def edit_game_name(game_id):
    if "edited_name" in st.session_state:

        new_game_name = st.session_state["edited_name"]
        old_game_name = st.session_state["games"][game_id]["name"]
        game_type = st.session_state["games"][game_id]["game_type"]

        game_data = {"content": {"id": game_id, "name": new_game_name, "game_type": game_type}, "update_columns": ["name"]}
        print(f"GAME DATA: {game_data}")
        response = requests.put("http://backend_api:8000/contents/games", json=game_data)

        if response.status_code == 200:
            st.session_state["games"][game_id]["name"] = st.session_state["edited_name"]
            st.write(f"Game {old_game_name} name has changed into {new_game_name}.")
        else:
            st.write(f"Game {old_game_name} name could not be changed.")

        del st.session_state["edited_name"]


def remove_movie(movie_id):
    movie_data = st.session_state["movies"][movie_id]
    movie_data["id"] = movie_id
    response = requests.delete("http://backend_api:8000/contents/movies", json=movie_data)
    if response.status_code == 200:
        del st.session_state["movies"][movie_id]
        st.write("Movie was deleted")
    else:
        st.write("Movie could not be deleted.")

def remove_video(video_id):
    video_data = st.session_state["videos"][video_id]
    video_data["id"] = video_id
    response = requests.delete("http://backend_api:8000/contents/videos", json=video_data)
    if response.status_code == 200:
        del st.session_state["videos"][video_id]
        st.write("Video was deleted")
    else:
        st.write("Video could not be deleted.")

def remove_game(game_id):
    game_data = st.session_state["games"][game_id]
    game_data["id"] = game_id
    response = requests.delete("http://backend_api:8000/contents/games", json=game_data)
    if response.status_code == 200:
        del st.session_state["games"][game_id]
        st.write("Game was deleted")
    else:
        st.write("Game could not be deleted.")

def display_games(layout):
    if action == "Upload":
        with st.form("upload_form", clear_on_submit=True):
            uploaded_game = st.file_uploader(label="Upload", key="uploaded_file")
            uploaded_game_name = st.text_input("Game Name", key="uploaded_game_name")

            if not uploaded_game_name:
                if uploaded_game:
                    uploaded_game_name = uploaded_game.name

            uploaded_game_type = st.text_input("Game Type", key="uploaded_game_type")
            submitted = st.form_submit_button("Upload Game")
            if submitted:
                with st.spinner(f"Uploading Game {uploaded_game_name}..."):
                    # time.sleep(5)
                    game_data = {"name": uploaded_game_name, "game_type": uploaded_game_type}
                    response = requests.post("http://backend_api:8000/contents/games", json=game_data)

                    if response.status_code != 200:
                        st.write("Game could not be uploaded.")
                        print(f"GAME DATA: {game_data}")
                    else:
                        game_id = response.json()["id"]
                        print(f"retrieved game id: {game_id}")
                        st.session_state["games"][game_id] = game_data
                        st.write(f"Game uploaded")
                        st.write(f"Name: {uploaded_game_name}, Type:{uploaded_game_type}")
    else:
        for i, game_id in enumerate(st.session_state["games"]):
            # determine which columnar line does this game belong
            pos = i % 4

            name = st.session_state["games"][game_id]["name"]
            type = st.session_state["games"][game_id]["game_type"]

            text_placeholder = layout[pos].empty()
            text_placeholder.text(f"Game: {name}")

            text_placeholder = layout[pos].empty()
            text_placeholder.text(f"Review: {type}")

            if action == "Edit":
                button_placeholder = layout[pos].empty()
                button_placeholder.button(f"Remove", key=f"button{game_id}", on_click=remove_game, args=(game_id,))

                # if the edit button was pressed
                if f"rename{game_id}" in st.session_state and st.session_state[f"rename{game_id}"]:
                    layout[pos].text_input("Please enter new name for the game", key="edited_name", on_change=edit_game_name,
                                           args=(game_id,))
                else:
                    button_placeholder = layout[pos].empty()
                    button_placeholder.button(f"Rename", key=f"rename{game_id}")


def display_movies(layout):
    if action == "Upload":
        with st.form("upload_form", clear_on_submit=True):
            uploaded_movie = st.file_uploader(label="Upload", key="uploaded_file")#,on_change=upload_movie1)
            uploaded_movie_name = st.text_input("Movie Name", key="uploaded_movie_name")

            if not uploaded_movie_name:
                if uploaded_movie:
                    uploaded_movie_name = uploaded_movie.name

            uploaded_movie_imdb = st.text_input("Movie Imdb Rating", key="uploaded_movie_year")
            submitted = st.form_submit_button("Upload Movie")
            if submitted:
                with st.spinner(f"Uploading Movie {uploaded_movie_name}..."):
                    movie_data = {"name": uploaded_movie_name, "imdb_rating": uploaded_movie_imdb}
                    response = requests.post("http://backend_api:8000/contents/movies", json=movie_data)

                    if response.status_code != 200:
                        st.write("Movie could not be uploaded.")
                    else:
                        movie_id = response.json()["id"]
                        st.session_state["movies"][movie_id] = movie_data
                        st.write(f"Movie uploaded")
                        st.write(f"Name: {uploaded_movie_name}, Type:{uploaded_movie_imdb}")

    else:
        for i, movie_id in enumerate(st.session_state["movies"]):
            # determine which columnar line does this movie belong
            pos = i % 4

            imdb_rating = st.session_state["movies"][movie_id]["imdb_rating"]
            name = st.session_state["movies"][movie_id]["name"]

            text_placeholder = layout[pos].empty()
            text_placeholder.text(f"Movie: {name}")

            text_placeholder = layout[pos].empty()
            text_placeholder.text(f"Review: {imdb_rating}")

            if action == "Edit":
                button_placeholder = layout[pos].empty()
                button_placeholder.button(f"Remove", key=f"button{movie_id}", on_click=remove_movie, args=(movie_id,))

                # if the edit button was pressed
                if f"rename{movie_id}" in st.session_state and st.session_state[f"rename{movie_id}"]:
                    layout[pos].text_input("Please enter new name for the movie", key="edited_name", on_change=edit_movie_name,
                                           args=(movie_id,))
                else:
                    button_placeholder = layout[pos].empty()
                    button_placeholder.button(f"Rename", key=f"rename{movie_id}")


def display_videos(layout):
    if action == "Upload":
        with st.form("upload_form", clear_on_submit=True):
            uploaded_video = st.file_uploader(label="Upload", key="uploaded_file")

            uploaded_video_name = st.text_input("Video Name", key="uploaded_video_name", help="Default name will be the file name if not specified.")

            if not uploaded_video_name:
                if uploaded_video:
                    uploaded_video_name = uploaded_video.name

            uploaded_video_year = st.text_input("Video Year", key="uploaded_video_year")
            submitted = st.form_submit_button("Upload Video")
            if submitted:
                with st.spinner(f"Uploading Video {uploaded_video_name}..."):
                    video_data = {"name": uploaded_video_name, "year": uploaded_video_year}
                    response = requests.post("http://backend_api:8000/contents/videos", json=video_data)

                    if response.status_code != 200:
                        st.write("Video could not be uploaded.")
                    else:
                        video_id = response.json()["id"]
                        st.session_state["videos"][video_id] = video_data
                        st.write(f"Video uploaded")
                        st.write(f"Name: {uploaded_video_name}, Year:{uploaded_video_year}")

    else:
        for i, video_id in enumerate(st.session_state["videos"]):
            # determine which columnar line does this video belong
            pos = i % 4

            name = st.session_state["videos"][video_id]["name"]
            year = st.session_state["videos"][video_id]["year"]

            text_placeholder = layout[pos].empty()
            text_placeholder.text(f"Video: {name}")

            text_placeholder = layout[pos].empty()
            text_placeholder.text(f"Year: {year}")

            if action == "Edit":
                button_placeholder = layout[pos].empty()
                button_placeholder.button(f"Remove", key=f"button{video_id}", on_click=remove_video, args=(video_id,))

                # if the edit button was pressed
                if f"rename{video_id}" in st.session_state and st.session_state[f"rename{video_id}"]:
                    layout[pos].text_input("Please enter new name for the video", key="edited_name", on_change=edit_video_name,
                                           args=(video_id,))
                else:
                    button_placeholder = layout[pos].empty()
                    button_placeholder.button(f"Rename", key=f"rename{video_id}")


def display():
    load_init_data()
    layout = divide_section_into_columns()
    if content_type == 'Movies':
        display_movies(layout)

    if content_type == 'Videos':
        display_videos(layout)

    if content_type == 'Games':
        display_games(layout)


def build_content_dict(content_list: List[Dict]):
    """
    Function to take a content list in the form of List[Dict], i.e. each content is a dictionary in the list
    and converts it in a format {content_id:content_data_dict} format in order to facilitate to retrieve a
    content by its id
    :param content_list:
    :return:
    """
    result_dict = {}
    for data in content_list:
        if type(data) == dict:
            print(f"DATA: {data}")
            id = data["id"]

            # remove the id part from the data since this is going to be key on the resulting dictionary format
            del data["id"]

            result_dict[id] = data

    return result_dict

def load_init_data():
    try:
        if "init" not in st.session_state:
            print("loading initial data")

            movie_data = requests.get("http://backend_api:8000/contents/movies")
            movie_data = movie_data.json()
            st.session_state["movies"] = build_content_dict(movie_data)


            video_data = requests.get("http://backend_api:8000/contents/videos")
            video_data = video_data.json()
            st.session_state["videos"] = build_content_dict(video_data)

            game_data = requests.get("http://backend_api:8000/contents/games")
            print(f"PROBLEMATIC GAME DATA --> {game_data}")
            game_data = game_data.json()
            st.session_state["games"] = build_content_dict(game_data)

            st.session_state["init"] = True
            st.session_state["uploaded"] = False
    except requests.exceptions.ConnectionError:
        st.write("Server is not responding at the moment...")


# source: https://docs.streamlit.io/knowledge-base/deploy/authentication-without-sso
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == "123":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("Password incorrect")
        return False
    else:
        # Password correct.
        return True


if __name__ == "__main__":
    if check_password():
        # 1. as sidebar menu
        with st.sidebar:
            content_type = option_menu("Media Contents", ['Movies', 'Games', 'Videos'],
                                       menu_icon="cast", default_index=1)

        # 2. horizontal menu
        action = option_menu(None, ["View", "Edit", "Upload"],
                             icons=['home', 'gear', 'cloud-upload'],
                             menu_icon="cast", default_index=0, orientation="horizontal")

        display()
    