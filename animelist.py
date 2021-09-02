import csv

animes = {}
genre = {}
ep = {}
rank = {}
pic = {}
link = {}
season = {}
with open("animes.csv", 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    for data in reader:
        name = data[0]
        animes[name] = name
        # genre[name] = data[3]
        ep[name] = data[1]
        link[name] = data[2]
        pic[name] = data[3]
        season[name] = data[4]
        # rank[name] = data[8].replace(".0", "")


