import scrapy
import json

class TechCrunchSpider(scrapy.Spider):
    
    name = "TechCrunch"
    # This is the name of this particular spider.. name must be unique for every spider 

    start_urls = [
        'https://techcrunch.com/'
    ]
    # These are all the list of urls needed to be crawled by the spider 

    dictList = []
    # This is the List which contains all the dictionaries [JSON Objects] which we will finally convert into a JSON Array

    def parse(self, response):
        # Parsing the required data from response

        dum = response.css('.post-block__title__link::text').getall()
        titles = [s.strip() for s in dum]
        del dum

        dum = response.css('.river-byline__authors a::text').getall()
        authors = [s.strip() for s in dum]
        del dum 

        dum = response.css('.post-block__content::text').getall()
        descriptions = [s.strip() for s in dum]
        del dum

        urls = response.css('.post-block__title a::attr(href)').getall()
        images = response.css('.post-block__media img::attr(src)').getall()
        dates = response.css('.river-byline time::attr(datetime)').getall()

        for item in zip(titles, descriptions, urls, images, authors, dates):
            d = {
                'Title': item[0],
                'Desc': item[1],
                'Url': item[2],
                'Img': item[3],
                'Author': item[4],
                'Source': "Tech Crunch",
                'Date' : item[5]
            }
            # Here we are creating a JSON Object from the parsed data 
            self.dictList.append(d)
            # We are appending the dictionary to the list so that we can finally convert it into a JSON Array

        with open("results/TechCrunch.json", 'w') as f:
            f.write(json.dumps(self.dictList)) 
            #json.dumps converts the List of dictionaries into a Json Array
            # writing the json array into a file 

            # Either we can write into a file here or we can specify the command in shell [direct the output flag towards file.json]
            # E.g:
            # scrapy crawl Beebom -o Beebom.json 
