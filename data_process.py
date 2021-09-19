import csv

animes = []
genre = []
ep = {}
rank = {}
pic = {}
link = {}
season = {}

with open("animes_data.csv", 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        n = row[0]  # name
        g = [i.lower() for i in row[5].split()]  # every rows

        if "hentai" not in g:
            animes.append(n)
            genre.append(g)
        ep[n] = row[1]
        link[n] = row[2]
        pic[n] = row[3]
        season[n] = row[4]
        rank[n] = row[6]

#  Update data
