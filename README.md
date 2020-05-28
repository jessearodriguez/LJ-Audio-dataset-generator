#### An Extension to https://github.com/Kyubyong/dc_tts. Includes modifications from https://github.com/SeanPLeary/dc_tts-transfer-learning as well.


The purpose of this repo is to test whether a decent audio dataset could be automatically generated based off of a few youtube links. 
In addition, this will serve as an experiment in machine learning for myself. 

The new additions to this project are located in the dataset_generator.py file.

Usage involves feeding in youtube video ids (ex: dQw4w9WgXcQ) for however many videos you want. Final output is a audio dataset that is transcribed in the .csv metadata file alongside accompanying audio clips related to the transcribed text

For demonstration purposes, the sample video ids I used for the dataset generation can be found in the ids.txt file. 


Papers referenced: 

Exploring Transfer Learning for Low Resource
Emotional TTS

https://arxiv.org/pdf/1901.04276.pdf


Efficiently Trainable Text-to-Speech System Based on Deep Convolutional Networks with Guided Attention

https://arxiv.org/pdf/1710.08969.pdf
