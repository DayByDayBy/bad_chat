from flask import Flask, request, jsonify
import ollama
# import asyncio

app = Flask(__name__)

model_name = "llama3"


@app.route('/')
def index():
    return "your weird little flask application is running."

@app.route('/generate_sequence', methods=['POST'])
@app.route('/generate_sequence', methods=['POST'])
def generate_sequence():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid input, JSON expected'}), 400

        initial_prompt = data.get('initial_prompt', 'generate an innovative prompt.')
        iterations = data.get('iterations', 8)

        results = []
        current_prompt = initial_prompt

        for i in range(iterations):
            try:
                response = ollama.generate(prompt=current_prompt, model=model_name)
                response_text = response['response']  # ollama should return a dict with 'response' key
                results.append({'prompt': current_prompt, 'response': response_text})
                current_prompt = response_text
            except Exception as e:
                print(f"Error during generation {i+1}:", e)
                return jsonify({'error': f'generation failed at iteration {i+1}: {str(e)}'}), 500

        return jsonify({'results': results})
    except Exception as e:
        print("Error in /generate_sequence:", e)
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return "This route is not found. Please check the URL.", 404








if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    
    
    
    
        #     p_and_r_pairs = dict(zip(prompts, responses))
        # print(p_and_r_pairs)