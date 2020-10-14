import wave
import pyaudio

chunkSize = 1024

def playSample():
    soundData = wave.open('test.wav', 'rb')
    pya = pyaudio.PyAudio()

    print("sampleWidth: {}, channels: {}, frameRate: {}".format(
          soundData.getsampwidth(),
          soundData.getnchannels(),
          soundData.getframerate()))

    stream = pya.open(format=pya.get_format_from_width(soundData.getsampwidth()),
                      channels=soundData.getnchannels(),
                      rate=soundData.getframerate(),
                      output=True)

    frame = soundData.readframes(chunkSize)
    while frame != b'':
        print(frame)
        stream.write(frame)
        frame = soundData.readframes(chunkSize)

    stream.close()
    pya.terminate()


def record():
    sampleFormat = pyaudio.paInt16
    channels = 2
    fs = 44100
    second = 1
    fileName = 'test.wav'

    pya = pyaudio.PyAudio()
    stream = pya.open(format=sampleFormat,
                      channels=channels,
                      rate=fs,
                      frames_per_buffer=chunkSize,
                      input=True)

    frames = []
    # fs / chunkSize means how many chunks per second,
    # so (fs / chunkSize) * second means total chunks.
    for i in range(int((fs / chunkSize) * second)):
        frames.append(stream.read(chunkSize))

    stream.stop_stream()
    stream.close()
    pya.terminate()

    waveFile = wave.open(fileName, 'wb')
    waveFile.setnchannels(channels)
    waveFile.setsampwidth(pya.get_sample_size(sampleFormat))
    waveFile.setframerate(fs)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()


if __name__ == '__main__':
    playSample()
