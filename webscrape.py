import newspaper
from newspaper import news_pool
import pandas as pd

##CREDITS
## https://towardsdatascience.com/the-easy-way-to-web-scrape-articles-online-d28947fc5979
## edited by: Kayra Arai
# The code below is a simple web scraping code that will scrape articles from CNN and BBC News.


# The various News Sources we will like to web scrape from
cnn = newspaper.build('https://edition.cnn.com', memoize_articles=False)
bbc = newspaper.build("https://www.bbc.com/news", memoize_articles=False)

# Place the sources in a list
papers = [cnn, bbc]

# Essentially you will be downloading 4 articles parallely per source.
# Since we have two sources, that means 8 articles are downloaded at any one time. 
# Greatly speeding up the processes.
# Once downloaded it will be stored in memory to be used in the for loop below 
# to extract the bits of data we want.
news_pool.set(papers, threads_per_source=4)

news_pool.join()

# Create our final dataframe
final_df = pd.DataFrame()

# Create a download limit per sources
# NOTE: You may not want to use a limit
limit = 100

for source in papers:
    # temporary lists to store each element we want to extract
    list_title = []
    list_text = []
    list_source =[]

    count = 0

for source in papers:
    # Initialize temporary lists to store each element we want to extract
    list_title = []
    list_text = []
    list_source = []

    # Initialize count to keep track of how many articles we've processed
    count = 0

    # Process each article in the source
    for article_extract in source.articles:
        # Check the limit at the beginning to avoid unnecessary processing
        if count >= limit:  # Adjusted to >= to include exactly 'limit' articles
            break

        try:
            article_extract.parse()

            # Append the elements we want to extract
            list_title.append(article_extract.title)
            list_text.append(article_extract.text)
            list_source.append(article_extract.source_url)

            print(f"Article {count} downloaded")
            count += 1  # Update count after a successful download
        except Exception as e:
            print(f"Error occurred while scraping article: {str(e)}")

    # Create a temporary DataFrame for the current source
    temp_df = pd.DataFrame({'Title': list_title, 'Text': list_text, 'Source': list_source})
    
    # Use pd.concat instead of .append to avoid AttributeError
    final_df = pd.concat([final_df, temp_df], ignore_index=True)

# From here you can export this to csv file
final_df.to_csv('scraped_articles.csv')