# NOTE: This script is intended to run in a local environment with SSL and internet access.
# It will not work in a restricted environment without the 'ssl' module or external HTTP access.

import random
import webbrowser

try:
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
except ModuleNotFoundError:
    raise ImportError("The 'spotipy' library is required. Please install it with 'pip install spotipy'.")

try:
    import ssl
except ModuleNotFoundError:
    raise ImportError("The 'ssl' module is required but not available in your environment. Please run this in a full Python environment.")

# 1. === SETUP SPOTIFY AUTHENTICATION ===
SPOTIPY_CLIENT_ID = '2339aa7532ab4cf09b7e1faab59c547f'
SPOTIPY_CLIENT_SECRET = 'e83b2cc2447b4d158d6fe2d5fb834115'

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET
))

# 2. === MAIN LOOP ===
while True:
    print("\nWelcome to the Music Recommendation System")
    listener_name = input("Please enter your name (or type 'exit' to quit): ").strip()
    if listener_name.lower() == 'exit':
        print("Thank you for using the Music Recommendation System. Goodbye!")
        break

    age = input("Please enter your age: ").strip()
    languages = input("What languages do you prefer to listen to music in? (e.g., English, Korean, Spanish): ").strip().split(',')
    location = input("Where are you from? (e.g., Mumbai, Delhi, Seoul): ").strip()
    preferred_style = input("What is your favorite music style? (e.g., pop, classical, rock): ").strip()
    fav_artists = input("List a few of your favorite artists (comma separated): ").strip().split(',')

    while True:
        mood = input("\nMay I know your mood? (e.g., sad, happy, romantic, classic, party, solo travelling): ").strip().lower()

        query_parts = [mood, preferred_style]
        if fav_artists:
            query_parts.append(random.choice(fav_artists).strip())

        search_query = " ".join(query_parts)

        try:
            results = sp.search(q=search_query, type='track', limit=10)
            tracks = results['tracks']['items']
        except Exception as e:
            print("An error occurred while fetching data from Spotify:", e)
            break

        if not tracks:
            print("Sorry, no songs found matching your mood and preferences.")
            continue

        print(f"\nTop song recommendations for {listener_name.title()} (Mood: {mood}):\n")
        for i, track in enumerate(tracks, 1):
            song_name = track['name']
            artist_name = track['artists'][0]['name']
            print(f"{i}. {song_name} by {artist_name}")

        played_indices = set()
        while True:
            play_choice = input("\nWould you like to play a song from the above list? (yes/no): ").strip().lower()
            if play_choice == 'yes':
                try:
                    choice = int(input("Enter the number of the song you want to play (1-10): "))
                    if 1 <= choice <= len(tracks):
                        if choice - 1 in played_indices:
                            print("This song has already been played. Choose another one.")
                        else:
                            track_url = tracks[choice - 1]['external_urls']['spotify']
                            print(f"Opening {tracks[choice - 1]['name']} on Spotify...")
                            webbrowser.open(track_url)
                            played_indices.add(choice - 1)
                    else:
                        print("Invalid choice. Please choose a number between 1 and 10.")
                except ValueError:
                    print("Invalid input. Please enter a number between 1 and 10.")
            else:
                break

            continue_playing = input("\nDo you want to play another song from the list? (yes/no): ").strip().lower()
            if continue_playing != 'yes':
                break

        next_action = input("\nWould you like to change mood or allow a new user to enter? (change/new/exit): ").strip().lower()
        if next_action == 'change':
            continue  # Loop back to ask for new mood
        elif next_action == 'new':
            break     # Break to outer loop for new user
        elif next_action == 'exit':
            print("Thank you for using the Music Recommendation System. Goodbye!")
            exit()
