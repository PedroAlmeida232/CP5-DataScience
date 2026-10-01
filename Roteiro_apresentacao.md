# Apresentação — até 10 minutos

- Pedro Rodrigues Almeida — RM 564711
- Alexandre Martins Lucas — RM 561732
- Vitor Carvalho Alexandre — RM 562298
- Gabriel Barbosa — RM 570133

Tempo planejado: 9min30. Usar o relatório e a aplicação como apoio visual; não é necessário criar slides extras. Todos devem conhecer o fluxo completo.

## 0:00–2:00 — Pedro

Apresente a pergunta: identificar a classe de cultivar com medidas químicas, sem estimar qualidade. Mostre as 178 amostras e 13 atributos. Explique que há rótulos conhecidos, portanto classificação supervisionada. Mostre o gráfico das classes e justifique F1 macro: as três classes têm o mesmo peso. Diga que a base histórica é adequada ao exercício, mas limitada para aplicação comercial.

## 2:00–4:00 — Alexandre

Mostre o diagnóstico: não havia ausências, duplicatas ou valores não positivos no treino. Explique por que mantivemos extremos e não padronizamos árvores. A mediana está no pipeline e aprende apenas dentro dos folds. Mostre a separação 142/36 e os três folds iguais para todos. Reforce que teste não foi usado na exploração nem no tuning.

## 4:00–6:20 — Vitor

Mostre a tabela das nove configurações. Random Forest baseline ficou em 0,9525, XGBoost em 0,9300 e LightGBM em 0,9512. Explique 8 combinações por grade versus 20 trials TPE. RF não melhorou; XGBoost melhorou com Optuna; LightGBM/Optuna teve 0,9665 e desvio 0,0243. Não diga que pequena diferença comprova superioridade estatística. A escolha foi feita por CV antes do teste.

## 6:20–9:30 — Gabriel

Mostre curva de aprendizado: treino perfeito, gap final 0,0335 e melhora da validação com mais amostras, com oscilação nas menores frações. Mostre importância e ressalte que não é causalidade. No teste: 36/36 corretas, log loss 0,00521; poucos exemplos não garantem resultado externo.

Abra o Streamlit, selecione a amostra 121 e clique em Classificar. Esperado: classe 1, probabilidade aproximadamente 90,17%, igual ao notebook. Explique o aviso: flavonoides fora da faixa do treino. Selecione a amostra 108 para um acerto de confiança alta. Mostre que cinco casos passaram pelo teste automatizado. Finalize com a necessidade de mais dados e validação em safras novas.

## Perguntas para ensaiar

- Por que não usar acurácia como métrica principal? F1 macro atribui o mesmo peso a todas as classes; acurácia continua no relatório.
- Como evitar leakage? Separação antecipada, imputação nos folds, teste fora do tuning e da seleção.
- Optuna sempre ganha? Não: RF empatou e gastou mais; os espaços e orçamentos diferem.
- Por que não usar o teste para escolher? Isso transformaria teste em validação e contaminaria a estimativa final.
- Por que 100% não prova perfeição? Apenas 36 amostras da mesma origem; intervalo de Wilson da acurácia aproximadamente 90,4% a 100%.
- O que significa a probabilidade? Saída do modelo, não garantia nem probabilidade calibrada.
- Onde estão os links públicos? Publicação pendente; preencher os endereços reais antes da submissão.
