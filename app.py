import os
import random
from flask import (
    Flask, 
    render_template, 
    request,
    redirect
)

import vertexai
from vertexai.generative_models import (
    GenerativeModel, 
    Image
)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB per image

vertexai.init(project="your-project-id", location="us-central1")


def generate(wireframe, model, prompt):
    model = GenerativeModel(model)
    contents = [
        wireframe,
        prompt
    ]
    
    responses = model.generate_content(
        contents=contents,
        stream=True,
    )

    response = ""
    for res in responses:
        response += res.text.strip()
    return response


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/response', methods=['GET', 'POST'])
def response():
    if request.method == 'POST':
        uploaded_image = request.files['image-upload']
        wireframe = Image.from_bytes(uploaded_image.read())
        model = request.form['model']
        prompt = request.form['prompt'] 

        try:
            response = generate(wireframe, model, prompt)
            return render_template('response.html', response=response)
        except ValueError as e:
            raise e
        
    else:
        return redirect('/')


if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
