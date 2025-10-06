import numpy as np
import wave
import struct
import os

def generate_beep(filename, frequency, duration, sample_rate=44100):
    """Generate a simple beep sound and save as WAV file"""
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Generate time array
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Generate sine wave with fade out to avoid clicking
    audio = np.sin(2 * np.pi * frequency * t)
    
    # Apply fade out in last 20% to avoid clicks
    fade_samples = int(len(audio) * 0.2)
    fade = np.linspace(1, 0, fade_samples)
    audio[-fade_samples:] *= fade
    
    # Scale to 16-bit integer range
    audio = (audio * 0.3 * 32767).astype(np.int16)
    
    # Write WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio.tobytes())
    
    print(f"Generated: {filename}")

# Generate the three sound effects
print("Generating sound effects...")

# Paddle hit - high pitched short beep
generate_beep('assets/sounds/paddle_hit.wav', 800, 0.1)

# Wall bounce - medium pitched shorter beep
generate_beep('assets/sounds/wall_bounce.wav', 400, 0.08)

# Score - lower pitched longer beep
generate_beep('assets/sounds/score.wav', 600, 0.25)

print("\nAll sound effects generated successfully!")
print("You can now run your game with sound effects.")
