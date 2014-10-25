from flask import Flask, request, render_template
from app_backend import StatExtractor, ArticleExtractor
app = Flask(__name__)

# TODO landing/results -- prettify css
# TODO results -- add article summary, maybe nlp

@app.route('/')
def index():
    a = ArticleExtractor()
    articles = a.get_articles()

    content = '''
                <title>Basketball Alchemy</title>
                <h1> Basketball Alchemy -- Transform Hoops Rumors into Pure Numbers </h1>
                <h3> Who the f*ck is that?! Just show me his numbers! </h3>
                '''
    articles_show = render_template('stats_articles.html', data=articles)
    form = render_template('stats_form.html', data=articles[0][1])

    return content + form + articles_show

@app.route('/results', methods=['GET', 'POST'])
def classification_results():
    footer = '''<br><h3><a href="../">Go back for more</a><h3>'''
    if request.method == 'POST':
        user_input = request.form['user_input']
    if request.method == 'GET':
        return '<img src="static/tumblr_m3k1juHo3v1ro2d43.gif">' + footer
    url_init = str(user_input)
    s = StatExtractor(url_init)
    title, stats, topics = s.get_data()
    link_init = "".join(['<a href="', url_init, '">', title, '</a>'])

    header_rendered = render_template('stats_header.html', data=title)
    # tables = render_template('stats_tables.html', data=stats)
    topics_rendered = render_template('stats_topics.html', data=topics)
    return "".join([header_rendered, link_init, topics_rendered] + stats + [footer])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1313, debug=True)