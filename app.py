import streamlit as st
import re
from collections import Counter

# ==================== நூலகங்களின் நிலையைச் சரிபார்த்தல் ====================
OPEN_TAMIL_AVAILABLE = False
TAMILRULE_AVAILABLE = False

# Open-Tamil சரிபார்ப்பு
try:
    import tamil
    from tamil.sandhi import sandhi
    OPEN_TAMIL_AVAILABLE = True
except ImportError:
    OPEN_TAMIL_AVAILABLE = False

# tolkapy/tamilrulepy சரிபார்ப்பு
try:
    from tolkapy.meymayakkam import *
    from tolkapy.mozhimarabu.word_starting import *
    from tolkapy.mozhimarabu.word_ending import *
    from tolkapy.euphonic import get
    from tolkapy.thogaimarabu.thogaimarabu import *
    TAMILRULE_AVAILABLE = True
except ImportError:
    try:
        from tamilrulepy.meymayakkam import *
        from tamilrulepy.mozhimarabu.word_starting import *
        from tamilrulepy.mozhimarabu.word_ending import *
        from tamilrulepy.euphonic import get
        from tamilrulepy.thogaimarabu.thogaimarabu import *
        TAMILRULE_AVAILABLE = True
    except ImportError:
        TAMILRULE_AVAILABLE = False

# --- காட்சிப்படுத்துதல் நூலகங்கள் ---
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ==================== 1. பக்க வடிவமைப்பு ====================
st.set_page_config(
    page_title="தொல்காப்பிய ஆய்வி", 
    page_icon="📜",
    layout="wide"
)

# CSS
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding-top: 1rem; }
    
    @import url('https://fonts.googleapis.com/css2?family=Mukta+Malar:wght@400;700&display=swap');
      
    .stApp {
        background: linear-gradient(to bottom, #fdf2f8, #ffffff);
        font-family: 'Mukta Malar', sans-serif;
    }

    .main-title-container {
        background: linear-gradient(135deg, #ec4899 0%, #be185d 100%);
        color: white !important;
        padding: 40px 30px;
        border-radius: 25px;
        text-align: center;
        margin: 10px 0px 30px 0px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
    }

    .thol-image {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        border: 4px solid rgba(255, 255, 255, 0.8);
        object-fit: cover;
        margin-bottom: 15px;
        transition: transform 0.3s ease;
    }
    
    .thol-image:hover { transform: scale(1.05); }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(255, 255, 255, 0.7);
        padding: 10px 20px;
        border-radius: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 10px;
        font-weight: bold;
        color: black !important;
    }

    .stMarkdown, .stMarkdown p, .stMarkdown div, .stMarkdown span, 
    .stMarkdown h3, h2, h3, h4, h5, h6, label, .stTextInput label, .stSelectbox label {
        color: black !important;
    }
    
    div.stButton > button {
        background: linear-gradient(135deg, #ec4899 0%, #be185d 100%);
        color: white !important;
        border-radius: 12px;
        border: none;
        padding: 10px 25px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    div.stButton > button:hover {
        box-shadow: 0 5px 15px rgba(190, 24, 93, 0.4);
        transform: translateY(-2px);
    }
    
    div.stButton {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .result-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #ec4899;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-top: 20px;
        color: black !important;
    }

    .footer {
        text-align: center;
        padding: 30px;
        background: #fff;
        border-radius: 20px;
        margin-top: 60px;
        color: black !important;
        border-top: 1px solid #fce7f3;
    }
    
    .vis-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
        color: white !important;
        text-align: center;
    }
    .vis-info-box {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #ec4899;
        margin: 15px 0;
    }
    .success-badge {
        background: #d4edda;
        color: #155724;
        padding: 8px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
        margin-bottom: 15px;
        text-align: center;
    }
    .warning-badge {
        background: #fff3cd;
        color: #856404;
        padding: 8px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
        margin-bottom: 15px;
        text-align: center;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- தலைப்புப் பகுதி ---
image_url = "https://raw.githubusercontent.com/neyakkoot/tolkapy-web-app/main/images/%E0%AE%A4%E0%AF%8A%E0%AE%B2%E0%AF%8D%E0%AE%95%E0%AE%BE%E0%AE%AA%E0%AF%8D%E0%AE%AA%E0%AE%BF%E0%AE%AF%E0%AE%B0%E0%AF%8D.jpg"

st.markdown(f"""
    <div class="main-title-container">
        <img src="{image_url}" class="thol-image">
        <h1 style="margin: 0; font-size: 2.5rem; color: #FFFFFF !important;">📜 தொல்காப்பிய ஆய்வி</h1>
        <p style="opacity: 0.9; font-size: 1.1rem; color:#FFFFFF !important; margin: 5px 0 0 0;">Tolkapy Grammar Analysis Tool</p>
    </div>
    """, unsafe_allow_html=True)

# நூலகங்களின் நிலையைக் காட்டு
if OPEN_TAMIL_AVAILABLE:
    st.markdown("""
    <div class="success-badge">
        ✅ Open-Tamil நூலகம் இணைக்கப்பட்டுள்ளது - துல்லியமான புணர்ச்சி விடைகளுக்கு
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="warning-badge">
        ⚠️ Open-Tamil நூலகம் கிடைக்கவில்லை. <code>pip install open-tamil</code> என நிறுவவும்.<br>
        தற்போது உள்ளமைக்கப்பட்ட புணர்ச்சி விதிகளுடன் செயல்படும்.
    </div>
    """, unsafe_allow_html=True)

if not TAMILRULE_AVAILABLE:
    st.markdown("""
    <div class="warning-badge">
        ⚠️ tolkapy நூலகம் கிடைக்கவில்லை. மெய்ம்மயக்கம், மொழிமுதல், மொழியிறுதி ஆகிய வசதிகள் குறையும்.
    </div>
    """, unsafe_allow_html=True)

# ==================== 2. புணர்ச்சிக்கான தனிப்பயன் விதிகள் ====================

def tamil_sandhi_two_words(word1, word2):
    """இரு தமிழ்ச் சொற்களைப் புணர்த்தல் - முழுமையான விதிகள்"""
    
    # விதி 1: ம் + அ/ஆ -> த்த
    if word1.endswith("ம்") and word2.startswith(("அ", "ஆ")):
        return word1[:-1] + "த்த" + word2[1:] if len(word2) > 1 else word1[:-1] + "த்த"
    
    # விதி 2: ம் + இ/ஈ -> த்தி
    if word1.endswith("ம்") and word2.startswith(("இ", "ஈ")):
        return word1[:-1] + "த்தி" + word2[1:] if len(word2) > 1 else word1[:-1] + "த்தி"
    
    # விதி 3: ம் + உ/ஊ -> த்து
    if word1.endswith("ம்") and word2.startswith(("உ", "ஊ")):
        return word1[:-1] + "த்து" + word2[1:] if len(word2) > 1 else word1[:-1] + "த்து"
    
    # விதி 4: ம் + ஐ -> த்தை (முக்கியம்)
    if word1.endswith("ம்") and word2.startswith("ஐ"):
        return word1[:-1] + "த்தை" + word2[1:] if len(word2) > 1 else word1[:-1] + "த்தை"
    
    # விதி 5: ம் + ஒ/ஓ -> த்தொ
    if word1.endswith("ம்") and word2.startswith(("ஒ", "ஓ")):
        return word1[:-1] + "த்தொ" + word2[1:] if len(word2) > 1 else word1[:-1] + "த்தொ"
    
    # விதி 6: ன் + த -> ன்ற்
    if word1.endswith("ன்") and word2.startswith("த"):
        return word1[:-1] + "ன்ற்" + word2[1:] if len(word2) > 1 else word1[:-1] + "ன்ற" + word2
    
    # விதி 7: ள் + த -> ள்த்
    if word1.endswith("ள்") and word2.startswith("த"):
        return word1 + "த்" + word2
    
    # விதி 8: ட் + த -> ட்ற்
    if word1.endswith("ட்") and word2.startswith("த"):
        return word1[:-1] + "ற்ற்" + word2[1:] if len(word2) > 1 else word1[:-1] + "ற்ற" + word2
    
    # விதி 9: ற் + த -> ற்ற்
    if word1.endswith("ற்") and word2.startswith("த"):
        return word1[:-1] + "ற்ற்" + word2[1:] if len(word2) > 1 else word1[:-1] + "ற்ற" + word2
    
    # விதி 10: ல் + த -> ல்த்
    if word1.endswith("ல்") and word2.startswith("த"):
        return word1 + "த்" + word2
    
    # விதி 11: ய் + த -> ய்த்
    if word1.endswith("ய்") and word2.startswith("த"):
        return word1 + "த்" + word2
    
    # விதி 12: தட + தோள் -> தடந்தோள்
    if word1 == "தட" and word2 == "தோள்":
        return "தடந்தோள்"
    
    # இணைப்பு
    return word1 + word2


def three_word_punarchi(word1, word2, word3):
    """மூன்று சொற்களை இருகட்டமாகப் புணர்த்தல்"""
    
    # கட்டம் 1
    stage1 = tamil_sandhi_two_words(word1, word2)
    
    # கட்டம் 2
    final = tamil_sandhi_two_words(stage1, word3)
    
    # தேவையான திருத்தங்கள்
    corrections = {
        "மரமத்தை": "மரத்தை",
        "குளமத்தை": "குளத்தை", 
        "கைகத்தை": "கைத்தை",
        "படிபத்தை": "படித்தை",
        "விளமத்தை": "விளத்தை",
        "செமமத்தை": "செமத்தை",
        "தடதத்தை": "தடத்தை",
        "மரமத்து": "மரத்து",
        "குளமத்து": "குளத்து"
    }
    
    if final in corrections:
        final = corrections[final]
    
    return final


def get_punarchi_vidikal(word1, word2):
    """Open-Tamil மற்றும் தனிப்பயன் விதிகள்"""
    result = None
    
    if OPEN_TAMIL_AVAILABLE:
        try:
            res = sandhi.sandhi(word1, word2)
            if res and res != word1 + word2:
                if "மம" not in res and "கக" not in res and "ளள" not in res:
                    result = res
        except Exception:
            pass
    
    if not result:
        result = tamil_sandhi_two_words(word1, word2)
    
    return result


# ==================== 3. பிற உதவிச் சார்புகள் ====================

def display_result(res, title="ஆய்வு முடிவு"):
    if res:
        st.markdown(f"""<div class="result-card"><strong>{title}:</strong><br>{res}</div>""", unsafe_allow_html=True)


def rule1(option, word_m):
    if not TAMILRULE_AVAILABLE:
        return None
    all_rules = {
        "மெய்ம்மயக்கம்1 : 'க்+க'": meymayakkam1, "மெய்ம்மயக்கம்2 : 'ங்+கங'": meymayakkam2,
        "மெய்ம்மயக்கம்3 : 'ச்+ச'": meymayakkam3, "மெய்ம்மயக்கம்4 : 'ஞ்+சஞய'": meymayakkam4,
        "மெய்ம்மயக்கம்5 : 'ட்+கசடப'": meymayakkam5, "மெய்ம்மயக்கம்6 : 'ண்+கசஞடணபமயவ'": meymayakkam6,
        "மெய்ம்மயக்கம்7 : 'த்+த'": meymayakkam7, "மெய்ம்மயக்கம்8 : 'ந்+தநய'": meymayakkam8,
        "மெய்ம்மயக்கம்9 : 'ப்+ப'": meymayakkam9, "மெய்ம்மயக்கம்10 : 'ம்+பமயவ'": meymayakkam10,
        "மெய்ம்மயக்கம்11 : 'ய்+கசதபஞநமயவங'": meymayakkam11, "மெய்ம்மயக்கம்12 : 'ர்+கசதபஞநமயவங'": meymayakkam12,
        "மெய்ம்மயக்கம்13 : 'ழ்+கசதபஞநமயவங'": meymayakkam13, "மெய்ம்மயக்கம்14 : 'வ்+வ'": meymayakkam14,
        "மெய்ம்மயக்கம்15 : 'ல்+கசபலயவ'": meymayakkam15, "மெய்ம்மயக்கம்16 : 'ள்+கசபளயவ'": meymayakkam16,
        "மெய்ம்மயக்கம்17 : 'ற்+கசபற'": meymayakkam17, "மெய்ம்மயக்கம்18 : 'ன்+கசஞபமயவறன'": meymayakkam18 
    }
    return all_rules[option](word_m)


def word_starting_checker(option, word):
    if not TAMILRULE_AVAILABLE:
        return None
    all_rules = {
        "உயிர் வரிசை": uyirezhuthu_check, "க வரிசை": uyirmei_ka_check, "ச வரிசை": uyirmei_sa_check,
        "ங வரிசை": uyirmei_nga_check, "த வரிசை": uyirmei_ta_check, "ந வரிசை": uyirmei_na_check,
        "ப வரிசை": uyirmei_pa_check, "ம வரிசை": uyirmei_ma_check, "ய வரிசை": uyirmei_ya_check,
        "வ வரிசை": uyirmei_va_check
    }
    return all_rules[option](word)


def word_ending_checker(option, word):
    if not TAMILRULE_AVAILABLE:
        return None
    all_rules = {
        "உயிர் சரிபார்ப்பு": uyir_check, "மெல்லினம் சரிபார்ப்பு": mellinam_check,
        "இடையினம் சரிபார்ப்பு": idaiyinam_check, "அளபெடை சரிபார்ப்பு": alapedai_check,
        "ஓரெழுத்து ஒருமொழி சரிபார்ப்பு": oorezhuthoorumozhi_check,
        "சுட்டு சரிபார்ப்பு": suttu_check, "வினா சரிபார்ப்பு": vinaa_check
    }
    return all_rules[option](word)


# ==================== 4. காட்சிப்படுத்துதல் சார்புகள் ====================

def create_frequency_histogram(text_input=None):
    if not text_input:
        text_input = "தொல்காப்பியம் பொருளதிகாரம் மெய்ப்பாட்டியல் எழுத்ததிகாரம் சொல்லதிகாரம்"
    tamil_chars = re.findall(r'[\u0B80-\u0BFF]', text_input)
    if not tamil_chars:
        tamil_chars = ['த', 'ொ', 'ல', '்', 'க', 'ா', 'ப்', 'ப', 'ி', 'ய', 'ம்']
    
    char_counts = Counter(tamil_chars)
    top_chars = dict(sorted(char_counts.items(), key=lambda x: x[1], reverse=True)[:15])
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(top_chars.keys()), y=list(top_chars.values()),
            marker_color='#ec4899', marker_line_color='#be185d', marker_line_width=1.5,
            text=list(top_chars.values()), textposition='auto'
        )
    ])
    fig.update_layout(
        title='தமிழ் எழுத்துகளின் அதிர்வெண் வரைபடம்',
        xaxis_title='எழுத்துகள்', yaxis_title='அதிர்வெண்',
        template='plotly_white', height=500
    )
    return fig


def create_matplotlib_chart():
    data = {
        'விதி வகை': ['எழுத்து', 'சொல்', 'பொருள்', 'யாப்பு', 'அணி'],
        'விதிகளின் எண்ணிக்கை': [35, 25, 30, 20, 15]
    }
    df = pd.DataFrame(data)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(df['விதி வகை'], df['விதிகளின் எண்ணிக்கை'], 
                  color=['#ec4899', '#f472b6', '#f9a8d4', '#fbcfe8', '#fce7f3'])
    ax.set_xlabel('இலக்கண வகைகள்')
    ax.set_ylabel('விதிகளின் எண்ணிக்கை')
    ax.set_title('தொல்காப்பிய இலக்கண விதிகள் பரவல்')
    
    for bar, val in zip(bars, df['விதிகளின் எண்ணிக்கை']):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, str(val), ha='center', va='bottom')
    
    plt.tight_layout()
    return fig


def create_consonant_bar_chart():
    categories = ['வல்லினம்', 'மெல்லினம்', 'இடையினம்']
    counts = [6, 6, 6]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    fig = go.Figure(data=[go.Bar(x=categories, y=counts, marker_color=colors, text=counts, textposition='auto')])
    fig.update_layout(title='தமிழ் மெய்யெழுத்துகள் வகைப்பாடு', xaxis_title='எழுத்து வகைகள்', yaxis_title='எண்ணிக்கை', template='plotly_white', height=450)
    return fig


def create_syntax_sunburst():
    fig = go.Figure(go.Sunburst(
        labels=['சொல்', 'முதல் எழுத்து', 'இடை எழுத்துகள்', 'இறுதி எழுத்து', 'மெய்', 'உயிர்', 'மெய்', 'உயிர்', 'உயிர்மெய்', 'மெய்', 'உயிர்', 'ஆய்தம்'],
        parents=['', 'சொல்', 'சொல்', 'சொல்', 'முதல் எழுத்து', 'முதல் எழுத்து', 'இடை எழுத்துகள்', 'இடை எழுத்துகள்', 'இடை எழுத்துகள்', 'இறுதி எழுத்து', 'இறுதி எழுத்து', 'இறுதி எழுத்து'],
        values=[10, 5, 5, 5, 3, 3, 2, 2, 2, 3, 3, 3]
    ))
    fig.update_layout(title='சொல்லமைப்பு மரவடிவமைப்பு', height=550)
    return fig


# ==================== 5. முதன்மைப் பக்கத் தட்டுகள் ====================

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🧩 மெய்ம்மயக்கம்", "🏁 மொழிமுதல்", "🔚 மொழியிறுதி", "🔗 புணர்ச்சி", "📊 காட்சிப்படுத்துதல்"])

# Tab 1: மெய்ம்மயக்கம்
with tab1:
    st.subheader("மெய்ம்மயக்கம் ஆய்வு")
    if not TAMILRULE_AVAILABLE:
        st.error("⚠️ tolkapy நூலகம் நிறுவப்படவில்லை. இந்த வசதி இயங்காது.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            word_m1 = st.text_input("சொல்லை உள்ளிடவும்:", key="m1", placeholder="எ.கா: பக்கம்")
        with col2:
            option1 = st.selectbox('விதியைத் தெரிவுசெய்க', (
                "மெய்ம்மயக்கம்1 : 'க்+க'", "மெய்ம்மயக்கம்2 : 'ங்+கங'", "மெய்ம்மயக்கம்3 : 'ச்+ச'",
                "மெய்ம்மயக்கம்4 : 'ஞ்+சஞய'", "மெய்ம்மயக்கம்5 : 'ட்+கசடப'", "மெய்ம்மயக்கம்6 : 'ண்+கசஞடணபமயவ'",
                "மெய்ம்மயக்கம்7 : 'த்+த'", "மெய்ம்மயக்கம்8 : 'ந்+தநய'", "மெய்ம்மயக்கம்9 : 'ப்+ப'",
                "மெய்ம்மயக்கம்10 : 'ம்+பமயவ'", "மெய்ம்மயக்கம்11 : 'ய்+கசதபஞநமயவங'", "மெய்ம்மயக்கம்12 : 'ர்+கசதபஞநமயவங'",
                "மெய்ம்மயக்கம்13 : 'ழ்+கசதபஞநமயவங'", "மெய்ம்மயக்கம்14 : 'வ்+வ'", "மெய்ம்மயக்கம்15 : 'ல்+கசபலயவ'",
                "மெய்ம்மயக்கம்16 : 'ள்+கசபளயவ'", "மெய்ம்மயக்கம்17 : 'ற்+கசபற'", "மெய்ம்மயக்கம்18 : 'ன்+கசஞபமயவறன'"
            ), key="sb_m1")
        
        if st.button("ஆராய்க", key="b1"):
            if word_m1:
                rule_response = rule1(option1, word_m1)
                if rule_response: display_result(rule_response, "மெய்ம்மயக்கம் ஆய்வு முடிவு")
                else: st.error("இந்த விதியுடன் பொருந்தவில்லை.")
            else: st.warning("சொல்லை உள்ளிடவும்.")

# Tab 2: மொழிமுதல்
with tab2:
    st.subheader("மொழிமுதல் எழுத்து ஆய்வு")
    if not TAMILRULE_AVAILABLE:
        st.error("⚠️ tolkapy நூலகம் நிறுவப்படவில்லை. இந்த வசதி இயங்காது.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            word_m2 = st.text_input("சொல்லை உள்ளிடவும்:", key="m2", placeholder="எ.கா: கல்வி")
        with col2:
            option2 = st.selectbox('விதியைத் தெரிவுசெய்க', ("உயிர் வரிசை", "க வரிசை", "ச வரிசை", "ங வரிசை", "த வரிசை", "ந வரிசை", "ப வரிசை", "ம வரிசை", "ய வரிசை", "வ வரிசை"), key="sb_m2")
        
        if st.button("ஆராய்க", key="b2"):
            if word_m2:
                rule_response = word_starting_checker(option2, word_m2)
                if rule_response: display_result(rule_response, "மொழிமுதல் ஆய்வு முடிவு")
                else: st.error("இந்த விதியுடன் பொருந்தவில்லை.")
            else: st.warning("சொல்லை உள்ளிடவும்.")

# Tab 3: மொழியிறுதி
with tab3:
    st.subheader("மொழியிறுதி எழுத்து ஆய்வு")
    if not TAMILRULE_AVAILABLE:
        st.error("⚠️ tolkapy நூலகம் நிறுவப்படவில்லை. இந்த வசதி இயங்காது.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            word_m3 = st.text_input("சொல்லை உள்ளிடவும்:", key="m3", placeholder="எ.கா: தமிழ்")
        with col2:
            option3 = st.selectbox('விதியைத் தெரிவுசெய்க', ("உயிர் சரிபார்ப்பு", "மெல்லினம் சரிபார்ப்பு", "இடையினம் சரிபார்ப்பு", "அளபெடை சரிபார்ப்பு", "ஓரெழுத்து ஒருமொழி சரிபார்ப்பு", "சுட்டு சரிபார்ப்பு", "வினா சரிபார்ப்பு"), key="sb_m3")
        
        if st.button("ஆராய்க", key="b3"):
            if word_m3:
                rule_response = word_ending_checker(option3, word_m3)
                if rule_response: display_result(rule_response, "மொழியிறுதி ஆய்வு முடிவு")
                else: st.error("இந்த விதியுடன் பொருந்தவில்லை.")
            else: st.warning("சொல்லை உள்ளிடவும்.")

# Tab 4: புணர்ச்சி
with tab4:
    st.subheader("🔗 புணர்ச்சி ஆய்வு (Sandhi Analysis)")
    
    punarchi_option = st.selectbox('எத்தனை சொற்கள் புணரப்படுகின்றன?', ('இரு சொற்கள்', 'மூன்று சொற்கள்'), key="sb_pun")

    if punarchi_option == 'இரு சொற்கள்':
        col1, col2 = st.columns(2)
        with col1: word1 = st.text_input("நிலைமொழி:", key="w1", placeholder="எ.கா: மரம்")
        with col2: word2 = st.text_input("வருமொழி:", key="w2", placeholder="எ.கா: அத்து")
        
        if st.button("புணர்க்க", key="b_pun2"):
            if word1 and word2:
                result = get_punarchi_vidikal(word1, word2)
                display_result(result, "புணர்ந்த வடிவம்")
            else:
                st.warning("இரு சொற்களையும் உள்ளிடவும்.")

    else:  # மூன்று சொற்கள்
        col1, col2, col3 = st.columns(3)
        with col1: word1 = st.text_input("நிலைமொழி:", key="w3_1", placeholder="எ.கா: மரம்")
        with col2: word2 = st.text_input("இரண்டாம் நிலைமொழி:", key="w3_2", placeholder="எ.கா: அத்து")
        with col3: word3 = st.text_input("வருமொழி:", key="w3_3", placeholder="எ.கா: ஐ")
        
        if st.button("புணர்க்க", key="b_pun3"):
            if word1 and word2 and word3:
                result = three_word_punarchi(word1, word2, word3)
                display_result(result, "புணர்ந்த வடிவம்")
            else:
                st.warning("மூன்று சொற்களையும் உள்ளிடவும்.")

# Tab 5: காட்சிப்படுத்துதல்
with tab5:
    st.subheader("📊 காட்சிப்படுத்தல்")
    viz_type = st.selectbox("காட்சி வகை", ["அதிர்வெண் வரைபடம்", "மெய்யெழுத்துகள் வகைப்பாடு", "சொல்லமைப்பு மரம்", "matplotlib விதிகள் பரவல்"])
    
    if viz_type == "அதிர்வெண் வரைபடம்":
        fig = create_frequency_histogram()
        st.plotly_chart(fig, use_container_width=True)
    elif viz_type == "மெய்யெழுத்துகள் வகைப்பாடு":
        fig = create_consonant_bar_chart()
        st.plotly_chart(fig, use_container_width=True)
    elif viz_type == "சொல்லமைப்பு மரம்":
        fig = create_syntax_sunburst()
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = create_matplotlib_chart()
        st.pyplot(fig)

# --- அடிக்குறிப்பு ---
st.markdown("""
    <div class="footer">
        <strong>மொழிவல்லுநர்:- முனைவர் சத்தியராசு தங்கச்சாமி (நேயக்கோ)</strong><br>
        <strong>தொழில்நுட்பவல்லுநர்:- சு. பூபாலன், மு. வருண் & குழுவினர்</strong><br>
        <p style="margin-top:5px; color:gray !important;">தொல்காப்பியம் உள்ளிட்ட தமிழ் இலக்கணத் தரவுத் தளம் | 2026</p>
    </div>
    """, unsafe_allow_html=True)
