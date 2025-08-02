import streamlit as st
import pickle
import pandas as pd
import requests





def fetch_poster(movie_id):
    try:
        # Set the base URL and API key as variables for better readability.
        base_url = 'https://api.themoviedb.org/3/movie/{}'
        api_key = '7a576d4725b59b825baffb35a071b132'
        
        # Make the GET request with a timeout of 10 seconds.
        response = requests.get(
            base_url.format(movie_id), 
            params={'api_key': api_key, 'language': 'en-US'}, 
            timeout=10
        )
        
        # Check if the request was successful.
        response.raise_for_status()
        data = response.json()

        # Construct and return the full URL for the movie poster.
        return "https://image.tmdb.org/t/p/w500/" + data.get('poster_path', '')

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.Timeout:
        print("The request timed out.")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error: {req_err}")
    except KeyError:
        print("The poster path could not be found in the response data.")

    # Return a placeholder image or None if there is an error.
    return "https://via.placeholder.com/500x750?text=No+Image+Available"







# def fetch_poster(movie_id):
#     response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=7a576d4725b59b825baffb35a071b132&language=en-US'.format(movie_id))
#     data = response.json()
#     return "https://image.tmdb.org/t/p/w500/" + data['poster_path']





# selected_movie --> selected_movie
def recommend(selected_movie):
    movie_index = movies[movies['title'] == selected_movie].index[0]
    distances = similarity[movie_index]
    sorted_distance = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]  # Sort and get top 5 related movies

    recommended_names = []
    recommended_posters = []

    for i in sorted_distance:
        # st.write(movies.iloc[i[0]].title)
        movie_id = movies.iloc[i[0]].movie_id
        recommended_names.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_names, recommended_posters



movies_dict = pickle.load(open('movie_dict.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movies = pd.DataFrame(movies_dict)

st.title('Movie Recommender System')
option = st.selectbox('Select a Movie', movies['title'].values)
st.write('You selected:', option)

if st.button('Recommend'):
    # recommend(option)

    names, posters = recommend(option)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])


