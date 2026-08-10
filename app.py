import streamlit as st
import plotly.graph_objects as go
from model_utils import UnbiasedClassifierMock

# Initialize the structural model engine
classifier = UnbiasedClassifierMock()

# Page Configurations
st.set_page_config(page_title="VeritasAI | Unbiased News Engine", layout="wide", page_icon="🌟")

st.title("🌟 VeritasAI: Deep Learning News Verification Workspace")
st.markdown("---")

# Layout Split: 40% Control Deck, 60% Visualization Output
col1, col2 = st.columns([2, 3])

with col1:
    st.subheader("🛠️ Control Deck & Content Ingestion")
    
    # 1. Geographic Scope Configurator
    news_scope = st.selectbox(
        "Select Verification Scope Tier:",
        ["Global Tier", "National Level", "Local/City Level"]
    )
    
    # Dynamic Spatial Input Node
    city_input = ""
    if news_scope == "Local/City Level":
        st.info("📍 Interactive Spatial Targeting Mode Enabled")
        city_input = st.text_input("Enter City/Municipal District Target Node:", placeholder="e.g., Mumbai, New York, London")
        if city_input:
            st.success(f"Context locked into regional databases for: **{city_input}**")
            
    # 2. Text Input Payload
    news_text = st.text_area(
        "Paste News Article Content Layer (Raw Strings):", 
        height=280,
        placeholder="Paste text here... (Note: The structural evaluation vectorizer completely strips out entity nouns, individual names, and slang words to ensure unbiased network metrics)."
    )
    
    analyze_btn = st.button("Run Adversarial Debiased Analysis", type="primary", use_container_width=True)

with col2:
    st.subheader("📊 Multi-Dimensional Analysis Matrix")
    
    if analyze_btn and news_text.strip():
        # Execute analytical extraction pipeline
        results = classifier.predict_credibility(news_text, news_scope, city_input)
        
        # Display overall scoring metric metric blocks
        score = results["overall"]
        if score >= 75:
            st.success(f"### High Credibility Verified: {score}/100")
        elif score >= 50:
            st.warning(f"### Mixed Structural Signals Detected: {score}/100")
        else:
            st.error(f"### Structural Discrepancy Found: {score}/100")
            
        # Compile Radar/Spider Chart Visual Data Layers
        metrics_dict = results["metrics"]
        categories = list(metrics_dict.keys())
        values = list(metrics_dict.values())
        # Append initial item back to list to seal radar graphic ring geometry
        categories.append(categories[0])
        values.append(values[0])
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Credibility Signature',
            fillcolor='rgba(29, 185, 84, 0.2)' if score >= 75 else 'rgba(219, 68, 85, 0.2)',
            line=dict(color='#1DB954' if score >= 75 else '#DB4455', width=2)
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100])
            ),
            showlegend=False,
            height=400,
            margin=dict(l=40, r=40, t=20, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Textual metrics breakdown list
        st.markdown("#### Feature Tensor Parameters Breakdown:")
        m_cols = st.columns(len(results["metrics"]))
        for idx, (metric_name, val) in enumerate(results["metrics"].items()):
            m_cols[idx].metric(label=metric_name, value=f"{val}%")
            
    else:
        st.info("Input a news text structure sequence on the left and trigger the analyzer to render the evaluation matrix profiles.")
      
