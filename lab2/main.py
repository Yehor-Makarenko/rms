from mido import Message, MidiFile, MidiTrack
import matplotlib.pyplot as plt
import random

def data_to_midi_notes(data):
    min_note = 60 
    max_note = 72
    min_data, max_data = min(data), max(data)

    notes = [
        (int(min_note + (value - min_data) * (max_note - min_note) / (max_data - min_data)), int(dur * 1000))
        for (value, dur) in data
    ]
    return notes

data = [(60, 0.5), (62, 0.5), (64, 0.5), (65, 0.5), (67, 0.5), 
(69, 0.5), (67, 0.5), (65, 0.5), (64, 0.5), (62, 0.5), 
(60, 0.7), (62, 0.5), (64, 0.5), (67, 0.5), 
(69, 0.5), (71, 0.5), (69, 0.5), (67, 0.5), (65, 0.5), 
(64, 0.7), (65, 0.5), 
(64, 0.5), (62, 0.5), (60, 0.5), (62, 0.5), (64, 0.5), 
(65, 0.5), (67, 0.7), (65, 0.5), (64, 0.5), (62, 0.5), (60, 1)]
notes = data_to_midi_notes(data)

midi = MidiFile()
track = MidiTrack()
midi.tracks.append(track)
for note, dur in notes:
    track.append(Message('note_on', note=note, velocity=64, time=20))
    track.append(Message('note_off', note=note, velocity=64, time=dur))     
    
midi.save('output.mid')
