import pandas as pd
from emotion_detection import EmotionDetector
from affective_alignment import AffectiveAlignmentDetector

# Load your existing data
df = pd.read_csv('./results/manual_classifications.csv')

# Initialize detectors
emotion_detector = EmotionDetector(threshold=0.3)
alignment_detector = AffectiveAlignmentDetector('./data/affective_alignment_rules.json')

# Add emotion analysis columns
results = []
for idx, row in df.iterrows():
    # Detect emotions in AI response
    ai_emotions = emotion_detector.get_emotion_labels(row['response'])
    
    # Check alignment
    alignment = alignment_detector.check_alignment(
        category=row['category'],
        subcategory=row['subcategory'],
        ai_emotions=ai_emotions
    )
    
    results.append({
        **row.to_dict(),
        'ai_emotions': '|'.join(ai_emotions),
        'inappropriate_emotions': '|'.join(alignment.inappropriate_emotions),
        'affective_alignment': 'aligned' if alignment.aligned else 'misaligned'
    })

# Save enriched dataset
results_df = pd.DataFrame(results)
results_df.to_csv('./results/classifications_with_emotions.csv', index=False)

# Analyze correlation
print("Safety classification vs Affective alignment:")
print(pd.crosstab(
    results_df['classification'], 
    results_df['affective_alignment']
))