import json
import pyperclip
import os
import sys

NOTES_FILE = "ticket_notes.json"

# Default notes (UE will be replaced automatically)
DEFAULT_NOTES = {
    "Fake": [
        "UE Inauthentic Account #VITx"
    ],
    "User": [
        "UE User Impersonation against Musk Family #VITx",
        "UE User Impersonation against EM #VITx"
    ],
    "Brand": [
        "UE Brand Impersonation against GROK #VITx"
    ],
    "Spam": [
        "UE Content Spam #VITx"
    ],
    "FP": [
        "#FalsePositive"
    ],
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
    "WoH": [
        "UE - VS Wish of Harm - Specific Human Target - Major 3 Strike Policy"
    ]
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

def replace_ue(text, ue_number):
    return text.replace("UE", ue_number)

def show_list(notes):
    print("\n📋 ALL SAVED KEYWORDS:")
    print("-" * 60)
    for keyword in sorted(notes.keys()):
        print(f"• {keyword} ({len(notes[keyword])} notes)")
    print("-" * 60)
    print("Tip: Type a keyword to use it.")

def main():
    notes = load_notes()
    
    print("🚀 UE Notes App - Ready")
    print("=" * 55)
    print("How to use:")
    print("   1. Type UE number")
    print("   2. Type Keyword")
    print("   • Type 'list'  → see all keywords")
    print("   • Type 'add'   → add new note")
    print("   • Type 'edit'  → edit existing note")
    print("   • Type 'exit'  → quit\n")

    while True:
        try:
            ue_input = input("\nUE Number (or list/add/edit/exit): ").strip()
            
            if ue_input.lower() == 'exit':
                print("👋 Goodbye!")
                break
                
            elif ue_input.lower() == 'list':
                show_list(notes)
                continue
                
            elif ue_input.lower() == 'add':
                keyword = input("Enter new Keyword: ").strip()
                if not keyword:
                    print("Keyword cannot be empty.")
                    continue
                print("Paste the full note (press Enter twice when done):")
                lines = []
                while True:
                    line = input()
                    if line == "" and (not lines or lines[-1] == ""):
                        break
                    lines.append(line)
                note_text = "\n".join(lines).strip()
                
                if keyword not in notes:
                    notes[keyword] = []
                notes[keyword].append(note_text)
                save_notes(notes)
                print(f"✅ Added new note under keyword: {keyword}")
                continue
                
            elif ue_input.lower() == 'edit':
                keyword = input("Which keyword do you want to edit? ").strip()
                if keyword not in notes or not notes[keyword]:
                    print("❌ Keyword not found.")
                    continue
                print(f"\nCurrent notes for '{keyword}':")
                for i, note in enumerate(notes[keyword], 1):
                    print(f"{i}. {note[:100]}{'...' if len(note) > 100 else ''}")
                try:
                    choice = int(input("\nWhich number to edit? ")) - 1
                    if 0 <= choice < len(notes[keyword]):
                        print("Paste the new note (press Enter twice when done):")
                        lines = []
                        while True:
                            line = input()
                            if line == "" and (not lines or lines[-1] == ""):
                                break
                            lines.append(line)
                        new_text = "\n".join(lines).strip()
                        notes[keyword][choice] = new_text
                        save_notes(notes)
                        print("✅ Note updated.")
                    else:
                        print("Invalid number.")
                except:
                    print("Invalid input.")
                continue

            # Normal flow: UE Number + Keyword
            ue_number = ue_input
            if not ue_number:
                continue
                
            keyword = input("Keyword: ").strip()
            
            if keyword not in notes or not notes[keyword]:
                print(f"❌ No note found for keyword '{keyword}'")
                print("Tip: Type 'list' to see available keywords.")
                continue
            
            matching_notes = notes[keyword]
            
            if len(matching_notes) == 1:
                final_note = replace_ue(matching_notes[0], ue_number)
                pyperclip.copy(final_note)
                print(f"✅ COPIED TO CLIPBOARD! (UE: {ue_number} | Keyword: {keyword})")
                print(f"Preview: {final_note[:120].replace(chr(10), ' ')}...")
            else:
                # Multiple notes - let user choose
                print(f"\nFound {len(matching_notes)} notes for keyword '{keyword}':")
                for i, note in enumerate(matching_notes, 1):
                    preview = note[:80].replace("\n", " ") + "..." if len(note) > 80 else note
                    print(f"{i}. {preview}")
                
                try:
                    choice = int(input("\nChoose number: ")) - 1
                    if 0 <= choice < len(matching_notes):
                        final_note = replace_ue(matching_notes[choice], ue_number)
                        pyperclip.copy(final_note)
                        print(f"✅ COPIED TO CLIPBOARD! (UE: {ue_number} | Keyword: {keyword})")
                        print(f"Preview: {final_note[:120].replace(chr(10), ' ')}...")
                    else:
                        print("Invalid choice.")
                except:
                    print("Invalid input.")
                    
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    try:
        import pyperclip
    except ImportError:
        print("Installing pyperclip (one time only)...")
        os.system(f"{sys.executable} -m pip install pyperclip --quiet")
        import pyperclip
    
    main()
