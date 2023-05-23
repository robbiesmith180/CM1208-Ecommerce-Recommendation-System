import math
import numpy as np

# Read in the purchase history
with open('history.txt') as f:
    # Splitting each line into 3 variables - using map function to convert string to integers
    num_customers, num_items, num_transactions = map(int, f.readline().split())

    # Instantiate purchase matrix with zeros
    purchase_history = np.zeros((num_customers, num_items))

    for line in f:
        customer_id, item_id = map(int, line.split())
        # Set positive entries to 1 in the matrix
        purchase_history[customer_id-1][item_id-1] = 1

# Count number of positive entries
num_positive_entries = np.sum(purchase_history)

# Output the result
print(f"Positive entries: {int(num_positive_entries)}")

# Compute item-to-item angles
corr = np.corrcoef(purchase_history.T)
angles = np.degrees(np.arccos(corr))

# Calculate average angle and print output
average_angle = np.mean(angles[np.triu_indices(num_items, k=1)])
print(f"Average angle: {average_angle:.2f}")

#Read in shopping cart items 
with open('queries.txt') as f:
    for line in f:
        shopping_cart = list(map(int, line.split()))
        print(f"Shopping cart: {' '.join(map(str, shopping_cart))}")
        recommended_items = []

        for item_id in shopping_cart:
            # Filter out items that are already in the shopping cart
            item_indices = [i for i in range(num_items) if i not in shopping_cart]

            # Compute correlation coefficients between the current item and all other items
            corr_coeffs = corr[item_id-1, item_indices]

            # Compute angles between the current item and all other items
            angles = np.degrees(np.arccos(corr_coeffs))

            # Find the item with the smallest angle
            best_index = np.argmin(angles)

            # If the angle is less than 90 degrees, add it to the recommended items list
            if angles[best_index] < 90 and angles[best_index] > 0:
                best_match = item_indices[best_index] + 1
                best_angle = angles[best_index]
                recommended_items.append((item_id, best_match, best_angle))
                print(f"Item: {item_id}; match: {best_match}; angle: {best_angle:.2f}")
            else:
                print(f"Item: {item_id}; no match")

        # Sort recommended items by angle in ascending order
        recommendation_list = [item[1] for item in sorted(recommended_items, key=lambda x: x[2])]

        # Output recommended item
        print(f"Recommend: {' '.join(map(str, recommendation_list))}")