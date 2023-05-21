import soundfile

from vocode.streaming.output_device.base_output_device import BaseOutputDevice
from vocode.streaming.telephony.constants import (
    DEFAULT_AUDIO_ENCODING,
    DEFAULT_SAMPLING_RATE,
)


class WavOutputDevice(BaseOutputDevice):
    def __init__(self, wav_filename: str = None):
        super().__init__(
            sampling_rate=DEFAULT_SAMPLING_RATE, audio_encoding=DEFAULT_AUDIO_ENCODING
        )
        self.wav_filename = wav_filename
        self.sf = soundfile.SoundFile(self.wav_filename, "w", self.sampling_rate, 2)
        self.active = True

    def send_nonblocking(self, chunk: bytes):
        self.sf.buffer_write(chunk, 'int16')

    def terminate(self):
        self.sf.close()
        self.active = False


def create_file_outpt() -> WavOutputDevice:
    return WavOutputDevice("output.wav")