from pathlib import Path
import json
import joblib
import pandas as pd
import streamlit as st
from inference import predict_sample

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title='Wine Classifier | CP5', page_icon='🍇', layout='wide')
@st.cache_resource
def load_artifacts():
    return joblib.load(ROOT / 'artifacts/pipeline.joblib'), json.loads((ROOT / 'artifacts/metadata.json').read_text())

st.title('Identificação de vinhos')
st.caption('Checkpoint 5 • Random Forest, XGBoost e LightGBM')
try:
    model, meta = load_artifacts()
except FileNotFoundError:
    st.error('Execute o notebook completo para gerar os artefatos.')
    st.stop()
st.write('Informe as 13 medidas químicas no mesmo padrão numérico da base Wine. A saída identifica uma das três classes da base; não é uma nota de qualidade.')
st.info(f"Modelo: {meta['modelo']} / {meta['estrategia']} • F1 macro no teste: {meta['test_metrics']['f1_macro']:.4f}")
cases = pd.read_csv(ROOT / 'results/consistencia.csv').set_index('id_amostra')
case = st.selectbox('Preencher com uma amostra de consistência', ['Manual'] + [str(i) for i in cases.index])
if st.session_state.get('last_case') != case:
    values = meta['defaults'] if case == 'Manual' else cases.loc[int(case)].to_dict()
    for name in meta['features']:
        st.session_state[name] = float(values[name])
    st.session_state.last_case = case
with st.form('prediction_form'):
    cols = st.columns(3)
    values = {}
    for i, (name, label) in enumerate(zip(meta['features'], meta['labels_pt'])):
        low, high = meta['ranges'][name]
        with cols[i % 3]:
            values[name] = st.number_input(label, min_value=0.000001, format='%.6f', key=name,
                help=f'{name} | Faixa observada no treino: {low:g} a {high:g}. Use a escala original da base.')
    submitted = st.form_submit_button('Classificar amostra', type='primary')
if submitted:
    try:
        label, probabilities = predict_sample(model, meta['features'], values)
        st.session_state['prediction'] = label
        st.session_state['probabilities'] = probabilities.tolist()
        st.success(f'Classe prevista: {label}')
        st.metric('Probabilidade da classe prevista', f'{probabilities.max():.2%}')
        st.dataframe(pd.DataFrame({'Classe': meta['classes'], 'Probabilidade': probabilities}), hide_index=True)
        outside = [n for n in meta['features'] if not meta['ranges'][n][0] <= values[n] <= meta['ranges'][n][1]]
        if outside:
            st.warning('Medidas fora da faixa de treino: ' + ', '.join(outside))
        if case != 'Manual':
            original = cases.loc[int(case)]
            unchanged = all(abs(values[n] - float(original[n])) < 1e-10 for n in meta['features'])
            if unchanged:
                st.write(f"Classe real: {int(original.y_real)} | Notebook: {int(original.y_previsto)}")
                st.write('Paridade com o notebook: ' + ('confirmada' if label == int(original.y_previsto) else 'divergente'))
    except ValueError as exc:
        st.error(str(exc))
st.caption('Base histórica com 178 amostras. Probabilidades não calibradas; desempenho externo não validado.')
with st.expander('Integrantes'):
    for rm, name in meta['integrantes'].items():
        st.write(f'RM {rm} — {name}')
