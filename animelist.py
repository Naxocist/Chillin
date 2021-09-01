import csv

animes = {}
genre = {}
ep = {}
synopsis = {}
rank = {}
pic = {}
link = {}
with open("animes.csv", 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    for data in reader:
        name = data[1]
        animes[name] = data[0]
        synopsis[name] = data[2]
        genre[name] = data[3]
        ep[name] = data[5].replace(".0", "")
        rank[name] = data[8].replace(".0", "")
        pic[name] = data[10]
        link[name] = data[11]
