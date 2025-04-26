import tweepy
from dotenv import load_dotenv
import os

load_dotenv()

bearer_token = os.getenv("BEARERTOKEN")
consumer_key = os.getenv("APIKEY")
consumer_secret = os.getenv("APIKEYSECRET")
access_token = os.getenv("ACESSTOKEN")
access_token_secret = os.getenv("ACESSTOKENSECRET")


def create_tweet(text: str) -> None:
    client = tweepy.Client(
        bearer_token=bearer_token,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    response = client.create_tweet(text=text)
    print(f"Tweet ID: {response.data['id']}")
