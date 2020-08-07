from threading import Event
import sounddevice as sd
import win32api

SAMPLE_RATE = 10000  # Sample rate for our input stream
BLOCK_SIZE = 100  # Number of samples before we trigger a processing callback
PRESS_SECONDS = 0.1  # Number of seconds button should be held to register press
PRESS_SAMPLE_THRESHOLD = 0.7  # Signal amplitude to register as a button press
VK_MEDIA_PLAY_PAUSE = 0xB3
BLOCKS_TO_PRESS = (SAMPLE_RATE / BLOCK_SIZE) * PRESS_SECONDS


class HeadsetButtonController:
    def process_frames(self, indata, frames, time, status):
        mean = sum([y for x in indata[:] for y in x]) / len(indata[:])

        if mean < PRESS_SAMPLE_THRESHOLD:
            self.times_pressed += 1

            if self.times_pressed > BLOCKS_TO_PRESS and not self.is_held:
                toggle_play()
                self.is_held = True
        else:
            self.is_held = False
            self.times_pressed = 0

    def __init__(self):
        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            blocksize=BLOCK_SIZE,
            channels=1,
            callback=self.process_frames
        )
        self.stream.start()

        self.is_held = True
        self.times_pressed = 0


def toggle_play():
    win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, 0, 0)


controller = HeadsetButtonController()
Event().wait()
