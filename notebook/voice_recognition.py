import json
import os
import subprocess
from vosk import KaldiRecognizer, Model, SetLogLevel

# убираем встроенные логи консоли
SetLogLevel(-1)


class STT:
    default_init = {
        'model_path': './notebook/models/vosk/model',
        'sample_rate': 16000,
    }

    def __init__(self, model_path=None, sample_rate=None) -> None:

        self.model_path = model_path if model_path\
            else STT.default_init['model_path']
        self.sample_rate = sample_rate if sample_rate\
            else STT.default_init['sample_rate']
        self._check_model()
        model = Model(self.model_path)
        self.recognizer = KaldiRecognizer(model, self.sample_rate)
        self.recognizer.SetWords(True)

    def _check_model(self):
        if not os.path.exists(self.model_path):
            raise Exception('Модель не найден')

    def audio_to_text(self, audio_file=None) -> str:
        with subprocess.Popen(["C:/ffmpeg/bin/ffmpeg.exe",
                               "-loglevel", "quiet", "-i",
                               audio_file,
                               "-ar", str(self.sample_rate),
                               "-ac", "1", "-f", "s16le", "-"],
                              stdout=subprocess.PIPE,
                              shell=True) as process:
            while True:
                data = process.stdout.read(4000)
                if len(data) == 0:
                    break
                if self.recognizer.AcceptWaveform(data):
                    pass

            result_json = self.recognizer.FinalResult()
            result_dict = json.loads(result_json)
            return result_dict['text']
