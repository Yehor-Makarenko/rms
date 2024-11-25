from mido import Message, MidiFile, MidiTrack
import matplotlib.pyplot as plt
import random

def data_to_midi_notes(data):
    min_note = 60  # Мінімальна нота (Середнє "До")
    max_note = 72  # Максимальна нота
    min_data, max_data = min(data), max(data)

    # Нормалізація даних до діапазону нот
    notes = [
        int(min_note + (value - min_data) * (max_note - min_note) / (max_data - min_data))
        for value in data
    ]
    return notes

data = [random.randint(0, 100) for _ in range(10)]
notes = data_to_midi_notes(data)

midi = MidiFile()
track = MidiTrack()
midi.tracks.append(track)

# Додавання нот до MIDI-файлу
for note in notes:
    track.append(Message('note_on', note=note, velocity=64, time=200))  # Нота вмикається
    track.append(Message('note_off', note=note, velocity=64, time=200))  # Нота вимикається

# Збереження файлу
midi.save('output.mid')
print("MIDI-файл збережено як 'output.mid'")

plt.plot(data, label="Дані")
plt.scatter(range(len(notes)), notes, color='red', label="MIDI-ноти")
plt.legend()
plt.title("Соніфікація даних")
plt.xlabel("Індекс")
plt.ylabel("Значення/Ноти")
plt.show()
