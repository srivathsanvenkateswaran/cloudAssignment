import scrapy
import json

class AndroidAuthoritySpider(scrapy.Spider):
    
    name = "AndroidAuthority"
    # This is the name of this particular spider.. name must be unique for every spider 

    start_urls = [
        "https://www.androidauthority.com/news/",
        "https://www.androidauthority.com/reviews/",
        "https://www.androidauthority.com/apps/"
    ]
    # These are all the list of urls needed to be crawled by the spider 

    dictList = []
    # This is the List which contains all the dictionaries [JSON Objects] which we will finally convert into a JSON Array

    def parse(self, response):
        # Parsing the required data from response
        titles = response.css('.article-title::text').getall()
        descriptions = response.css('.excerpt::text').getall()
        urls = response.css('.loop-info a::attr(href)').getall()

        divs = response.css('.loop-image').getall()
        images = []
        for item in divs:
            images.append(item.split(" ")[4][10:-1])
        del divs


        # images = response.css('.td-module-thumb img::attr(src)').getall() 
        # response.css('.loop-image').get().split(" ")[4][10:-1]
        # This is done to remove duplicates [first 4 entries are duplicates]

        # RESOLVE THE BUG WITH DATE AND AUTHOR ASAP 

        dates = response.css('.aa_item_time::text').getall()
        for i in range(0,4):
            dates.pop(0)
        # This is done to remove duplicates [first 4 entries are duplicates]

        authors = response.css('.bottom-loop-info span::text').getall()
        del authors[1::2]
        # Delete all the odd index occurances in the list

        for i in range(0,4):
            authors.pop(0)

        for item in zip(titles, descriptions, urls, images, authors, dates):
            d = {
                'Title': item[0],
                'Desc': item[1],
                'Url': item[2],
                'Img': item[3],
                'Author': item[4],
                'Source': "Android Authority",
                'Date' : item[5]
            }
            # Here we are creating a JSON Object from the parsed data 
            self.dictList.append(d)
            # We are appending the dictionary to the list so that we can finally convert it into a JSON Array

        with open("results/AndroidAuthority.json", 'w') as f:
            f.write(json.dumps(self.dictList)) 
            #json.dumps converts the List of dictionaries into a Json Array
            # writing the json array into a file 

            # Either we can write into a file here or we can specify the command in shell [direct the output flag towards file.json]
            # E.g:
            # scrapy crawl Beebom -o Beebom.json 
