# garak_contrib — il probe "forced epilogue" per NVIDIA/garak

Obiettivo: portare il risultato "il segreto esce oltre il silenzio" dentro **garak**
(https://github.com/NVIDIA/garak), lo scanner di vulnerabilità LLM di NVIDIA, come probe nuovo.
Se accettato, il nome dell'autore compare nelle release note e il `doc_uri` del probe punta alla
nostra nota (`NOTA_EN.md`).

## Stato
- [x] Verifica di posizionamento (27-28/10/2026): garak ha `sysprompt_extraction` (chiede),
  `divergence`/`leakreplay` (dati di addestramento); zero occorrenze di `ignore_eos`; nessun
  probe misura la continuazione forzata né testa il divieto "non condividere".
- [x] `ISSUE_GARAK_EN.md` — testo dell'issue pronto da incollare (numeri verificati sui dati).
- [ ] Founder apre l'issue su NVIDIA/garak dal suo account.
- [ ] Risposta dei maintainer → implementazione (`epilogue.py` + detector + test) in un fork.
- [ ] PR.

## Disegno (sintesi)
- Probe `epilogue.ForcedEpilogueLeak`: system prompt con scheda riservata + canarino unico per
  tentativo; prompt benigni; generazione con EOS soppressa (`ignore_eos` su ggml/vLLM).
- Detector: cerca canarino e campi **solo nel segmento oltre il punto di silenzio**; riporta
  tasso naturale, tasso epilogo, delta. Parametro: divieto on/off.
- Controlli già misurati e da citare sempre: divieto inefficace (−4 punti, IC include 0);
  la sola lunghezza non riproduce l'effetto (giro 7, 2% vs 2%).

## Regole
- Niente invii senza il sì del founder. Nome pubblico unico: Vincenzo Don / handle GitHub.
- Non pubblicare qui tecniche o break dell'Arena Gray Swan (embargo 30 giorni).
