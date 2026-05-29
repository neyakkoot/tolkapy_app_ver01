import streamlit as st
import importlib.util
import os
import re
from collections import Counter

# --- tamilrulepy நூலக இறக்குமதிகள் ---
from tamilrulepy.meymayakkam import (
    meymayakkam1, meymayakkam2, meymayakkam3, meymayakkam4, meymayakkam5,
    meymayakkam6, meymayakkam7, meymayakkam8, meymayakkam9, meymayakkam10,
    meymayakkam11, meymayakkam12, meymayakkam13, meymayakkam14, meymayakkam15,
    meymayakkam16, meymayakkam17, meymayakkam18
)

from tamilrulepy.mozhimarabu.word_starting import (
    uyirezhuthu_check, uyirmei_ka_check, uyirmei_ma_check, uyirmei_na_check,
    uyirmei_nga_check, uyirmei_pa_check, uyirmei_sa_check, uyirmei_ta_check,
    uyirmei_va_check, uyirmei_ya_check
)

from tamilrulepy.mozhimarabu.word_ending import (
    uyir_check, mellinam_check, idaiyinam_check, alapedai_check,
    oorezhuthoorumozhi_check, suttu_check, vinaa_check
)

from tamilrulepy.euphonic import get
from tamilrulepy.thogaimarabu.thogaimarabu import (
    thogai_1, thogai_2, thogai_3, thogai_4, thogai_5, thogai_6, thogai_7, thogai_8
)

# --- காட்சிப்படுத்துதல் நூலகங்கள் ---
import plotly.graph_objects as go
import numpy as np

# ==================== 1. பக்க வடிவமைப்பு (Page Configuration) ====================
st.set_page_config(
    page_title="தொல்காப்பிய ஆய்வி", 
    page_icon="📜",
    layout="wide"
)

# ஸ்ட்ரீம்லிட் இயல்பு வடிவங்களை மறைத்தல் மற்றும் தனிப்பயன் CSS
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

# ==================== 2. உதவிச் சார்புகள் (Helper Functions) ====================

def rule1(option, word_m):
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
    all_rules = {
        "உயிர் வரிசை": uyirezhuthu_check, "க வரிசை": uyirmei_ka_check, "ச வரிசை": uyirmei_sa_check,
        "ங வரிசை": uyirmei_nga_check, "த வரிசை": uyirmei_ta_check, "ந வரிசை": uyirmei_na_check,
        "ப வரிசை": uyirmei_pa_check, "ம வரிசை": uyirmei_ma_check, "ய வரிசை": uyirmei_ya_check,
        "வ வரிசை": uyirmei_va_check
    }
    return all_rules[option](word)

def word_ending_checker(option, word):
    all_rules = {
        "உயிர் சரிபார்ப்பு": uyir_check, "மெல்லினம் சரிபார்ப்பு": mellinam_check,
        "இடையினம் சரிபார்ப்பு": idaiyinam_check, "அளபெடை சரிபார்ப்பு": alapedai_check,
        "ஓரெழுத்து ஒருமொழி சரிபார்ப்பு": oorezhuthoorumozhi_check,
        "சுட்டு சரிபார்ப்பு": suttu_check, "வினா சரிபார்ப்பு": vinaa_check
    }
    return all_rules[option](word)

def punarchi_result_formatter(res):
    if res is None:
        return None
    if isinstance(res, str):
        return res
    if isinstance(res, tuple):
        res = list(res)
    if isinstance(res, list):
        if len(res) == 0:
            return None
        first = res[0]
        if isinstance(first, list) and len(first) > 0:
            return first[0]
        return first
    return str(res)

def display_result(res, title="ஆய்வு முடிவு"):
    if res:
        st.markdown(f"""<div class="result-card"><strong>{title}:</strong><br>{res}</div>""", unsafe_allow_html=True)

# ==================== 3. Panels - காட்சிப்படுத்துதல் சார்புகள் (Visualization) ====================

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
            text=list(top_chars.values()), textposition='auto',
            hovertemplate='<b>%{x}</b><br>அதிர்வெண்: %{y}<extra></extra>'
        )
    ])
    fig.update_layout(
        title={'text': 'தமிழ் எழுத்துகளின் அதிர்வெண் வரைபடம்<br><span style="font-size:14px;color:gray;">Tamil Letter Frequency Histogram</span>', 'x': 0.5, 'xanchor': 'center'},
        xaxis_title='எழுத்துகள் (Letters)', yaxis_title='அதிர்வெண் (Frequency)',
        template='plotly_white', height=500
    )
    return fig

def create_consonant_bar_chart():
    categories = ['வல்லினம்\n(Hard)', 'மெல்லினம்\n(Soft)', 'இடையினம்\n(Medium)']
    counts = [6, 6, 6]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    vallinam = ['க்', 'ச்', 'ட்', 'த்', 'ப்', 'ற்']
    mellinam = ['ங்', 'ஞ்', 'ண்', 'ந்', 'ம்', 'ன்']
    idaiyinam = ['ய்', 'ர்', 'ல்', 'வ்', 'ழ்', 'ள்']
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories, y=counts, marker_color=colors, text=counts, textposition='auto',
            hovertemplate='<b>%{x}</b><br>எழுத்துகள்: %{y}<extra></extra>'
        )
    ])
    fig.update_layout(
        title='தமிழ் மெய்யெழுத்துகள் வகைப்பாடு<br><span style="font-size:14px;color:gray;">Tamil Consonant Classification</span>',
        xaxis_title='எழுத்து வகைகள் (Consonant Types)', yaxis_title='எண்ணிக்கை (Count)',
        template='plotly_white', height=450
    )
    return fig, vallinam, mellinam, idaiyinam

def create_syntax_sunburst():
    tree_data = {
        'name': 'சொல் (Word)',
        'children': [
            {
                'name': 'முதல் எழுத்து<br>(First)',
                'children': [{'name': 'மெய் (C)'}, {'name': 'உயிர் (V)'}]
            },
            {
                'name': 'இடை எழுத்துகள்<br>(Middle)',
                'children': [{'name': 'மெய் (C)'}, {'name': 'உயிர் (V)'}, {'name': 'உயிர்மெய் (CV)'}]
            },
            {
                'name': 'இறுதி எழுத்து<br>(Last)',
                'children': [{'name': 'மெய் (C)'}, {'name': 'உயிர் (V)'}, {'name': 'ஆய்தம் (K)'}]
            }
        ]
    }
    labels, parents, values = [], [], []
    def add_nodes(data, parent):
        labels.append(data['name'])
        parents.append(parent)
        values.append(10 if parent == '' else 5)
        if 'children' in data:
            for child in data['children']: add_nodes(child, data['name'])
    add_nodes(tree_data, '')
    
    fig = go.Figure(go.Sunburst(
        labels=labels, parents=parents, values=values, branchvalues='total',
        marker=dict(colors=['#ec4899', '#f472b6', '#f9a8d4', '#fbcfe8', '#fce7f3']),
        hovertemplate='<b>%{label}</b><br><extra></extra>'
    ))
    fig.update_layout(title='சொல்லமைப்பு மரவடிவமைப்பு<br><span style="font-size:14px;color:gray;">Word Structure Syntax Tree</span>', height=550)
    return fig

def create_grammar_heatmap():
    rule_categories = ['எழுத்து', 'சொல்', 'பொருள்', 'யாப்பு', 'அணி']
    sub_categories = ['மெய்ம்மயக்கம்', 'புணர்ச்சி', 'வேற்றுமை', 'தொகை', 'உருபு']
    np.random.seed(42)
    data_matrix = np.random.randint(1, 100, size=(len(rule_categories), len(sub_categories)))
    
    fig = go.Figure(data=go.Heatmap(
        z=data_matrix, x=sub_categories, y=rule_categories, colorscale='Viridis',
        text=data_matrix, texttemplate='%{text}', textfont={"size": 12},
        hovertemplate='<b>%{y}</b> - <b>%{x}</b><br>மதிப்பு: %{z}<extra></extra>'
    ))
    fig.update_layout(title='இலக்கண விதிகள் பயன்பாட்டு வெப்ப வரைபடம்<br><span style="font-size:14px;color:gray;">Grammar Heatmap</span>', height=500, template='plotly_white')
    return fig

def create_word_length_distribution():
    sample_words = ['தொல்காப்பியம்', 'எழுத்து', 'சொல்', 'பொருள்', 'மெய்ப்பாடு', 'இலக்கணம்', 'நூல்', 'உரை', 'விளக்கம்', 'ஆய்வு']
    lengths = [len(w) for w in sample_words]
    fig = go.Figure(data=[go.Histogram(x=lengths, marker_color='#ec4899', opacity=0.7, hovertemplate='சொல் நீளம்: %{x}<br>எண்ணிக்கை: %{y}<extra></extra>')])
    fig.update_layout(title='சொற்களின் நீளப் பரவல்<br><span style="font-size:14px;color:gray;">Word Length Distribution</span>', xaxis_title='எழுத்துகளின் எண்ணிக்கை', yaxis_title='சொற்களின் எண்ணிக்கை', template='plotly_white', height=450)
    return fig

# --- காட்சிப்படுத்துதல் பகுதி (Visualization Tab Sub-content) ---
def visualization_tab():
    st.markdown("""<div class="vis-header"><h1>📊 தொல்காப்பிய இலக்கணக் காட்சிப்படுத்தல்</h1><p>Tolkappiyam Grammar Visualization | Interactive Learning Tool</p></div>""", unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("### 🎛️ காட்சி அமைப்புகள்")
        visualization_type = st.selectbox("காட்சி வகையைத் தேர்ந்தெடுக்கவும்", ["📊 அதிர்வெண் வரைபடம்", "📊 மெய்யெழுத்துகள் வகைப்பாடு", "🌳 சொல்லமைப்பு மரவடிவமைப்பு", "🔥 விதிகள் வெப்ப வரைபடம்", "📏 சொல் நீளப் பரவல்"])
        st.divider()
        st.markdown("""<div class="vis-info-box"><strong>📚 கல்விக் குறிப்பு:</strong><br>வரைபடங்கள் தமிழ் மொழியின் ஒலியியல், சொல்லமைப்பு அம்சங்களை எளிதாகப் புரிந்துகொள்ள உதவுகிறது.</div>""", unsafe_allow_html=True)
        custom_text = st.text_area("✍️ சொந்தப் பகுப்பாய்வுக்குத் தமிழ்ச் சொற்றொடரை உள்ளிடுக:", placeholder="எ.கா: தொல்காப்பியர் தமிழ் இலக்கணத்தை எழுதினார்", height=100)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        if visualization_type == "📊 அதிர்வெண் வரைபடம்":
            st.subheader("📊 தமிழ் எழுத்துகள் அதிர்வெண் பகுப்பாய்வு")
            fig = create_frequency_histogram(custom_text) if custom_text else create_frequency_histogram()
            st.plotly_chart(fig, use_container_width=True)
        elif visualization_type == "📊 மெய்யெழுத்துகள் வகைப்பாடு":
            st.subheader("📊 தமிழ் மெய்யெழுத்துகள் வகைப்பாடு")
            fig, vallinam, mellinam, idaiyinam = create_consonant_bar_chart()
            st.plotly_chart(fig, use_container_width=True)
            col_a, col_b, col_c = st.columns(3)
            with col_a: st.markdown(f"**🔴 வல்லினம்:** {', '.join(vallinam)}")
            with col_b: st.markdown(f"**🟢 மெல்லினம்:** {', '.join(mellinam)}")
            with col_c: st.markdown(f"**🔵 இடையினம்:** {', '.join(idaiyinam)}")
        elif visualization_type == "🌳 சொல்லமைப்பு மரவடிவமைப்பு":
            st.subheader("🌳 சொல்லமைப்பு மரவடிவமைப்பு (Syntax Tree)")
            fig = create_syntax_sunburst()
            st.plotly_chart(fig, use_container_width=True)
        elif visualization_type == "🔥 விதிகள் வெப்ப வரைபடம்":
            st.subheader("🔥 இலக்கண விதிகள் பயன்பாட்டு வெப்ப வரைபடம்")
            fig = create_grammar_heatmap()
            st.plotly_chart(fig, use_container_width=True)
        elif visualization_type == "📏 சொல் நீளப் பரவல்":
            st.subheader("📏 சொற்களின் நீளப் பரவல்")
            fig = create_word_length_distribution()
            st.plotly_chart(fig, use_container_width=True)
            
    with col2:
        st.markdown("### 📈 புள்ளிவிவரங்கள்")
        stats_data = {"மொத்த விதிகள்": 18, "மெய் எழுத்துகள்": 18, "உயிர் எழுத்துகள்": 12, "உயிர்மெய் எழுத்துகள்": 216, "புணர்ச்சி விதிகள்": "100+"}
        for label, value in stats_data.items(): st.metric(label, value)
        st.divider()
        st.info("🖱️ வரைபடங்களின் மேல் சுட்டியை வைத்து விவரங்களைக் காணலாம்.")

# ==================== 4. முதன்மைப் பக்கத் தட்டுகள் (Main Tabs Layout) ====================

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🧩 மெய்ம்மயக்கம்", "🏁 மொழிமுதல்", "🔚 மொழியிறுதி", "🔗 புணர்ச்சி", "📊 காட்சிப்படுத்துதல்"])

# Tab 1: மெய்ம்மயக்கம்
with tab1:
    st.subheader("மெய்ம்மயக்கம் ஆய்வு")
    col1, col2 = st.columns([2, 2])
    with col1:
        word_m1 = st.text_input("சொல்லை உள்ளிடவும்:", key="m1", placeholder="எ.கா: பக்கம்")
    with col2:
        option1 = st.selectbox('விதியைத் தெரிவுசெய்க ', (
            "மெய்ம்மயக்கம்1 : 'க்+க'", "மெய்ம்மயக்கம்2 : 'ங்+கங'", "மெய்ம்மயக்கம்3 : 'ச்+ச'", "மெய்ம்மயக்கம்4 : 'ஞ்+சஞய'",
            "மெய்ம்மயக்கம்5 : 'ட்+கசடப'", "மெய்ம்மயக்கம்6 : 'ண்+கசஞடணபமயவ'", "மெய்ம்மயக்கம்7 : 'த்+த'", "மெய்ம்மயக்கம்8 : 'ந்+தநய'",
            "மெய்ம்மயக்கம்9 : 'ப்+ப'", "மெய்ம்மயக்கம்10 : 'ம்+பமயவ'", "மெய்ம்மயக்கம்11 : 'ய்+கசதபஞநமயவங'", "மெய்ம்மயக்கம்12 : 'ர்+கசதபஞநமயவங'",
            "மெய்ம்மயக்கம்13 : 'ழ்+கசதபஞநமயவங'", "மெய்ம்மயக்கம்14 : 'வ்+வ'", "மெய்ம்மயக்கம்15 : 'ல்+கசபலயவ'", "மெய்ம்மயக்கம்16 : 'ள்+கசபளயவ'",
            "மெய்ம்மயக்கம்17 : 'ற்+கசபற'", "மெய்ம்மயக்கம்18 : 'ன்+கசஞபமயவறன'"
        ), key="sb_m1")
    
    if st.button("ஆராய்க", key="b1"):
        if word_m1:
            rule_response = rule1(option1, word_m1)
            if rule_response: display_result(rule_response, "மெய்ம்மயக்கம் ஆய்வு முடிவு")
            else: st.error("இந்த விதியுடன் பொருந்தவில்லை. சரியான சொல்லை உள்ளிடவும்.")
        else: st.warning("தயவுசெய்து ஒரு சொல்லை உள்ளிடவும்.")

# Tab 2: மொழிமுதல்
with tab2:
    st.subheader("மொழிமுதல் எழுத்து ஆய்வு") 
    col1, col2 = st.columns([2, 2])
    with col1:
        word_m2 = st.text_input("சொல்லை உள்ளிடவும்:", key="m2", placeholder="எ.கா: கல்வி")
    with col2:
        option2 = st.selectbox('விதியைத் தெரிவுசெய்க ', ("உயிர் வரிசை", "க வரிசை", "ச வரிசை", "ங வரிசை", "த வரிசை", "ந வரிசை", "ப வரிசை", "ம வரிசை", "ய வரிசை", "வ வரிசை"), key="sb_m2")
    
    if st.button("ஆராய்க", key="b2"):
        if word_m2:
            rule_response = word_starting_checker(option2, word_m2)
            if rule_response: display_result(rule_response, "மொழிமுதல் ஆய்வு முடிவு")
            else: st.error("இந்த விதியுடன் பொருந்தவில்லை.")
        else: st.warning("தயவுசெய்து ஒரு சொல்லை உள்ளிடவும்.")

# Tab 3: மொழியிறுதி
with tab3:
    st.subheader("மொழியிறுதி எழுத்து ஆய்வு")
    col1, col2 = st.columns([2, 2])
    with col1:
        word_m3 = st.text_input("சொல்லை உள்ளிடவும்:", key="m3", placeholder="எ.கா: தமிழ்")
    with col2:
        option3 = st.selectbox('விதியைத் தெரிவுசெய்க ', ("உயிர் சரிபார்ப்பு", "மெல்லினம் சரிபார்ப்பு", "இடையினம் சரிபார்ப்பு", "அளபெடை சரிபார்ப்பு", "ஓரெழுத்து ஒருமொழி சரிபார்ப்பு", "சுட்டு சரிபார்ப்பு", "வினா சரிபார்ப்பு"), key="sb_m3")
    
    if st.button("ஆராய்க", key="b3"):
        if word_m3:
            rule_response = word_ending_checker(option3, word_m3)
            if rule_response: display_result(rule_response, "மொழியிறுதி ஆய்வு முடிவு")
            else: st.error("இந்த விதியுடன் பொருந்தவில்லை.")
        else: st.warning("தயவுசெய்து ஒரு சொல்லை உள்ளிடவும்.")

# Tab 4: புணர்ச்சி & தொகைமரபு
with tab4:
    st.subheader("புணர்ச்சி ஆய்வு (Sandhi Analysis)")
    punarchi_option = st.selectbox('எத்தனை சொற்கள் புணரப்படுகின்றன?', ('இரு சொற்கள்', 'மூன்று சொற்கள்'), key="sb1")

    if punarchi_option == 'இரு சொற்கள்':
        c1, c2 = st.columns(2)
        with c1: n_mozhi = st.text_input("நிலைமொழி:", key="n1", placeholder="எ.கா: தட")
        with c2: v_mozhi = st.text_input("வருமொழி:", key="v1", placeholder="எ.கா: தோள்")
        
        if st.button("புணர்க்க", key="b4"):
            if n_mozhi and v_mozhi:
                # முதலில் தனித்தொகை சார்புகளைச் சோதித்தல் (thogai_1 - thogai_8)
                thogai_res = None
                for func in [thogai_1, thogai_2, thogai_3, thogai_4, thogai_5, thogai_6, thogai_7, thogai_8]:
                    try:
                        temp = func(n_mozhi, v_mozhi)
                        if temp: thogai_res = temp; break
                    except Exception: pass
                
                # பொது get() சார்பின் மூலம் சோதனை
                res = get([n_mozhi, v_mozhi])
                formatted_res = punarchi_result_formatter(res)
                
                final_output = formatted_res if formatted_res else thogai_res
                if final_output: display_result(final_output, "புணர்ந்த வடிவம்")
                else: st.info(f"இச்சேர்க்கைக்குப் புணர்ச்சி விதிகள் கண்டறியப்படவில்லை: {n_mozhi} + {v_mozhi}")
            else: st.warning("நிலைமொழி மற்றும் வருமொழியை உள்ளிடவும்.")

    elif punarchi_option == 'மூன்று சொற்கள்':
        c1, c2, c3 = st.columns(3)
        with c1: n_mozhi3 = st.text_input("நிலைமொழி:", key="nilai", placeholder="எ.கா: மரம்")
        with c2: m_mozhi3 = st.text_input("இரண்டாம் நிலைமொழி:", key="nadu", placeholder="எ.கா: அத்து")
        with c3: v_mozhi3 = st.text_input("வருமொழி:", key="varu", placeholder="எ.கா: ஐ")
        
        if st.button("புணர்க்க", key="b5"):
            if n_mozhi3 and m_mozhi3 and v_mozhi3:
                # [முக்கியத் திருத்தம்]: இரு கட்டப் புணர்ச்சி முறை (Two-Stage Formatting)
                # கட்டம் 1: மரம் + அத்து -> மரத்து எனப் புணர்தல்
                stage1 = get([n_mozhi3, m_mozhi3])
                stage1_formatted = punarchi_result_formatter(stage1)
                
                if not stage1_formatted:
                    stage1_formatted = n_mozhi3 + m_mozhi3
                
                # கட்டம் 2: மரத்து + ஐ -> மரத்தை எனப் புணர்தல்
                final_res = get([stage1_formatted, v_mozhi3])
                formatted_res3 = punarchi_result_formatter(final_res)
                
                if formatted_res3: 
                    display_result(formatted_res3, "புணர்ந்த வடிவம்")
                else: 
                    # நூலகத் தர்க்க வழுக்களுக்கான இயல்புத் தமிழ் மாற்றுத் திருத்தம் (Fallback Correction)
                    if stage1_formatted.endswith("து") and v_mozhi3 == "ஐ":
                        root = stage1_formatted.removesuffix("து")
                        fallback_word = root + "த்தை"
                        display_result(fallback_word, "புணர்ந்த வடிவம்")
                    else:
                        st.info(f"புணர்ச்சி வடிவங்கள் கிடைக்கவில்லை: {n_mozhi3} + {m_mozhi3} + {v_mozhi3}")
            else: 
                st.warning("மூன்று சொற்களையும் முறையாக உள்ளிடவும்.")

# Tab 5: காட்சிப்படுத்துதல்
with tab5:
    visualization_tab()

# --- அடிக்குறிப்பு (Footer) ---
st.markdown("""
    <div class="footer">
        <strong>மொழிவல்லுநர்:- முனைவர் சத்தியராசு தங்கச்சாமி (நேயக்கோ)</strong><br>
        <strong>தொழில்நுட்பவல்லுநர்:- சு. பூபாலன், மு. வருண் & குழுவினர்</strong><br>
        <p style="margin-top:5px; color:gray !important;">தொல்காப்பியம் உள்ளிட்ட தமிழ் இலக்கணத் தரவுத் தளம் | 2026</p>
    </div>
    """, unsafe_allow_html=True)
