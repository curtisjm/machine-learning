from collections import Counter
import numpy as np
import pandas as pd
import random
import warnings


def k_nearest_neighbors(data, predict, k=3):
    if len(data) >= k:
        warnings.warn("K is set to a value less than total voting groups")
    # list of [euclidean_distance, group]
    distances = []
    for group in data:
        for features in data[group]:
            euclidean_distance = np.linalg.norm(np.array(features) - np.array(predict))
            distances.append([euclidean_distance, group])

    votes = [i[1] for i in sorted(distances)[:k]]
    vote_result = Counter(votes).most_common(1)[0][0]

    return vote_result


df = pd.read_csv("data/breast-cancer-wisconsin.data")
df.replace("?", -99999, inplace=True)
df.drop(columns="id", axis=1, inplace=True)

# convert data to a list of lists
full_data = df.astype(float).values.tolist()
random.shuffle(full_data)

test_size = 0.2
train_set = {2: [], 4: []}
test_set = {2: [], 4: []}
# train with first 20% of data
train_data = full_data[: -int(test_size * len(full_data))]
# test with last 20% of data
test_data = full_data[-int(test_size * len(full_data)) :]

for i in train_data:
    # last column of lists is class column, append up until then
    train_set[i[-1]].append(i[:-1])

for i in test_data:
    test_set[i[-1]].append(i[:-1])

correct = 0
total = 0

for group in test_set:
    for data in test_set[group]:
        vote = k_nearest_neighbors(train_set, data, k=5)
        if group == vote:
            correct += 1
        total += 1

print("Accuracy: ", correct / total)
