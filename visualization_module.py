# visualization_module.py (Minimum working version)
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import re

def main_visualization_tab():
    """Main visualization tab for Streamlit"""
    
    st.markdown("""
    <style>
    .vis-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
        color: white;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="vis-header">
        <h1>📊 தொல்காப்பிய இலக்கணக் காட்சிப்படுத்தல்</h1>
        <p>Tolkappiyam Grammar Visualization | Interactive Learning Tool</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simple frequency chart
    st.subheader("📊 தமிழ் எழுத்துகள் அதிர்வெண் வரைபடம்")
    
    sample_text = st.text_area("தமிழ்ச் சொற்றொடரை உள்ளிடுக:", 
                                value="தொல்காப்பியர் தமிழ் இலக்கணத்தை எழுதினார்")
    
    if sample_text:
        # Extract Tamil characters
        tamil_chars = re.findall(r'[\u0B80-\u0BFF]', sample_text)
        if tamil_chars:
            char_counts = Counter(tamil_chars)
            top_chars = dict(sorted(char_counts.items(), key=lambda x: x[1], reverse=True)[:15])
            
            fig = go.Figure(data=[
                go.Bar(
                    x=list(top_chars.keys()),
                    y=list(top_chars.values()),
                    marker_color='#ec4899',
                    text=list(top_chars.values()),
                    textposition='auto'
                )
            ])
            
            fig.update_layout(
                title="தமிழ் எழுத்துகளின் அதிர்வெண்",
                xaxis_title="எழுத்துகள்",
                yaxis_title="அதிர்வெண்",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("தமிழ் எழுத்துகள் எதுவும் கிடைக்கவில்லை")
    
    # Simple network graph
    st.subheader("🔗 மெய்யெழுத்துகள் வகைப்பாடு")
    
    # Create simple matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    categories = ['வல்லினம் (Hard)', 'மெல்லினம் (Soft)', 'இடையினம் (Medium)']
    counts = [6, 6, 6]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    bars = ax.bar(categories, counts, color=colors)
    ax.set_ylabel('எழுத்துகளின் எண்ணிக்கை')
    ax.set_title('தமிழ் மெய்யெழுத்துகள் வகைப்பாடு')
    
    # Add value labels on bars
    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                str(count), ha='center', va='bottom', fontweight='bold')
    
    st.pyplot(fig)
    
    # Information box
    st.markdown("""
    <div style="background: #f0f2f6; padding: 20px; border-radius: 10px; margin-top: 20px;">
        <h4>📚 இலக்கணக் குறிப்புகள்:</h4>
        <ul>
            <li><strong>வல்லினம்:</strong> க், ச், ட், த், ப், ற் (6 எழுத்துகள்)</li>
            <li><strong>மெல்லினம்:</strong> ங், ஞ், ண், ந், ம், ன் (6 எழுத்துகள்)</li>
            <li><strong>இடையினம்:</strong> ய், ர், ல், வ், ழ், ள் (6 எழுத்துகள்)</li>
        </ul>
        <p>மொத்த மெய்யெழுத்துகள்: 18</p>
    </div>
    """, unsafe_allow_html=True)

# Simple fallback if main function not found
def show_visualization():
    main_visualization_tab()
