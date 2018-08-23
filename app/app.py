from flask import Flask, request, render_template, jsonify
import pickle
#from build_model import TextClassifier

app = Flask(__name__)


#with open('./data/model.pkl', 'rb') as f:
#    model = pickle.load(f)


@app.route('/', methods=['GET'])
def index():
    """Render a simple page."""
    return render_template('index.html')


@app.route('/submit', methods=['GET'] )
def submit():
    """Render a page for text input"""
    return render_template('submit.html')
    

@app.route('/predict', methods=['POST'])
def predict():
    """Receive the input text and use model to classify"""
    data = str(request.form['article_body'])
    pred = str(model.predict([data])[0])
    return render_template('predict.html', article=data, predicted=pred)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
