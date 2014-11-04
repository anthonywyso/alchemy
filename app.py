from flask import Flask, request, render_template
from app_backend import StatExtractor, ArticleExtractor
import os
app = Flask(__name__)

# TODO results -- add article summary, maybe nlp
# TODO results -- add 2col view of article & stats

@app.route('/')
def index():
    a = ArticleExtractor()
    articles = a.get_articles()
    return render_template('index.html', most_recent=articles[0][1], articles=articles)

@app.route('/results', methods=['GET', 'POST'])
def classification_results():
    if request.method == 'POST':
        user_input = request.form['user_input']
    if request.method == 'GET':
        return render_template('error.html')
    url_init = str(user_input)
    s = StatExtractor(url_init)
    title, stats, topics = s.get_data()
    return render_template('results.html', article=title, article_url=url_init, topics=topics) + stats


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, debug=True)
    app.run(host=os.environ['OPENSHIFT_PYTHON_IP'], port=8080)