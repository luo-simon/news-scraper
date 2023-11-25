import scrapy

class CnbcTechSpider(scrapy.Spider):
    name = 'cnbc_tech'
    allowed_domains = ['cnbc.com']
    start_urls = ['https://www.cnbc.com/technology/']

    def parse(self, response):
        # Extract the first 5 article links
        article_links = response.css('a.Card-title::attr(href)').getall()[:5]

        # Follow each article link
        for link in article_links:
            yield response.follow(link, self.parse_article)

    def parse_article(self, response):
        # Extract the title
        title = response.css('h1.ArticleHeader-headline::text').get()
        
        # Extract the timestamp
        timestamp = response.css('time[data-testid="published-timestamp"]::text').get()

        # Extract the article content
        content = ' '.join(response.css('div.group p::text').getall())

        # Extract key points
        key_points = response.css('div.RenderKeyPoints-wrapper li::text').getall()
        key_points = ' | '.join(key_points)  # Joining key points with a separator

        # Yield the scraped data
        yield {
            'title': title,
            'timestamp': timestamp,
            'content': content,
            'key_points': key_points,
            'url': response.url
        }
