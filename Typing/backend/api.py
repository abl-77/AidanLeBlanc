from flask import Flask, jsonify, request
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForCausalLM
import re

tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")

prompt = "Once upon a time"

state = {
    "prompt": prompt,
    "input_ids": tokenizer(f"{prompt}", return_tensors="pt").input_ids
}

app = Flask(__name__)
CORS(app)

@app.route("/api/line", methods=["GET"])
def get_line():
    output_ids = model.generate(
        state["input_ids"], 
        max_new_tokens=10, 
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        temperature=0.8,
        top_k=50,
    )
    text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    indices = [m.start() for m in re.finditer(re.escape(" "), text)]
    state["prompt"] = text[indices[-3]:indices[-1]]
    state["input_ids"] = tokenizer(f"{state["prompt"]}", return_tensors="pt").input_ids
    return jsonify({"text": text[:indices[-3]].replace("\n", " ").replace("  ", " ").strip() + " "})

@app.route("/api/reset", methods=["POST"])
def reset():
    try:
        data = request.get_json()
        prompt = data["prompt"]

        state["prompt"] = prompt
        state["input_ids"] = tokenizer(f"{prompt}", return_tensors="pt").input_ids
        
        return jsonify({"message": "Prompt reset succesfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

if __name__=="__main__":
    test = [0, 1, 2, 3, 4]
    print(test[1:])

'''
curl -X GET http://127.0.0.1:5000/api/line
'''