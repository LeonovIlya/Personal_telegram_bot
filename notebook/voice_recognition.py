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
        self.recognizer.SetWords(False)

    def _check_model(self) -> None:
        if not os.path.exists(self.model_path):
            raise Exception('Модель не найдена!')

    def audio_to_text(self, audio_file=None) -> str:
        cmd = f'ffmpeg -loglevel quiet -i {audio_file} -ar' \
              f' {str(self.sample_rate)} -ac 1 -f s16le -'
        with subprocess.Popen(cmd,
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
