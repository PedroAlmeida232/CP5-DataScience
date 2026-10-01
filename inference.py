"""Preparação de entrada compartilhada pelo notebook e pelo Streamlit."""
import numpy as np
import pandas as pd

def predict_sample(pipeline, features, values):
    missing = set(features) - set(values)
    if missing:
        raise ValueError(f'Campos ausentes: {sorted(missing)}')
    frame = pd.DataFrame([{name: float(values[name]) for name in features}], columns=features)
    if not np.isfinite(frame.to_numpy()).all() or (frame <= 0).any().any():
        raise ValueError('Informe medidas numéricas, finitas e positivas.')
    probabilities = pipeline.predict_proba(frame)[0]
    label = int(pipeline.classes_[np.argmax(probabilities)])
    return label, probabilities
