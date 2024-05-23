import csv
import instaloader
from instaloader import Profile, Post
import time
import networkx as nx
from geopy.geocoders import Nominatim

# Configuration (Customize these)
your_username = 'your_instagram_username'  # Replace with your actual username
target_profile = 'your_club_profile'  # Replace with your club's Instagram profile
genre_keywords = ['jazz', 'hip-hop', 'electronic', 'funk', 'soul']  # Add more genres relevant to Concord
max_depth = 2  # How many levels of followers to explore
post_keywords = ['#musician', '#livemusic', '#artist', '#concord', '#bayarea']  # Add Concord-specific hashtags
min_follower_count = 1000  # Minimum follower count for potential artists
min_engagement_rate = 0.02  # Minimum average engagement rate for posts
max_distance_miles = 50  # Maximum distance from Concord, CA (adjust as needed)

# Geocoding Setup
geolocator = Nominatim(user_agent="concord_artist_discovery")
concord_location = geolocator.geocode("Concord, CA, USA")

L = instaloader.Instaloader()
L.load_session_from_file(your_username)

# Build Graph
G = nx.Graph()
explored_profiles = set()


def explore_profile(profile, depth=0):
    # ... (same as before)


# Start Exploration
starting_profile = Profile.from_username(L.context, target_profile)
explore_profile(starting_profile)

# Filter and Analyze
potential_artists = []
for node, data in G.nodes(data=True):
    bio = data.get('bio', '').lower()
    if not data['is_private'] and data['follower_count'] >= min_follower_count and any(keyword in bio for keyword in genre_keywords):
        profile = Profile.from_username(L.context, node)
        
        # Location Filtering
        try:
            artist_location = geolocator.geocode(profile.location)
            distance = geopy.distance.distance(concord_location.point, artist_location.point).miles
            if distance > max_distance_miles:
                continue  # Skip artists too far away
        except (AttributeError, TypeError):
            pass  # Skip if location data is unavailable
            
        # Post Filtering & Engagement Calculation
        total_likes = 0
        total_comments = 0
        post_count = 0
        for post in profile.get_posts():
            if any(keyword in post.caption_hashtags for keyword in post_keywords):
                total_likes += post.likes
                total_comments += post.comments
                post_count += 1
        if post_count > 0:
            avg_engagement = (total_likes + total_comments) / (profile.followers * post_count)
            if avg_engagement >= min_engagement_rate:
                potential_artists.append({
                    'username': node,
                    'bio': bio,
                    'followers': data['follower_count'],
                    'avg_engagement': avg_engagement,
                    'location': profile.location  # Include location information
                    # Add more fields like recent posts, etc.
                })

# Export Data
with open('potential_artists_concord.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # ... (same as before)

print("Potential artists data saved to potential_artists_concord.csv")
