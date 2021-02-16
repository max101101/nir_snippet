import vk
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
import numpy as np

def get_members(groupid):
	first = vk_api.groups.getMembers(group_id=groupid, v=5.92)
	data = first["items"]
	count = first["count"] // 1000

	for i in range(1, count+1):
		data = data + vk_api.groups.getMembers(group_id=groupid, v=5.92, offset=i*1000)["items"]

	return data


def save_data(data, filename="data.txt"):
	with open(filename, "w") as file:
		for item in data:
			file.write(str(item) + "\n")


def enter_data(filename="data.txt"):
	with open(filename) as file:
		b = []
		for line in file:
			b.append(line[:-1])

	return b


def get_intersection(group1, group2):
	group1 = set(group1)
	group2 = set(group2)
	intersection = group1.intersection(group2)

	return list(intersection)


def union_members(group1, group2):
	group1 = set(group1)
	group2 = set(group2)
	union = group1.union(group2)

	return list(union)

mapping = {
	"baraholka_graufr": 0, # 92996
	"airsoft_life": 1, # 64174
	"airsoft_pain": 2, # 55527
	"airsoftgroup": 3, # 132067
	"ostrike": 4, # 23123
}

def form_data():
	union = []
	for group in mapping.keys():
		members = enter_data(filename=group+".txt")
		union = union_members(union, members)

	data = {}
	for user in union:
		data[user] = [0 for _ in range(len(mapping))]

	for group in mapping.keys():
		members = enter_data(filename=group+".txt")
		for user in members:
			data[user][mapping[group]] = 1

	return data

def form_Xy(data):
	X = []
	y = []
	for row in data.values():
		X.append(row[:-1]) 
		y.append(row[-1]) 

	return np.array(X), np.array(y)

if __name__ == "__main__":
	#token = "7af307a27af307a27af307a2847a8571be77af37af307a21ad8cdc3a1c9eca11a1ca8b9"
	#session = vk.Session(access_token=token)
	#vk_api = vk.API(session)

	#members = get_members(group)
	#save_data(members, filename=group+".txt")

	data = form_data()

	X, y = form_Xy(data)
	#X, y = load_iris(return_X_y=True)
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)
	gnb = GaussianNB()
	y_pred = gnb.fit(X_train, y_train).predict(X_test)
	print("Number of mislabeled points out of a total %d points : %d" % (X_test.shape[0], (y_test != y_pred).sum()))
	counts = [0, 0]
	for v in y_pred:
		counts[v] = counts[v] + 1 
	print(counts)
