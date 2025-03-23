import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec

def plot_customer_segments(rfm_data):
    # Create visualizations of customer segments

    plt.figure(figsize=(15, 10))

    # Plot 1: Customer Distribution by Segment
    plt.subplot(2,2,1)
    segment_counts=rfm_data["Segment"].value_counts()
    segment_counts.plot(kind="barh", color=sns.color_palette("viridis", 4))
    plt.title("Customer Distribution by Segment")
    plt.xlabel("Number of Customers")

    # Plot 2:Recency vs Frequency
    plt.subplot(2,2,2)
    sns.scatterplot(x="Recency",y="Frequency", hue="Segment", data=rfm_data, palette="viridis", alpha=0.7)
    plt.title("Recency vs Frequency")

    # Plot 3:Frequency vs Monetary
    plt.subplot(2,2,3)
    sns.scatterplot(x="Frequency", y="Monetary", hue="Segment", data=rfm_data, palette="viridis", alpha=0.7)
    plt.title("Frequency vs Monetary")

    # Plot 4:Recency vs Monetary
    plt.subplot(2,2,4)
    sns.scatterplot(x="Recency", y="Monetary", hue="Segment", data=rfm_data, palette="viridis", alpha=0.7)
    plt.title("Recency vs Monetary")

    plt.tight_layout()
    plt.savefig("visualizations/customer_segments.png", dpi=300, bbox_inches="tight")
    plt.show()

    return

def create_dashboard(rfm_data, retail_data_clean):
    """
    Create a comprehensive dashboard visualizing key metrics and insights
    from the e-commerce customer analysis.
    
    Parameters:
    rfm_data (DataFrame): DataFrame containing RFM metrics and customer segments
    retail_data_clean (DataFrame): Cleaned retail transaction data
    
    Returns:
    None (saves visualization to file and displays it)
    """
    # Create a larger figure for the dashboard
    plt.figure(figsize=(20, 16))
    gs = GridSpec(3, 3, figure=plt.gcf())
    
    # Set the style
    plt.style.use('seaborn-whitegrid')
    sns.set_palette("viridis")
    
    # 1. Customer Segmentation Pie Chart
    ax1 = plt.subplot(gs[0, 0])
    segment_counts = rfm_data['Segment'].value_counts()
    ax1.pie(segment_counts, labels=segment_counts.index, autopct='%1.1f%%', 
            startangle=90, colors=sns.color_palette('viridis', len(segment_counts)))
    ax1.set_title('Customer Segments Distribution', fontsize=12)
    
    # 2. RFM Metrics by Segment (Radar Chart-like using bar chart)
    ax2 = plt.subplot(gs[0, 1:])
    segment_metrics = rfm_data.groupby('Segment')[['Recency', 'Frequency', 'Monetary']].mean()
    
    # Normalize the values for better visualization
    for col in ['Recency', 'Frequency', 'Monetary']:
        segment_metrics[col] = segment_metrics[col] / segment_metrics[col].max()
    
    segment_metrics.plot(kind='bar', ax=ax2)
    ax2.set_title('Normalized RFM Metrics by Segment', fontsize=12)
    ax2.set_ylim(0, 1.1)
    ax2.set_ylabel('Normalized Value')
    ax2.legend(title='Metric')
    
    # 3. Monthly Sales Trend
    ax3 = plt.subplot(gs[1, :2])
    retail_data_clean['YearMonth'] = retail_data_clean['InvoiceDate'].dt.strftime('%Y-%m')
    monthly_sales = retail_data_clean.groupby('YearMonth')['TotalPrice'].sum().reset_index()
    sns.lineplot(x='YearMonth', y='TotalPrice', data=monthly_sales, marker='o', ax=ax3)
    ax3.set_title('Monthly Sales Trend', fontsize=12)
    ax3.set_xlabel('Month')
    ax3.set_ylabel('Total Sales')
    # Rotate x-axis labels for better readability
    ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45, ha='right')
    
    # 4. Top Products Horizontal Bar Chart
    ax4 = plt.subplot(gs[1, 2])
    top_products = retail_data_clean.groupby('Description')['Quantity'].sum().nlargest(10).sort_values(ascending=True)
    sns.barplot(y=top_products.index, x=top_products.values, ax=ax4, palette='viridis')
    ax4.set_title('Top 10 Products by Quantity Sold', fontsize=12)
    ax4.set_xlabel('Quantity Sold')
    ax4.set_ylabel('')
    
    # 5. Customer Recency vs Monetary Value Scatter Plot
    ax5 = plt.subplot(gs[2, 0])
    sns.scatterplot(x='Recency', y='Monetary', hue='Segment', data=rfm_data, palette='viridis', alpha=0.7, ax=ax5)
    ax5.set_title('Recency vs Monetary Value', fontsize=12)
    ax5.legend(loc='upper right')
    
    # 6. Sales by Country
    ax6 = plt.subplot(gs[2, 1])
    country_sales = retail_data_clean.groupby('Country')['TotalPrice'].sum().nlargest(10).sort_values(ascending=True)
    sns.barplot(y=country_sales.index, x=country_sales.values, ax=ax6, palette='viridis')
    ax6.set_title('Top 10 Countries by Sales', fontsize=12)
    ax6.set_xlabel('Total Sales')
    ax6.set_ylabel('')
    
    # 7. Customer Purchase Frequency Distribution
    ax7 = plt.subplot(gs[2, 2])
    sns.histplot(rfm_data['Frequency'], bins=30, kde=True, ax=ax7)
    ax7.set_title('Customer Purchase Frequency Distribution', fontsize=12)
    ax7.set_xlabel('Number of Purchases')
    ax7.set_ylabel('Number of Customers')
    
    # Add a title to the entire dashboard
    plt.suptitle('E-commerce Customer Analysis Dashboard', fontsize=16, y=0.98)
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    
    # Save the dashboard
    plt.savefig('visualizations/ecommerce_dashboard.png', dpi=300, bbox_inches='tight')
    
    # Display the dashboard
    plt.show()
    
    return
