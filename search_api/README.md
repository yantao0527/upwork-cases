Search API
==========

There is the example code of the google Custom Search API with python.

First, you'll need to install the google-api-python-client package. You can do this by running the following command in your terminal:

```
make install
```

You'll also need to initiate the .env file.

```
cp .env.example .env
```

Next, you'll need to create a project on the Google Cloud Platform, enable the Custom Search API, and create an API key. You can follow the instructions here to do that: https://developers.google.com/custom-search/v1/overview#create_a_project_and_api_key

Once you have your API key, replace YOUR_API_KEY in the .env file with your actual API key.

In the SEARCH_ENGINE_ID variable, you'll need to replace YOUR_SEARCH_ENGINE_ID with the ID of the Custom Search Engine you created.

In the QUERY variable, you can specify the search term you want to use.

```
make demo
```

The script will print the title and link of each search result.