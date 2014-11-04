from flask import Flask, request, render_template
from app_backend import StatExtractor, ArticleExtractor
import os
app = Flask(__name__)

# TODO results -- fix styling, add header
# TODO results -- fix relative link paths within tables
# TODO results -- add article summary, maybe nlp
# TODO results -- add 2col view of article & stats

@app.route('/')
def index():
    a = ArticleExtractor()
    articles = a.get_articles()
    return render_template('index.html', most_recent=articles[0][1], articles=articles)

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

    header_rendered = render_template('stats_header.html')
    title_rendered = render_template('stats_title.html', data=title)
    # tables = render_template('stats_tables.html', data=stats)
    topics_rendered = render_template('stats_topics.html', data=topics)
    return "".join([header_rendered, title_rendered, link_init, topics_rendered, stats, footer])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    # app.run(host=os.environ['OPENSHIFT_PYTHON_IP'], port=8080)