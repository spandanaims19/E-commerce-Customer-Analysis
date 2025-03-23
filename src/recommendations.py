import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

def create_purchase_matrix(data):
    # Create a purchase matrix for association rules

    purchase_history=data.groupby(["CustomerID","StockCode"])["Quantity"].sum().unstack().fillna(0)
    purchase_history_binary=(purchase_history>0).astype(int)

    return purchase_history_binary

def generate_association_rules(purchase_matrix, min_support=0.01):
    # Generate the association rules from the purchase history

    # Simple data reduction by taking only items purchased at least 20 times
    item_counts=purchase_matrix.sum()
    frequent_items=item_counts[item_counts>=20].index
    reduced_matrix=purchase_matrix[frequent_items]

    # Ensure boolean type to avoid warning and improve performance
    reduced_matrix=reduced_matrix.astype(bool)

    # Increase min_support to reduce memory requirements
    frequent_items=apriori(reduced_matrix, min_support=0.03, use_colnames=True)

    if(len(frequent_items))>0:
        rules=association_rules(frequent_items, metric="lift", min_threshold=1)
        return rules
    else:
        print("No frequent itmes found with the given support threshold.")
        return None
    

def get_recommendations(customer_id, purchase_matrix, rules, product_info, num_recommendations=5):
    # Get product recommendations for a specific customer

    if customer_id not in purchase_matrix.index:
        return []
    
    customer_purchases=purchase_matrix.loc[customer_id]
    items_purchased=set(customer_purchases[customer_purchases>0].index)

    recommendations={}

    # For each item that the customer has purchased
    for item in items_purchased:
        # Find rules where this item is in the antecedent
        item_rules=rules[rules["antecedents"].apply(lambda x:item in x)]

        # for each rule

        for _,rule in item_rules.iterrows():
            # Get the consequent items
            consequent_items=set(rule["consequents"])

            # Add items not already purchased to recommendations with their lift score
            for rec_item in consequent_items - items_purchased:
                if rec_item in recommendations:
                    recommendations[rec_item]=max(recommendations[rec_item], rule["lift"])
                else:
                    recommendations[rec_item]=rule["lift"]
        
    # Sort by lift and return top N
    sorted_recommendations=sorted(recommendations.items(), key=lambda x:x[1], reverse=True)

    # Get actual product descriptions
    result=[]

    for stock_code, lift in sorted_recommendations[:num_recommendations]:
        try:
            product_desc=product_info[product_info["StockCode"]==stock_code]["Description"].iloc[0]
            result.append((stock_code, product_desc, lift))
        except:
            result.append((stock_code, "Unknown Product", lift))
    
    return result
