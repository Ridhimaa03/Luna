import streamlit as st
from textblob import TextBlob
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# --- Page config should be FIRST Streamlit command ---
st.set_page_config(page_title="🎧 Music Mood Matcher", layout="wide")

# --- Optional: Load custom CSS ---
with open('style1.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# --- Spotify API Setup ---
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="d1deeba498f74d8c887d7df306d78584",
    client_secret="360c8da50dab470e8b88e5722b94cd2e"
))

# --- Enhanced Mood Detection ---
def detect_mood(text):
    text = text.lower()

    keyword_map = {
        "Sad": ["cry", "tears", "depressed", "hopeless", "dying", "lonely", "heartbroken", "worthless"],
        "Angry": ["fight", "angry", "rage", "furious", "mad", "fighting"],
        "Happy": ["joy", "excited", "wonderful", "grateful", "awesome", "yay"],
        "Calm": ["peaceful", "relaxed", "serene", "calm", "okay"],
        "Excited": ["energetic", "party", "thrilled", "ecstatic", "amazing"],
        "Depressed": ["worthless", "dying", "hopeless", "end it all", "nothing matters"]
    }

    for mood, keywords in keyword_map.items():
        if any(word in text for word in keywords):
            return mood

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity >= 0.5:
        return "Excited"
    elif polarity >= 0.2:
        return "Happy"
    elif polarity >= 0.0:
        return "Calm"
    elif polarity > -0.2:
        return "Neutral"
    elif polarity > -0.5:
        return "Sad"
    elif polarity > -0.7:
        return "Angry"
    else:
        return "Depressed"

# --- Music Recommendation with Album Art ---
def recommend_tracks(mood, language, limit=12):
    genre_map = {
        "Excited": "dance",
        "Happy": "pop",
        "Calm": "chill",
        "Neutral": "indie",
        "Sad": "acoustic",
        "Angry": "metal",
        "Depressed": "lofi"
    }

    genre = genre_map.get(mood, "pop")
    query = f"{genre} {language}"
    results = sp.search(q=query, type='track', limit=limit)
    tracks = results['tracks']['items']

    recommended = []
    for track in tracks:
        if track['type'] == 'track':
            recommended.append({
                "name": track['name'],
                "artist": track['artists'][0]['name'],
                "url": track['external_urls']['spotify'],
                "image": track['album']['images'][0]['url'] if track['album']['images'] else None
            })
    return recommended

# --- Streamlit Interface ---
st.title("🎧 Music Mood Matcher")
st.markdown("Tell us how you're feeling and get a personalized music playlist!")

user_input = st.text_input("How are you feeling today?")
language = st.selectbox(
    "Select your preferred language for music:",
    ["English", "Hindi", "Spanish", "French", "Korean", "Punjabi"]
)

# Add number input for how many songs user wants (min 1, max 20)
num_songs = st.number_input("How many songs would you like?", min_value=1, max_value=20, value=12, step=1)

if st.button("Detect Mood"):
    if user_input.strip() == "":
        st.warning("Please enter how you're feeling.")
    else:
        mood = detect_mood(user_input)
        st.success(f"🎭 Detected Mood: **{mood}**")

        tracks = recommend_tracks(mood, language, limit=num_songs)
        st.subheader("🎶 Your Personalized Playlist:")

        # Display 4 songs per row
        for i in range(0, len(tracks), 4):
            row = st.columns(4)
            for j in range(4):
                if i + j < len(tracks):
                    track = tracks[i + j]
                    with row[j]:
                        if track['image']:
                            st.image(track['image'], use_column_width=True)
                        st.markdown(f"**{track['name']}**", unsafe_allow_html=True)
                        st.markdown(f"*{track['artist']}*")
                        st.markdown(f"[🎵 Listen on Spotify]({track['url']})", unsafe_allow_html=True)
