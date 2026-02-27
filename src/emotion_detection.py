from transformers import pipeline
import pandas as pd
from typing import List, Dict, Tuple
import re

class EmotionDetector:
    def __init__(self, threshold: float = 0.3):
        """
        Initialize GoEmotions classifier
        
        Args:
            threshold: Minimum score to consider emotion present
        """
        self.classifier = pipeline(
            "text-classification",
            model="SamLowe/roberta-base-go_emotions",
            top_k=None
        )
        self.threshold = threshold
        
    def detect_emotions(self, text: str) -> List[Dict[str, float]]:
        """
        Detect emotions using sentence-level analysis (research standard)
        """
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
        
        if not sentences:
            return []
        
        # Analyze each sentence
        emotion_scores = {}
        
        for sentence in sentences:
            results = self.classifier(sentence, truncation=True, max_length=512)[0]
            
            for r in results:
                emotion = r['label']
                score = r['score']
                
                # Take maximum score seen across all sentences
                if emotion not in emotion_scores or score > emotion_scores[emotion]:
                    emotion_scores[emotion] = score
        
        # Filter and format
        emotions = [
            {'emotion': emotion, 'score': score}
            for emotion, score in emotion_scores.items()
            if score >= self.threshold
        ]
        
        return sorted(emotions, key=lambda x: x['score'], reverse=True)
    
    def get_dominant_emotion(self, text: str) -> Tuple[str, float]:
        """Get single highest-scoring emotion"""
        emotions = self.detect_emotions(text)
        if emotions:
            return emotions[0]['emotion'], emotions[0]['score']
        return 'neutral', 0.0
    
    def get_emotion_labels(self, text: str) -> List[str]:
        """Get just the emotion labels above threshold"""
        emotions = self.detect_emotions(text)
        return [e['emotion'] for e in emotions]
    
    def calculate_emotional_intensity(self, text: str) -> str:
        """
        Calculate overall emotional intensity
        
        Returns:
            'low', 'medium', or 'high'
        """
        emotions = self.detect_emotions(text)
        
        if not emotions:
            return 'low'
        
        # Average of top 3 emotion scores
        top_scores = [e['score'] for e in emotions[:3]]
        avg_score = sum(top_scores) / len(top_scores)
        
        if avg_score >= 0.6:
            return 'high'
        elif avg_score >= 0.4:
            return 'medium'
        else:
            return 'low'