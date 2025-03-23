# E-Commerce Customer Segmentation & Recommendation Engine

A data analytics project that transforms e-commerce transaction data into actionable business insights through customer segmentation and personalized product recommendations.

## Overview

This project analyzes online retail data to help businesses better understand their customers and increase sales. It segments customers using RFM analysis and K-means clustering, then generates personalized product recommendations using association rule mining.

## Tech Stack

- **Python**: Core programming language
- **Pandas & NumPy**: Data manipulation and numerical operations
- **Scikit-learn**: Implementation of K-means clustering
- **MLxtend**: Association rule mining for product recommendations
- **Seaborn & Matplotlib**: Data visualization
- **Jupyter Notebooks**: Analysis documentation and presentation

## Project Structure

The project follows a modular approach for better organization and reusability:

- **`src/`**: Core Python modules
  - `data_processing.py`: Data loading, cleaning, and preprocessing
  - `segmentation.py`: RFM analysis and customer clustering
  - `recommendations.py`: Association rule mining and product suggestions
  - `visualization.py`: Functions for creating insightful visualizations

- **`notebooks/`**: Jupyter notebooks that demonstrate the analysis
  - `1_data_exploration.ipynb`: Initial data investigation and cleaning
  - `2_customer_segmentation.ipynb`: Customer segmentation analysis
  - `3_product_recommendations.ipynb`: Product recommendation generation

## Key Features

- Customer segmentation based on purchase behavior using RFM and K-means
- Product recommendation system using association rule mining
- Comprehensive data visualizations for business insights
- Modular code design for easy extension and reuse

## Getting Started

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the Jupyter notebooks in sequence to see the analysis

## Future Improvements

- Implement time-series analysis for seasonal trends
- Add demographic data for enhanced segmentation
- Create interactive dashboard for business users
