# Animazioni Manim

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Manim](https://img.shields.io/badge/Manim-Community-5079a4)](https://www.manim.community/)
[![Licenza](https://img.shields.io/github/license/FedericoArdesi/animazioni-manim?color=0969da)](LICENSE)

Raccolta di progetti di animazione realizzati con Manim Community in risoluzione 4K a 60fps.

I video renderizzati in risoluzione nativa sono disponibili nella sezione [Releases](https://github.com/FedericoArdesi/animazioni-manim/releases).

---

## Indice dei progetti

- [1. Funzioni goniometriche](#1-funzioni-goniometriche)
- [2. Dimostrazione angoli notevoli](#2-dimostrazione-angoli-notevoli)
- [3. Formule di addizione e sottrazione](#3-formule-di-addizione-e-sottrazione)
- [Architettura della repository](#architettura-della-repository)
- [Requisiti e installazione](#requisiti-e-installazione)
- [Parametri di rendering](#parametri-di-rendering)
- [Autore](#autore)

---

## 1. Funzioni goniometriche
Directory: `funzioni-goniometriche/`
Download master: [Goniometria.mp4 (4K 60fps)](https://github.com/FedericoArdesi/animazioni-manim/releases/tag/funzioni-goniometriche-v1.0.0)

Script a file singolo che visualizza il comportamento delle sei funzioni trigonometriche (seno, coseno, tangente, cotangente, secante e cosecante) collegando la circonferenza goniometrica al corrispondente grafico cartesiano con tracciamento dinamico degli asintoti.

```bash
cd funzioni-goniometriche
manim -pqk goniometria.py Goniometria
```

---

## 2. Dimostrazione angoli notevoli
Directory: `dimostrazione-angoli-notevoli/`
Download master: [Dimostrazione_Seno_Coseno_Angoli_Notevoli_4K.mp4 (4K 60fps)](https://github.com/FedericoArdesi/animazioni-manim/releases/tag/dimostrazione-angoli-notevoli-v1.0.0)

Sequenza di dodici scene modulari dedicate alla costruzione grafica e analitica dei valori notevoli di seno e coseno. Contiene le definizioni condivise di stile e la lista per il montaggio sequenziale dei render parziali.

```bash
cd dimostrazione-angoli-notevoli
manim -pqk scena01.py Scena01Tesi
```

---

## 3. Formule di addizione e sottrazione
Directory: `manim-seno-coseno-alpha-piu-meno-beta/`
Download master: [manim-seno-coseno-alpha-piu-meno-beta.mp4 (4K 60fps)](https://github.com/FedericoArdesi/animazioni-manim/releases/tag/formule-addizione-sottrazione-v1.0.0)

Progetto strutturato in otto scene che visualizza la derivazione delle formule di addizione e sottrazione tramite rotazione del triangolo unitario e scomposizione delle proiezioni su rettangolo. Fa uso di una palette di colori condivisa.

```bash
cd manim-seno-coseno-alpha-piu-meno-beta
manim -pqk scene_06_somma.py Scene06Somma
```

---

## Architettura della repository

```text
.
├── .gitignore
├── README.md
│
├── funzioni-goniometriche/
│   └── goniometria.py
│
├── dimostrazione-angoli-notevoli/
│   ├── common.py
│   ├── lista.txt
│   └── scena01.py ... scena12_crediti.py
│
└── manim-seno-coseno-alpha-piu-meno-beta/
    ├── palette.py
    └── scene_01_intro.py ... scene_08_riepilogo.py
```

---

## Requisiti e installazione

1. Python 3.10 o superiore
2. FFmpeg configurato nelle variabili d'ambiente
3. Distribuzione LaTeX completa con dvisvgm

Configurazione locale:
```bash
git clone https://github.com/FedericoArdesi/animazioni-manim.git
cd animazioni-manim

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install manim
```

---

## Parametri di rendering

| Flag | Risoluzione | Frame rate | Utilizzo |
| :--- | :--- | :--- | :--- |
| -pql | 854x480 | 15 fps | Bozza rapida |
| -pqm | 1280x720 | 30 fps | Anteprima intermedia |
| -pqh | 1920x1080 | 60 fps | Full HD standard |
| -pqk | 3840x2160 | 60 fps | Master finale 4K |

---

## Autore

Federico Ardesi
