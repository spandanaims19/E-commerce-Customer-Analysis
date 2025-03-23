import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def calculate_rfm(data):
    # Setting the analysis date
    max_date=data["InvoiceDate"].max()+pd.Timedelta(days=1)
    # Group by customer
    rfm=data.groupby("CustomerID").agg({"InvoiceDate":lambda x: (max_date-x.max()).days,"InvoiceNo":"nunique", "TotalPrice":"sum"})

    rfm.columns=["Recency","Frequency","Monetary"]
    rfm=rfm[rfm["Monetary"]>0]

    return rfm

def segment_customers(rfm_data, n_clusters=4):
    # Segmenting using K-means clustering
    rfm_log=rfm_data.copy()
    rfm_log["Recency"]=np.log1p(rfm_log["Recency"])
    rfm_log["Frequency"]=np.log1p(rfm_log["Frequency"])
    rfm_log["Monetary"]=np.log1p(rfm_log["Monetary"])

    # Scale the data

    scaler=StandardScaler()
    rfm_scaled=scaler.fit_transform(rfm_log)

    # Apply K-means clustering

    kmeans=KMeans(n_clusters=n_clusters, random_state=42)
    rfm_data["Cluster"]=kmeans.fit_predict(rfm_scaled)

    # Analyzing the clusters to assign the names

    cluster_avg=rfm_data.groupby("Cluster").mean().sort_values("Monetary", ascending=False)

    # Map clusters to segment names

    segment_mapping={
        cluster_avg.index[0]:"VIP Customers",
        cluster_avg.index[1]:"Loyal Customers",
        cluster_avg.index[2]:"Potential Customers",
        cluster_avg.index[3]:"At Risk Customers",
    }

    rfm_data["Segment"]=rfm_data["Cluster"].map(segment_mapping)

    return rfm_data, cluster_avg
