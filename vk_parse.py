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
	"bmw": 0,
	"mercedesbenzrussia": 1,
	"audi": 2,
	"german_luxury": 3,
	"nissanrussia": 4,
	"baraholka_graufr": 5, # 92996
	"airsoft_life": 6, # 64174
	"airsoft_pain": 7, # 55527
	"airsoftgroup": 8, # 132067
	"ostrike": 9, # 23123
	"mvdota": 10,
	"itpedia_youtube": 11,
	"it_joke": 12,
	"otchisleno": 13,
	"gnummetv": 14,
	"cartwork": 15,
	"hobbyworld": 16,
	"mhkoff": 17,
	"catism": 18,
	"playstation.world": 19,
	"questions_of_chgk": 20,
	"igromania": 21,
	"igroman": 22,
	"vizit.condoms": 23,
	"navi": 24,
	"softclubgames": 25,
	"ustami_msu": 26,
	"playstationru": 27,
	"gagagames": 28,
	"by_duran": 29,
}

def form_report():
	f = open("report.txt", "w")
	keys = list(mapping.keys())
	l = len(keys)
	for i in range(l):
		group1 = keys[i]
		members1 = enter_data(filename=group1+".txt")
		for j in range(i+1, l):
			group2 = keys[j]
			members2 = enter_data(filename=group2+".txt")
			inter = get_intersection(members1, members2)
			f.write(group1 + " " + group2 + " " + str(len(inter)/min(len(members1), len(members2))) + "\n")
		print(i, l)


def form_data():
	union = []
	for group in mapping.keys():
		members = enter_data(filename=group+".txt")
		union = union_members(union, members)

	print("union done")

	data = {}
	for user in union:
		data[user] = [0 for _ in range(len(mapping))]

	print("mem alloc done")

	for group in mapping.keys():
		members = enter_data(filename=group+".txt")
		for user in members:
			data[user][mapping[group]] = 1

	print("dataset done")

	return data


def form_Xy(data):
	X = []
	y = []
	for row in data.values():
		X.append(row[:-1]) 
		y.append(row[-1]) 

	return np.array(X), np.array(y)

if __name__ == "__main__":
	'''
	token = "7af307a27af307a27af307a2847a8571be77af37af307a21ad8cdc3a1c9eca11a1ca8b9"
	session = vk.Session(access_token=token)
	vk_api = vk.API(session)

	group = "by_duran"
	members = get_members(group)
	save_data(members, filename=group+".txt")
	'''


	#form_report()


	print(len(form_data().keys()))


	'''
	X, y = form_Xy(data)
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)
	gnb = GaussianNB()
	y_pred = gnb.fit(X_train, y_train).predict(X_test)
	print("Number of mislabeled points out of a total %d points : %d" % (X_test.shape[0], (y_test != y_pred).sum()))
	counts = [0, 0]
	for v in y_pred:
		counts[v] = counts[v] + 1 
	print(counts)
	'''
