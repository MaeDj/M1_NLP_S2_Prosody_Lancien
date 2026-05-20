# M1_NLP_S2_Prosody_Lancien

## Project context

This project was made for the validation of Prosody course that took place during the second semester of the first year of NLP master at IDMC, Nancy.

This part of this course was supervised by Mélanie Lancien. All the Praat script used in this project are under her intellectual proprety. 

## Project's purpose

The purpose of this course is to study the harmonies of a given audio file and compute features metrics from it. 

- F0 curve 
- Mean 
- Median
- Standard deviation
- F1-F3 dimention schema

## Data description

The chosen base audio is "The-Very-Hungry-Caterpillar.wav". This audio is 2min18 long and present a clear spectogram without parasite noises, clear formants and and balenced level of energy. 

Audio features were extracted via Praat and "fixed_formants_extraction.praat" script, an adapted version of "ScriptProsody.praat" originally made by Mélanie Lancien and given as base script for this project. 

This script provided .txt output (resultThe-Very-Hungry-Caterpillar.txt) that were converted into a .csv file (The-Very-Hungry-Caterpillar.csv) to simplify the next computation step. 



