import pandas as pd
from fuzzywuzzy import fuzz
from openai import OpenAI

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


# AI Version below
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

completion = client.chat.completions.create(
  extra_headers={
    "HTTP-Referer": "", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "", # Optional. Site title for rankings on openrouter.ai.
  },
  extra_body={},
  model="deepseek/deepseek-r1-distill-llama-70b:free",
  messages=[
    {
      "role": "user",
      "content": "Please create a negative keyword list from search terms collected over a few months. We are running google shopping ads for an online grocery store. These are the search terms - " + str(search_terms['search_term']) + ". Please analyse the full entire list and only return search terms that are not high value terms and that do not relate to grocery items or general store items."
    }
  ]
)
print(completion.choices[0].message.content)

# Create a new column to label search terms as relevant or irrelevant
#search_terms['relevant'] = search_terms['search_term'].apply(lambda x: is_relevant(x, products['product_name']))

# Filter out irrelevant search terms
#irrelevant_search_terms = search_terms[search_terms['relevant'] == False]

# Export irrelevant search terms to a file for negative keywords
#irrelevant_search_terms.to_csv('irrelevant_search_terms.csv', index=False)


