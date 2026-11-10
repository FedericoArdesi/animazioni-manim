
# Visual Mathematics with Manim

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Manim](https://img.shields.io/badge/Manim-Community_v0.22.1-ECE6E2?style=for-the-badge&logo=manim&logoColor=black)
![Resolution](https://img.shields.io/badge/Rendering-4K_%7C_60fps-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

Una raccolta di animazioni matematiche e dimostrazioni geometriche interattive realizzate con **Manim Community**, con rendering nativo in **4K UHD @ 60fps** e una rigorosa filosofia di coerenza visiva e semantica dei colori.

---

## Indice dei Progetti

- [1. Le Sei Funzioni Goniometriche](#1-le-sei-funzioni-goniometriche)
- [2. Dimostrazione: Seno e Coseno degli Angoli Notevoli](#2-dimostrazione-seno-e-coseno-degli-angoli-notevoli)
- [3. Formule di Addizione e Sottrazione di Seno e Coseno](#3-formule-di-addizione-e-sottrazione-di-seno-e-coseno)
- [Architettura del Repository](#architettura-del-repository)
- [Requisiti e Installazione](#requisiti-e-installazione)
- [Standard di Render](#standard-di-render)
- [Autore](#autore)

---

## 1. Le Sei Funzioni Goniometriche
**Directory:** `funzioni-goniometriche/`

Animazione sincronizzata tra circonferenza goniometrica e grafico cartesiano per le 6 funzioni trigonometriche fondamentali:

$$\sin\theta, \quad \cos\theta, \quad \tan\theta, \quad \cot\theta, \quad \sec\theta, \quad \csc\theta$$

### Caratteristiche visive:
- **Doppio viewport coordinato:** la circonferenza unitaria a sinistra pilota l'evoluzione del grafico a destra tramite `ValueTracker`.
- **Rappresentazione geometrica reale:** segmenti goniometrici proiettati sulle rette tangenti ($x = 1$, $y = 1$) e intercette delle rette tangenti al punto $P(\cos\theta, \sin\theta)$.
- **Gestione singolarità:** clipping dinamico degli asintoti verticali per $\tan, \cot, \sec, \csc$ tramite algoritmo di Liang-Barsky personalizzato.
- **Finale globale:** visualizzazione simultanea di tutte le curve con tracciamento vettoriale in tempo reale.

```bash
cd funzioni-goniometriche
manim -pqk goniometria.py Goniometria
```

---

## 2. Dimostrazione: Seno e Coseno degli Angoli Notevoli
**Directory:** `dimostrazione-angoli-notevoli/`

Dimostrazione geometrica rigorosa e **non circolare** che risponde a due quesiti chiave della goniometria elementare:
1. *Perché vale la formula compatta $\sin\theta = \frac{\sqrt{n}}{2}$ con $n \in \{0, 1, 2, 3, 4\}$?*
2. *Perché i salti di $\theta$ sono irregolari ($30^\circ, 15^\circ, 15^\circ, 30^\circ$) se $n$ cresce di passo $1$?*

### Tappe della dimostrazione:
1. **Passaggio alla corda:** Riconduzione della formula a $AB = 2\sin\theta = \sqrt{n}$, ovvero la corda sottesa dall'angolo al centro $2\theta$.
2. **Geometria sintetica elementare:** Calcolo delle 5 corde senza presupporre valori trigonometrici (solo triangolo equilatero, teorema di Pitagora e teorema di Talete sul triangolo inscritto nella semicirconferenza).
3. **Ponte analitico con le coordinate:** Dimostrazione che $AB^2 = 2 - 2\cos(2\theta) = n \implies \cos(2\theta) = 1 - \frac{n}{2}$.
4. **La curvatura del coseno:** Spiegazione visiva dei salti non lineari: il coseno è piatto agli estremi ($0^\circ, 180^\circ$) e ripido al centro ($90^\circ$). Salti uniformi di quota $\Delta y = \frac{1}{2}$ producono salti d'arco differenti.
5. **Simmetria a specchio:** Derivazione naturale di $\cos\theta = \frac{\sqrt{4-n}}{2}$ tramite la riflessione rispetto alla bisettrice a $45^\circ$ ($\theta \mapsto 90^\circ - \theta$).

```bash
cd dimostrazione-angoli-notevoli
# Render di una singola scena:
manim -pqk scena01.py Scena01Tesi
```

---

## 3. Formule di Addizione e Sottrazione di Seno e Coseno
**Directory:** `manim-seno-coseno-alpha-piu-meno-beta/`

Dimostrazione puramente geometrica delle formule di addizione e sottrazione senza l'ausilio dell'algebra lineare o dei numeri complessi:

$$\cos(\alpha \pm \beta) = \cos\alpha \cos\beta \mp \sin\alpha \sin\beta$$
$$\sin(\alpha \pm \beta) = \sin\alpha \cos\beta \pm \cos\alpha \sin\beta$$

### Metodologia:
- Costruzione di un triangolo rettangolo con ipotenusa unitaria orientato a un angolo $\beta$.
- Rotazione rigida del sistema di un angolo $\alpha$ attorno all'origine.
- Proiezione su rettangolo circoscritto e individuazione degli angoli alterni interni.
- Calcolo dei singoli segmenti e ricomposizione analitica dei lati verticali e orizzontali.
- Estensione per parità/disparità alle formule di sottrazione con $\beta \to -\beta$.

```bash
cd manim-seno-coseno-alpha-piu-meno-beta
manim -pqk scene_06_somma.py Scene06Somma
```

---

## Architettura del Repository

```text
.
├── .gitignore
├── README.md
│
├── funzioni-goniometriche/
│   └── goniometria.py              # Script completo: le 6 funzioni simultanee
│
├── dimostrazione-angoli-notevoli/
│   ├── common.py                   # Parametri cromatici e macro LaTeX
│   ├── lista.txt                   # Concat list per montaggio finale ffmpeg
│   ├── scena01.py ... scena10.py   # Passaggi dimostrativi modulari
│   ├── scena11_chiusura.py         # Sintesi analitica non circolare
│   └── scena12_crediti.py          # Crediti d'autore e outro
│
└── manim-seno-coseno-alpha-piu-meno-beta/
    ├── palette.py                  # Tavolozza cromatica e parser MathTex
    ├── scene_01_intro.py           # Enunciato generale
    ├── scene_02_problema.py        # Perché cos(a+b) != cos(a) + cos(b)
    ├── scene_03_triangolo.py       # Triangolo elementare di base
    ├── scene_04_rotazione.py       # Rotazione rigida di angolo alpha
    ├── scene_05_rettangolo.py      # Rettangolo circoscritto
    ├── scene_06_somma.py           # Dimostrazione formule di addizione
    ├── scene_07_differenza.py      # Dimostrazione formule di sottrazione
    └── scene_08_riepilogo.py       # Quadro sinottico finale
```

---

## Requisiti e Installazione

1. **Python 3.10+** (consigliato 3.12)
2. **FFmpeg** configurato nel PATH di sistema
3. **Distribuzione LaTeX** completa (MiKTeX o TeX Live) con `dvisvgm`

Clona la repository e installa le dipendenze:

```bash
git clone https://github.com/TUO_USERNAME/manim-animations.git
cd manim-animations

python -m venv .venv
source .venv/bin/activate       # Su Windows: .\.venv\Scripts\Activate.ps1
pip install manim
```

---

## Standard di Render

Tutte le produzioni finali adottano il preset di massima qualità grafica:

| Flag | Risoluzione | Frame Rate | Utilizzo |
| :--- | :--- | :--- | :--- |
| `-pql` | $854 \times 480$ | 15 fps | Debug rapido della composizione |
| `-pqm` | $1280 \times 720$ | 30 fps | Anteprima e timing audio |
| `-pqh` | $1920 \times 1080$ | 60 fps | Full HD per upload standard |
| `-pqk` | $3840 \times 2160$ | 60 fps | **Master finale UHD 4K** |

---

## Autore

Ideato, codificato e animato da **Federico Ardesi**.
