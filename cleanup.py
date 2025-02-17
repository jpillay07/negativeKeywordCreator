import pandas as pd
from fuzzywuzzy import fuzz

# Load your data (search terms and products)
search_terms = pd.read_excel('SearchTerms/search_terms.xlsx')  # Search terms from Google Ads
products = pd.read_csv('Products/products.csv')  # Product list

# Function to check for relevance (exact or fuzzy match)
def is_relevant(search_term, product_names):
    for product in product_names:
        # Fuzzy match (you can adjust the threshold based on your needs)
        if fuzz.partial_ratio(search_term.lower(), product.lower()) > 50:
            return True
    print("Done with " + search_term)
    return False

# Create a new column to label search terms as relevant or irrelevant
search_terms['relevant'] = search_terms['search_term'].apply(lambda x: is_relevant(x, products['product_name']))

# Filter out irrelevant search terms
irrelevant_search_terms = search_terms[search_terms['relevant'] == False]

# Export irrelevant search terms to a file for negative keywords
irrelevant_search_terms.to_csv('irrelevant_search_terms.csv', index=False)
