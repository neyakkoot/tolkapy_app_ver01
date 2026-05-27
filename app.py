import streamlit as st
import importlib.util
import os
import re
from collections import Counter

from tamilrulepy.meymayakkam import meymayakkam1,meymayakkam2,meymayakkam3,meymayakkam4,meymayakkam5,meymayakkam6,meymayakkam7,meymayakkam8,meymayakkam9,meymayakkam10,meymayakkam11,meymayakkam12,meymayakkam13,meymayakkam14,meymayakkam15,meymayakkam16,meymayakkam17,meymayakkam18

from tamilrulepy.mozhimarabu.word_starting import (
    uyirezhuthu_check,
    uyirmei_ka_check,
    uyirmei_ma_check,
    uyirmei_na_check,
    uyirmei_nga_check,
    uyirmei_pa_check,
    uyirmei_sa_check,
    uyirmei_ta_check,
    uyirmei_va_check,
    uyirmei_ya_check,
)

from tamilrulepy.mozhimarabu.word_ending import (
    uyir_check,
    mellinam_check,
    idaiyinam_check,
    alapedai_check,
    oorezhuthoorumozhi_check,
    suttu_check,
    vinaa_check,
)

from tamilrulepy.euphonic import get

# Visualization imports
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np

# 1. பக்க வடிவமைப்பு
st.set_page_config(
    page_title="தொல்காபை ஆய்வி", 
    page_icon="📜",
    layout="wide"
)

hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .block-container {
    padding-top: 0rem;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Mukta+Malar:wght@400;700&display=swap');
      
    /* ஒட்டுமொத்த பின்னணி மற்றும் எழுத்துரு */
    .stApp {
        background: linear-gradient(to bottom, #fdf2f8, #ffffff);
        font-family: 'Anek Tamil', sans-serif;
        font-weight: semibold;
    }

    /* தலைப்புப் பகுதி */
    .main-title-container {
        background: linear-gradient(135deg, #ec4899 0%, #be185d 100%);
        color: white !important;
        padding: 40px 30px;
        border-radius: 50px 50px 50px 50px;
        text-align: center;
        margin: 20px -20px 50px -20px;
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
    
    .thol-image:hover {
        transform: scale(1.05);
    }

    /* Tabs ஸ்டைல் */
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

    /* All text elements to black */
    .stMarkdown, .stMarkdown p, .stMarkdown div, .stMarkdown span {
        color: black !important;
    }
            
    .stMarkdown h3 {
        color: black !important;
    }
    
    /* Subheader styling */
    h2, h3, h4, h5, h6 {
        color: black !important;
    }
    
    /* Text input labels */
    label, .stTextInput label {
        color: black !important;
    }
    
    /* Selectbox labels */
    .stSelectbox label {
        color: black !important;
    }
    
    /* இன்புட் மற்றும் பட்டன் வடிவமைப்பு */
    div.stButton > button {
        background: linear-gradient(135deg, #ec4899 0%, #be185d 100%);
        color: white;
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
    
    /* Center align button */
    div.stButton {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* கார்டு வடிவமைப்பு */
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
        border-radius: 30px 30px 0 0;
        margin-top: 60px;
        color: black !important;
        border-top: 1px solid #fce7f3;
    }
    
    /* Visualization specific styles */
    .vis-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
        color: white;
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
    """, unsafe_allow_html=True)

# --- தலைப்பு மற்றும் படம் (GitHub Raw Link) ---
image_url = "https://raw.githubusercontent.com/neyakkoot/tolkapy-web-app/main/images/%E0%AE%A4%E0%AF%8A%E0%AE%B2%E0%AF%8D%E0%AE%95%E0%AE%BE%E0%AE%AA%E0%AF%8D%E0%AE%AA%E0%AE%BF%E0%AE%AF%E0%AE%B0%E0%AF%8D.jpg"

st.markdown(f"""
    <div class="main-title-container">
        <img src="{image_url}" class="thol-image">
        <h1 style="margin: 0; font-size: 2.5rem; color: #FFFFFF">📜 தொல்காபை ஆய்வி</h1>
        <p style="opacity: 0.9; font-size: 1.1rem; color:#FFFFFF !important;">Tolkapy Grammar Analysis Tool</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== HELPER FUNCTIONS ====================

def rule1(option, word_m):
    all_rules = {
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
    return all_rules[option](word_m)

def word_starting_checker(option, word):
    all_rules = {
        "உயிர் வரிசை": uyirezhuthu_check,
        "க வரிசை": uyirmei_ka_check,
        "ச வரிசை": uyirmei_sa_check,
        "ஞ வரிசை": uyirmei_nga_check,
        "த வரிசை": uyirmei_ta_check,
        "ந வரிசை": uyirmei_na_check,
        "ப வரிசை": uyirmei_pa_check,
        "ம வரிசை": uyirmei_ma_check,
        "ய வரிசை": uyirmei_ya_check,
        "வ வரிசை": uyirmei_va_check
    }
    return all_rules[option](word)

def word_ending_checker(option, word):
    all_rules = {
        "உயிர் சரிபார்ப்பு": uyir_check,
        "மெல்லினம் சரிபார்ப்பு": mellinam_check,
        "இடையினம் சரிபார்ப்பு": idaiyinam_check,
        "அளபெடை சரிபார்ப்பு": alapedai_check,
        "ஓரெழுத்து ஒருமொழி சரிபார்ப்பு": oorezhuthoorumozhi_check,
        "சுட்டு சரிபார்ப்பு": suttu_check,
        "வினா சரிபார்ப்பு": vinaa_check,
    }
    return all_rules[option](word)

def punarchi_result_formatter(res):
    if res:
        return res[0][0]
    return None

def display_result(res, title="ஆய்வு முடிவு"):
    if res:
        st.markdown(f"""<div class="result-card"><strong>{title}:</strong><br>{res}</div>""", unsafe_allow_html=True)

# ==================== VISUALIZATION FUNCTIONS ====================

def create_frequency_histogram(text_input=None):
    """Create frequency histogram for Tamil letters"""
    if not text_input:
        text_input = "தொல்காப்பியம் பொருளதிகாரம் மெய்ப்பாட்டியல் எழுத்ததிகாரம் சொல்லதிகாரம்"
    
    # Extract Tamil characters
    tamil_chars = re.findall(r'[\u0B80-\u0BFF]', text_input)
    
    if not tamil_chars:
        tamil_chars = ['த', 'ொ', 'ல', '்', 'க', 'ா', 'ப்', 'ப', 'ி', 'ய', 'ம்']
    
    char_counts = Counter(tamil_chars)
    top_chars = dict(sorted(char_counts.items(), key=lambda x: x[1], reverse=True)[:15])
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(top_chars.keys()),
            y=list(top_chars.values()),
            marker_color='#ec4899',
            marker_line_color='#be185d',
            marker_line_width=1.5,
            text=list(top_chars.values()),
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>அதிர்வெண்: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title={
            'text': 'தமிழ் எழுத்துகளின் அதிர்வெண் வரைபடம்<br><span style="font-size:14px">Tamil Letter Frequency Histogram</span>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18}
        },
        xaxis_title='எழுத்துகள் (Letters)',
        yaxis_title='அதிர்வெண் (Frequency)',
        template='plotly_white',
        height=500,
        hoverlabel={'bgcolor': 'white', 'font_size': 14}
    )
    
    return fig

def create_consonant_bar_chart():
    """Create bar chart for consonant classification"""
    categories = ['வல்லினம்\n(Hard)', 'மெல்லினம்\n(Soft)', 'இடையினம்\n(Medium)']
    counts = [6, 6, 6]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    # List of consonants in each category
    vallinam = ['க்', 'ச்', 'ட்', 'த்', 'ப்', 'ற்']
    mellinam = ['ங்', 'ஞ்', 'ண்', 'ந்', 'ம்', 'ன்']
    idaiyinam = ['ய்', 'ர்', 'ல்', 'வ்', 'ழ்', 'ள்']
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=counts,
            marker_color=colors,
            text=counts,
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>எழுத்துகள்: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title='தமிழ் மெய்யெழுத்துகள் வகைப்பாடு<br><span style="font-size:14px">Tamil Consonant Classification</span>',
        xaxis_title='எழுத்து வகைகள் (Consonant Types)',
        yaxis_title='எண்ணிக்கை (Count)',
        template='plotly_white',
        height=450
    )
    
    return fig, vallinam, mellinam, idaiyinam

def create_syntax_sunburst():
    """Create sunburst chart for Tamil word structure"""
    tree_data = {
        'name': 'சொல் (Word)',
        'children': [
            {
                'name': 'முதல் எழுத்து<br>(First Letter)',
                'children': [
                    {'name': 'மெய்<br>(Consonant)'},
                    {'name': 'உயிர்<br>(Vowel)'}
                ]
            },
            {
                'name': 'இடை எழுத்துகள்<br>(Middle Letters)',
                'children': [
                    {'name': 'மெய்<br>(Consonant)'},
                    {'name': 'உயிர்<br>(Vowel)'},
                    {'name': 'உயிர்மெய்<br>(C+Vowel)'}
                ]
            },
            {
                'name': 'இறுதி எழுத்து<br>(Last Letter)',
                'children': [
                    {'name': 'மெய்<br>(Consonant)'},
                    {'name': 'உயிர்<br>(Vowel)'},
                    {'name': 'ஆய்தம்<br>(Aytham)'}
                ]
            }
        ]
    }
    
    labels = []
    parents = []
    values = []
    
    def add_nodes(data, parent):
        labels.append(data['name'])
        parents.append(parent)
        values.append(10 if parent == '' else 5)
        if 'children' in data:
            for child in data['children']:
                add_nodes(child, data['name'])
    
    add_nodes(tree_data, '')
    
    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        branchvalues='total',
        marker=dict(colors=['#ec4899', '#f472b6', '#f9a8d4', '#fbcfe8', '#fce7f3']),
        hovertemplate='<b>%{label}</b><br><extra></extra>'
    ))
    
    fig.update_layout(
        title='சொல்லமைப்பு மரவடிவமைப்பு<br><span style="font-size:14px">Word Structure Syntax Tree</span>',
        height=550,
        showlegend=False
    )
    
    return fig

def create_grammar_heatmap():
    """Create heatmap for grammar rules"""
    rule_categories = ['எழுத்து', 'சொல்', 'பொருள்', 'யாப்பு', 'அணி']
    sub_categories = ['மெய்ம்மயக்கம்', 'புணர்ச்சி', 'வேற்றுமை', 'தொகை', 'உருபு']
    
    # Sample data
    np.random.seed(42)
    data_matrix = np.random.randint(1, 100, size=(len(rule_categories), len(sub_categories)))
    
    fig = go.Figure(data=go.Heatmap(
        z=data_matrix,
        x=sub_categories,
        y=rule_categories,
        colorscale='Viridis',
        text=data_matrix,
        texttemplate='%{text}',
        textfont={"size": 12},
        hoverongaps=False,
        hovertemplate='<b>%{y}</b> - <b>%{x}</b><br>மதிப்பு: %{z}<extra></extra>'
    ))
    
    fig.update_layout(
        title='இலக்கண விதிகள் பயன்பாட்டு வெப்ப வரைபடம்<br><span style="font-size:14px">Grammar Rules Application Heatmap</span>',
        xaxis_title='விதி வகைகள் (Rule Types)',
        yaxis_title='இலக்கணப் பிரிவுகள் (Grammar Sections)',
        height=500,
        template='plotly_white'
    )
    
    return fig

def create_word_length_distribution():
    """Create distribution chart for word lengths"""
    sample_words = ['தொல்காப்பியம்', 'எழுத்து', 'சொல்', 'பொருள்', 'மெய்ப்பாடு', 
                    'இலக்கணம்', 'நூல்', 'உரை', 'விளக்கம்', 'ஆய்வு']
    lengths = [len(w) for w in sample_words]
    
    fig = go.Figure(data=[
        go.Histogram(
            x=lengths,
            marker_color='#ec4899',
            opacity=0.7,
            hovertemplate='சொல் நீளம்: %{x}<br>எண்ணிக்கை: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title='சொற்களின் நீளப் பரவல்<br><span style="font-size:14px">Word Length Distribution</span>',
        xaxis_title='எழுத்துகளின் எண்ணிக்கை (Number of Letters)',
        yaxis_title='சொற்களின் எண்ணிக்கை (Number of Words)',
        template='plotly_white',
        height=450
    )
    
    return fig

# ==================== VISUALIZATION TAB ====================

def visualization_tab():
    """Main visualization tab content"""
    
    st.markdown("""
    <div class="vis-header">
        <h1>📊 தொல்காப்பிய இலக்கணக் காட்சிப்படுத்தல்</h1>
        <p>Tolkappiyam Grammar Visualization | Interactive Learning Tool</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar controls
    with st.sidebar:
        st.markdown("### 🎛️ காட்சி அமைப்புகள்")
        
        visualization_type = st.selectbox(
            "காட்சி வகையைத் தேர்ந்தெடுக்கவும்",
            [
                "📊 அதிர்வெண் வரைபடம்",
                "📊 மெய்யெழுத்துகள் வகைப்பாடு",
                "🌳 சொல்லமைப்பு மரவடிவமைப்பு",
                "🔥 விதிகள் வெப்ப வரைபடம்",
                "📏 சொல் நீளப் பரவல்"
            ]
        )
        
        st.divider()
        
        st.markdown("""
        <div class="vis-info-box">
            <strong>📚 கல்விக் குறிப்பு:</strong><br>
            இக்காட்சிகள் தொல்காப்பிய இலக்கண விதிகளைப் புரிந்துகொள்ள உதவும் வகையில் 
            வடிவமைக்கப்பட்டுள்ளன. ஒவ்வொரு வரைபடமும் தமிழ் மொழியின் 
            ஒலியியல், சொல்லமைப்பு அம்சங்களை எளிதாகப் புரிந்துகொள்ள உதவுகிறது.
        </div>
        """, unsafe_allow_html=True)
        
        # Custom text input for frequency analysis
        custom_text = st.text_area(
            "✍️ சொந்தப் பகுப்பாய்வுக்குத் தமிழ்ச் சொற்றொடரை உள்ளிடுக:", 
            placeholder="எ.கா: தொல்காப்பியர் தமிழ் இலக்கணத்தை எழுதினார்",
            height=100
        )
    
    # Main content
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if visualization_type == "📊 அதிர்வெண் வரைபடம்":
            st.subheader("📊 தமிழ் எழுத்துகள் அதிர்வெண் பகுப்பாய்வு")
            if custom_text:
                fig = create_frequency_histogram(custom_text)
            else:
                fig = create_frequency_histogram()
            st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("📖 விளக்கம்"):
                st.markdown("""
                இந்த வரைபடம் தமிழ் எழுத்துகளின் பயன்பாட்டு அதிர்வெண்ணைக் காட்டுகிறது.
                - **x-அச்சு**: தமிழ் எழுத்துகள்
                - **y-அச்சு**: அதிர்வெண் (எத்தனை முறை வருகிறது)
                - **குறிப்பு**: அதிக அதிர்வெண் உள்ள எழுத்துகள் தமிழில் அதிகம் பயன்படுபவை
                """)
        
        elif visualization_type == "📊 மெய்யெழுத்துகள் வகைப்பாடு":
            st.subheader("📊 தமிழ் மெய்யெழுத்துகள் வகைப்பாடு")
            fig, vallinam, mellinam, idaiyinam = create_consonant_bar_chart()
            st.plotly_chart(fig, use_container_width=True)
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.markdown("**🔴 வல்லினம் (Hard)**")
                st.write(", ".join(vallinam))
            with col_b:
                st.markdown("**🟢 மெல்லினம் (Soft)**")
                st.write(", ".join(mellinam))
            with col_c:
                st.markdown("**🔵 இடையினம் (Medium)**")
                st.write(", ".join(idaiyinam))
            
            with st.expander("📖 விளக்கம்"):
                st.markdown("""
                **வண்ணக் குறியீடுகள்:**
                - 🔴 **சிவப்பு**: வல்லினம் (Hard Consonants) - க், ச், ட், த், ப், ற்
                - 🟢 **பச்சை**: மெல்லினம் (Soft Consonants) - ங், ஞ், ண், ந், ம், ன்
                - 🔵 **நீலம்**: இடையினம் (Medium Consonants) - ய், ர், ல், வ், ழ், ள்
                
                **மொத்த மெய்யெழுத்துகள்:** 18
                """)
        
        elif visualization_type == "🌳 சொல்லமைப்பு மரவடிவமைப்பு":
            st.subheader("🌳 சொல்லமைப்பு மரவடிவமைப்பு (Syntax Tree)")
            fig = create_syntax_sunburst()
            st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("📖 விளக்கம்"):
                st.markdown("""
                **சொல்லமைப்பு மரம் (Sunburst Chart):**
                
                இந்த வரைபடம் ஒரு சொல்லின் உள் அமைப்பை விளக்குகிறது:
                - **மையம்**: மொத்தச் சொல்
                - **முதல் வளையம்**: முதல், இடை, இறுதி எழுத்துகள்
                - **வெளிவளையம்**: ஒவ்வொரு எழுத்தின் வகை (உயிர்/மெய்/உயிர்மெய்)
                
                *குறிப்பு: இது பொதுவான கட்டமைப்பைக் காட்டுகிறது*
                """)
        
        elif visualization_type == "🔥 விதிகள் வெப்ப வரைபடம்":
            st.subheader("🔥 இலக்கண விதிகள் பயன்பாட்டு வெப்ப வரைபடம்")
            fig = create_grammar_heatmap()
            st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("📖 விளக்கம்"):
                st.markdown("""
                **வெப்ப வரைபடம் (Heatmap) விளக்கம்:**
                
                - **x-அச்சு**: விதி வகைகள் (மெய்ம்மயக்கம், புணர்ச்சி, வேற்றுமை, தொகை, உருபு)
                - **y-அச்சு**: இலக்கணப் பிரிவுகள் (எழுத்து, சொல், பொருள், யாப்பு, அணி)
                - **வண்ணம்**: அடர் நிறம் = அதிக பயன்பாடு
                
                *இது மாதிரித் தரவுகளை அடிப்படையாகக் கொண்டது*
                """)
        
        elif visualization_type == "📏 சொல் நீளப் பரவல்":
            st.subheader("📏 சொற்களின் நீளப் பரவல்")
            fig = create_word_length_distribution()
            st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("📖 விளக்கம்"):
                st.markdown("""
                **சொல் நீளப் பரவல் (Word Length Distribution):**
                
                இந்த வரைபடம் தமிழ்ச் சொற்களின் எழுத்துகளின் எண்ணிக்கையைக் காட்டுகிறது.
                - **x-அச்சு**: ஒரு சொல்லில் உள்ள எழுத்துகளின் எண்ணிக்கை
                - **y-அச்சு**: அந்த நீளத்தில் உள்ள சொற்களின் எண்ணிக்கை
                """)
    
    with col2:
        st.markdown("### 📈 புள்ளிவிவரங்கள்")
        
        stats_data = {
            "மொத்த விதிகள்": 18,
            "மெய் எழுத்துகள்": 18,
            "உயிர் எழுத்துகள்": 12,
            "உயிர்மெய் எழுத்துகள்": 216,
            "புணர்ச்சி விதிகள்": "100+"
        }
        
        for label, value in stats_data.items():
            st.metric(label, value)
        
        st.divider()
        
        st.markdown("### 💡 விரைவுக் குறிப்புகள்")
        tips = [
            "🖱️ வரைபடங்களின் மேல் சுட்டியை வைத்து விவரங்களைக் காணலாம்",
            "📊 அதிர்வெண் வரைபடத்தில் சொந்த உரையைப் பகுப்பாய்வு செய்யலாம்",
            "📈 ஒவ்வொரு வரைபடமும் ஊடாடும் தன்மை கொண்டது",
            "🔄 வெவ்வேறு காட்சிகளை மாற்றிப் பார்க்கலாம்"
        ]
        
        for tip in tips:
            st.info(tip)

# ==================== MAIN TABS ====================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🧩 மெய்ம்மயக்கம்", 
    "🏁 மொழிமுதல்", 
    "🔚 மொழியிறுதி", 
    "🔗 புணர்ச்சி",
    "📊 காட்சிப்படுத்துதல்"
])

# Tab 1: மெய்ம்மயக்கம்
with tab1:
    st.subheader("மெய்ம்மயக்கம் ஆய்வு")
    col1, col2 = st.columns([2, 2])
    with col1:
        word_m = st.text_input("சொல்லை உள்ளிடவும்:", key="m1", placeholder="எ.கா: கற்க")
    
    with col2:
        option = st.selectbox('விதியைத் தெரிவுசெய்க ', (
            "மெய்ம்மயக்கம்1 : 'க்+க'",
            "மெய்ம்மயக்கம்2 : 'ங்+கங'",
            "மெய்ம்மயக்கம்3 : 'ச்+ச'",
            "மெய்ம்மயக்கம்4 : 'ஞ்+சஞய'",
            "மெய்ம்மயக்கம்5 : 'ட்+கசடப'",
            "மெய்ம்மயக்கம்6 : 'ண்+கசஞடணபமயவ'",
            "மெய்ம்மயக்கம்7 : 'த்+த'",
            "மெய்ம்மயக்கம்8 : 'ந்+தநய'",
            "மெய்ம்மயக்கம்9 : 'ப்+ப'", 
            "மெய்ம்மயக்கம்10 : 'ம்+பமயவ'",
            "மெய்ம்மயக்கம்11 : 'ய்+கசதபஞநமயவங'",
            "மெய்ம்மயக்கம்12 : 'ர்+கசதபஞநமயவங'",
            "மெய்ம்மயக்கம்13 : 'ழ்+கசதபஞநமயவங'",
            "மெய்ம்மயக்கம்14 : 'வ்+வ'",
            "மெய்ம்மயக்கம்15 : 'ல்+கசபலயவ'",
            "மெய்ம்மயக்கம்16 : 'ள்+கசபளயவ'",
            "மெய்ம்மயக்கம்17 : 'ற்+கசபற'",
            "மெய்ம்மயக்கம்18 : 'ன்+கசஞபமயவறன'", 
        ))
    
    st.write("##")
    btn1 = st.button("ஆராய்க", key="b1")
        
    if btn1:
        rule_responce = rule1(option, word_m)
        if rule_responce:
            display_result(rule_responce)
        else:
            st.error("இந்த விதியுடன் பொருந்தவில்லை. சரியான சொல்லை உள்ளிடவும்.")

# Tab 2: மொழிமுதல்
with tab2:
    st.subheader("மொழிமுதல் எழுத்து ஆய்வு") 
   
    col1, col2 = st.columns([2, 2])
    with col1:
        word_m = st.text_input("சொல்லை உள்ளிடவும்:", key="m2", placeholder="எ.கா: கற்க")
    
    with col2:
        option = st.selectbox('விதியைத் தெரிவுசெய்க ', (
            "உயிர் வரிசை",
            "க வரிசை",
            "ச வரிசை",
            "ஞ வரிசை",
            "த வரிசை",
            "ந வரிசை",
            "ப வரிசை",
            "ம வரிசை",
            "ய வரிசை",
            "வ வரிசை"  
        ))
    
    st.write("##")
    btn1 = st.button("ஆராய்க", key="b2")
        
    if btn1:
        rule_responce = word_starting_checker(option, word_m)
        if rule_responce:
            display_result(rule_responce)
        else:
            st.error("இந்த விதியுடன் பொருந்தவில்லை. சரியான சொல்லை உள்ளிடவும்.")

# Tab 3: மொழியிறுதி
with tab3:
    st.subheader("மொழியிறுதி எழுத்து ஆய்வு")

    col1, col2 = st.columns([2, 2])
    with col1:
        word_m = st.text_input("சொல்லை உள்ளிடவும்:", key="m3", placeholder="எ.கா: கற்க")
    
    with col2:
        option = st.selectbox('விதியைத் தெரிவுசெய்க ', (
            "உயிர் சரிபார்ப்பு",
            "மெல்லினம் சரிபார்ப்பு",
            "இடையினம் சரிபார்ப்பு",
            "அளபெடை சரிபார்ப்பு",
            "ஓரெழுத்து ஒருமொழி சரிபார்ப்பு",
            "சுட்டு சரிபார்ப்பு",
            "வினா சரிபார்ப்பு",
        ))
    
    st.write("##")
    btn1 = st.button("ஆராய்க", key="b3")
        
    if btn1:
        if word_ending_checker:
            rule_responce = word_ending_checker(option, word_m)
            if rule_responce:
                display_result(rule_responce)
            else:
                st.error("இந்த விதியுடன் பொருந்தவில்லை. சரியான சொல்லை உள்ளிடவும்.")
        else:
            st.warning("மொழியிறுதி ஆய்வுச் செயல்பாடு இன்னும் இணைக்கப்படவில்லை.")

# Tab 4: புணர்ச்சி
with tab4:
    st.subheader("புணர்ச்சி ஆய்வு (Sandhi Analysis)")

    option = st.selectbox('எத்தனை சொற்கள் புணரப்படுகின்றன?', ('இரு சொற்கள்', 'மூன்று சொற்கள்'), key="sb1")

    if option == 'இரு சொற்கள்':
        c1, c2 = st.columns(2)
        with c1:
            n_mozhi = st.text_input("நிலைமொழி:", key="n1", placeholder="எ.கா: பனை")
        with c2:
            v_mozhi = st.text_input("வருமொழி:", key="v1", placeholder="எ.கா: காய்")
        
        if st.button("புணர்க்க", key="b4"):
            if get:
                res = get([n_mozhi, v_mozhi])
                res = punarchi_result_formatter(res)
                display_result(res, "புணர்ந்த வடிவம்")
            else:
                st.info(f"விதிகள் கிடைக்கவில்லை: {n_mozhi} + {v_mozhi}")

    elif option == 'மூன்று சொற்கள்':
        c1, c2, c3 = st.columns(3)
        with c1:
            n_mozhi = st.text_input("நிலைமொழி:", key="nilai", placeholder="எ.கா: பனை")
        with c2:
            m_mozhi = st.text_input("இரண்டாம் நிலைமொழி:", key="nadu", placeholder="எ.கா: காய்")
        with c3:
            v_mozhi = st.text_input("வருமொழி:", key="varu", placeholder="எ.கா: பழம்")
        
        if st.button("புணர்க்க", key="b5"):
            if get:
                res1 = get([n_mozhi, m_mozhi, v_mozhi])
                res1 = punarchi_result_formatter(res1)
                if res1:
                    display_result(res1, "புணர்ந்த வடிவம்")
            else:
                st.info(f"விதிகள் கிடைக்கவில்லை: {n_mozhi} + {m_mozhi} + {v_mozhi}")

# Tab 5: காட்சிப்படுத்துதல்
with tab5:
    visualization_tab()

# --- அடிக்குறிப்பு ---
st.markdown("""
    <div class="footer">
        <strong>மொழிவல்லுநர்:- முனைவர் சத்தியராசு தங்கச்சாமி</strong><br>
        <strong>தொழில்நுட்பவல்லுநர்:-  சு. பூபாலன், மு. வருண் & குழுவினர்</strong><br>
        <p style="margin-top:5px;">தொல்காப்பியம் உள்ளிட்ட தமிழ் இலக்கணத் தரவுத் தளம் | 2026</p>
    </div>
    """, unsafe_allow_html=True)
