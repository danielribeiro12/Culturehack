from flask import Flask, request, jsonify, render_template

# Initialize the Flask application
app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return "<h1>Hello world</h1>"



# Example route with query parameters
@app.route('/translate')
def greet():
    from_language = request.args.get("from_lang")
    to_language = request.args.get("to_lang")
    text = request.args.get("text")

    # translate()
    
    return 

# Example route using a template
@app.route('/template')
def template_example():
    return render_template('index.html', name="Flask")

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
