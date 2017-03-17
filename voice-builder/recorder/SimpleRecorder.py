import pyaudio
import wave

class SimpleRecorder(object):

    def __init__(self, fname, rate=48000, channels=1,format=pyaudio.paInt16,frames_per_buffer=1024):

        self._frames = []
        self._rate = rate
        self._channels = channels
        self._format = format
        self._framesperbuffer = frames_per_buffer
        self._fname = fname
        self._stream = None

        self._p = pyaudio.PyAudio()


    def start_recording(self):

        self._stream = self._p.open(format=self._format,
                                    channels=self._channels,
                                    rate=self._rate,
                                    input=True,
                                    frames_per_buffer=self._framesperbuffer)

        print "Recording......"


    def continue_recording(self):
        data = self._stream.read(self._framesperbuffer)
        self._frames.append(data)

    def stop_recording(self):
        self._stream.stop_stream()
        self._stream.close()
        self._p.terminate()

        wf = wave.open(self._fname, 'wb')
        wf.setnchannels(self._channels)
        wf.setsampwidth(self._p.get_sample_size(self._format))
        wf.setframerate(self._rate)
        wf.writeframes(b''.join(self._frames))
        wf.close()

        

