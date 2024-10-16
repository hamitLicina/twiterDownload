import tweepy
import requests
import youtube_dl

# Twitter API credentials
API_KEY = 'your-api-key'
API_SECRET = 'your-api-secret'
ACCESS_TOKEN = 'your-access-token'
ACCESS_SECRET = 'your-access-token-secret'

# Set up Twitter API client
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# Function to get the tweet content
def get_tweet_video_url(tweet_url):
    # Extract tweet ID from the URL
    tweet_id = tweet_url.split("/")[-1]

    # Fetch the tweet using the API
    tweet = api.get_status(tweet_id, tweet_mode='extended')

    # Check if the tweet contains media
    media = tweet.entities.get('media', [])
    if len(media) > 0:
        # Extract video information
        if 'video_info' in tweet.extended_entities['media'][0]:
            video_info = tweet.extended_entities['media'][0]['video_info']
            variants = video_info['variants']

            # Filter the best quality video URL
            best_video_url = None
            highest_bitrate = 0
            for variant in variants:
                if variant.get('content_type') == 'video/mp4':
                    bitrate = variant.get('bitrate', 0)
                    if bitrate > highest_bitrate:
                        best_video_url = variant['url']
                        highest_bitrate = bitrate
            return best_video_url
    return None

# Function to download the video
def download_video(video_url, filename):
    ydl_opts = {
        'format': 'bestvideo/best',
        'outtmpl': filename,
        'noplaylist': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

# Example usage
tweet_url = 'https://twitter.com/username/status/1234567890123456789'  # Example tweet URL
video_url = get_tweet_video_url(tweet_url)

if video_url:
    print(f"Video URL: {video_url}")
    download_video(video_url, 'twitter_video.mp4')
    print("Video downloaded successfully!")
else:
    print("No video found in this tweet.")
