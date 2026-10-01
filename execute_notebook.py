"""Executa o CP inteiro, inclusive todas as buscas e geração do artefato."""
from pathlib import Path
import nbformat
from nbclient import NotebookClient
root = Path(__file__).resolve().parent
path = root / 'Checkpoint05.ipynb'
nb = nbformat.read(path, as_version=4)
NotebookClient(nb, timeout=1800, kernel_name='python3', resources={'metadata': {'path': str(root)}}).execute()
nbformat.write(nb, path)
print('Notebook executado e salvo sem erros.')
