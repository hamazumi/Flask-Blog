from flask import Flask, render_template, url_for
app = Flask(__name__)

posts = [
    {
        'author': 'KEN test',
        'title': 'TEST Post 1',
        'content': 'TEST content 1',
        'date_posted': 'July 26, 2021'
    },
    {
        'author': 'JESS test',
        'title': 'TEST Post 2',
        'content': 'TEST content 2',
        'date_posted': 'July 26, 2021'
    },
    {
        'author': 'BUDDHA test',
        'title': 'TEST Post 3',
        'content': 'TEST content 3',
        'date_posted': 'July 26, 2021'
    }
]

@app.route('/')
@app.route('/home')
def homepage():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

if __name__ == '__main__':
    app.run(debug=True)