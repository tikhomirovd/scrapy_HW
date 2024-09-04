import scrapy


class LitresSpider(scrapy.Spider):
    name = 'litres'
    allowed_domains = ['litres.ru']
    start_urls = ['https://www.litres.ru/genre/programmirovanie-5272/']

    def parse(self, response):
        books = response.css('div.ArtDefault_wrapper__VmWpW')
        for book in books:
            book_link = response.urljoin(book.css('a[data-testid="art__title"]::attr(href)').get())
            rating = book.css('div[data-testid="art__ratingAvg"]::text').get()
            rating_count = book.css('div[data-testid="art__ratingCount"]::text').get()
            yield scrapy.Request(url=book_link, callback=self.parse_book, meta={
                'rating': rating,
                'rating_count': rating_count
            })

            # Переход на следующую страницу
            next_page = response.css('a[rel="next"]::attr(href)').get()
            if next_page is not None:
                yield response.follow(next_page, self.parse)

    def parse_book(self, response):
        authors = response.css(
            'div.BookAuthor_author__info__5eDIs a.StyledLink_link__xB81c span[itemprop="name"]::text').getall()
        price = response.css('strong.SaleBlock_block__price__default__MitcJ::text').re_first(
            r'(\d[\d\s]+)₽')
        if price is not None:
            price = price.replace('\xa0', '').replace(' ', '')
        book_data = {
            'name': response.css('h1[itemprop="name"]::text').get(),
            'author': ', '.join(authors),
            'link': response.url,
            'rating': response.meta.get('rating'),
            'rating_count': response.meta.get('rating_count'),
            'review_count': response.css(
                'div[data-testid="book-factoids__reviews"] div.BookFactoids_primary__TVFhL span::text').get(),
            "pages_count": response.css('div[data-testid="book-volume__wrapper"] p::text').re_first(r'(\d+) страниц'),
            "price": price,
            'text_reviews': response.css('div.Comment_reviewText__PEkHn p::text').getall(),
            'age': response.css(
                'div.CharacteristicsBlock_characteristic__title__atG_Z:contains("Возрастное ограничение") + span::text').get(),
            'year': response.css(
                'div.CharacteristicsBlock_characteristic__title__atG_Z:contains("Дата написания") + span::text').get(),
        }
        reviews_link = response.url + 'otzivi/'
        yield scrapy.Request(url=reviews_link, callback=self.parse_reviews,
                             meta={'book_data': book_data, 'reviews': []})

    def parse_reviews(self, response):
        book_data = response.meta['book_data']
        reviews = response.meta['reviews']

        current_reviews = response.css('div.Comment_reviewText__PEkHn p::text').getall()
        reviews.extend(current_reviews)

        next_page = response.css('a.SpriteIcon_wrapper__eYwS1::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse_reviews, meta={'book_data': book_data, 'reviews': reviews})
        else:
            book_data['text_reviews'] = reviews
            yield book_data
