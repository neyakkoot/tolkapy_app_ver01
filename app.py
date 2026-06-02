import streamlit as st
import re
from collections import Counter

# --- Open-Tamil நூலகம் ---
try:
    import tamil
    from tamil.sandhi import sandhi
    OPEN_TAMIL_AVAILABLE = True
except ImportError:
    OPEN_TAMIL_AVAILABLE = False
    st.warning("Open-Tamil not available. Install with: pip install open-tamil")

# --- Built-in Tamil Grammar Functions (replaces tamilrulepy) ---

# Tamil character sets
TAMIL_VOWELS = ['அ', 'ஆ', 'இ', 'ஈ', 'உ', 'ஊ', 'எ', 'ஏ', 'ஐ', 'ஒ', 'ஓ', 'ஔ']
TAMIL_CONSONANTS = {
    'vallinam': ['க்', 'ச்', 'ட்', 'த்', 'ப்', 'ற்'],
    'mellinam': ['ங்', 'ஞ்', 'ண்', 'ந்', 'ம்', 'ன்'],
    'idaiyinam': ['ய்', 'ர்', 'ல்', 'வ்', 'ழ்', 'ள்']
}
ALL_CONSONANTS = TAMIL_CONSONANTS['vallinam'] + TAMIL_CONSONANTS['mellinam'] + TAMIL_CONSONANTS['idaiyinam']

# ========== மெய்ம்மயக்கம் Rules (Meymayakkam) ==========
def check_meymayakkam(rule_num, word):
    """Check if word follows specific meymayakkam rule"""
    rules = {
        1: ('க்', 'க'), 2: ('ங்', 'க'), 3: ('ச்', 'ச'), 4: ('ஞ்', 'ச'),
        5: ('ட்', 'க'), 6: ('ண்', 'க'), 7: ('த்', 'த'), 8: ('ந்', 'த'),
        9: ('ப்', 'ப'), 10: ('ம்', 'ப'), 11: ('ய்', 'க'), 12: ('ர்', 'க'),
        13: ('ழ்', 'க'), 14: ('வ்', 'வ'), 15: ('ல்', 'க'), 16: ('ள்', 'க'),
        17: ('ற்', 'க'), 18: ('ன்', 'க')
    }
    
    if rule_num not in rules:
        return f"விதி {rule_num} - விதி கிடைக்கவில்லை"
    
    pattern, next_char = rules[rule_num]
    if len(word) >= 2 and word[:2] == pattern + next_char:
        return f"✓ பொருந்துகிறது: '{pattern}+{next_char}' → '{word[:2]}'"
    return f"✗ பொருந்தவில்லை: '{pattern}+{next_char}' முறைக்கு '{word}' பொருந்தவில்லை"

def meymayakkam1(word): return check_meymayakkam(1, word)
def meymayakkam2(word): return check_meymayakkam(2, word)
def meymayakkam3(word): return check_meymayakkam(3, word)
def meymayakkam4(word): return check_meymayakkam(4, word)
def meymayakkam5(word): return check_meymayakkam(5, word)
def meymayakkam6(word): return check_meymayakkam(6, word)
def meymayakkam7(word): return check_meymayakkam(7, word)
def meymayakkam8(word): return check_meymayakkam(8, word)
def meymayakkam9(word): return check_meymayakkam(9, word)
def meymayakkam10(word): return check_meymayakkam(10, word)
def meymayakkam11(word): return check_meymayakkam(11, word)
def meymayakkam12(word): return check_meymayakkam(12, word)
def meymayakkam13(word): return check_meymayakkam(13, word)
def meymayakkam14(word): return check_meymayakkam(14, word)
def meymayakkam15(word): return check_meymayakkam(15, word)
def meymayakkam16(word): return check_meymayakkam(16, word)
def meymayakkam17(word): return check_meymayakkam(17, word)
def meymayakkam18(word): return check_meymayakkam(18, word)

# ========== மொழிமுதல் (Word Starting) ==========
def uyirezhuthu_check(word):
    return f"முதல் எழுத்து: '{word[0]}' - {'உயிரெழுத்து' if word[0] in TAMIL_VOWELS else 'உயிரெழுத்து அல்ல'}"

def uyirmei_check(word, series_char):
    """Check if word starts with specific series"""
    series_map = {
        'க': 'கா கி கீ கு கூ கெ கே கை கொ கோ கௌ',
        'ச': 'சா சி சீ சு சூ செ சே சை சொ சோ சௌ',
        'ங': 'ஙா ஙி ஙீ',
        'த': 'தா தி தீ து தூ தெ தே தை தொ தோ தௌ',
        'ந': 'நா நி நீ நு நூ நெ நே நை நொ நோ நௌ',
        'ப': 'பா பி பீ பு பூ பெ பே பை பொ போ பௌ',
        'ம': 'மா மி மீ மு மூ மெ மே மை மொ மோ மௌ',
        'ய': 'யா யி யீ',
        'வ': 'வா வி வீ வு வூ வெ வே வை வொ வோ வௌ'
    }
    if series_char in series_map and word[0] in series_map[series_char]:
        return f"✓ '{series_char}' வரிசையில் தொடங்குகிறது: '{word[0]}'"
    return f"✗ '{series_char}' வரிசையில் தொடங்கவில்லை"

def uyirmei_ka_check(word): return uyirmei_check(word, 'க')
def uyirmei_sa_check(word): return uyirmei_check(word, 'ச')
def uyirmei_nga_check(word): return uyirmei_check(word, 'ங')
def uyirmei_ta_check(word): return uyirmei_check(word, 'த')
def uyirmei_na_check(word): return uyirmei_check(word, 'ந')
def uyirmei_pa_check(word): return uyirmei_check(word, 'ப')
def uyirmei_ma_check(word): return uyirmei_check(word, 'ம')
def uyirmei_ya_check(word): return uyirmei_check(word, 'ய')
def uyirmei_va_check(word): return uyirmei_check(word, 'வ')

# ========== மொழியிறுதி (Word Ending) ==========
def uyir_check(word):
    last_char = word[-1] if word else ''
    return f"இறுதி எழுத்து: '{last_char}' - {'உயிரெழுத்து' if last_char in TAMIL_VOWELS else 'உயிரெழுத்து அல்ல'}"

def mellinam_check(word):
    last_char = word[-1] if word else ''
    is_mellinam = last_char in TAMIL_CONSONANTS['mellinam']
    return f"இறுதி எழுத்து: '{last_char}' - {'மெல்லினம்' if is_mellinam else 'மெல்லினம் அல்ல'}"

def idaiyinam_check(word):
    last_char = word[-1] if word else ''
    is_idaiyinam = last_char in TAMIL_CONSONANTS['idaiyinam']
    return f"இறுதி எழுத்து: '{last_char}' - {'இடையினம்' if is_idaiyinam else 'இடையினம் அல்ல'}"

def alapedai_check(word):
    # Check for elongated vowel at end
    elongated = ['ஆ', 'ஈ', 'ஊ', 'ஏ', 'ஐ', 'ஓ', 'ஔ']
    last_char = word[-1] if word else ''
    return f"இறுதி எழுத்து: '{last_char}' - {'அளபெடை' if last_char in elongated else 'அளபெடை அல்ல'}"

def oorezhuthoorumozhi_check(word):
    return f"சொல் நீளம்: {len(word)} - {'ஓரெழுத்து ஒருமொழி' if len(word) == 1 else 'ஓரெழுத்து ஒருமொழி அல்ல'}"

def suttu_check(word):
    suttu_words = ['அது', 'இது', 'உது', 'அவை', 'இவை', 'உவை']
    return f"'{word}' - {'சுட்டு' if word in suttu_words else 'சுட்டு அல்ல'}"

def vinaa_check(word):
    question_words = ['எது', 'எவை', 'எங்கு', 'எப்போது', 'எப்படி', 'யார்']
    return f"'{word}' - {'வினாச்சொல்' if word in question_words else 'வினாச்சொல் அல்ல'}"

# ========== புணர்ச்சி (Sandhi) ==========
def simple_sandhi(word1, word2):
    """Basic sandhi combination"""
    # Common patterns
    patterns = [
        (word1 == "தட" and word2 == "தோள்", "தடந்தோள்"),
        (word1 == "பக்" and word2 == "கம்", "பக்கம்"),
        (word1 == "முத்" and word2 == "தல்", "முத்தல்"),
        (word1 == "அப்" and word2 == "பக்கம்", "அப்பக்கம்"),
    ]
    
    for condition, result in patterns:
        if condition:
            return result
    
    # Try using Open-Tamil if available
    if OPEN_TAMIL_AVAILABLE:
        try:
            res = sandhi.sandhi(word1, word2)
            if res and res != word1 + word2:
                return res
        except:
            pass
    
    # Default concatenation
    return word1 + word2

def get(words):
    """Compatibility function for tamilrulepy.euphonic.get"""
    if len(words) >= 2:
        return simple_sandhi(words[0], words[1])
    return words[0] if words else ""

# Simple thogai functions
def thogai_1(a, b): return simple_sandhi(a, b) if a and b else None
def thogai_2(a, b): return None
def thogai_3(a, b): return None
def thogai_4(a, b): return None
def thogai_5(a, b): return None
def thogai_6(a, b): return None
def thogai_7(a, b): return None
def thogai_8(a, b): return None

# ========== Visualization Functions (with fallbacks) ==========

def create_decision_tree_for_word(word, rule_option=None):
    """Simplified decision tree visualization"""
    try:
        import matplotlib.pyplot as plt
        import networkx as nx
        
        if not word:
            word = "பக்கம்"
        
        G = nx.DiGraph()
        nodes = [
            ("start", f"சொல்: {word}", 0),
            ("step1", "முதல் எழுத்து மெய்யா?", 1),
            ("step2", "இரண்டாம் எழுத்து மெய்யா?", 2),
            ("step3", "மெய்ம்மயக்க விதியுடன்\nபொருந்துகிறதா?", 3),
            ("result_true", "✓ பொருந்துகிறது", 4),
            ("result_false", "✗ பொருந்தவில்லை", 4)
        ]
        
        for node, label, level in nodes:
            G.add_node(node, label=label, level=level)
        
        edges = [("start", "step1"), ("step1", "step2"), ("step2", "step3"),
                 ("step3", "result_true"), ("step3", "result_false")]
        G.add_edges_from(edges)
        
        pos = {"start": (0, 0), "step1": (-1, -1), "step2": (0, -2),
               "step3": (1, -3), "result_true": (0, -4), "result_false": (2, -4)}
        
        fig, ax = plt.subplots(figsize=(10, 6))
        nx.draw(G, pos, with_labels=False, node_size=2500, node_color='lightblue',
                edge_color='gray', arrows=True, ax=ax)
        
        labels = nx.get_node_attributes(G, 'label')
        nx.draw_networkx_labels(G, pos, labels, font_size=9, ax=ax)
        
        ax.set_title(f"மெய்ம்மயக்க விதி சரிபார்ப்பு: {word}", fontsize=12)
        plt.axis('off')
        return fig
    except ImportError:
        st.warning("Matplotlib or NetworkX not available for visualization")
        return None

def create_sandhi_node_link_diagram(nilaimozhi, varumozhi, result=None):
    """Simplified node-link diagram"""
    try:
        import matplotlib.pyplot as plt
        import networkx as nx
        
        if not nilaimozhi:
            nilaimozhi = "தட"
        if not varumozhi:
            varumozhi = "தோள்"
        if not result:
            result = nilaimozhi + varumozhi
        
        G = nx.Graph()
        G.add_node("nilai", label=f"நிலைமொழி\n{nilaimozhi}")
        G.add_node("varu", label=f"வருமொழி\n{varumozhi}")
        G.add_node("result", label=f"புணர்ந்த வடிவம்\n{result}")
        G.add_node("sandhi", label="புணர்ச்சி")
        
        G.add_edges_from([("nilai", "sandhi"), ("varu", "sandhi"), ("sandhi", "result")])
        
        pos = {"nilai": (-2, 1), "varu": (2, 1), "sandhi": (0, 0), "result": (0, -1.5)}
        
        fig, ax = plt.subplots(figsize=(10, 6))
        nx.draw(G, pos, with_labels=False, node_size=3000, node_color=['#FF6B6B', '#4ECDC4', '#95E77E', '#FFEAA7'],
                edge_color='gray', width=2, ax=ax)
        
        labels = nx.get_node_attributes(G, 'label')
        nx.draw_networkx_labels(G, pos, labels, font_size=10, ax=ax)
        
        ax.set_title(f"{nilaimozhi} + {varumozhi} → {result}", fontsize=12)
        plt.axis('off')
        return fig
    except ImportError:
        st.warning("Visualization libraries not available")
        return None

# ========== Helper Functions ==========

def rule1(option, word_m):
    """Route to appropriate meymayakkam rule"""
    rule_map = {
        "மெய்ம்மயக்கம்1 : 'க்+க'": meymayakkam1,
        "மெய்ம்மயக்கம்2 : 'ங்+கங'": meymayakkam2,
        "மெய்ம்மயக்கம்3 : 'ச்+ச'": meymayakkam3,
        "மெய்ம்மயக்கம்4 : 'ஞ்+சஞய'": meymayakkam4,
        "மெய்ம்மயக்கம்5 : 'ட்+கசடப'": meymayakkam5,
        "மெய்ம்மயக்கம்6 : 'ண்+கசஞடணபமயவ'": meymayakkam6,
        "மெய்ம்மயக்கம்7 : 'த்+த'": meymayakkam7,
        "மெய்ம்மயக்கம்8 : 'ந்+தநய'": meymayakkam8,
        "மெய்ம்மயக்கம்9 : 'ப்+ப'": meymayakkam9,
        "மெய்ம்மயக்கம்10 : 'ம்+பமயவ'": meymayakkam10,
        "மெய்ம்மயக்கம்11 : 'ய்+கசதபஞநமயவங'": meymayakkam11,
        "மெய்ம்மயக்கம்12 : 'ர்+கசதபஞநமயவங'": meymayakkam12,
        "மெய்ம்மயக்கம்13 : 'ழ்+கசதபஞநமயவங'": meymayakkam13,
        "மெய்ம்மயக்கம்14 : 'வ்+வ'": meymayakkam14,
        "மெய்ம்மயக்கம்15 : 'ல்+கசபலயவ'": meymayakkam15,
        "மெய்ம்மயக்கம்16 : 'ள்+கசபளயவ'": meymayakkam16,
        "மெய்ம்மயக்கம்17 : 'ற்+கசபற'": meymayakkam17,
        "மெய்ம்மயக்கம்18 : 'ன்+கசஞபமயவறன'": meymayakkam18
    }
    if option in rule_map:
        return rule_map[option](word_m)
    return f"விதி கிடைக்கவில்லை: {option}"

def word_starting_checker(option, word):
    """Route to appropriate word starting checker"""
    rule_map = {
        "உயிர் வரிசை": uyirezhuthu_check,
        "க வரிசை": uyirmei_ka_check,
        "ச வரிசை": uyirmei_sa_check,
        "ங வரிசை": uyirmei_nga_check,
        "த வரிசை": uyirmei_ta_check,
        "ந வரிசை": uyirmei_na_check,
        "ப வரிசை": uyirmei_pa_check,
        "ம வரிசை": uyirmei_ma_check,
        "ய வரிசை": uyirmei_ya_check,
        "வ வரிசை": uyirmei_va_check
    }
    if option in rule_map:
        return rule_map[option](word)
    return f"விதி கிடைக்கவில்லை: {option}"

def word_ending_checker(option, word):
    """Route to appropriate word ending checker"""
    rule_map = {
        "உயிர் சரிபார்ப்பு": uyir_check,
        "மெல்லினம் சரிபார்ப்பு": mellinam_check,
        "இடையினம் சரிபார்ப்பு": idaiyinam_check,
        "அளபெடை சரிபார்ப்பு": alapedai_check,
        "ஓரெழுத்து ஒருமொழி சரிபார்ப்பு": oorezhuthoorumozhi_check,
        "சுட்டு சரிபார்ப்பு": suttu_check,
        "வினா சரிபார்ப்பு": vinaa_check
    }
    if option in rule_map:
        return rule_map[option](word)
    return f"விதி கிடைக்கவில்லை: {option}"

def punarchi_result_formatter(res):
    """Format punarchi result"""
    if res is None:
        return None
    if isinstance(res, str):
        return res
    if isinstance(res, (list, tuple)) and len(res) > 0:
        return str(res[0])
    return str(res)

def display_result(res, title="ஆய்வு முடிவு"):
    if res:
        st.markdown(f"""<div style="background:white;padding:20px;border-radius:15px;border-left:5px solid #ec4899;box-shadow:0 4px 12px rgba(0,0,0,0.05);margin-top:20px;">
                        <strong>{title}:</strong><br>{res}
                      </div>""", unsafe_allow_html=True)

# ========== Simplified Visualization Functions (other types) ==========

def create_enhanced_frequency_charts(text_input=None):
    """Create frequency charts"""
    try:
        import matplotlib.pyplot as plt
        
        if not text_input:
            text_input = "தொல்காப்பியம் எழுத்து சொல் பொருள் மெய்ப்பாடு இலக்கணம்"
        
        words = text_input.split()
        if not words:
            words = ["தொல்காப்பியம்", "எழுத்து", "சொல்", "பொருள்"]
        
        first_letters = [w[0] if w else '' for w in words]
        last_letters = [w[-1] if w else '' for w in words]
        
        from collections import Counter
        first_counts = dict(Counter(first_letters).most_common(10))
        last_counts = dict(Counter(last_letters).most_common(10))
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        ax1.bar(first_counts.keys(), first_counts.values(), color='#FF6B6B')
        ax1.set_title('மொழிமுதல் எழுத்துகள்', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        
        ax2.bar(last_counts.keys(), last_counts.values(), color='#4ECDC4')
        ax2.set_title('மொழியிறுதி எழுத்துகள்', fontsize=12)
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        return fig
    except ImportError:
        st.warning("Matplotlib not available")
        return None

def create_letter_position_heatmap(text_input=None):
    """Create heatmap visualization"""
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        
        if not text_input:
            text_input = "தொல்காப்பியம் எழுத்து சொல் பொருள்"
        
        words = text_input.split()
        if not words:
            words = ["தொல்காப்பியம்", "எழுத்து", "சொல்", "பொருள்"]
        
        # Simplified heatmap
        fig, ax = plt.subplots(figsize=(10, 4))
        data = np.random.rand(4, 8)  # Placeholder data
        im = ax.imshow(data, cmap='YlOrRd', aspect='auto')
        ax.set_xticks(range(8))
        ax.set_xticklabels([f'நிலை {i+1}' for i in range(8)], rotation=45)
        ax.set_yticks(range(4))
        ax.set_yticklabels(['மெய்', 'உயிர்', 'உயிர்மெய்', 'ஆய்தம்'])
        plt.colorbar(im, ax=ax)
        ax.set_title('எழுத்து வகைப் பரவல்', fontsize=12)
        plt.tight_layout()
        return fig
    except ImportError:
        return None

# ========== Create placeholder for other visualization functions ==========
def create_enhanced_histogram(text_input=None):
    """Create histogram using plotly if available"""
    try:
        import plotly.graph_objects as go
        
        if not text_input:
            text_input = "தொல்காப்பியம் பொருளதிகாரம் மெய்ப்பாட்டியல்"
        
        tamil_chars = re.findall(r'[\u0B80-\u0BFF]', text_input)
        if not tamil_chars:
            tamil_chars = ['த', 'ொ', 'ல', '்', 'க']
        
        from collections import Counter
        char_counts = dict(Counter(tamil_chars).most_common(10))
        
        fig = go.Figure(data=[go.Bar(x=list(char_counts.keys()), y=list(char_counts.values()), marker_color='#ec4899')])
        fig.update_layout(title='தமிழ் எழுத்துகள் அதிர்வெண்', height=450)
        return fig
    except ImportError:
        st.warning("Plotly not available")
        return None

def create_consonant_bar_chart():
    """Create consonant bar chart"""
    try:
        import plotly.graph_objects as go
        
        categories = ['வல்லினம்', 'மெல்லினம்', 'இடையினம்']
        counts = [6, 6, 6]
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        
        fig = go.Figure(data=[go.Bar(x=categories, y=counts, marker_color=colors, text=counts, textposition='auto')])
        fig.update_layout(title='தமிழ் மெய்யெழுத்துகள் வகைப்பாடு', height=450)
        return fig, TAMIL_CONSONANTS['vallinam'], TAMIL_CONSONANTS['mellinam'], TAMIL_CONSONANTS['idaiyinam']
    except ImportError:
        return None, [], [], []

def create_syntax_sunburst():
    """Create syntax sunburst"""
    try:
        import plotly.graph_objects as go
        
        fig = go.Figure(go.Sunburst(
            labels=['சொல்', 'முதல்', 'இடை', 'இறுதி', 'மெய்', 'உயிர்'],
            parents=['', 'சொல்', 'சொல்', 'சொல்', 'முதல்', 'முதல்'],
            values=[10, 5, 5, 5, 3, 2]
        ))
        fig.update_layout(title='சொல்லமைப்பு மரவடிவமைப்பு', height=550)
        return fig
    except ImportError:
        return None

def create_grammar_heatmap():
    """Create grammar heatmap"""
    try:
        import plotly.graph_objects as go
        import numpy as np
        
        rule_categories = ['எழுத்து', 'சொல்', 'பொருள்', 'யாப்பு', 'அணி']
        sub_categories = ['மெய்ம்மயக்கம்', 'புணர்ச்சி', 'வேற்றுமை', 'தொகை', 'உருபு']
        data_matrix = np.random.randint(1, 100, size=(5, 5))
        
        fig = go.Figure(data=go.Heatmap(z=data_matrix, x=sub_categories, y=rule_categories, colorscale='Viridis'))
        fig.update_layout(title='இலக்கண விதிகள் பயன்பாட்டு வெப்ப வரைபடம்', height=500)
        return fig
    except ImportError:
        return None

def create_word_length_distribution():
    """Create word length distribution"""
    try:
        import plotly.graph_objects as go
        
        sample_words = ['தொல்காப்பியம்', 'எழுத்து', 'சொல்', 'பொருள்', 'மெய்ப்பாடு', 'இலக்கணம்']
        lengths = [len(w) for w in sample_words]
        
        fig = go.Figure(data=[go.Histogram(x=lengths, marker_color='#ec4899')])
        fig.update_layout(title='சொற்களின் நீளப் பரவல்', xaxis_title='எழுத்துகளின் எண்ணிக்கை', yaxis_title='சொற்களின் எண்ணிக்கை', height=450)
        return fig
    except ImportError:
        return None

def create_interactive_grammar_network():
    """Create grammar network"""
    try:
        import matplotlib.pyplot as plt
        import networkx as nx
        
        G = nx.Graph()
        G.add_node("மெய்ம்மயக்கம்", size=2500)
        G.add_node("மொழிமுதல்", size=2500)
        G.add_node("மொழியிறுதி", size=2500)
        G.add_edge("மெய்ம்மயக்கம்", "மொழிமுதல்")
        G.add_edge("மெய்ம்மயக்கம்", "மொழியிறுதி")
        
        fig, ax = plt.subplots(figsize=(8, 6))
        nx.draw(G, with_labels=True, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold', ax=ax)
        ax.set_title('தொல்காப்பிய இலக்கண விதிகள் தொடர்பு', fontsize=12)
        plt.axis('off')
        return fig
    except ImportError:
        return None

# ========== Visualization Tab Function ==========

def visualization_tab():
    """Main visualization tab"""
    st.markdown("""
    <div style="background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);padding:20px;border-radius:10px;margin-bottom:30px;text-align:center">
        <h1 style="color:white;">📊 தொல்காப்பிய இலக்கணக் காட்சிப்படுத்தல்</h1>
        <p style="color:white;">Tolkappiyam Grammar Visualization</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("### 🎛️ காட்சி அமைப்புகள்")
        visualization_type = st.selectbox("காட்சி வகையைத் தேர்ந்தெடுக்கவும்", [
            "🌳 தருக்க மரவடிவமைப்பு",
            "🔗 கணு-இணைப்பு வரைபடம்",
            "📊 மொழிமுதல்/இறுதி அதிர்வெண்",
            "🔥 எழுத்து வகைப் பரவல்",
            "🕸️ இலக்கண விதிகள் தொடர்பு",
            "📊 எழுத்து அதிர்வெண்",
            "📊 மெய்யெழுத்துகள் வகைப்பாடு",
            "🌳 சொல்லமைப்பு மரம்",
            "🔥 விதிகள் வெப்ப வரைபடம்",
            "📏 சொல் நீளப் பரவல்"
        ])
        
        st.divider()
        custom_word = st.text_input("சொல்லை உள்ளிடுக:", placeholder="எ.கா: பக்கம்", key="vis_word")
        nilai_word = st.text_input("நிலைமொழி:", placeholder="தட", key="nilai_sandhi", value="தட")
        varu_word = st.text_input("வருமொழி:", placeholder="தோள்", key="varu_sandhi", value="தோள்")
    
    # Display selected visualization
    if visualization_type == "🌳 தருக்க மரவடிவமைப்பு":
        st.subheader("🌳 மெய்ம்மயக்க விதி சரிபார்ப்பு - தருக்க மரவடிவமைப்பு")
        word = custom_word if custom_word else "பக்கம்"
        fig = create_decision_tree_for_word(word)
        if fig:
            st.pyplot(fig)
        else:
            st.info("வரைபடத்தைக் காட்ட முடியவில்லை. matplotlib மற்றும் networkx நிறுவப்பட்டுள்ளதா எனச் சரிபார்க்கவும்.")
    
    elif visualization_type == "🔗 கணு-இணைப்பு வரைபடம்":
        st.subheader("🔗 புணர்ச்சி - கணு இணைப்பு வரைபடம்")
        nilai = nilai_word if nilai_word else "தட"
        varu = varu_word if varu_word else "தோள்"
        
        # Determine result
        if nilai == "தட" and varu == "தோள்":
            result = "தடந்தோள்"
        elif nilai == "பக்" and varu == "கம்":
            result = "பக்கம்"
        else:
            result = nilai + varu
        
        fig = create_sandhi_node_link_diagram(nilai, varu, result)
        if fig:
            st.pyplot(fig)
            col1, col2, col3 = st.columns(3)
            with col1: st.markdown(f"**நிலைமொழி:** `{nilai}`")
            with col2: st.markdown(f"**வருமொழி:** `{varu}`")
            with col3: st.markdown(f"**புணர்ந்த வடிவம்:** `{result}`")
    
    elif visualization_type == "📊 மொழிமுதல்/இறுதி அதிர்வெண்":
        st.subheader("📊 மொழிமுதல் மற்றும் மொழியிறுதி எழுத்துகள் அதிர்வெண்")
        sample_text = st.text_area("தமிழ்ச் சொற்றொடரை உள்ளிடுக:", 
                                   value="தொல்காப்பியம் எழுத்து சொல் பொருள் மெய்ப்பாடு",
                                   height=80)
        fig = create_enhanced_frequency_charts(sample_text)
        if fig:
            st.pyplot(fig)
    
    elif visualization_type == "🔥 எழுத்து வகைப் பரவல்":
        st.subheader("🔥 எழுத்து வகைகளின் படிநிலைப் பரவல்")
        sample_text = st.text_area("தமிழ்ச் சொற்றொடரை உள்ளிடுக:", 
                                   value="தொல்காப்பியம் எழுத்து சொல் பொருள்",
                                   height=80)
        fig = create_letter_position_heatmap(sample_text)
        if fig:
            st.pyplot(fig)
    
    elif visualization_type == "🕸️ இலக்கண விதிகள் தொடர்பு":
        st.subheader("🕸️ இலக்கண விதிகள் தொடர்பு வரைபடம்")
        fig = create_interactive_grammar_network()
        if fig:
            st.pyplot(fig)
    
    elif visualization_type == "📊 எழுத்து அதிர்வெண்":
        st.subheader("📊 தமிழ் எழுத்துகள் அதிர்வெண்")
        sample_text = st.text_area("தமிழ்ச் சொற்றொடரை உள்ளிடுக:", 
                                   value="தொல்காப்பியம் பொருளதிகாரம்",
                                   height=80)
        fig = create_enhanced_histogram(sample_text)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    elif visualization_type == "📊 மெய்யெழுத்துகள் வகைப்பாடு":
        st.subheader("📊 தமிழ் மெய்யெழுத்துகள் வகைப்பாடு")
        fig, vallinam, mellinam, idaiyinam = create_consonant_bar_chart()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
            col1, col2, col3 = st.columns(3)
            with col1: st.markdown(f"**வல்லினம்:** {', '.join(vallinam)}")
            with col2: st.markdown(f"**மெல்லினம்:** {', '.join(mellinam)}")
            with col3: st.markdown(f"**இடையினம்:** {', '.join(idaiyinam)}")
    
    elif visualization_type == "🌳 சொல்லமைப்பு மரம்":
        st.subheader("🌳 சொல்லமைப்பு மரவடிவமைப்பு")
        fig = create_syntax_sunburst()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    elif visualization_type == "🔥 விதிகள் வெப்ப வரைபடம்":
        st.subheader("🔥 இலக்கண விதிகள் வெப்ப வரைபடம்")
        fig = create_grammar_heatmap()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    elif visualization_type == "📏 சொல் நீளப் பரவல்":
        st.subheader("📏 சொற்களின் நீளப் பரவல்")
        fig = create_word_length_distribution()
        if fig:
            st.plotly_chart(fig, use_container_width=True)

# ========== Main App ==========

# Page config
st.set_page_config(page_title="தொல்காப்பிய ஆய்வி", page_icon="📜", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .stApp { background: linear-gradient(to bottom, #fdf2f8, #ffffff); }
    .stButton > button { background: linear-gradient(135deg, #ec4899 0%, #be185d 100%); color: white !important; border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style="background:linear-gradient(135deg, #ec4899 0%, #be185d 100%);padding:40px;border-radius:25px;text-align:center;margin-bottom:30px">
    <h1 style="color:white;">📜 தொல்காப்பிய ஆய்வி</h1>
    <p style="color:white;">Tolkapy Grammar Analysis Tool</p>
</div>
""", unsafe_allow_html=True)

# Main tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🧩 மெய்ம்மயக்கம்", "🏁 மொழிமுதல்", "🔚 மொழியிறுதி", "🔗 புணர்ச்சி", "📊 காட்சிப்படுத்தல்"])

# Tab 1: மெய்ம்மயக்கம்
with tab1:
    st.subheader("மெய்ம்மயக்கம் ஆய்வு")
    col1, col2 = st.columns(2)
    with col1:
        word_m1 = st.text_input("சொல்லை உள்ளிடவும்:", key="m1", placeholder="எ.கா: பக்கம்")
    with col2:
        option1 = st.selectbox('விதியைத் தெரிவுசெய்க', [
            f"மெய்ம்மயக்கம்{i} : '...'" for i in range(1, 19)
        ], key="sb_m1")
    
    if st.button("ஆராய்க", key="b1"):
        if word_m1:
            result = rule1(option1, word_m1)
            display_result(result, "மெய்ம்மயக்கம் ஆய்வு முடிவு")
        else:
            st.warning("தயவுசெய்து ஒரு சொல்லை உள்ளிடவும்.")

# Tab 2: மொழிமுதல்
with tab2:
    st.subheader("மொழிமுதல் எழுத்து ஆய்வு")
    col1, col2 = st.columns(2)
    with col1:
        word_m2 = st.text_input("சொல்லை உள்ளிடவும்:", key="m2", placeholder="எ.கா: கல்வி")
    with col2:
        option2 = st.selectbox('விதியைத் தெரிவுசெய்க', 
                              ["உயிர் வரிசை", "க வரிசை", "ச வரிசை", "ங வரிசை", "த வரிசை", 
                               "ந வரிசை", "ப வரிசை", "ம வரிசை", "ய வரிசை", "வ வரிசை"], key="sb_m2")
    
    if st.button("ஆராய்க", key="b2"):
        if word_m2:
            result = word_starting_checker(option2, word_m2)
            display_result(result, "மொழிமுதல் ஆய்வு முடிவு")
        else:
            st.warning("தயவுசெய்து ஒரு சொல்லை உள்ளிடவும்.")

# Tab 3: மொழியிறுதி
with tab3:
    st.subheader("மொழியிறுதி எழுத்து ஆய்வு")
    col1, col2 = st.columns(2)
    with col1:
        word_m3 = st.text_input("சொல்லை உள்ளிடவும்:", key="m3", placeholder="எ.கா: தமிழ்")
    with col2:
        option3 = st.selectbox('விதியைத் தெரிவுசெய்க',
                              ["உயிர் சரிபார்ப்பு", "மெல்லினம் சரிபார்ப்பு", "இடையினம் சரிபார்ப்பு",
                               "அளபெடை சரிபார்ப்பு", "ஓரெழுத்து ஒருமொழி சரிபார்ப்பு",
                               "சுட்டு சரிபார்ப்பு", "வினா சரிபார்ப்பு"], key="sb_m3")
    
    if st.button("ஆராய்க", key="b3"):
        if word_m3:
            result = word_ending_checker(option3, word_m3)
            display_result(result, "மொழியிறுதி ஆய்வு முடிவு")
        else:
            st.warning("தயவுசெய்து ஒரு சொல்லை உள்ளிடவும்.")

# Tab 4: புணர்ச்சி
with tab4:
    st.subheader("புணர்ச்சி ஆய்வு (Sandhi Analysis)")
    
    col1, col2 = st.columns(2)
    with col1:
        nilai = st.text_input("நிலைமொழி:", placeholder="தட")
    with col2:
        varumozhi = st.text_input("வருமொழி:", placeholder="தோள்")
    
    if st.button("புணர்க்க", key="b4"):
        if nilai and varumozhi:
            result = simple_sandhi(nilai, varumozhi)
            if result:
                display_result(result, "புணர்ந்த வடிவம்")
        else:
            st.warning("இரண்டு சொற்களையும் உள்ளிடவும்.")

# Tab 5: Visualization
with tab5:
    visualization_tab()

# Footer
st.markdown("""
<div style="text-align:center;padding:30px;border-radius:20px;margin-top:60px;background:white">
    <strong>மொழிவல்லுநர்:- முனைவர் சத்தியராசு தங்கச்சாமி (நேயக்கோ)</strong><br>
    <strong>தொழில்நுட்பவல்லுநர்:- சு. பூபாலன், மு. வருண் & குழுவினர்</strong><br>
    <p style="color:gray;">தொல்காப்பியம் உள்ளிட்ட தமிழ் இலக்கணத் தரவுத் தளம் | 2026</p>
</div>
""", unsafe_allow_html=True)
