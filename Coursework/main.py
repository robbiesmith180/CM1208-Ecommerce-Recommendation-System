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
num_positive_entries = sum(sum(row) for row in purchase_history)

# Output the result
print(f"Positive entries: {int(num_positive_entries)}")

# Compute item-to-item angles
sum_angles = 0
count_angles = 0
for i in range(num_items):
    for j in range(i+1, num_items):
        #Calculate dot product between first 2 columns of matrix
        dot_product = np.dot(purchase_history[:,i], purchase_history[:,j])
        #Calculating norms of each column
        norm_i = np.linalg.norm(purchase_history[:,i])
        norm_j = np.linalg.norm(purchase_history[:,j])
        #Calculate cosine simularity
        cosine_sim = dot_product / (norm_i * norm_j)
        #Calculate anlge in degrees between two columns of matrix
        angle = math.degrees(math.acos(cosine_sim))
        sum_angles += angle
        count_angles += 1

# Calculate average angle and print output
average_angle = sum_angles / count_angles
print(f"Average angle: {average_angle:.2f}")

#Read in shopping cart items 
with open('queries.txt') as f:

    for line in f:
        shopping_cart = list(map(int, line.split()))
        print(f"Shopping cart: {' '.join(map(str, shopping_cart))}")
        recommended_items = {}
        
        for item_id in shopping_cart:
            best_match = None
            best_angle = 90

            for i in range(num_items):
                #Only use items not in current shopping cart
                if i not in shopping_cart:
                    #Calculate dot product between current item and potential match
                    dot_product = np.dot(purchase_history[:,item_id-1], purchase_history[:,i])
                    #Calculate norms of each vector
                    norm_i = np.linalg.norm(purchase_history[:,item_id-1])
                    norm_j = np.linalg.norm(purchase_history[:,i])
                    #Calculate cosine simularity between two items
                    cosine_sim = dot_product / (norm_i * norm_j)
                    #If cosine simularity is within allowed range, calculate angle between two vectors
                    if -1 <= cosine_sim <= 1:
                        angle = math.degrees(math.acos(cosine_sim))
                    else:
                        angle = 90
                    #Updating the best match and best angle if the current match is better than the previous ones
                    if angle < best_angle:
                        best_match = i+1
                        best_angle = angle
            #If match is less than 90 degrees add it to recommended items
            if best_angle < 90 and best_angle > 0:
                print(f"Item: {item_id}; match: {best_match}; angle: {best_angle:.2f}")
                recommended_items[best_match] = min(recommended_items.get(best_match, 91), best_angle)
            else:
                print(f"Item: {item_id}; no match")
        
        #Sort dictionary by angle in ascending order and return list of keys
        recommendation_list = sorted(recommended_items, key=recommended_items.get)

        #Output recommended item
        print(f"Recommend: {' '.join(map(str, recommendation_list))}")

                         

