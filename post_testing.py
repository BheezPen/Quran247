import requests
import json

# Set the Instagram API endpoint
API_ENDPOINT = "https://www.instagram.com/graphql/query/"

# Set the access token for the Instagram API
ACCESS_TOKEN = "your_access_token_here"

# Set the message to be posted on Instagram
MESSAGE = "Hello, Instagram!"

# Set the Instagram API parameters
params = {
    "query_hash": "your_query_hash_here",
    "variables": {
        "input": {
            "text": MESSAGE
        }
    }
}

# Make the POST request to the Instagram API
response = requests.post(API_ENDPOINT, json=params, headers={ "Authorization": "Bearer " + ACCESS_TOKEN })

# Print the response from the Instagram API
print(response.text)
'''
This script uses the requests library to send a POST request to the Instagram GraphQL API. 
You will need to replace your_access_token_here with a valid access token and your_query_hash_here with the appropriate query hash. 
You can also modify the MESSAGE variable to specify the message that you want to post.

Note that this script is just an example and may not work out of the box. 
You may need to make additional modifications or perform additional setup in order to use it successfully.'''



'''
Instagram token gotten is 
IGQVJYWDBPYXdjaTNIMExBMUJaRDV3M1ZA5X1JzR1MyeEluLVlPV3lSM3pOaF9SdEJLY056VGE4RlNXNk04cjJSRFhNMnVwNXRwYUhINllFWjlMdUhGWHdicksydWhkQzVucUpXTEZAoMVZAaWkxNSmVpSQZDZD

generated in the 19th april 2023'''