import csv

animes = {}
genre = {}
ep = {}
rank = {}
pic = {}
link = {}
season = {}
nsfw = []

with open("animes.csv", 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)

    for row in reader:
        name = row[0]
        if "Hentai" not in row[5]:
            animes[name] = name
        else:
            nsfw.append(name)
        genre[name] = row[5]
        ep[name] = row[1]
        link[name] = row[2]
        pic[name] = row[3]
        season[name] = row[4]
        rank[name] = row[6]



