# praw client setup and Reddit API wrapper
import praw
import yaml
import os

def get_reddit_client(config_path='../config/config.yaml'):
    """
    Initializes and returns a PRAW Reddit instance using credentials
    from a YAML configuration file.

    Args:
        config_path (str): The relative path to the configuration file.

    Returns:
        praw.Reddit: An authenticated Reddit instance, or None if authentication fails.
    """
    print(f"Attempting to load configuration from: {os.path.abspath(config_path)}")

    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        reddit_config = config['reddit']

        # Check if essential keys are present
        if not all(key in reddit_config for key in ['client_id', 'client_secret', 'user_agent']):
            print("Error: Missing one or more required keys (client_id, client_secret, user_agent) in config.yaml")
            return None

        print("Configuration loaded successfully. Initializing PRAW client...")
        
        # Initialize the Reddit instance
        reddit_client = praw.Reddit(
            client_id=reddit_config['client_id'],
            client_secret=reddit_config['client_secret'],
            user_agent=reddit_config['user_agent']
        )

        # The read_only property will be True if the client is in read-only mode.
        # A quick check to see if we have a valid, unauthenticated (read-only) or authenticated session.
        print(f"PRAW client initialized. Read-only mode: {reddit_client.read_only}")
        return reddit_client

    except FileNotFoundError:
        print(f"Error: Configuration file not found at {os.path.abspath(config_path)}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during PRAW initialization: {e}")
        return None

# --- Test Block ---
# This block allows to run the file directly to test Reddit API connection.


# if __name__ == "__main__":
#     print("--- Running Reddit Client Test ---")
    
#     # Initialize the client
#     # The path is relative to this script's location in `ingestion/`
#     reddit = get_reddit_client(config_path='../config/config.yaml')

#     if reddit:
#         try:
#             # Choose a subreddit to test with
#             subreddit_name = 'cybersecurity'
#             print(f"\nSuccessfully connected to Reddit API. Fetching top 5 posts from r/{subreddit_name}...")
            
#             # Fetch the subreddit
#             subreddit = reddit.subreddit(subreddit_name)
            
#             # Get the top 5 "hot" posts
#             hot_posts = subreddit.hot(limit=5)
            
#             # Print the title of each post
#             for i, post in enumerate(hot_posts):
#                 print(f"  {i+1}. {post.title} (Score: {post.score})")
            
#             print("\n--- Test complete. Connection successful! ---")

#         except Exception as e:
#             print(f"\nAn error occurred while fetching data from Reddit: {e}")
#             print("Please check your API credentials and network connection.")
#     else:
#         print("\n--- Test failed. Could not initialize Reddit client. ---")
#         print("Please check the error messages above and ensure your config/config.yaml is correct.")

