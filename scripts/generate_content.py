import json
import os

CONTENT_DIR = os.path.join(os.path.dirname(__file__), '..', 'content')

def write_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def generate_modules():
    fire_module = {
        "id": "fire",
        "titleKey": "mod_fire_title",
        "isLite": False,
        "steps": [
            {"id": "intro", "type": "INTRO", "titleKey": "fire_s1_t", "instructionKey": "fire_s1_i", "audioKey": "fire_s1", "maxPoints": 5},
            {"id": "find_exits", "type": "FIND_TARGETS", "titleKey": "fire_s2_t", "instructionKey": "fire_s2_i", "audioKey": "fire_s2", "maxPoints": 20, "params": {"targets": ["exit1", "exit2", "exit3"], "distractors": ["blocked_exit"]}},
            {"id": "select_ext", "type": "SELECT_ITEM", "titleKey": "fire_s3_t", "instructionKey": "fire_s3_i", "audioKey": "fire_s3", "maxPoints": 20, "params": {"correct": "ext_co2", "tray": ["ext_water", "ext_co2", "ext_powder"]}},
            {"id": "pass_action", "type": "ACTION_SEQUENCE", "titleKey": "fire_s4_t", "instructionKey": "fire_s4_i", "audioKey": "fire_s4", "maxPoints": 25, "params": {"sequence": ["pull_pin", "aim_base", "squeeze", "sweep"]}},
            {"id": "evac_order", "type": "ORDER_SEQUENCE", "titleKey": "fire_s5_t", "instructionKey": "fire_s5_i", "audioKey": "fire_s5", "maxPoints": 20, "params": {"cards": ["raise_alarm", "cut_power", "help_others", "evacuate", "assembly_point"]}},
            {"id": "walk_path", "type": "WALK_PATH", "titleKey": "fire_s6_t", "instructionKey": "fire_s6_i", "audioKey": "fire_s6", "maxPoints": 10, "params": {"waypoints": [ [1,0,2], [2,0,4] ]}}
        ]
    }
    
    gas_module = {
        "id": "gas",
        "titleKey": "mod_gas_title",
        "isLite": False,
        "steps": [
            {"id": "intro", "type": "INTRO", "titleKey": "gas_s1_t", "instructionKey": "gas_s1_i", "audioKey": "gas_s1", "maxPoints": 5},
            {"id": "find_zones", "type": "FIND_TARGETS", "titleKey": "gas_s2_t", "instructionKey": "gas_s2_i", "audioKey": "gas_s2", "maxPoints": 20, "params": {"targets": ["co_zone", "h2s_zone", "sign_1"], "distractors": ["safe_zone"]}},
            {"id": "read_gauge", "type": "READ_GAUGE", "titleKey": "gas_s3_t", "instructionKey": "gas_s3_i", "audioKey": "gas_s3", "maxPoints": 20, "params": {"readings": [{"o2": 19.5, "lel": 5, "h2s": 10, "co": 35, "correct": "evacuate"}]}},
            {"id": "pack_kit", "type": "SELECT_ITEM", "titleKey": "gas_s4_t", "instructionKey": "gas_s4_i", "audioKey": "gas_s4", "maxPoints": 20, "params": {"correct": "full_kit", "tray": ["full_kit", "cotton_mask", "phone"]}},
            {"id": "buddy_order", "type": "ORDER_SEQUENCE", "titleKey": "gas_s5_t", "instructionKey": "gas_s5_i", "audioKey": "gas_s5", "maxPoints": 25, "params": {"cards": ["permit", "isolate", "test", "lifeline", "enter"]}},
            {"id": "emergency", "type": "ACTION_SEQUENCE", "titleKey": "gas_s6_t", "instructionKey": "gas_s6_i", "audioKey": "gas_s6", "maxPoints": 10, "params": {"sequence": ["alarm", "do_not_enter", "call_rescue"]}}
        ]
    }
    
    lite_modules = [
        {"id": "machinery", "titleKey": "mod_mach_title", "isLite": True, "steps": [
            {"id": "intro", "type": "INTRO", "titleKey": "mach_s1_t", "instructionKey": "mach_s1_i", "audioKey": "mach_s1", "maxPoints": 10},
            {"id": "loto", "type": "ORDER_SEQUENCE", "titleKey": "mach_s2_t", "instructionKey": "mach_s2_i", "audioKey": "mach_s2", "maxPoints": 90, "params": {"cards": ["notify", "shutdown", "isolate", "lock", "test"]}}
        ]},
        {"id": "electrical", "titleKey": "mod_elec_title", "isLite": True, "steps": [
            {"id": "intro", "type": "INTRO", "titleKey": "elec_s1_t", "instructionKey": "elec_s1_i", "audioKey": "elec_s1", "maxPoints": 10},
            {"id": "isolate", "type": "ORDER_SEQUENCE", "titleKey": "elec_s2_t", "instructionKey": "elec_s2_i", "audioKey": "elec_s2", "maxPoints": 90, "params": {"cards": ["identify", "disconnect", "lockout", "verify"]}}
        ]},
        {"id": "ppe", "titleKey": "mod_ppe_title", "isLite": True, "steps": [
            {"id": "intro", "type": "INTRO", "titleKey": "ppe_s1_t", "instructionKey": "ppe_s1_i", "audioKey": "ppe_s1", "maxPoints": 10},
            {"id": "select", "type": "SELECT_ITEM", "titleKey": "ppe_s2_t", "instructionKey": "ppe_s2_i", "audioKey": "ppe_s2", "maxPoints": 90, "params": {"correct": "helmet_boots_vest", "tray": ["helmet_boots_vest", "sneakers_cap"]}}
        ]}
    ]

    write_json(os.path.join(CONTENT_DIR, 'modules', 'fire.json'), fire_module)
    write_json(os.path.join(CONTENT_DIR, 'modules', 'gas.json'), gas_module)
    for m in lite_modules:
        write_json(os.path.join(CONTENT_DIR, 'modules', f"{m['id']}.json"), m)

def generate_questions():
    q_fire = [
        {"id": "fire_q1", "type": "MCQ", "stemKey": "fq1_s", "options": ["fq1_o1", "fq1_o2", "fq1_o3"], "answer": 1, "difficulty": 1}
    ]
    q_gas = [
        {"id": "gas_q1", "type": "MCQ", "stemKey": "gq1_s", "options": ["gq1_o1", "gq1_o2", "gq1_o3"], "answer": 0, "difficulty": 1}
    ]
    for m in ["machinery", "electrical", "ppe"]:
        write_json(os.path.join(CONTENT_DIR, 'questions', f"{m}.json"), [{"id": f"{m}_q1", "type": "MCQ", "stemKey": "dummy", "options": ["1","2"], "answer": 0}])
        
    write_json(os.path.join(CONTENT_DIR, 'questions', 'fire.json'), q_fire)
    write_json(os.path.join(CONTENT_DIR, 'questions', 'gas.json'), q_gas)

def generate_strings():
    en = {
        "_status": "draft",
        "mod_fire_title": "Fire & Explosion Response",
        "mod_gas_title": "Gas Leak & Confined Space",
        "mod_mach_title": "Machinery Safety (LOTO)",
        "mod_elec_title": "Electrical Safety",
        "mod_ppe_title": "PPE & Working at Height",
        "fire_s1_t": "Introduction to Fire Safety",
        "fire_s1_i": "Fires need heat, fuel, and oxygen. In mines, coal dust and oil are primary fuels. Smoke inhalation is the leading cause of death.",
        "fire_s2_t": "Find the Exits",
        "fire_s2_i": "Tap all safe exits in the room. Beware of blocked pathways.",
        "fire_s3_t": "Choose Extinguisher",
        "fire_s3_i": "Electrical panel is on fire. Select the correct extinguisher.",
        "fire_s4_t": "PASS Method",
        "fire_s4_i": "Execute the PASS method: Pull pin, Aim, Squeeze, Sweep.",
        "fire_s5_t": "Evacuation Sequence",
        "fire_s5_i": "Drag the steps into the correct evacuation order.",
        "fire_s6_t": "Walk to Assembly",
        "fire_s6_i": "Follow the floor arrows to the safe assembly point."
    }
    
    hi = {
        "_status": "draft-machine-translated, review by native speaker",
        "mod_fire_title": "आग और विस्फोट प्रतिक्रिया",
        "mod_gas_title": "गैस रिसाव और सीमित स्थान",
        "mod_mach_title": "मशीनरी सुरक्षा (LOTO)",
        "mod_elec_title": "विद्युत सुरक्षा",
        "mod_ppe_title": "पीपीई और ऊंचाई पर काम",
        "fire_s1_t": "अग्नि सुरक्षा का परिचय",
        "fire_s1_i": "आग को गर्मी, ईंधन और ऑक्सीजन की आवश्यकता होती है। धुएं में सांस लेना मौत का प्रमुख कारण है।",
        "fire_s2_t": "निकास खोजें",
        "fire_s2_i": "कमरे में सभी सुरक्षित निकासों पर टैप करें। अवरुद्ध रास्तों से सावधान रहें।",
        "fire_s3_t": "अग्निशामक चुनें",
        "fire_s3_i": "इलेक्ट्रिकल पैनल में आग लगी है। सही अग्निशामक चुनें।",
        "fire_s4_t": "PASS विधि",
        "fire_s4_i": "PASS विधि निष्पादित करें: पिन खींचें, लक्ष्य करें, दबाएं, घुमाएं।",
        "fire_s5_t": "निकासी क्रम",
        "fire_s5_i": "कदमों को सही निकासी क्रम में खींचें।",
        "fire_s6_t": "असेंबली पॉइंट तक चलें",
        "fire_s6_i": "सुरक्षित असेंबली पॉइंट तक फर्श के तीरों का पालन करें।"
    }

    sat = {
        "_status": "draft-machine-translated, review by native speaker",
        "mod_fire_title": "ᱥᱮᱸᱜᱮᱞ ᱟᱨ ᱯᱚᱥᱟᱜᱚᱜ ᱨᱮᱭᱟᱜ ᱛᱮᱞᱟ",
        "mod_gas_title": "ᱜᱮᱥ ᱞᱤᱠ ᱟᱨ ᱮᱥᱮᱫ ᱡᱟᱭᱜᱟ",
        "mod_mach_title": "ᱢᱤᱥᱤᱱ ᱨᱩᱠᱷᱤᱭᱟᱹ (LOTO)",
        "mod_elec_title": "ᱵᱤᱡᱽᱞᱤ ᱨᱩᱠᱷᱤᱭᱟᱹ",
        "mod_ppe_title": "PPE ᱟᱨ ᱪᱮᱛᱟᱱ ᱨᱮ ᱠᱟᱹᱢᱤ",
        "fire_s1_t": "ᱥᱮᱸᱜᱮᱞ ᱨᱩᱠᱷᱤᱭᱟᱹ ᱩᱯᱨᱩᱢ",
        "fire_s1_i": "ᱥᱮᱸᱜᱮᱞ ᱞᱟᱹᱜᱤᱫ ᱞᱚᱞᱚ, ᱥᱟᱦᱟᱱ ᱟᱨ ᱚᱠᱥᱤᱡᱮᱱ ᱞᱟᱹᱠᱛᱤᱭᱟ᱾",
        "fire_s2_t": "ᱚᱰᱚᱠᱚᱜ ᱦᱚᱨ ᱧᱟᱢ ᱢᱮ",
        "fire_s2_i": "ᱚᱲᱟᱜ ᱨᱮᱱᱟᱜ ᱡᱚᱛᱚ ᱱᱟᱯᱟᱭ ᱚᱰᱚᱠᱚᱜ ᱦᱚᱨ ᱨᱮ ᱴᱮᱯ ᱢᱮ᱾",
        "fire_s3_t": "ᱥᱮᱸᱜᱮᱞ ᱤᱬᱤᱡ ᱵᱟᱪᱷᱟᱣ ᱢᱮ",
        "fire_s3_i": "ᱵᱤᱡᱽᱞᱤ ᱵᱳᱨᱰ ᱨᱮ ᱥᱮᱸᱜᱮᱞ ᱞᱟᱜᱟᱣ ᱟᱠᱟᱱᱟ᱾ ᱴᱷᱤᱠ ᱥᱮᱸᱜᱮᱞ ᱤᱬᱤᱡ ᱵᱟᱪᱷᱟᱣ ᱢᱮ᱾",
        "fire_s4_t": "PASS ᱦᱚᱨᱟ",
        "fire_s4_i": "PASS ᱦᱚᱨᱟ ᱠᱟᱹᱢᱤ ᱨᱮ ᱞᱟᱜᱟᱣ ᱢᱮ: ᱯᱤᱱ ᱚᱨ ᱢᱮ, ᱴᱟᱨᱜᱮᱴ ᱢᱮ, ᱞᱤᱱ ᱢᱮ, ᱟᱹᱪᱩᱨ ᱢᱮ᱾",
        "fire_s5_t": "ᱚᱰᱚᱠᱚᱜ ᱥᱟᱡᱟᱣ",
        "fire_s5_i": "ᱚᱰᱚᱠᱚᱜ ᱨᱮᱱᱟᱜ ᱴᱷᱤᱠ ᱥᱟᱡᱟᱣ ᱨᱮ ᱠᱟᱹᱢᱤ ᱠᱚ ᱴᱟᱱᱟᱣ ᱢᱮ᱾",
        "fire_s6_t": "ᱮᱥᱮᱢᱵᱽᱞᱤ ᱯᱚᱭᱮᱱᱴ ᱛᱮ ᱪᱟᱞᱟᱜ ᱢᱮ",
        "fire_s6_i": "ᱱᱟᱯᱟᱭ ᱮᱥᱮᱢᱵᱽᱞᱤ ᱯᱚᱭᱮᱱᱴ ᱛᱮ ᱪᱟᱞᱟᱜ ᱞᱟᱹᱜᱤᱫ ᱚᱛ ᱨᱮᱱᱟᱜ ᱛᱤᱨ ᱠᱚ ᱯᱟᱸᱡᱟᱭ ᱢᱮ᱾"
    }
    
    write_json(os.path.join(CONTENT_DIR, 'strings', 'en.json'), en)
    write_json(os.path.join(CONTENT_DIR, 'strings', 'hi.json'), hi)
    write_json(os.path.join(CONTENT_DIR, 'strings', 'sat.json'), sat)

if __name__ == '__main__':
    generate_modules()
    generate_questions()
    generate_strings()
    print("Content packs generated.")
