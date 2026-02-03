# gesture-vocal-alignment (ongoing)
This repository provides data and R- & Python-scripts to analyse longitudinal development of the alignment of the gesture-vocal modalities for 1-3 year old infants. Goal if this project is to test if the gesture-vocal modalities align similarly in infants before full-fledged speech emergence, mirroring associations found in adult co-speech gestures.
Collaborators: Lucie Greco, Clément François, Isabelle Dautriche

## Annotations
We longitudinally annotated different gesture types in infants from 12- to 18-months from open-source videos on the CHILDES corpus (https://phon.talkbank.org/access/French/Paris.html; https://phon.talkbank.org/access/French/Lyon.html). Further annotations ongoing upto 36-months (n = 6)

Gestures were annotated following the scheme below:
<img width="2128" height="990" alt="image" src="https://github.com/user-attachments/assets/51942921-a2f0-474c-a6d0-851604465649" />

Details of annotations of gesture types can be found in this paper (https://doi.org/10.1111/infa.12645)

Gestures were categorised as Referential gestures (**R**), comprising of deictic, iconic and conventional gestures; and as Non-referential gestures (**NR**).

Vocalisations were annotated as Short Vocalisations (SV) with audible breaks in between, and Long Vocalisation (LV) without any audible breaks in between (after Iverson & Fagan, 2004). When gestures occurred without any vocalisations, it was annoted as Nothing (**NTH**).

[Download the dataset](perm_long.xlsx)

## Hypothesis
H1: Preverbal referential gestures (deictic, iconic, conventional) would align with  short vocalisations and/or words, mirroring co-speech referential gestures (Kendon 2004; McNeill 1992) 
H2: Preverbal non-referential gestures would align with long vocalisations, mirroring co-speech beat gestures (Prieto et al., 2018; Bavelas et al., 1992)

## Analyses
Raw data from observations were transformed into long format for running permutation tests. 
We  analyzed two gesture types: R and N gestures, each associated  with SV, LV and no vocalisations (NTH). We calculated actual proportions of each vocalisation type within each gesture category and conducted a permutation test to generate chance distributions of gesture-vocalisation proportions, comparing observed proportions to random chance to compare observed proportions of gesture-vocal associations to shuffled data to test any level of significance. 

[Download R-script](permutation_test.R)

## Findings (so far)

<img width="612" height="389" alt="image" src="https://github.com/user-attachments/assets/40acdd3a-f349-4be6-9615-5affccdcba0c" />

From 12- to 18-months, we find infants displya
- a significnat co-occurrence of referential gestures (**R**) and short vocalisations (**SV**)

- a significant co-occurrence of non-referential gestures (**NR**) and long (**LV**) or no vocalisations (**NTH**)

So far, this aligns with our two hypptheses. More to come with further annotations.


## Unsupervised classification

In an ongoing collaboration with Dr Paul Best, we are developing a script to apply unsupervised clustering methods for further examining ordering of gesture-vocal units.

[Download Python-script](moot_diya.py)

