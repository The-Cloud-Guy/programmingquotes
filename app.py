import random
from flask import Flask, jsonify


app = Flask(__name__)

quotes = [
    "Programming is the art of algorithm design and the craft of debugging errant code. – Ellen Ullman",
    "Any fool can write code that a computer can understand. Good programmers write code that humans can understand. ― Martin Fowler",
    "Programming is the art of telling another human being what one wants the computer to do. ― Donald Ervin Knuth",
    "Confusion is part of programming. ― Felienne Hermans",
    "If we want users to like our software, we should design it to behave like a likable person.  – Alan Cooper",
    "Quality is a product of a conflict between programmers and testers. ― Yegor Bugayenk",
    "Most good programmers do programming not because they expect to get paid or get adulation by the public, but because it is fun to program. – Linus Torvalds"
]

@app.route('/quote')
def get_quote():
    quote = random.choice(quotes)
    return jsonify({'quote': quote})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

