"""Paridade real da interface com as cinco amostras avaliadas no notebook."""
from pathlib import Path
import json
import sys
import numpy as np
import pandas as pd
from streamlit.testing.v1 import AppTest

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
meta = json.loads((root / 'artifacts/metadata.json').read_text())
cases = pd.read_csv(root / 'results/consistencia.csv')
app = AppTest.from_file(str(root / 'app.py'), default_timeout=30).run()
assert not app.exception
results = []
for _, row in cases.iterrows():
    sample_id = int(row.id_amostra)
    app.selectbox[0].select(str(sample_id)).run()
    app.button[0].click().run()
    assert not app.exception
    assert app.session_state['prediction'] == int(row.y_previsto)
    expected = [row[f'p_classe_{c}'] for c in meta['classes']]
    np.testing.assert_allclose(app.session_state['probabilities'], expected, rtol=1e-10, atol=1e-12)
    results.append({'id_amostra': sample_id, 'classe': int(row.y_previsto), 'paridade_interface': True})
(root / 'results/paridade_interface.json').write_text(json.dumps(results, indent=2))
print('Interface Streamlit: 5/5 casos com classe e probabilidades idênticas ao notebook.')
