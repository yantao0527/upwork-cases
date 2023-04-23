Search Params
=============

 Here's an example of how you can modify your Python API code to sort search results by date and retrieve only articles published within the last 7 days:

 ```
 import requests
from datetime import datetime, timedelta

def search_news(url):
    # Get the text from the post on your website
    post_text = get_post_text(url)

    # Construct the search query
    search_query = construct_search_query(post_text)

    # Define the search parameters
    search_params = {
        "q": search_query,
        "tbm": "nws",  # Search news articles only
        "tbs": f"qdr:w",  # Search articles published within the last week
        "num": 10,  # Return 10 results
        "gl": "us",  # Search from the United States
        "hl": "en"  # Search results in English
    }

    # Make the API call to the search engine
    response = requests.get("https://www.google.com/search", params=search_params)

    # Parse the search results
    search_results = parse_search_results(response.text)

    # Return the search results
    return search_results
```

Here, we've added the "tbs": f"qdr:w" parameter to the search parameters, which tells the search engine to only return articles published within the last week. You can modify this parameter to "qdr:d" if you want to search articles published within the last 24 hours, or "qdr:m" if you want to search articles published within the last month.

To search the news section instead of the web, you can modify the "tbm" parameter in the search parameters from "nws" to "nws":

```
search_params = {
    "q": search_query,
    "tbm": "nws",  # Search news articles only
    "tbs": f"qdr:w",  # Search articles published within the last week
    "num": 10,  # Return 10 results
    "gl": "us",  # Search from the United States
    "hl": "en"  # Search results in English
}
```

This tells the search engine to only return results from the news section.

If you only want to search news articles and exclude other types of content, you can also add the "nws" value to the "restrict_sr" parameter:

```
search_params = {
    "q": search_query,
    "tbm": "nws",  # Search news articles only
    "tbs": f"qdr:w",  # Search articles published within the last week
    "num": 10,  # Return 10 results
    "gl": "us",  # Search from the United States
    "hl": "en",  # Search results in English
    "restrict_sr": "nws"  # Only search news articles
}
```
