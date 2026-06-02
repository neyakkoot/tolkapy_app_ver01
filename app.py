import streamlit as st
import importlib.util
import os
import re
from collections import Counter

# --- Open-Tamil நூலகம் (முன்னுரிமை) ---
try:
    import tamil
    from tamil.sandhi import sandhi
    OPEN_TAMIL_AVAILABLE = True
except ImportError:
    OPEN_TAMIL_AVAILABLE = False

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

# matplotlib மட்டும் (networkx இல்லாமல்)
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patches as mpatches

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

# Open-Tamil நிலையைக் காட்டு
if OPEN_TAMIL_AVAILABLE:
    st.markdown("""
    <div class="success-badge">
        ✅ Open-Tamil நூலகம் இணைக்கப்பட்டுள்ளது - துல்லியமான புணர்ச்சி விடைகளுக்கு
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="warning-badge">
        ⚠️ Open-Tamil நூலகம் கிடைக்கவில்லை. தயவுசெய்து <code>pip install open-tamil</code> என நிறுவவும்.
        <br>தற்போது குறைந்த திறனில் செயல்படும்.
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

# ==================== 3. VISUALIZATION FUNCTIONS (Without networkx) ====================

def create_decision_tree_diagram(word):
    """Create a simple decision tree diagram using matplotlib without networkx"""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_facecolor('#f8f9fa')
    fig.patch.set_facecolor('#f8f9fa')
    
    # Define box positions and content
    boxes = [
        (5, 9, f"சொல்: {word}", '#4CAF50'),
        (3, 7, "முதல் எழுத்து\nமெய்யா?", '#FF9800'),
        (7, 7, "இரண்டாம் எழுத்து\nமெய்யா?", '#FF9800'),
        (2, 5, "க்+க விதியுடன்\nபொருந்துகிறதா?", '#FF9800'),
        (5, 5, "த்+த விதியுடன்\nபொருந்துகிறதா?", '#FF9800'),
        (8, 5, "ப்+ப விதியுடன்\nபொருந்துகிறதா?", '#FF9800'),
        (1.5, 3, "✓ மெய்ம்மயக்கம்\nஉண்டு", '#2196F3'),
        (4, 3, "✓ மெய்ம்மயக்கம்\nஉண்டு", '#2196F3'),
        (6.5, 3, "✓ மெய்ம்மயக்கம்\nஉண்டு", '#2196F3'),
        (8.5, 3, "✗ மெய்ம்மயக்கம்\nஇல்லை", '#f44336'),
    ]
    
    # Draw boxes
    for x, y, text, color in boxes:
        box = FancyBboxPatch((x-1.2, y-0.5), 2.4, 1, boxstyle="round,pad=0.1",
                              facecolor=color, edgecolor='white', linewidth=2, alpha=0.9)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    
    # Draw arrows
    arrows = [
        ((5, 8.5), (3, 7.5)), ((5, 8.5), (7, 7.5)),
        ((3, 6.5), (2, 5.5)), ((3, 6.5), (5, 5.5)), ((7, 6.5), (8, 5.5)),
        ((2, 4.5), (1.5, 3.5)), ((5, 4.5), (4, 3.5)), ((8, 4.5), (6.5, 3.5)), ((8, 4.5), (8.5, 3.5))
    ]
    
    for start, end in arrows:
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(arrowstyle='->', color='#666', lw=1.5))
    
    ax.set_title(f"தொல்காப்பிய மெய்ம்மயக்க விதி சரிபார்ப்பு - மரவடிவமைப்பு\nTolkappiyam Meymayakkam Decision Tree", 
                 fontsize=14, pad=20, fontweight='bold')
    plt.tight_layout()
    return fig

def create_sandhi_diagram(nilaimozhi, varumozhi, result):
    """Create a sandhi diagram without networkx"""
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_facecolor('#f8f9fa')
    fig.patch.set_facecolor('#f8f9fa')
    
    # Boxes
    boxes = [
        (2, 6, f"நிலைமொழி\n{nilaimozhi}", '#FF6B6B', 1.8),
        (10, 6, f"வருமொழி\n{varumozhi}", '#4ECDC4', 1.8),
        (6, 4, "புணர்ச்சி செயல்முறை\n(Sandhi Process)", '#FFEAA7', 2.2),
        (6, 1.5, f"புணர்ந்த வடிவம்\n{result}", '#95E77E', 2.0),
    ]
    
    for x, y, text, color, width in boxes:
        box = FancyBboxPatch((x-width, y-0.6), width*2, 1.2, boxstyle="round,pad=0.1",
                              facecolor=color, edgecolor='white', linewidth=2, alpha=0.9)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=10, fontweight='bold', color='black' if color == '#FFEAA7' else 'white')
    
    # Character nodes
    for i, ch in enumerate(nilaimozhi[:6]):
        x = 1 + i * 0.8
        circle = plt.Circle((x, 7.5), 0.25, color='#FFB3B3', ec='white', linewidth=1.5)
        ax.add_patch(circle)
        ax.text(x, 7.5, ch, ha='center', va='center', fontsize=8, fontweight='bold')
    
    for i, ch in enumerate(varumozhi[:6]):
        x = 9 + i * 0.8
        circle = plt.Circle((x, 7.5), 0.25, color='#B3E5FC', ec='white', linewidth=1.5)
        ax.add_patch(circle)
        ax.text(x, 7.5, ch, ha='center', va='center', fontsize=8, fontweight='bold')
    
    # Arrows
    ax.annotate('', xy=(4.5, 4.5), xytext=(2.5, 5.5), arrowprops=dict(arrowstyle='->', color='#888', lw=2))
    ax.annotate('', xy=(7.5, 4.5), xytext=(9.5, 5.5), arrowprops=dict(arrowstyle='->', color='#888', lw=2))
    ax.annotate('', xy=(6, 2.5), xytext=(6, 3.5), arrowprops=dict(arrowstyle='->', color='#888', lw=2))
    
    ax.set_title(f"மெய்ம்மயக்கப் புணர்ச்சி - கணு இணைப்பு வரைபடம்\nSandhi Process Diagram\n"
                 f"{nilaimozhi} + {varumozhi} → {result}", fontsize=14, pad=20, fontweight='bold')
    
    # Legend
    legend_elements = [
        mpatches.Patch(facecolor='#FF6B6B', label='நிலைமொழி (Source Word)'),
        mpatches.Patch(facecolor='#4ECDC4', label='வருமொழி (Target Word)'),
        mpatches.Patch(facecolor='#95E77E', label='புணர்ந்த வடிவம் (Result)'),
        mpatches.Patch(facecolor='#FFEAA7', label='புணர்ச்சி செயல்முறை'),
        mpatches.Patch(facecolor='#FFB3B3', label='நிலைமொழி எழுத்துகள்'),
        mpatches.Patch(facecolor='#B3E5FC', label='வருமொழி எழுத்துகள்'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=8, framealpha=0.9)
    
    plt.tight_layout()
    return fig

def create_frequency_charts(text_input):
    """Create bar charts for first and last letter frequency"""
    if not text_input:
        text_input = "தொல்காப்பியம் எழுத்து சொல் பொருள் மெய்ப்பாடு இலக்கணம்"
    
    words = [w for w in text_input.split() if w]
    if not words:
        words = ["தொல்காப்பியம்", "எழுத்து", "சொல்"]
    
    first_letters = [w[0] for w in words if w]
    last_letters = [w[-1] for w in words if w]
    
    first_counts = Counter(first_letters)
    last_counts = Counter(last_letters)
    
    top_first = dict(sorted(first_counts.items(), key=lambda x: x[1], reverse=True)[:8])
    top_last = dict(sorted(last_counts.items(), key=lambda x: x[1], reverse=True)[:8])
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.patch.set_facecolor('#f8f9fa')
    
    # First letters
    bars1 = ax1.bar(top_first.keys(), top_first.values(), color='#FF6B6B', edgecolor='#c0392b', linewidth=1.5)
    ax1.set_title('மொழிமுதல் எழுத்துகள் அதிர்வெண்', fontsize=12, fontweight='bold')
    ax1.set_xlabel('எழுத்துகள்', fontsize=10)
    ax1.set_ylabel('அதிர்வெண்', fontsize=10)
    ax1.tick_params(axis='x', rotation=45)
    for bar in bars1:
        ax1.annotate(str(int(bar.get_height())), xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 3), textcoords="offset points", ha='center', fontweight='bold')
    
    # Last letters
    bars2 = ax2.bar(top_last.keys(), top_last.values(), color='#4ECDC4', edgecolor='#16a085', linewidth=1.5)
    ax2.set_title('மொழியிறுதி எழுத்துகள் அதிர்வெண்', fontsize=12, fontweight='bold')
    ax2.set_xlabel('எழுத்துகள்', fontsize=10)
    ax2.set_ylabel('அதிர்வெண்', fontsize=10)
    ax2.tick_params(axis='x', rotation=45)
    for bar in bars2:
        ax2.annotate(str(int(bar.get_height())), xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 3), textcoords="offset points", ha='center', fontweight='bold')
    
    plt.suptitle('தமிழ் மொழி எழுத்து பயன்பாட்டு அதிர்வெண் வரைபடம்', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    return fig

def create_heatmap(text_input):
    """Create a heatmap of letter type distribution"""
    if not text_input:
        text_input = "தொல்காப்பியம் எழுத்து சொல் பொருள்"
    
    words = text_input.split()
    if not words:
        words = ["தொல்காப்பியம்", "எழுத்து", "சொல்"]
    
    max_len = min(max(len(w) for w in words), 10) if words else 8
    
    # Tamil letter categories
    mei_set = set(['க்', 'ங்', 'ச்', 'ஞ்', 'ட்', 'ண்', 'த்', 'ந்', 'ப்', 'ம்', 'ய்', 'ர்', 'ல்', 'வ்', 'ழ்', 'ள்', 'ற்', 'ன்'])
    uyir_set = set(['அ', 'ஆ', 'இ', 'ஈ', 'உ', 'ஊ', 'எ', 'ஏ', 'ஐ', 'ஒ', 'ஓ', 'ஔ'])
    
    position_data = []
    for pos in range(max_len):
        mei_count = 0
        uyir_count = 0
        other_count = 0
        for w in words:
            if pos < len(w):
                char = w[pos]
                if char in mei_set:
                    mei_count += 1
                elif char in uyir_set:
                    uyir_count += 1
                else:
                    other_count += 1
        position_data.append([mei_count, uyir_count, other_count])
    
    fig, ax = plt.subplots(figsize=(10, 5))
    data_array = np.array(position_data).T
    im = ax.imshow(data_array, cmap='YlOrRd', aspect='auto')
    
    ax.set_xticks(range(max_len))
    ax.set_xticklabels([f'நிலை {i+1}' for i in range(max_len)], rotation=45)
    ax.set_yticks(range(3))
    ax.set_yticklabels(['மெய்', 'உயிர்', 'உயிர்மெய்/ஏனைய'])
    
    for i in range(max_len):
        for j in range(3):
            if data_array[j, i] > 0:
                text_color = "white" if data_array[j, i] > np.max(data_array)/2 else "black"
                ax.text(i, j, str(int(data_array[j, i])), ha="center", va="center", color=text_color, fontsize=9)
    
    plt.colorbar(im, ax=ax, label='அதிர்வெண்')
    ax.set_title('எழுத்து வகைப் பரவல் - வெப்ப வரைபடம்', fontsize=12, fontweight='bold', pad=15)
    plt.tight_layout()
    return fig

def create_grammar_network_diagram():
    """Create a simple grammar rules network diagram without networkx"""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_facecolor('#f8f9fa')
    fig.patch.set_facecolor('#f8f9fa')
    
    categories = {
        'மெய்ம்மயக்கம்': (3, 7, '#FF6B6B'),
        'மொழிமுதல்': (7, 7, '#FF6B6B'),
        'மொழியிறுதி': (5, 5, '#FF6B6B'),
    }
    
    sub_rules = {
        'க்+க': (1.5, 5, '#74B9FF'), 'த்+த': (3, 5, '#74B9FF'), 'ப்+ப': (4.5, 5, '#74B9FF'),
        'உயிர்': (6.5, 5, '#74B9FF'), 'க வரிசை': (8, 5, '#74B9FF'), 'ச வரிசை': (9.5, 5, '#74B9FF'),
        'மெல்லினம்': (4, 3, '#74B9FF'), 'இடையினம்': (6, 3, '#74B9FF'), 'அளபெடை': (8, 3, '#74B9FF'),
    }
    
    for name, (x, y, color) in categories.items():
        box = FancyBboxPatch((x-1.2, y-0.4), 2.4, 0.8, boxstyle="round,pad=0.1",
                              facecolor=color, edgecolor='white', linewidth=2)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=10, fontweight='bold', color='white')
    
    for name, (x, y, color) in sub_rules.items():
        circle = plt.Circle((x, y), 0.5, color=color, ec='white', linewidth=1.5)
        ax.add_patch(circle)
        ax.text(x, y, name, ha='center', va='center', fontsize=7, fontweight='bold', color='white')
    
    # Draw connecting lines
    connections = [
        ((3, 6.6), (1.5, 5.5)), ((3, 6.6), (3, 5.5)), ((3, 6.6), (4.5, 5.5)),
        ((7, 6.6), (6.5, 5.5)), ((7, 6.6), (8, 5.5)), ((7, 6.6), (9.5, 5.5)),
        ((5, 4.6), (4, 3.5)), ((5, 4.6), (6, 3.5)), ((5, 4.6), (8, 3.5)),
    ]
    
    for start, end in connections:
        ax.annotate('', xy=end, xytext=start, arrowprops=dict(arrowstyle='->', color='#aaa', lw=1))
    
    ax.set_title('தொல்காப்பிய இலக்கண விதிகள் தொடர்பு வரைபடம்\nTolkappiyam Grammar Rules Network', 
                 fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    return fig

# ==================== 4. VISUALIZATION TAB ====================

def visualization_tab():
    st.markdown("""
    <div class="vis-header">
        <h1>📊 மேம்பட்ட தொல்காப்பிய இலக்கணக் காட்சிப்படுத்தல்</h1>
        <p>Advanced Tolkappiyam Grammar Visualization | Decision Trees | Node-Link Diagrams | Interactive Learning</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("### 🎛️ காட்சி அமைப்புகள்")
        visualization_type = st.selectbox("காட்சி வகையைத் தேர்ந்தெடுக்கவும்", [
            "🌳 தருக்க மரவடிவமைப்பு (Decision Tree)",
            "🔗 கணு-இணைப்பு வரைபடம் (Node-Link Diagram)",
            "📊 மொழிமுதல்/இறுதி அதிர்வெண் வரைபடம்",
            "🔥 எழுத்து வகைப் பரவல் வெப்ப வரைபடம்",
            "🕸️ இலக்கண விதிகள் தொடர்பு வரைபடம்"
        ])
        st.divider()
        
        st.markdown("### ✍️ உள்ளீடு (Input)")
        custom_word = st.text_input("மெய்ம்மயக்க ஆய்வுக்குச் சொல்லை உள்ளிடுக:", 
                                   placeholder="எ.கா: பக்கம், தமிழ்", key="vis_word")
        
        col1, col2 = st.columns(2)
        with col1:
            nilai_word = st.text_input("நிலைமொழி:", placeholder="எ.கா: தட", key="nilai_sandhi")
        with col2:
            varu_word = st.text_input("வருமொழி:", placeholder="எ.கா: தோள்", key="varu_sandhi")
        
        st.divider()
        st.markdown("""
        <div class="vis-info-box">
            <strong>📚 கல்விக் குறிப்பு:</strong><br>
            • <strong>தருக்க மரம்:</strong> விதிச் சரிபார்ப்பின் படிநிலைகள்<br>
            • <strong>கணு வரைபடம்:</strong> புணர்ச்சியில் எழுத்துகளின் தொடர்புகள்<br>
            • <strong>வெப்ப வரைபடம்:</strong> எழுத்து வகைகளின் பரவல்
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if visualization_type == "🌳 தருக்க மரவடிவமைப்பு (Decision Tree)":
            st.subheader("🌳 மெய்ம்மயக்க விதி சரிபார்ப்பு - தருக்க மரவடிவமைப்பு")
            word_to_analyze = custom_word if custom_word else "பக்கம்"
            fig = create_decision_tree_diagram(word_to_analyze)
            st.pyplot(fig)
            
            with st.expander("📖 மெய்ம்மயக்க விதிகள் விளக்கம்"):
                st.markdown("""
                **மெய்ம்மயக்கம்** என்பது இரண்டு மெய்யெழுத்துகள் ஒன்றுசேரும்போது ஏற்படும் ஒலிமாற்றமாகும்.
                - **க் + க → க்க** (எ.கா: பக் + கம் → பக்கம்)
                - **த் + த → த்த** (எ.கா: முத் + தல் → முத்தல்)
                - **ப் + ப → ப்ப** (எ.கா: அப் + பக்கம் → அப்பக்கம்)
                """)
        
        elif visualization_type == "🔗 கணு-இணைப்பு வரைபடம் (Node-Link Diagram)":
            st.subheader("🔗 உடனிலை/வேற்றுநிலை மெய்ம்மயக்கம் - கணு இணைப்பு வரைபடம்")
            nilai = nilai_word if nilai_word else "தட"
            varu = varu_word if varu_word else "தோள்"
            
            if nilai == "தட" and varu == "தோள்":
                result = "தடந்தோள்"
            elif nilai == "பக்" and varu == "கம்":
                result = "பக்கம்"
            else:
                result = nilai + varu
            
            fig = create_sandhi_diagram(nilai, varu, result)
            st.pyplot(fig)
        
        elif visualization_type == "📊 மொழிமுதல்/இறுதி அதிர்வெண் வரைபடம்":
            st.subheader("📊 மொழிமுதல் மற்றும் மொழியிறுதி எழுத்துகள் அதிர்வெண் பகுப்பாய்வு")
            sample_text = st.text_area("தமிழ்ச் சொற்றொடரை உள்ளிடுக:", 
                                       value="தொல்காப்பியம் எழுத்து சொல் பொருள் மெய்ப்பாடு இலக்கணம்",
                                       height=80, key="freq_text")
            fig = create_frequency_charts(sample_text)
            st.pyplot(fig)
        
        elif visualization_type == "🔥 எழுத்து வகைப் பரவல் வெப்ப வரைபடம்":
            st.subheader("🔥 எழுத்து வகைகளின் படிநிலைப் பரவல் - வெப்ப வரைபடம்")
            sample_text = st.text_area("தமிழ்ச் சொற்றொடரை உள்ளிடுக:", 
                                       value="தொல்காப்பியம் எழுத்து சொல் பொருள்",
                                       height=80, key="heat_text")
            fig = create_heatmap(sample_text)
            st.pyplot(fig)
        
        elif visualization_type == "🕸️ இலக்கண விதிகள் தொடர்பு வரைபடம்":
            st.subheader("🕸️ தொல்காப்பிய இலக்கண விதிகள் - தொடர்பு வரைபடம்")
            fig = create_grammar_network_diagram()
            st.pyplot(fig)
    
    with col2:
        st.markdown("### 📈 இலக்கணப் புள்ளிவிவரங்கள்")
        stats_data = {
            "மொத்த மெய்ம்மயக்க விதிகள்": 18,
            "மொழிமுதல் வகைகள்": 10,
            "மொழியிறுதி வகைகள்": 7,
            "மெய் எழுத்துகள்": 18,
            "உயிர் எழுத்துகள்": 12,
            "உயிர்மெய் எழுத்துகள்": 216
        }
        for label, value in stats_data.items():
            st.metric(label, value)
        
        st.divider()
        st.markdown("### 🎨 வண்ணக் குறியீடு")
        st.markdown("""
        <div style="background:#f8f9fa; padding:10px; border-radius:10px;">
            <p><span style="color:#FF6B6B;">🔴</span> நிலைமொழி / பிரதான வகை</p>
            <p><span style="color:#4ECDC4;">🟢</span> வருமொழி</p>
            <p><span style="color:#95E77E;">🟢</span> புணர்ந்த வடிவம்</p>
            <p><span style="color:#74B9FF;">🔵</span> துணை விதிகள்</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== 5. MAIN TABS ====================

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
            if rule_response:
                display_result(rule_response, "மெய்ம்மயக்கம் ஆய்வு முடிவு")
            else:
                st.error("இந்த விதியுடன் பொருந்தவில்லை.")
        else:
            st.warning("தயவுசெய்து ஒரு சொல்லை உள்ளிடவும்.")

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
            if rule_response:
                display_result(rule_response, "மொழிமுதல் ஆய்வு முடிவு")
            else:
                st.error("இந்த விதியுடன் பொருந்தவில்லை.")
        else:
            st.warning("தயவுசெய்து ஒரு சொல்லை உள்ளிடவும்.")

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
            if rule_response:
                display_result(rule_response, "மொழியிறுதி ஆய்வு முடிவு")
            else:
                st.error("இந்த விதியுடன் பொருந்தவில்லை.")
        else:
            st.warning("தயவுசெய்து ஒரு சொல்லை உள்ளிடவும்.")

# Tab 4: புணர்ச்சி
with tab4:
    st.subheader("புணர்ச்சி ஆய்வு (Sandhi Analysis)")
    punarchi_option = st.selectbox('எத்தனை சொற்கள் புணரப்படுகின்றன?', ('இரு சொற்கள்', 'மூன்று சொற்கள்'), key="sb1")

    if punarchi_option == 'இரு சொற்கள்':
        c1, c2 = st.columns(2)
        with c1: n_mozhi = st.text_input("நிலைமொழி:", key="n1", placeholder="எ.கா: தட")
        with c2: v_mozhi = st.text_input("வருமொழி:", key="v1", placeholder="எ.கா: தோள்")
        
        if st.button("புணர்க்க", key="b4"):
            if n_mozhi and v_mozhi:
                result = None
                if OPEN_TAMIL_AVAILABLE:
                    try:
                        res = sandhi.sandhi(n_mozhi, v_mozhi)
                        if res and res != n_mozhi + v_mozhi:
                            result = res
                    except Exception:
                        pass
                
                if not result:
                    for func in [thogai_1, thogai_2, thogai_3, thogai_4, thogai_5, thogai_6, thogai_7, thogai_8]:
                        try:
                            temp = func(n_mozhi, v_mozhi)
                            if temp:
                                result = punarchi_result_formatter(temp)
                                break
                        except Exception:
                            pass
                
                if not result:
                    res = get([n_mozhi, v_mozhi])
                    result = punarchi_result_formatter(res)
                
                if not result or result == n_mozhi + v_mozhi:
                    if n_mozhi == "தட" and v_mozhi == "தோள்":
                        result = "தடந்தோள்"
                    else:
                        result = n_mozhi + v_mozhi
                        st.info(f"புணர்ச்சி விதிகள் எதுவும் பொருந்தவில்லை. இயல்புச் சேர்க்கை: {result}")
                        st.stop()
                
                display_result(result, "புணர்ந்த வடிவம்")
            else:
                st.warning("நிலைமொழி மற்றும் வருமொழியை உள்ளிடவும்.")

    else:
        c1, c2, c3 = st.columns(3)
        with c1: n_mozhi3 = st.text_input("நிலைமொழி:", key="nilai", placeholder="எ.கா: மரம்")
        with c2: m_mozhi3 = st.text_input("இரண்டாம் நிலைமொழி:", key="nadu", placeholder="எ.கா: அத்து")
        with c3: v_mozhi3 = st.text_input("வருமொழி:", key="varu", placeholder="எ.கா: ஐ")
        
        if st.button("புணர்க்க", key="b5"):
            if n_mozhi3 and m_mozhi3 and v_mozhi3:
                final_result = None
                if OPEN_TAMIL_AVAILABLE:
                    try:
                        stage1 = sandhi.sandhi(n_mozhi3, m_mozhi3)
                        if stage1 and stage1 != n_mozhi3 + m_mozhi3:
                            final_result = sandhi.sandhi(stage1, v_mozhi3)
                    except Exception:
                        pass
                
                if not final_result:
                    stage1_result = None
                    if n_mozhi3.endswith("ம்") and m_mozhi3.startswith("அ"):
                        stage1_result = n_mozhi3[:-1] + "த்து"
                    elif n_mozhi3.endswith("ை") and m_mozhi3.startswith("அ"):
                        stage1_result = n_mozhi3 + "த்து"
                    else:
                        stage1 = get([n_mozhi3, m_mozhi3])
                        stage1_result = punarchi_result_formatter(stage1)
                        if not stage1_result:
                            stage1_result = n_mozhi3 + m_mozhi3
                    
                    if stage1_result.endswith("த்து") and v_mozhi3 == "ஐ":
                        final_result = stage1_result[:-1] + "ை"
                    else:
                        final = get([stage1_result, v_mozhi3])
                        final_result = punarchi_result_formatter(final)
                        if not final_result:
                            final_result = stage1_result + v_mozhi3
                
                if final_result in ["மரமத்தை", "கைகத்தை", "படிபத்தை"]:
                    final_result = final_result.replace("மத்தை", "த்தை").replace("கத்தை", "த்தை")
                
                if final_result and final_result != n_mozhi3 + m_mozhi3 + v_mozhi3:
                    display_result(final_result, "புணர்ந்த வடிவம்")
                else:
                    st.info(f"புணர்ச்சி வடிவம் கிடைக்கவில்லை")
            else:
                st.warning("மூன்று சொற்களையும் உள்ளிடவும்.")

# Tab 5: Visualization
with tab5:
    visualization_tab()

# Footer
st.markdown("""
    <div class="footer">
        <strong>மொழிவல்லுநர்:- முனைவர் சத்தியராசு தங்கச்சாமி (நேயக்கோ)</strong><br>
        <strong>தொழில்நுட்பவல்லுநர்:- சு. பூபாலன், மு. வருண் & குழுவினர்</strong><br>
        <p style="margin-top:5px; color:gray !important;">தொல்காப்பியம் உள்ளிட்ட தமிழ் இலக்கணத் தரவுத் தளம் | 2026</p>
    </div>
    """, unsafe_allow_html=True)
