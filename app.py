from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from ice_breaker import ice_breake_with  # Uncomment this line

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    print("📄 INDEX ROUTE HIT!")
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    print("🚀 PROCESS ROUTE HIT!")
    print(f"Request method: {request.method}")
    print(f"Form data: {dict(request.form)}")
    
    try:
        name = request.form.get('name')
        print(f"Extracted name: '{name}'")
        
        if not name:
            print("❌ No name provided!")
            return jsonify({"error": "No name provided"})
            
        print(f"🔍 Calling ice_breake_with for: {name}")
        summary, photo_url = ice_breake_with(name)
        print(f"✅ Got results from ice_breaker")
        
        # Debug: Print the actual objects
        print(f"🔍 Summary object: {summary}")
        print(f"🔍 Summary type: {type(summary)}")
        print(f"🔍 Photo URL: {photo_url}")
        
        result = summary.to_dict()
        print(f"🔍 Result dict: {result}")
        
        # Handle None profile_pic - use photo_url as fallback
        if photo_url and photo_url.startswith("http"):
            result['profile_pic'] = photo_url
        elif result.get('profile_pic') is None:
            result['profile_pic'] = "https://via.placeholder.com/300"
        
        # Debug: Print final result
        print(f"🔍 Final result being sent: {result}")
        
        print("✅ Success! Returning results")
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)