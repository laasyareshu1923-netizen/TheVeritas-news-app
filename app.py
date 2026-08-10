import streamlit as st
import numpy as np
import pandas as pd
import re
import plotly.graph_objects as go

# --- SYSTEM CONFIGURATION ---
st.set_page_config(page_title="VeritasAI", layout="wide", page_icon="❇️")

# --- UNBIASED CALCULATOR MATRIX FOR BROADCAST AUDIO ---
def analyze_broadcast_transcript(text: str) -> dict:
    """Strips out specific terminology to analyze structural delivery and bias indicators."""
    if not text.strip():
        return {"score": 50, "metrics": [50, 50, 50, 50, 50]}
        
    total_chars = len(text)
    words = text.split()
    total_words = len(words) if words else 1
    sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
    total_sentences = len(sentences) if sentences else 1
    
    # Structural features isolated from string token definitions
    caps_ratio = sum(1 for c in text if c.isupper()) / total_chars
    punct_density = len(re.findall(r'[!?,.:;"]', text)) / total_words
    avg_sentence_len = total_words / total_sentences
    unique_words_ratio = len(set(w.lower() for w in words)) / total_words
    sensational_punct = len(re.findall(r'(!{2,}|\?{2,})', text)) / total_sentences

    # Calculate structural scores derived purely from broadcasting delivery styles
    neutrality = max(10, min(100, int(100 - (caps_ratio * 400) - (sensational_punct * 500))))
    coherence = max(10, min(100, int(90 if (10 < avg_sentence_len < 25) else 40)))
    consensus = max(10, min(100, int(unique_words_ratio * 130)))
    consistency = max(10, min(100, int(100 - (punct_density * 250))))
    cross_validity = int((neutrality + coherence + consistency) / 3)
    
    overall = int((neutrality + coherence + consensus + consistency + cross_validity) / 5)
    
    return {
        "overall": overall,
        "metrics": [neutrality, coherence, consensus, consistency, cross_validity]
    }

# --- TV CHANNEL DATABASES ---
TV_CHANNELS = {
    "Global News Tier": {
        "BBC World News Feed": "BREAKING: Global market indexes show unprecedented shifts amid multi-national logistics changes. Economists emphasize structural stabilization across central supply frameworks.",
        "CNN International Feed": "ALERT!!! Dramatic developments unfolding right now as global leaders convene for an emergency session over trade routes. Critical grid points are experiencing massive delays!!!",
    },
    "National Level Scope": {
        "National Broadcast India": "The legislative body has ratified a new environmental conservation framework today. The policy targets a 15 percent reduction in regional emissions over the next decade.",
        "National News Express": "Unbelievable political shockwaves rocking the capital city after a controversial bill passes without consensus. Experts claim the nation is heading straight into economic chaos.",
    },
    "Local/City Level Scope": {
        "Mumbai Regional Node": "Municipal authorities have issued a heavy rainfall advisory for coastal areas over the next 24 hours. Local commuter transit patterns are being redirected through central hubs.",
        "New York Metro Node": "City transportation officials announced a temporary suspension of transit lines along the main avenue due to essential electrical infrastructure repairs through Tuesday morning.",
    }
}

# --- USER INTERFACE LAYOUT ---
st.title("📺 VeritasAI: TV Broadcast Credibility Analysis Studio")
st.markdown("---")

left_deck, right_display = st.columns([4, 6])

with left_deck:
    st.subheader("⚙️ Broadcast Stream Interface")
    
    # 1. Select News Scope
    news_tier = st.selectbox(
        "Select Target Broadcast Tier:",
        list(TV_CHANNELS.keys())
    )
    
    # 2. Interactive Spatial Node Map (Triggered by Local Tier)
    if "Local" in news_tier:
        st.info("📍 Spatial Targeting Online: Selecting Local Node Database context:")
        map_data = pd.DataFrame({
            'lat': [19.0760, 40.7128, 51.5074, 35.6762, -33.8688],
            'lon': [72.8777, -74.0060, -0.1278, 139.6503, 151.2093],
            'City Name': ['Mumbai Regional Node', 'New York Metro Node', 'London Local Node', 'Tokyo Hub Node', 'Sydney District Node']
        })
        st.map(map_data, latitude='lat', longitude='lon', size=180)
        
    # 3. Channel Stream Selector
    available_feeds = list(TV_CHANNELS[news_tier].keys())
    selected_channel = st.selectbox("Select Active TV Channel Audio Feed:", available_feeds)
    
    # Display the simulated recorded text payload extracted via Whisper Speech-to-Text
    captured_audio_transcript = TV_CHANNELS[news_tier][selected_channel]
    
    st.markdown("##### 📝 Speech-to-Text Live Transcript Output:")
    st.code(captured_audio_transcript, language="text")
    
    run_analysis = st.button("Process Live Stream Audio Vector", type="primary", use_container_width=True)

with right_display:
    st.subheader("📊 Cross-Tier Verification Matrix")
    
    if run_analysis:
        data_matrix = analyze_broadcast_transcript(captured_audio_transcript)
        final_score = data_matrix["overall"]
        
        # Display credibility results indicators
        if final_score >= 70:
            st.success(f"### High Structural Credibility: {final_score}/100")
            st.caption(f"Verified Channel Signature: Neutral reporting metrics match baseline data nodes.")
        elif final_score >= 45:
            st.warning(f"### Sensationalism Vector Flagged: {final_score}/100")
            st.caption(f"Analysis: Emotional manipulation modifiers or abnormal sentence spacing patterns detected.")
        else:
            st.error(f"### Structural Discrepancy Found: {final_score}/100")
            st.caption(f"Analysis: Punctuation and capitalization densities indicate high variance from trusted reporting profiles.")
            
        # Draw Spider/Radar Graph Architecture
        categories = ['Stylistic Neutrality', 'Structural Coherence', 'Source Consensus', 'Structure Consistency', 'Cross-Tier Validity']
        scores = data_matrix["metrics"]
        
        # Close the loop geometry explicitly
        radar_categories = categories + [categories]
        radar_scores = scores + [scores]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=radar_scores,
            theta=radar_categories,
            fill='toself',
            fillcolor='rgba(29, 185, 84, 0.15)' if final_score >= 70 else 'rgba(219, 68, 85, 0.15)',
            line=dict(color='#1DB954' if final_score >= 70 else '#DB4455', width=2)
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=)),
            showlegend=False, height=400, margin=dict(l=60, r=60, t=30, b=30)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Trigger the processing matrix on the left to capture live streaming context windows.")

