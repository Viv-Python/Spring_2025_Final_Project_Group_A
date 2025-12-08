"""
Audio generation script to create victory music for the game.
This generates a simple celebratory tune in WAV format.
"""

import wave
import struct
import math

def generate_victory_music():
    """Generate a simple victory music tune"""
    sample_rate = 44100
    duration = 4  # 4 seconds
    num_samples = sample_rate * duration
    
    # Frequency sequence for a simple celebratory melody
    # C major scale notes (in Hz): C, E, G, C (higher)
    notes = [262, 330, 392, 523]  # C, E, G, C
    note_durations = [1, 1, 1, 1]  # Each note lasts 1 second
    
    # Create audio data
    audio_data = []
    current_sample = 0
    
    for note_freq, duration_sec in zip(notes, note_durations):
        samples_per_note = sample_rate * duration_sec
        for i in range(int(samples_per_note)):
            # Generate a sine wave
            t = (current_sample + i) / sample_rate
            # Add slight envelope for smooth note transitions
            envelope = 0.9 if i < samples_per_note * 0.1 else (0.9 if i > samples_per_note * 0.9 else 1.0)
            sample = int(32767 * 0.3 * envelope * math.sin(2 * math.pi * note_freq * t))
            audio_data.append(sample)
        current_sample += samples_per_note
    
    # Write to WAV file
    filename = 'assets/victory_music.wav'
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b''.join(struct.pack('<h', sample) for sample in audio_data))
    
    print(f"Victory music generated: {filename}")
    print("You can replace this with your own music file in .wav, .mp3, or .ogg format")

if __name__ == '__main__':
    generate_victory_music()
