import threading
import signal
from gui_control import Param, run_gui
from renderer import Renderer
from audio_fft import AudioAnalyzer

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    param = Param()
    renderer = Renderer(param)

    audio = AudioAnalyzer()
    audio.start()
    renderer.set_audio_source(audio)

    t = threading.Thread(target=renderer.run)
    t.start()

    run_gui(param)
