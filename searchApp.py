import streamlit as st
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

indexName = "all_products"
load_dotenv()

# Get the values
# ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")
# ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
# ELASTIC_HOST = "https://localhost:9200"


# ELASTIC_CLOUD_URL = os.getenv("Elasticsearch_URL")
# ELASTIC_API_KEY = os.getenv("ELASTIC_API_KEY")  
ELASTIC_CLOUD_URL = st.secrets["Elasticsearch_URL"]
ELASTIC_API_KEY = st.secrets["ELASTIC_API_KEY"]  

try:
    es = Elasticsearch(
    ELASTIC_CLOUD_URL,
    api_key=ELASTIC_API_KEY
    )   

except ConnectionError as e:
    print("Connection Error:", e)
    
if es.ping():
    print("Successfully connected to ElasticSearch!!")
else:
    print("Oops!! Can not connect to Elasticsearch!")


# Cache the model loading to improve performance
@st.cache_resource
def load_model():
    return SentenceTransformer('all-mpnet-base-v2')


def search(input_keyword):
    model = load_model()
    vector_of_input_keyword = model.encode(input_keyword)

    # Use the modern search method with knn parameter
    res = es.search(
        index="all_products",
        knn={
            "field": "DescriptionVector",
            "query_vector": vector_of_input_keyword.tolist(),  # Convert numpy array to list
            "k": 20,  # Get more results to filter from
            "num_candidates": 500
        },
        source=["ProductName", "Description", "ProductID", "ProductBrand", "Price (INR)", "PrimaryColor"]
    )
    
    results = res["hits"]["hits"]
    
    # Filter for distinct products based on ProductName and Description
    seen_products = set()
    distinct_results = []

    for hit in results:
        product_key = (hit['_source']['ProductName'], hit['_source']['Description'])
        if product_key not in seen_products:
            seen_products.add(product_key)
            distinct_results.append(hit)
            
        # Stop when we have enough distinct results
        if len(distinct_results) >= 10:  # Limit to 10 distinct results
            break

    return distinct_results


def main():
    st.title("🛍️ Search Myntra Fashion Products")
    st.markdown("Find your perfect fashion items using AI-powered semantic search!")

    # Input: User enters search query
    search_query = st.text_input("Enter your search query", placeholder="e.g., blue shoes, casual shirt, women dress")

    # Button: User triggers the search
    if st.button("🔍 Search", type="primary"):
        if search_query:
            with st.spinner("Searching for products..."):
                # Perform the search and get results
                results = search(search_query)

            # Display search results
            if results:
                st.subheader(f"Found {len(results)} distinct products")
                
                for i, result in enumerate(results, 1):
                    with st.container():
                        if '_source' in result:
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                try:
                                    st.markdown(f"### {i}. {result['_source']['ProductName']}")
                                except Exception as e:
                                    st.error(f"Error displaying product name: {e}")
                                
                                try:
                                    # Display additional product info
                                    st.write(f"**Brand:** {result['_source'].get('ProductBrand', 'N/A')}")
                                    st.write(f"**Color:** {result['_source'].get('PrimaryColor', 'N/A')}")
                                    st.write(f"**Description:** {result['_source']['Description']}")
                                except Exception as e:
                                    st.error(f"Error displaying product details: {e}")
                            
                            with col2:
                                try:
                                    # Display price and similarity score
                                    price = result['_source'].get('Price (INR)', 'N/A')
                                    if price != 'N/A':
                                        st.metric("Price", f"₹{price:,}")
                                    
                                    # Display similarity score
                                    score = result.get('_score', 0)
                                    st.metric("Similarity", f"{score:.3f}")
                                    
                                except Exception as e:
                                    st.error(f"Error displaying metrics: {e}")
                            
                            st.divider()
            else:
                st.warning("No products found matching your search query. Try different keywords!")
        else:
            st.warning("Please enter a search query!")

    # Add some helpful information
    with st.sidebar:
        st.markdown("### 💡 Search Tips")
        st.markdown("""
        - Use descriptive terms like colors, styles, or occasions
        - Try different variations: "formal shirt" vs "dress shirt"
        - Combine attributes: "red summer dress"
        - Search by material: "cotton t-shirt"
        """)
        
        st.markdown("### 📊 How it works")
        st.markdown("""
        This app uses AI semantic search to understand the meaning 
        behind your search queries and find the most relevant products 
        based on their descriptions.
        """)


if __name__ == "__main__":
    main()