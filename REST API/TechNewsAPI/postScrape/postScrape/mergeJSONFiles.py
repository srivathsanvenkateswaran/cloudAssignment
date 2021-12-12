if __name__ == "__main__":
    import json

    with open("results/Beebom.json", "r") as b:
        BeebomJsonArray = json.loads(b.read())

    with open("results/AndroidAuthority.json", "r") as b:
        AndroidAuthorityJsonArray = json.loads(b.read())
        
    with open("results/TechCrunch.json", "r") as b:
        TechCrunchJsonArray = json.loads(b.read())

    with open("results/TheVerge.json", "r") as b:
        TheVergeJsonArray = json.loads(b.read())

    with open("results/VentureBeat.json", "r") as b:
        VentureBeatJsonArray = json.loads(b.read())

    CombinedJsonArray = BeebomJsonArray + AndroidAuthorityJsonArray + TechCrunchJsonArray + TheVergeJsonArray + VentureBeatJsonArray

    d = {
        'totalResults' : len(CombinedJsonArray),
        'articles' : CombinedJsonArray
    }

    with open("results/finalArticleList.json", "w") as f:
        f.write(json.dumps(d))