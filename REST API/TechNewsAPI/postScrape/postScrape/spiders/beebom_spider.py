import scrapy
import json

class BeebomSpider(scrapy.Spider):
    
    name = "Beebom"
    # This is the name of this particular spider.. name must be unique for every spider 

    start_urls = [
        'https://beebom.com/category/news/',
        'https://beebom.com/category/reviews/',
        'https://beebom.com/category/how-to/'
    ]
    # These are all the list of urls needed to be crawled by the spider 

    dictList = []
    # This is the List which contains all the dictionaries [JSON Objects] which we will finally convert into a JSON Array

    def parse(self, response):
        # Parsing the required data from response
        titles = response.css('.entry-title a::text').getall()
        descriptions = response.css('.td-excerpt::text').getall()
        urls = response.css('.entry-title a::attr(href)').getall()
        images = response.css('.td-module-thumb img::attr(src)').getall()
        authors = response.css('.td-post-author-name a::text').getall()
        dates = response.css('.td-post-date time::attr(datetime)').getall()

        for item in zip(titles, descriptions, urls, images, authors, dates):
            d = {
                'Title': item[0],
                'Desc': item[1],
                'Url': item[2],
                'Img': item[3],
                'Author': item[4],
                'Source': "Beebom",
                'Date' : item[5]
            }
            # Here we are creating a JSON Object from the parsed data 
            self.dictList.append(d)
            # We are appending the dictionary to the list so that we can finally convert it into a JSON Array

        with open("results/Beebom.json", 'w') as f:
            f.write(json.dumps(self.dictList)) 
            #json.dumps converts the List of dictionaries into a Json Array
            # writing the json array into a file 

            # Either we can write into a file here or we can specify the command in shell [direct the output flag towards file.json]
            # E.g:
            # scrapy crawl Beebom -o Beebom.json 
