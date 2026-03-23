from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

NOTES_FILE = "ticket_notes.json"

# Your default notes
DEFAULT_NOTES = {
    "Fake": ["UE Inauthentic Account #VITx"],
    "User": [
        "UE User Impersonation against Musk Family #VITx",
        "UE User Impersonation against EM #VITx"
    ],
    "Brand": ["UE Brand Impersonation against GROK #VITx"],
    "Spam": ["UE Content Spam #VITx"],
    "FP": ["#FalsePositive"],
    "ATO": [
        "UE # - Suspend - Compromised (Taken Over). Treat appeals as hacked, and only release if they are filing from the original account phone or email. #VITx"
    ],
    "HC": [
        "UE FOSNR HC High VF - Slur/Tropes",
        "UE FOSNR HC High VF - IoF"
    ],
    "VS": [
        "UE FOSNR VS High VF - Reactive Commentary",
        "UE FOSNR VS High VF - Coded Language"
    ],
    "WoH": ["UE - VS Wish of Harm - Specific Human Target - Major 3 Strike Policy"]
}

def load_notes():
    if os.path.exists(NOTES_FILE):
        try:
            with open(NOTES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return DEFAULT_NOTES.copy()
    return DEFAULT_NOTES.copy()

def save_notes(notes):
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=4, ensure_ascii=False)

@app.route("/", methods=["GET", "POST"])
def index():
    notes = load_notes()
    
    if request.method == "POST":
        ue_number = request.form.get("ue_number", "").strip()
        keyword = request.form.get("keyword", "").strip()
        choice = request.form.get("choice")
        
        if ue_number and keyword and keyword in notes:
            matching = notes[keyword]
            
            if len(matching) == 1 or choice is not None:
                try:
                    idx = int(choice) if choice is not None else 0
                    selected_note = matching[idx]
                    final_note = selected_note.replace("UE", ue_number)
                    return jsonify({
                        "success": True,
                        "note": final_note,
                        "ue": ue_number,
                        "keyword": keyword
                    })
                except:
                    pass
            
            # Show choices if multiple
            return jsonify({
                "success": False,
                "multiple": True,
                "options": [n[:120] + "..." if len(n) > 120 else n for n in matching],
                "ue": ue_number,
                "keyword": keyword
            })
    
    return render_template("index.html", notes=notes)

@app.route("/add", methods=["POST"])
def add_note():
    notes = load_notes()
    keyword = request.form.get("keyword", "").strip()
    note_text = request.form.get("note_text", "").strip()
    
    if keyword and note_text:
        if keyword not in notes:
            notes[keyword] = []
        notes[keyword].append(note_text)
        save_notes(notes)
        return jsonify({"success": True, "message": f"Added under '{keyword}'"})
    return jsonify({"success": False, "message": "Missing data"})

if __name__ == "__main__":
    os.makedirs("templates", exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=True)