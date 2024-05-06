# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Import the necessary libraries.
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

# Initialize the Flask app.
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB per image

# Initialize the Vertex AI client library.
vertexai.init(project="duet-ai-cok", location="us-central1")

# Define a function to generate an image from a wireframe and a prompt.
def generate(wireframe, model, prompt):
    '''Generates the html code response from a wireframe and a prompt.
    Args:
    wireframe: The wireframe image.
    model: The generative model to use.
    prompt: The prompt to use.
    Returns:The generated response.
    '''
    # Create a GenerativeModel object.
    model = GenerativeModel(model)

    # Create a list of contents to pass to the model.
    contents = [
        wireframe,
        prompt
    ]
    
    # Generate the response.
    responses = model.generate_content(
        contents=contents,
        stream=True,
    )

    # Concatenate the response text.
    response = ""
    for res in responses:
        response += res.text.strip()
    
    # Return the generated response.
    return response

# Define the home page route.
@app.route('/', methods=['GET'])
def index():
    '''Renders the home page.
    Returns:The rendered template.
    '''
    return render_template('index.html')

# Define the response route.
@app.route('/response', methods=['GET', 'POST'])
def response():
    '''Handles the response to the user's input.
    Returns:The rendered template.
    '''
    # If the request is a POST request, process the form data.
    if request.method == 'POST':
        # Get the uploaded image from the request.
        uploaded_image = request.files['image-upload']
        
        # Convert the uploaded image to a wireframe image.
        wireframe = Image.from_bytes(uploaded_image.read())

        # Get the model and prompt from the request.
        model = request.form['model']
        prompt = request.form['prompt'] 
        
        # Generate the image and render the response template. 
        try:
            response = generate(wireframe, model, prompt)
            return render_template('response.html', response=response)
        except ValueError as e:
            raise e
    
    # If the request is a GET request, redirect to the home page.
    else:
        return redirect('/')

# Run the app.
if __name__ == '__main__':
    # Get the server port from the environment variables.
    server_port = os.environ.get('PORT', '8080')

    # Run the app.
    app.run(debug=False, port=server_port, host='0.0.0.0')
