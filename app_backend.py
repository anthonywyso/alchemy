import requests
import lxml.html


class ArticleExtractor(object):

    def __init__(self, url='http://www.hoopsrumors.com'):
        self.url = url
        self.headers = {'User-Agent': 'Chrome 37.0.2049.0'}

    def get_articles(self):
        '''
        INPUT: None
        OUTPUT: list(tuple)
        '''
        response = requests.get(self.url, headers=self.headers)
        r_html = lxml.html.fromstring(response.text)
        article_titles = r_html.xpath("//aside[@id='recent-posts-3']/descendant::a/text()")
        article_urls = r_html.xpath("//aside[@id='recent-posts-3']/descendant::a/@href")
        return zip(article_titles, article_urls)

class StatExtractor(object):

    def __init__(self, url='http://www.hoopsrumors.com/2014/10/harris-planning-extension.html'):
        self.url = url
        self.headers = {'User-Agent': 'Chrome 37.0.2049.0'}

    def parse_site(self):
        '''
        INPUT: None
        OUTPUT: string, list(str)
        '''
        response = requests.get(self.url, headers=self.headers)
        r_html = lxml.html.fromstring(response.text)
        title = r_html.xpath('//article/header/h1/text()')[0]
        urls = r_html.xpath('//article/div/p/strong/a/@href')
        topics = r_html.xpath('//article/div/p/strong/descendant::text()')
        topics = [term for term in topics if len(term.split(" ")) == 2]
        return title, urls, topics

    def get_tables(self, url_pl):
        '''
        INPUT: string
        OUTPUT: list(HtmlElement)
        '''
        # pull <div id=all_per_poss, all_advanced, all_shooting, all_college, all_salaries, all_contract>
        response = requests.get(url_pl, headers=self.headers)
        r_html = lxml.html.fromstring(response.text)
        player = r_html.xpath("//h1/text()")[0]
        tables = r_html.xpath("//div[contains(@id, 'all')]/*[not(parent::div[@id='all_player_news'])]")
        # tables1 = r_html.xpath("//div[contains(@id, 'all')]/div/table")
        # tables2 = r_html.xpath("//div[contains(@id, 'all')]/table")

        return player, tables

    def get_data(self):
        '''
        INPUT: None
        OUTPUT: string, list(str)
        '''
        t, urls, e = self.parse_site()
        tables_all = []
        for url in urls:
            player, player_tables = self.get_tables(url)
            player_header = "".join(["<h1>", player, "</h1>"])
            player_tables_str = "".join([lxml.html.tostring(table) for table in player_tables])
            tables_all.append(player_header)
            tables_all.append(player_tables_str)
        return t, tables_all, e