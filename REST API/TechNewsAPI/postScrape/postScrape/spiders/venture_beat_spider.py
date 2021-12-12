import scrapy
import json

class VentureBeatSpider(scrapy.Spider):
    
    name = "VentureBeat"
    # This is the name of this particular spider.. name must be unique for every spider 

    start_urls = [
        'https://venturebeat.com/'
    ]
    # These are all the list of urls needed to be crawled by the spider 

    dictList = []
    # This is the List which contains all the dictionaries [JSON Objects] which we will finally convert into a JSON Array

    def parse(self, response):
        # Parsing the required data from response

        arr = response.css('.ArticleListing__body').getall()
        a = []
        for i in range(len(arr)):
            if 'Press Release' in arr[i]:
                a.append(i)
        # This will help us to find all the articles which are Press Release and they will not have authors and date

        titles = response.css('.ArticleListing__title a::text').getall()
        descriptions = titles
        urls = response.css('.ArticleListing__title a::attr(href)').getall()
        images = response.css('.ArticleListing img::attr(src)').getall()
        authors = response.css('.ArticleListing__author::text').getall()
        dates = response.css('.ArticleListing__time::attr(datetime)').getall()

        for index in a:
            authors.insert(index, "Press Release")
            dates.insert(index, "")
        # This will add an empty string in articles which are Press Release thereby not tampering the order of information 

        del arr
        del a

        for item in zip(titles, descriptions, urls, images, authors, dates):
            d = {
                'Title': item[0],
                'Desc': item[1],
                'Url': item[2],
                'Img': item[3],
                'Author': item[4],
                'Source': "Venture Beat",
                'Date' : item[5]
            }
            # Here we are creating a JSON Object from the parsed data 
            self.dictList.append(d)
            # We are appending the dictionary to the list so that we can finally convert it into a JSON Array

        with open("results/VentureBeat.json", 'w') as f:
            f.write(json.dumps(self.dictList)) 
            #json.dumps converts the List of dictionaries into a Json Array
            # writing the json array into a file 

            # Either we can write into a file here or we can specify the command in shell [direct the output flag towards file.json]
            # E.g:
            # scrapy crawl Beebom -o Beebom.json 
