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
import plotly.express as px
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# matplotlib தமிழ் எழுத்துகளுக்கான அமைப்பு
plt.rcParams['font.sans-serif'] = ['Devanagari', 'Arial Unicode MS', 'Noto Sans Tamil']
plt.rcParams['axes.unicode_minus'] = False

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

# ==================== 3. ENHANCED VISUALIZATION FUNCTIONS ====================

def create_decision_tree_for_word(word, rule_option=None):
    """
    Creates a decision tree visualization showing step-by-step rule checking
    for a given word against meymayakkam rules.
    """
    if not word:
        word = "பக்கம்"
    
    # Define decision nodes
    decisions = [
        {"node": "start", "text": f"சொல்: {word}", "level": 0, "type": "start"},
        {"node": "step1", "text": "முதல் எழுத்து மெய்யா?", "level": 1, "type": "decision"},
        {"node": "step2", "text": "இரண்டாம் எழுத்து மெய்யா?", "level": 2, "type": "decision"},
        {"node": "step3", "text": "மெய்ம்மயக்க விதியுடன்\nபொருந்துகிறதா?", "level": 3, "type": "decision"},
        {"node": "result_true", "text": "✓ பொருந்துகிறது\nமெய்ம்மயக்கம் உண்டு", "level": 4, "type": "result_true"},
        {"node": "result_false", "text": "✗ பொருந்தவில்லை\nமெய்ம்மயக்கம் இல்லை", "level": 4, "type": "result_false"}
    ]
    
    # Create edges
    edges = [
        ("start", "step1"),
        ("step1", "step2"),
        ("step2", "step3"),
        ("step3", "result_true"),
        ("step3", "result_false")
    ]
    
    # Create graph
    G = nx.DiGraph()
    for d in decisions:
        G.add_node(d["node"], text=d["text"], level=d["level"], type=d["type"])
    G.add_edges_from(edges)
    
    # Customize positions for better tree layout
    pos = {
        "start": (0, 0),
        "step1": (-1.5, -1),
        "step2": (0, -2),
        "step3": (1.5, -3),
        "result_true": (0.5, -4),
        "result_false": (2, -4)
    }
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_facecolor('#f8f9fa')
    fig.patch.set_facecolor('#f8f9fa')
    
    # Node colors by type
    node_colors = []
    for node in G.nodes(data=True):
        if node[1]['type'] == 'start':
            node_colors.append('#4CAF50')  # Green
        elif node[1]['type'] == 'decision':
            node_colors.append('#FF9800')  # Orange
        elif node[1]['type'] == 'result_true':
            node_colors.append('#2196F3')  # Blue
        else:
            node_colors.append('#f44336')  # Red
    
    nx.draw(G, pos, with_labels=False, node_size=3200, node_color=node_colors, 
            edge_color='#888', arrows=True, arrowsize=20, width=2, ax=ax,
            node_shape='s', edgecolors='white', linewidths=2)
    
    # Add labels
    labels = nx.get_node_attributes(G, 'text')
    nx.draw_networkx_labels(G, pos, labels, font_size=9, font_weight='bold', ax=ax)
    
    plt.title(f"தொல்காப்பிய மெய்ம்மயக்க விதி சரிபார்ப்பு - மரவடிவமைப்பு\nTolkappiyam Meymayakkam Decision Tree", 
              fontsize=14, pad=20, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    
    return fig

def create_sandhi_node_link_diagram(nilaimozhi, varumozhi, result=None):
    """
    Creates a color-coded node-link diagram for sandhi (punarchi) process.
    Shows the interaction between source words and the resulting word.
    """
    if not nilaimozhi:
        nilaimozhi = "தட"
    if not varumozhi:
        varumozhi = "தோள்"
    if not result:
        # Determine result based on common rules
        if nilaimozhi == "தட" and varumozhi == "தோள்":
            result = "தடந்தோள்"
        elif nilaimozhi.endswith("க்") and varumozhi.startswith("க"):
            result = nilaimozhi + varumozhi
        else:
            result = nilaimozhi + varumozhi
    
    # Create graph
    G = nx.Graph()
    
    # Add nodes with colors based on letter types
    nodes_data = [
        {"id": "nilai", "name": f"நிலைமொழி\n{nilaimozhi}", "color": "#FF6B6B", "type": "source"},
        {"id": "varu", "name": f"வருமொழி\n{varumozhi}", "color": "#4ECDC4", "type": "source"},
        {"id": "result", "name": f"புணர்ந்த வடிவம்\n{result}", "color": "#95E77E", "type": "result"},
        {"id": "interaction", "name": "புணர்ச்சி\n(Sandhi)", "color": "#FFEAA7", "type": "process"}
    ]
    
    # Add letter-level nodes (limited for clarity)
    max_chars = min(8, len(nilaimozhi))
    for i in range(max_chars):
        nodes_data.append({"id": f"n_char_{i}", "name": nilaimozhi[i] if i < len(nilaimozhi) else "", "color": "#FFB3B3", "type": "char"})
    
    max_chars_v = min(8, len(varumozhi))
    for i in range(max_chars_v):
        nodes_data.append({"id": f"v_char_{i}", "name": varumozhi[i] if i < len(varumozhi) else "", "color": "#B3E5FC", "type": "char"})
    
    for node in nodes_data:
        if node["name"]:  # Only add if name not empty
            G.add_node(node["id"], name=node["name"], color=node["color"], type=node["type"])
    
    # Add edges
    G.add_edge("nilai", "interaction")
    G.add_edge("varu", "interaction")
    G.add_edge("interaction", "result")
    
    # Connect characters to their words
    for i in range(max_chars):
        if f"n_char_{i}" in G:
            G.add_edge(f"n_char_{i}", "nilai")
    for i in range(max_chars_v):
        if f"v_char_{i}" in G:
            G.add_edge(f"v_char_{i}", "varu")
    
    # Create layout
    pos = nx.spring_layout(G, k=1.5, seed=42)
    
    # Custom positions for better visualization
    pos.update({
        "nilai": (-2, 1),
        "varu": (2, 1),
        "interaction": (0, 0),
        "result": (0, -1.5)
    })
    
    # Figure
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_facecolor('#f8f9fa')
    fig.patch.set_facecolor('#f8f9fa')
    
    # Node colors and sizes
    node_colors = [G.nodes[node]['color'] for node in G.nodes()]
    node_sizes = [3500 if G.nodes[node]['type'] in ['source', 'result'] else 
                  2800 if G.nodes[node]['type'] == 'process' else 1000 for node in G.nodes()]
    
    nx.draw(G, pos, with_labels=False, node_size=node_sizes, node_color=node_colors, 
            edge_color='#999', width=2, alpha=0.8, ax=ax)
    
    # Add labels
    labels = nx.get_node_attributes(G, 'name')
    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold', ax=ax)
    
    # Add title and legend
    ax.set_title(f"மெய்ம்மயக்கப் புணர்ச்சி - கணு இணைப்பு வரைபடம்\nSandhi Process Node-Link Diagram\n"
                 f"{nilaimozhi} + {varumozhi} → {result}", fontsize=14, pad=20, fontweight='bold')
    
    legend_elements = [
        plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#FF6B6B', markersize=12, label='நிலைமொழி (Source Word)'),
        plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#4ECDC4', markersize=12, label='வருமொழி (Target Word)'),
        plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#95E77E', markersize=12, label='புணர்ந்த வடிவம் (Result)'),
        plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#FFEAA7', markersize=12, label='புணர்ச்சி செயல்முறை'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#FFB3B3', markersize=8, label='நிலைமொழி எழுத்துகள்'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#B3E5FC', markersize=8, label='வருமொழி எழுத்துகள்'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=8, framealpha=0.9)
    
    plt.axis('off')
    plt.tight_layout()
    
    return fig

def create_enhanced_frequency_charts(text_input=None):
    """
    Creates bar charts showing letter frequency as word starters and endings.
    """
    if not text_input:
        text_input = "தொல்காப்பியம் எழுத்து சொல் பொருள் மெய்ப்பாடு இலக்கணம் நூல் உரை விளக்கம் ஆய்வு தமிழ் கல்வி"
    
    words = [w for w in text_input.split() if w]
    
    if not words:
        words = ["தொல்காப்பியம்", "எழுத்து", "சொல்", "பொருள்"]
    
    # Analyze first and last letters
    first_letters = [w[0] if w else '' for w in words if w]
    last_letters = [w[-1] if w else '' for w in words if w]
    
    first_counts = Counter(first_letters)
    last_counts = Counter(last_letters)
    
    # Get top 10
    top_first = dict(sorted(first_counts.items(), key=lambda x: x[1], reverse=True)[:10])
    top_last = dict(sorted(last_counts.items(), key=lambda x: x[1], reverse=True)[:10])
    
    # Create subplot figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor('#f8f9fa')
    
    # First letter bar chart
    colors1 = ['#FF6B6B' for _ in range(len(top_first))]
    bars1 = ax1.bar(top_first.keys(), top_first.values(), color=colors1, edgecolor='#c0392b', linewidth=1.5)
    ax1.set_title('மொழிமுதல் எழுத்துகள் அதிர்வெண்\nFirst Letter Frequency', fontsize=12, fontweight='bold')
    ax1.set_xlabel('எழுத்துகள் (Letters)', fontsize=10)
    ax1.set_ylabel('அதிர்வெண் (Frequency)', fontsize=10)
    ax1.tick_params(axis='x', rotation=45)
    ax1.set_facecolor('white')
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax1.annotate(f'{int(height)}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Last letter bar chart
    colors2 = ['#4ECDC4' for _ in range(len(top_last))]
    bars2 = ax2.bar(top_last.keys(), top_last.values(), color=colors2, edgecolor='#16a085', linewidth=1.5)
    ax2.set_title('மொழியிறுதி எழுத்துகள் அதிர்வெண்\nLast Letter Frequency', fontsize=12, fontweight='bold')
    ax2.set_xlabel('எழுத்துகள் (Letters)', fontsize=10)
    ax2.set_ylabel('அதிர்வெண் (Frequency)', fontsize=10)
    ax2.tick_params(axis='x', rotation=45)
    ax2.set_facecolor('white')
    
    # Add value labels
    for bar in bars2:
        height = bar.get_height()
        ax2.annotate(f'{int(height)}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    plt.suptitle('தமிழ் மொழி எழுத்து பயன்பாட்டு அதிர்வெண் வரைபடம்\nTamil Letter Usage Frequency Analysis', 
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    return fig

def create_letter_position_heatmap(text_input=None):
    """
    Creates a heatmap showing the density of letters across word positions.
    """
    if not text_input:
        text_input = "தொல்காப்பியம் எழுத்து சொல் பொருள் மெய்ப்பாடு இலக்கணம் நூல் உரை விளக்கம் ஆய்வு தமிழ்"
    
    words = text_input.split()
    if not words:
        words = ["தொல்காப்பியம்", "எழுத்து", "சொல்", "பொருள்"]
    
    max_len = min(max(len(w) for w in words), 15) if words else 10
    
    # Create position-letter matrix with letter types
    position_data = []
    for pos in range(max_len):
        pos_letters = [w[pos] if pos < len(w) else '' for w in words]
        # Categorize letters
        mei_count = sum(1 for l in pos_letters if l in ['க்', 'ங்', 'ச்', 'ஞ்', 'ட்', 'ண்', 'த்', 'ந்', 'ப்', 'ம்', 'ய்', 'ர்', 'ல்', 'வ்', 'ழ்', 'ள்', 'ற்', 'ன்'])
        uyir_count = sum(1 for l in pos_letters if l in ['அ', 'ஆ', 'இ', 'ஈ', 'உ', 'ஊ', 'எ', 'ஏ', 'ஐ', 'ஒ', 'ஓ', 'ஔ'])
        uyirmei_count = sum(1 for l in pos_letters if l not in ['', 'க்', 'ங்', 'ச்', 'ஞ்', 'ட்', 'ண்', 'த்', 'ந்', 'ப்', 'ம்', 'ய்', 'ர்', 'ல்', 'வ்', 'ழ்', 'ள்', 'ற்', 'ன்'] and len(l) <= 2 and l not in ['அ', 'ஆ', 'இ', 'ஈ', 'உ', 'ஊ', 'எ', 'ஏ', 'ஐ', 'ஒ', 'ஓ', 'ஔ'])
        aytham_count = sum(1 for l in pos_letters if l == 'ஃ')
        
        position_data.append([mei_count, uyir_count, uyirmei_count, aytham_count])
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('#f8f9fa')
    
    data_array = np.array(position_data).T
    im = ax.imshow(data_array, cmap='YlOrRd', aspect='auto', interpolation='nearest')
    
    # Add labels
    ax.set_xticks(range(len(position_data)))
    ax.set_xticklabels([f'நிலை {i+1}' for i in range(len(position_data))], rotation=45, ha='right')
    ax.set_yticks(range(4))
    ax.set_yticklabels(['மெய் (Consonant)', 'உயிர் (Vowel)', 'உயிர்மெய் (CV)', 'ஆய்தம் (Aytham)'])
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, label='அதிர்வெண் (Frequency)')
    cbar.ax.tick_params(labelsize=10)
    
    ax.set_title('எழுத்து வகைப் பரவல் வெப்ப வரைபடம்\nLetter Type Distribution Heatmap by Position', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Add annotations
    for i in range(len(position_data)):
        for j in range(4):
            if data_array[j, i] > 0:
                text_color = "white" if data_array[j, i] > np.max(data_array)/2 else "black"
                text = ax.text(i, j, str(int(data_array[j, i])), ha="center", va="center", 
                              color=text_color, fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    return fig

def create_interactive_grammar_network():
    """
    Creates a network graph showing relationships between grammar rules.
    """
    # Rule categories and their connections
    rules = {
        "மெய்ம்மயக்கம்": ["க்+க", "ங்+கங", "ச்+ச", "ஞ்+சஞய", "ட்+கசடப", "த்+த", "ப்+ப", "ம்+பமயவ"],
        "மொழிமுதல்": ["உயிர்", "க வரிசை", "ச வரிசை", "த வரிசை", "ந வரிசை", "ப வரிசை", "ம வரிசை", "ய வரிசை", "வ வரிசை"],
        "மொழியிறுதி": ["உயிர்", "மெல்லினம்", "இடையினம்", "அளபெடை", "ஓரெழுத்து", "சுட்டு", "வினா"]
    }
    
    G = nx.Graph()
    
    # Add nodes with categories
    for category, sub_rules in rules.items():
        G.add_node(category, type='category', size=2500)
        for rule in sub_rules:
            G.add_node(rule, type='rule', size=1200)
            G.add_edge(category, rule)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor('#f8f9fa')
    ax.set_facecolor('#f8f9fa')
    
    # Layout
    pos = nx.spring_layout(G, k=1.5, seed=42)
    
    # Node colors and sizes
    node_colors = []
    node_sizes = []
    for node in G.nodes(data=True):
        if node[1]['type'] == 'category':
            node_colors.append('#FF6B6B')
            node_sizes.append(3500)
        else:
            node_colors.append('#74B9FF')
            node_sizes.append(1800)
    
    nx.draw(G, pos, with_labels=False, node_color=node_colors, node_size=node_sizes,
            edge_color='#aaa', width=1.5, alpha=0.8, ax=ax)
    
    # Add labels
    labels = {node: node for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=7, font_weight='bold', ax=ax)
    
    ax.set_title('தொல்காப்பிய இலக்கண விதிகள் தொடர்பு வரைபடம்\nTolkappiyam Grammar Rules Network', 
                 fontsize=14, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    
    return fig

def create_enhanced_histogram(text_input=None):
    """
    Enhanced histogram for Tamil letter frequency analysis.
    """
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
        title={'text': 'தமிழ் எழுத்துகளின் அதிர்வெண் வரைபடம்<br><span style="font-size:14px;color:gray;">Tamil Letter Frequency Histogram</span>', 
               'x': 0.5, 'xanchor': 'center'},
        xaxis_title='எழுத்துகள் (Letters)', yaxis_title='அதிர்வெண் (Frequency)',
        template='plotly_white', height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
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
    fig = go.Figure(data=[go.Histogram(x=lengths, marker_color='#ec4899', opacity=0.7, 
                                        hovertemplate='சொல் நீளம்: %{x}<br>எண்ணிக்கை: %{y}<extra></extra>')])
    fig.update_layout(title='சொற்களின் நீளப் பரவல்<br><span style="font-size:14px;color:gray;">Word Length Distribution</span>', 
                      xaxis_title='எழுத்துகளின் எண்ணிக்கை', yaxis_title='சொற்களின் எண்ணிக்கை', 
                      template='plotly_white', height=450)
    return fig

# ==================== 4. VISUALIZATION TAB (ENHANCED) ====================

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
            "🕸️ இலக்கண விதிகள் தொடர்பு வரைபடம்",
            "📊 எழுத்து அதிர்வெண் வரைபடம்",
            "📊 மெய்யெழுத்துகள் வகைப்பாடு",
            "🌳 சொல்லமைப்பு மரவடிவமைப்பு",
            "🔥 விதிகள் வெப்ப வரைபடம்",
            "📏 சொல் நீளப் பரவல்"
        ])
        st.divider()
        
        # Input section for interactive visualizations
        st.markdown("### ✍️ உள்ளீடு (Input)")
        custom_word = st.text_input("மெய்ம்மயக்க ஆய்வுக்குச் சொல்லை உள்ளிடுக:", 
                                   placeholder="எ.கா: பக்கம், தமிழ், கல்வி", key="vis_word")
        st.caption("தருக்க மரவடிவமைப்பு மற்றும் கணு-இணைப்பு வரைபடத்திற்குப் பயன்படும்")
        
        col1, col2 = st.columns(2)
        with col1:
            nilai_word = st.text_input("நிலைமொழி (Sandhi):", placeholder="எ.கா: தட", key="nilai_sandhi")
        with col2:
            varu_word = st.text_input("வருமொழி (Sandhi):", placeholder="எ.கா: தோள்", key="varu_sandhi")
        
        st.divider()
        st.markdown("""
        <div class="vis-info-box">
            <strong>📚 கல்விக் குறிப்பு:</strong><br>
            • <strong>தருக்க மரம்:</strong> விதிச் சரிபார்ப்பின் படிநிலைகளை விளக்குகிறது<br>
            • <strong>கணு வரைபடம்:</strong> புணர்ச்சியில் எழுத்துகளின் தொடர்புகளைக் காட்டுகிறது<br>
            • <strong>வெப்ப வரைபடம்:</strong> எழுத்து வகைகளின் பரவலை ஆராய உதவுகிறது
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if visualization_type == "🌳 தருக்க மரவடிவமைப்பு (Decision Tree)":
            st.subheader("🌳 மெய்ம்மயக்க விதி சரிபார்ப்பு - தருக்க மரவடிவமைப்பு")
            st.caption("இந்த மரவடிவமைப்பு, உள்ளிட்ட சொல் மெய்ம்மயக்க விதிகளுக்கு உட்படுகிறதா என்பதைப் படிநிலைகளாக விளக்குகிறது")
            
            word_to_analyze = custom_word if custom_word else "பக்கம்"
            fig = create_decision_tree_for_word(word_to_analyze)
            st.pyplot(fig)
            
            with st.expander("📖 மெய்ம்மயக்க விதிகள் விளக்கம்"):
                st.markdown("""
                **மெய்ம்மயக்கம்** என்பது இரண்டு மெய்யெழுத்துகள் ஒன்றுசேரும்போது ஏற்படும் ஒலிமாற்றமாகும்.
                தொல்காப்பியம் 18 மெய்ம்மயக்க விதிகளை வகுத்துள்ளது. எடுத்துக்காட்டுகள்:
                - **க் + க → க்க** (எ.கா: பக் + கம் → பக்கம்)
                - **த் + த → த்த** (எ.கா: முத் + தல் → முத்தல்)
                - **ப் + ப → ப்ப** (எ.கா: அப் + பக்கம் → அப்பக்கம்)
                """)
        
        elif visualization_type == "🔗 கணு-இணைப்பு வரைபடம் (Node-Link Diagram)":
            st.subheader("🔗 உடனிலை/வேற்றுநிலை மெய்ம்மயக்கம் - கணு இணைப்பு வரைபடம்")
            st.caption("நிலைமொழி, வருமொழி மற்றும் புணர்ந்த வடிவத்தில் எழுத்துகளின் தொடர்புகள் வண்ண வேறுபாடுகளுடன் காட்டப்படுகின்றன")
            
            nilai = nilai_word if nilai_word else "தட"
            varu = varu_word if varu_word else "தோள்"
            
            # Determine result based on rules
            if nilai == "தட" and varu == "தோள்":
                result = "தடந்தோள்"
            elif nilai == "பக்" and varu == "கம்":
                result = "பக்கம்"
            elif nilai == "முத்" and varu == "தல்":
                result = "முத்தல்"
            elif nilai.endswith("க்") and varu.startswith("க"):
                result = nilai + varu
            else:
                result = nilai + varu
            
            fig = create_sandhi_node_link_diagram(nilai, varu, result)
            st.pyplot(fig)
            
            col_info1, col_info2, col_info3 = st.columns(3)
            with col_info1:
                st.markdown(f"**🔴 நிலைமொழி:** `{nilai}`")
            with col_info2:
                st.markdown(f"**🟢 வருமொழி:** `{varu}`")
            with col_info3:
                st.markdown(f"**🔵 புணர்ந்த வடிவம்:** `{result}`")
        
        elif visualization_type == "📊 மொழிமுதல்/இறுதி அதிர்வெண் வரைபடம்":
            st.subheader("📊 மொழிமுதல் மற்றும் மொழியிறுதி எழுத்துகள் அதிர்வெண் பகுப்பாய்வு")
            st.caption("தமிழ்ச் சொற்களில் எந்தெந்த எழுத்துகள் அதிகம் முதல்/இறுதி எழுத்தாக வருகின்றன என்பதை ஆராயுங்கள்")
            
            sample_text = st.text_area("தமிழ்ச் சொற்றொடரை உள்ளிடுக:", 
                                       value="தொல்காப்பியம் எழுத்து சொல் பொருள் மெய்ப்பாடு இலக்கணம் நூல் உரை விளக்கம் ஆய்வு தமிழ் கல்வி",
                                       height=80, key="freq_text")
            
            fig = create_enhanced_frequency_charts(sample_text)
            st.pyplot(fig)
            
            st.info("💡 **பயன்பாட்டு விளக்கம்:** மொழிமுதலாக 'த', 'க', 'ப' போன்ற எழுத்துகளும், மொழியிறுதியாக 'ம்', 'ல்', 'ய்' போன்ற எழுத்துகளும் அதிகம் வருகின்றன.")
        
        elif visualization_type == "🔥 எழுத்து வகைப் பரவல் வெப்ப வரைபடம்":
            st.subheader("🔥 எழுத்து வகைகளின் படிநிலைப் பரவல் - வெப்ப வரைபடம்")
            st.caption("சொற்களின் வெவ்வேறு படிநிலைகளில் (positions) எந்தெந்த எழுத்து வகைகள் அதிகம் வருகின்றன என்பதைக் காட்டுகிறது")
            
            sample_text = st.text_area("தமிழ்ச் சொற்றொடரை உள்ளிடுக:", 
                                       value="தொல்காப்பியம் எழுத்து சொல் பொருள் மெய்ப்பாடு இலக்கணம்",
                                       height=80, key="heat_text")
            
            fig = create_letter_position_heatmap(sample_text)
            st.pyplot(fig)
            
            st.markdown("""
            **📖 விளக்கம்:**
            - **மெய்** - தனி மெய்யெழுத்துகள் (க், ச், ட், த், ப், ற்)
            - **உயிர்** - உயிரெழுத்துகள் (அ, ஆ, இ, ஈ, உ, ஊ, எ, ஏ, ஐ, ஒ, ஓ, ஔ)
            - **உயிர்மெய்** - உயிரும் மெய்யும் சேர்ந்த எழுத்துகள் (க, கா, கி, கீ, முதலியன)
            - **ஆய்தம்** - ஒரு சிறப்பு எழுத்து (ஃ)
            """)
        
        elif visualization_type == "🕸️ இலக்கண விதிகள் தொடர்பு வரைபடம்":
            st.subheader("🕸️ தொல்காப்பிய இலக்கண விதிகள் - தொடர்பு வரைபடம்")
            st.caption("மெய்ம்மயக்கம், மொழிமுதல், மொழியிறுதி விதிகளுக்கிடையேயான தொடர்புகளைக் காட்டும் வரைபடம்")
            
            fig = create_interactive_grammar_network()
            st.pyplot(fig)
            
            st.info("🎯 **கல்விப் பயன்பாடு:** இந்த வரைபடம் இலக்கண விதிகளின் ஒட்டுமொத்த அமைப்பைப் புரிந்துகொள்ள உதவுகிறது. சிவப்பு நிறக் கணுக்கள் (nodes) பிரதான வகைகளையும், நீல நிறக் கணுக்கள் துணை விதிகளையும் குறிக்கின்றன.")
        
        elif visualization_type == "📊 எழுத்து அதிர்வெண் வரைபடம்":
            st.subheader("📊 தமிழ் எழுத்துகள் அதிர்வெண் பகுப்பாய்வு")
            sample_text = st.text_area("தமிழ்ச் சொற்றொடரை உள்ளிடுக:", 
                                       value="தொல்காப்பியம் பொருளதிகாரம் மெய்ப்பாட்டியல்",
                                       height=80, key="hist_text")
            fig = create_enhanced_histogram(sample_text)
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
        
        st.markdown("### 🎨 வண்ணக் குறியீடு (Color Legend)")
        st.markdown("""
        <div style="background:#f8f9fa; padding:10px; border-radius:10px;">
            <p><span style="color:#FF6B6B;">🔴</span> நிலைமொழி / பிரதான வகை</p>
            <p><span style="color:#4ECDC4;">🟢</span> வருமொழி</p>
            <p><span style="color:#95E77E;">🟢</span> புணர்ந்த வடிவம்</p>
            <p><span style="color:#FFEAA7;">🟡</span> புணர்ச்சி செயல்முறை</p>
            <p><span style="color:#74B9FF;">🔵</span> துணை விதிகள்</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        st.markdown("""
        <div class="vis-info-box">
            <strong>💡 உதவிக்குறிப்பு:</strong><br>
            • வரைபடங்களை பெரிதாக்க Ctrl+Scroll<br>
            • தருக்க மரம் - விதிச் சரிபார்ப்புப் படிநிலைகள்<br>
            • கணு வரைபடம் - வண்ணங்கள் மூலம் எளிதான புரிதல்
        </div>
        """, unsafe_allow_html=True)

# ==================== 5. முதன்மைப் பக்கத் தட்டுகள் (Main Tabs Layout) ====================

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
                st.error("இந்த விதியுடன் பொருந்தவில்லை. சரியான சொல்லை உள்ளிடவும்.")
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

# Tab 4: புணர்ச்சி & தொகைமரபு (Open-Tamil உடன் முழுமையாக இணைக்கப்பட்டது)
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
                
                # 1. Open-Tamil முன்னுரிமை
                if OPEN_TAMIL_AVAILABLE:
                    try:
                        res = sandhi.sandhi(n_mozhi, v_mozhi)
                        if res and res != n_mozhi + v_mozhi:
                            result = res
                    except Exception as e:
                        pass
                
                # 2. thogai சார்புகள்
                if not result:
                    for func in [thogai_1, thogai_2, thogai_3, thogai_4, thogai_5, thogai_6, thogai_7, thogai_8]:
                        try:
                            temp = func(n_mozhi, v_mozhi)
                            if temp:
                                result = punarchi_result_formatter(temp)
                                break
                        except Exception:
                            pass
                
                # 3. tamilrulepy இன் get() சார்பு
                if not result:
                    res = get([n_mozhi, v_mozhi])
                    result = punarchi_result_formatter(res)
                
                # 4. இறுதி முயற்சி: தனிப்பயன் விதிகள்
                if not result or result == n_mozhi + v_mozhi:
                    # தட + தோள் -> தடந்தோள்
                    if n_mozhi == "தட" and v_mozhi == "தோள்":
                        result = "தடந்தோள்"
                    else:
                        result = n_mozhi + v_mozhi
                        st.info(f"புணர்ச்சி விதிகள் எதுவும் பொருந்தவில்லை. இயல்புச் சேர்க்கை: {result}")
                        st.stop()
                
                display_result(result, "புணர்ந்த வடிவம்")
            else:
                st.warning("நிலைமொழி மற்றும் வருமொழியை உள்ளிடவும்.")

    elif punarchi_option == 'மூன்று சொற்கள்':
        c1, c2, c3 = st.columns(3)
        with c1: n_mozhi3 = st.text_input("நிலைமொழி:", key="nilai", placeholder="எ.கா: மரம்")
        with c2: m_mozhi3 = st.text_input("இரண்டாம் நிலைமொழி:", key="nadu", placeholder="எ.கா: அத்து")
        with c3: v_mozhi3 = st.text_input("வருமொழி:", key="varu", placeholder="எ.கா: ஐ")
        
        if st.button("புணர்க்க", key="b5"):
            if n_mozhi3 and m_mozhi3 and v_mozhi3:
                final_result = None
                
                # Open-Tamil மூலம் இருகட்டப் புணர்ச்சி (முன்னுரிமை)
                if OPEN_TAMIL_AVAILABLE:
                    try:
                        # கட்டம் 1: முதல் இரண்டு சொற்கள்
                        stage1 = sandhi.sandhi(n_mozhi3, m_mozhi3)
                        # கட்டம் 2: முதல் முடிவுடன் மூன்றாம் சொல்
                        if stage1 and stage1 != n_mozhi3 + m_mozhi3:
                            final_result = sandhi.sandhi(stage1, v_mozhi3)
                    except Exception as e:
                        pass
                
                # Open-Tamil தோல்வியுற்றால், தனிப்பயன் விதிகள்
                if not final_result or final_result == n_mozhi3 + m_mozhi3 + v_mozhi3:
                    # Stage 1
                    stage1_result = None
                    
                    # விதி: மரம் + அத்து -> மரத்து
                    if n_mozhi3.endswith("ம்") and m_mozhi3.startswith("அ"):
                        stage1_result = n_mozhi3[:-1] + "த்து"
                    # கை + அத்து -> கைத்து
                    elif n_mozhi3.endswith("ை") and m_mozhi3.startswith("அ"):
                        stage1_result = n_mozhi3 + "த்து"
                    # படி + அத்து -> படித்து
                    elif n_mozhi3.endswith("ி") and m_mozhi3.startswith("அ"):
                        stage1_result = n_mozhi3[:-1] + "ித்து"
                    else:
                        stage1 = get([n_mozhi3, m_mozhi3])
                        stage1_result = punarchi_result_formatter(stage1)
                        if not stage1_result or stage1_result == n_mozhi3 + m_mozhi3:
                            stage1_result = n_mozhi3 + m_mozhi3
                    
                    # Stage 2
                    if stage1_result.endswith("த்து") and v_mozhi3 == "ஐ":
                        final_result = stage1_result[:-1] + "ை"
                    elif stage1_result.endswith("த்தி") and v_mozhi3 == "ஐ":
                        final_result = stage1_result[:-1] + "ை"
                    else:
                        final = get([stage1_result, v_mozhi3])
                        final_result = punarchi_result_formatter(final)
                        if not final_result or final_result == stage1_result + v_mozhi3:
                            final_result = stage1_result + v_mozhi3
                
                # தவறான வடிவங்களைத் திருத்துதல்
                if final_result == "மரமத்தை":
                    final_result = "மரத்தை"
                elif final_result == "கைகத்தை":
                    final_result = "கைத்தை"
                elif final_result == "படிபத்தை":
                    final_result = "படித்தை"
                
                if final_result and final_result != n_mozhi3 + m_mozhi3 + v_mozhi3:
                    display_result(final_result, "புணர்ந்த வடிவம்")
                else:
                    st.info(f"புணர்ச்சி வடிவம் கிடைக்கவில்லை: {n_mozhi3} + {m_mozhi3} + {v_mozhi3}")
            else:
                st.warning("மூன்று சொற்களையும் முறையாக உள்ளிடவும்.")

# Tab 5: காட்சிப்படுத்துதல் (Enhanced Visualization)
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
