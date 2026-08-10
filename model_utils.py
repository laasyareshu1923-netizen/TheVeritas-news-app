import numpy as np
import re
from sklearn.preprocessing import StandardScaler

class UnbiasedClassifierMock:
    """
    Extracts purely structural and stylometric features to classify news credibility,
    ensuring mathematical isolation from specific vocabulary, slang, or political entities.
    """
    def __init__(self):
        self.scaler = StandardScaler()
        
    def extract_stylometrics(self, text: str) -> np.ndarray:
        if not text.strip():
            return np.zeros(5)
            
        total_chars = len(text)
        words = text.split()
        total_words = len(words) if len(words) > 0 else 1
        sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
        total_sentences = len(sentences) if len(sentences) > 0 else 1
        
        # 1. Capitalization Intensity (Fake news often overuses ALL CAPS)
        caps_ratio = sum(1 for c in text if c.isupper()) / total_chars
        
        # 2. Punctuation Density (Excessive exclamation marks or structural chaos)
        punct_count = len(re.findall(r'[!?,.:;"]', text))
        punct_density = punct_count / total_words
        
        # 3. Structural Complexity (Average words per sentence)
        avg_sentence_length = total_words / total_sentences
        
        # 4. Lexical Richness (Unique words / total words - checks for low-effort repetition)
        unique_words = len(set(w.lower() for w in words))
        lexical_diversity = unique_words / total_words
        
        # 5. Sensationalism Index (Tracking emotional punctuation grouping like "!!!")
        sensational_punct = len(re.findall(r'(!{2,}|\?{2,})', text)) / total_sentences

        return np.array([caps_ratio, punct_density, avg_sentence_length, lexical_diversity, sensational_punct])

    def predict_credibility(self, text: str, scope: str, spatial_context: str = "") -> dict:
        features = self.extract_stylometrics(text)
        
        # Normalizing thresholds mathematically instead of looking at specific string tokens
        # Simulated Deep Learning weights mapping features to bias-free metrics
        stylistic_neutrality = max(10, min(100, int(100 - (features[0] * 300) - (features[4] * 200))))
        structural_coherence = max(10, min(100, int(85 if (10 < features[2] < 35) else 45)))
        
        # Adjusting contextual weights depending on scope parameters
        if scope == "Local/City Level":
            # Local news naturally has shorter, less complex structures; adjust thresholds to avoid penalty
            source_consensus = 75 if spatial_context else 50
            cross_tier_validity = 80 if (20 > features[2] > 8) else 60
        elif scope == "National Level":
            source_consensus = 82
            cross_tier_validity = 78
        else: # Global
            source_consensus = 88
            cross_tier_validity = 85
            
        context_coherence = int((stylistic_neutrality + structural_coherence) / 2)
        overall_score = int((stylistic_neutrality + structural_coherence + source_consensus + cross_tier_validity + context_coherence) / 5)
        
        return {
            "overall": overall_score,
            "metrics": {
                "Stylistic Neutrality": stylistic_neutrality,
                "Structural Coherence": structural_coherence,
                "Source Consensus": source_consensus,
                "Context Coherence": context_coherence,
                "Cross-Tier Validity": cross_tier_validity
            }
        }
      
