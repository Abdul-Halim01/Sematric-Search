# 🛍️ Myntra Fashion Semantic Search System (for test)

A powerful AI-driven semantic search engine that understands the meaning behind user queries to find the most relevant fashion products from Myntra's catalog. Unlike traditional keyword-based search, this system uses advanced sentence embeddings to deliver intelligent, context-aware search results.

## 🌟 Features

- **Semantic Understanding**: Uses BERT-based embeddings to understand query context and meaning
- **AI-Powered Search**: Leverages `all-mpnet-base-v2` model for high-quality sentence embeddings
- **Vector Database**: Utilizes Elasticsearch with dense vector support for fast similarity search
- **Real-time Search**: Interactive Streamlit web interface for instant search results
- **Duplicate Filtering**: Intelligent deduplication to show only unique products
- **Rich Product Information**: Displays product details including brand, color, price, and descriptions

## 🏗️ Architecture

```
User Query → Sentence Transformer → Vector Embedding → Elasticsearch KNN Search → Ranked Results
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Elasticsearch Cloud account or local Elasticsearch instance
- Required Python packages (see requirements below)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Abdul-Halim01/Sematric-Search.git
   cd semantic-search-myntra
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file or configure Streamlit secrets:
   ```env
   Elasticsearch_URL=your_elasticsearch_cloud_url
   ELASTIC_API_KEY=your_api_key
   ```

4. **Run the application**
   ```bash
   streamlit run searchApp.py
   ```

## 📦 Dependencies

```python
streamlit>=1.28.0
elasticsearch>=8.0.0
sentence-transformers>=2.2.2
python-dotenv>=1.0.0
pandas>=1.5.0
numpy>=1.24.0
```

## 🔧 Project Structure

```
├── searchApp.py           # Main Streamlit application
├── indexData1.ipynb       # Data preprocessing and indexing notebook
├── indexMapping.py        # Elasticsearch index mapping configuration
├── myntra_products_catalog.csv  # Product dataset
├── requirements.txt       # Python dependencies
└── README.md            
```

## 🎯 How It Works

### 1. Data Preprocessing
- Loads Myntra product catalog (500 products)
- Cleans and processes product descriptions
- Generates 768-dimensional embeddings using `all-mpnet-base-v2`

### 2. Vector Indexing
- Creates Elasticsearch index with dense vector mapping
- Stores product metadata alongside embeddings
- Optimizes for fast KNN (K-Nearest Neighbors) search

### 3. Semantic Search
- Converts user queries into vector embeddings
- Performs similarity search using cosine similarity
- Returns top-k most relevant products with confidence scores

## 🔍 Search Examples

Try these semantic queries:
- `"blue shoes"` - Finds blue footwear items
- `"casual summer dress"` - Locates appropriate seasonal clothing
- `"formal office wear"` - Discovers professional attire
- `"cotton comfortable shirt"` - Searches by material and comfort

## 🛠️ Technical Implementation

### Elasticsearch Configuration
```python
# Vector field mapping
"DescriptionVector": {
    "type": "dense_vector",
    "dims": 768,
    "index": True,
    "similarity": "l2_norm"
}
```

### Search Query Structure
```python
# KNN search with embedding similarity
res = es.search(
    index="all_products",
    knn={
        "field": "DescriptionVector",
        "query_vector": vector_of_input_keyword.tolist(),
        "k": 20,
        "num_candidates": 500
    }
)
```

## 📊 Performance Metrics

- **Index Size**: 500 products with 768-dimensional embeddings
- **Search Latency**: < 100ms for typical queries
- **Similarity Accuracy**: Uses cosine similarity for precise matching
- **Duplicate Handling**: Intelligent filtering for unique results

## 🎨 User Interface

The Streamlit interface provides:
- Clean, intuitive search box
- Real-time search results
- Product cards with images, prices, and descriptions
- Similarity scores for transparency
- Helpful search tips and suggestions

## 🚦 Getting Started - Step by Step

### 1. Set Up Elasticsearch

**Option A: Elasticsearch Cloud**
1. Create account at [Elastic Cloud](https://cloud.elastic.co/)
2. Create a deployment
3. Get your cloud URL and API key

**Option B: Local Installation**
1. Install Elasticsearch locally
2. Configure with proper security settings

### 2. Prepare the Data
```bash
# Run the Jupyter notebook to process and index data
jupyter notebook indexData1.ipynb
```

### 3. Launch the Search Interface
```bash
streamlit run searchApp.py
```

## 🔧 Configuration

### Environment Variables
- `Elasticsearch_URL`: Your Elasticsearch endpoint
- `ELASTIC_API_KEY`: Authentication key for Elasticsearch

### Model Configuration
- **Embedding Model**: `all-mpnet-base-v2` (384M parameters)
- **Vector Dimensions**: 768
- **Similarity Metric**: L2 norm (Euclidean distance)


## 🙏 Acknowledgments

- **Sentence Transformers**: For providing excellent embedding models
- **Elasticsearch**: For powerful vector search capabilities
- **Streamlit**: For the intuitive web interface framework
- **Myntra**: For the fashion product dataset

