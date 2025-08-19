from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from ice_breaker import ice_breake_with_url  # Uncomment this line

load_dotenv()

app = Flask(__name__)



@app.route("/")
def index():
    print("📄 INDEX ROUTE HIT!")
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    print("🚀 PROCESS ROUTE HIT!")
    print(f"Form data: {dict(request.form)}")
    
    try:
        name = request.form.get('name')
        action = request.form.get('action', 'search')
        
        print(f"👤 Name: {name}")
        print(f"🎯 Action: {action}")
        
        if action == 'search':
            print(f"🔍 Searching for: {name}")
            
            from agents.linkedin_lookup import lookup_multiple
            profiles = lookup_multiple(name)
            
            print(f"📊 Profiles returned: {len(profiles)}")
            for i, profile in enumerate(profiles):
                print(f"  Profile {i+1}: {profile.get('name', 'Unknown')}")
            
            if len(profiles) > 1:
                print("✅ Multiple profiles found, returning selection")
                return jsonify({
                    "type": "multiple_profiles", 
                    "profiles": profiles,
                    "message": f"Found {len(profiles)} profiles for {name}. Please select one:"
                })
            elif len(profiles) == 1:
                print("✅ Single profile found, processing directly...")
                summary, photo_url = ice_breake_with_url(profiles[0]['url'])
                result = summary.to_dict()
                if result.get('profile_pic') is None:
                    result['profile_pic'] = photo_url or "https://via.placeholder.com/300"
                return jsonify(result)
            else:
                print("⚠️ No profiles found with multiple search, trying original...")
                summary, photo_url = ice_breake_with(name)
                result = summary.to_dict()
                if result.get('profile_pic') is None:
                    result['profile_pic'] = photo_url or "https://via.placeholder.com/300"
                return jsonify(result)
            
        elif action == 'select':
            selected_url = request.form.get('profile_url')
            print(f"🎯 User selected: {selected_url}")
            selected_picture = request.form.get('profile_picture')  # Get the picture from frontend
            print(f"🖼️ Picture from selection: {selected_picture}")
            
            summary, photo_url = ice_breake_with_url(selected_url)
            result = summary.to_dict()
            if selected_picture:
                result['profile_pic'] = selected_picture
            elif result.get('profile_pic') is None:
                result['profile_pic'] = photo_url or "https://via.placeholder.com/300"
                
            return jsonify(result)
            # if result.get('profile_pic') is None:
            #     result['profile_pic'] = photo_url or "https://via.placeholder.com/300"
            # return jsonify(result)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)