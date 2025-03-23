import numpy as np
import pandas as pd
import os

from src.data_processing import load_and_clean_data
from src.segmentation import calculate_rfm, segment_customers
from src.recommendations import create_purchase_matrix, generate_association_rules, get_recommendations
from src.visualizations import plot_customer_segments, create_dashboard

def main():
    # Create visualization directory if it does not exists
    if not os.path.exists("visualizations"):
        os.makedirs("visualizations")
    
    print("Loading and cleaning the data......")
    retail_data_clean=load_and_clean_data("online+retail/Online Retail.xlsx")

    print("Performing RFM analysis and customer segmnetation......")
    rfm=calculate_rfm(retail_data_clean)
    rfm_segmented, cluster_avg=segment_customers(rfm)

    print("Creating Customer Segment Visualizations......")
    plot_customer_segments(rfm_segmented)

    print("Generating Product Recommendations......")
    purchase_matrix=create_purchase_matrix(retail_data_clean)
    rules=generate_association_rules(purchase_matrix)

    print("Creating Dashboard......")
    create_dashboard(rfm_segmented, retail_data_clean)

    if(rules is not None):
        customer_example=rfm_segmented.index[0]
        print(f"\nExample recommendations for customer {customer_example} : ")
        recommendations=get_recommendations(customer_example, purchase_matrix, rules, retail_data_clean)
        for rec in recommendations:
            print(f"Product : {rec[1]} (Code : {rec[0]}) - Lift : {rec[2]:.2f}")

    print("\nAnalysis Complete! Check the visualizations directory for outputs.")

if __name__=="__main__":
    main()
