import scrapy
import json

class TheVergeSpider(scrapy.Spider):
    
    name = "TheVerge"
    # This is the name of this particular spider.. name must be unique for every spider 

    start_urls = [
        'https://www.theverge.com/tech'
    ]
    # These are all the list of urls needed to be crawled by the spider 

    dictList = []
    # This is the List which contains all the dictionaries [JSON Objects] which we will finally convert into a JSON Array

    def parse(self, response):
        # Parsing the required data from response

        titles = response.css('.c-entry-box--compact__title a::text').getall()
        ind = titles.index('Reviews')
        descriptions = titles
        urls = response.css('.c-entry-box--compact__title a::attr(href)').getall()
        titles.pop(ind)
        urls.pop(ind)
        images = response.css('.c-entry-box--compact__image noscript img::attr(src)').getall()

        authors = response.css('.c-byline__author-name::text').getall()
        for i in range(0,2):
            authors.pop(0)
        authors.insert(5, "Unknown")

        dates = response.css('.c-byline__item time::attr(datetime)').getall()
        dates.insert(4, "")
        dates.insert(5, "")
        dates.insert(17, "")
        dates.insert(29, "")

        for item in zip(titles, descriptions, urls, images, authors, dates):
            d = {
                'Title': item[0],
                'Desc': item[1],
                'Url': item[2],
                'Img': item[3],
                'Author': item[4],
                'Source': "The Verge",
                'Date' : item[5]
            }
            # Here we are creating a JSON Object from the parsed data 
            self.dictList.append(d)
            # We are appending the dictionary to the list so that we can finally convert it into a JSON Array

        with open("results/TheVerge.json", 'w') as f:
            f.write(json.dumps(self.dictList)) 
            #json.dumps converts the List of dictionaries into a Json Array
            # writing the json array into a file 

            # Either we can write into a file here or we can specify the command in shell [direct the output flag towards file.json]
            # E.g:
            # scrapy crawl Beebom -o Beebom.json 
