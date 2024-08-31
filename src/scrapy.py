import wikipediaapi  # Requires installation: pip install wikipedia-api
import pandas as pd
import concurrent.futures
from tqdm import tqdm
import os

def fetch_wikipedia_data(topic_name, verbose=True):
    def get_page_data(link):
        try:
            page = wiki.page(link)
            if page.exists():
                return {'page': link, 'text': page.text, 'link': page.fullurl,
                        'categories': list(page.categories.keys())}
        except:
            return None

    # Initialize Wikipedia API
    wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.WIKI, user_agent='MyBot/1.0')
    page = wiki.page(topic_name)

    if not page.exists():
        print(f'Page {topic_name} does not exist.')
        return

    links = list(page.links.keys())
    progress_bar = tqdm(desc='Scraping Links', total=len(links)) if verbose else None

    collected_data = [{'page': topic_name, 'text': page.text, 'link': page.fullurl,
                       'categories': list(page.categories.keys())}]

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_link = {executor.submit(get_page_data, link): link for link in links}
        for future in concurrent.futures.as_completed(future_to_link):
            result = future.result()
            if result:
                collected_data.append(result)
            if verbose:
                progress_bar.update(1)
                
    if verbose:
        progress_bar.close()

    # Filter and clean up the data
    excluded_namespaces = ('Wikipedia', 'Special', 'Talk', 'LyricWiki', 'File', 'MediaWiki',
                           'Template', 'Help', 'User', 'Category talk', 'Portal talk')

    df = pd.DataFrame(collected_data)
    df = df[(df['text'].str.len() > 20) & ~(df['page'].str.startswith(excluded_namespaces))]
    df['categories'] = df['categories'].apply(lambda categories: [cat[9:] for cat in categories])
    df['topic'] = topic_name
    print(f'Wikipedia pages scraped: {len(df)}')

    return df

def scrape_single_page(page_title):
    wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.WIKI, user_agent='MyBot/1.0')
    page = wiki.page(page_title)
    if not page.exists():
        print(f'Page {page_title} does not exist.')
        return

    return pd.DataFrame({
        'page': [page_title],
        'text': [page.text],
        'link': [page.fullurl],
        'categories': [[cat[9:] for cat in list(page.categories.keys())]]
    })

# Load actor data
actor_file_path = os.path.join('assets', 'Best Actors - Top 2501.csv')
actors_df = pd.read_csv(actor_file_path, engine='python', encoding='windows-1252')

# Prepare the output directory
output_directory = os.path.join('..', 'actors and movies')
os.makedirs(output_directory, exist_ok=True)

# Scrape data for each actor and save as JSON
for actor in actors_df['Name']:
    print(f'Scraping data for actor: {actor}')
    actor_data = fetch_wikipedia_data(actor, verbose=True)
    if actor_data is not None:
        output_path = os.path.join(output_directory, f'{actor}.json')
        actor_data.to_json(output_path)

# Load movie data
movie_file_path = os.path.join('assets', 'Top 50001.csv')
movies_df = pd.read_csv(movie_file_path, engine='python')

# Scrape data for each movie and save as JSON
for movie in movies_df['Title']:
    print(f'Scraping data for movie: {movie}')
    movie_data = fetch_wikipedia_data(movie)
    if movie_data is not None:
        output_path = os.path.join(output_directory, f'{movie}.json')
        movie_data.to_json(output_path)
