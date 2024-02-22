import os
import subprocess
from pathlib import Path

from jplm.config import Config


ENCODER_TEMPLATE = """
{jplm_bin}/jpl-encoder-bin 
--show-progress-bar 
--show-runtime-statistics
--show-error-estimate
--input {input} 
--output {output}
"""


DECODER_TEMPLATE = """
{jplm_bin}/jpl-decoder-bin 
--show-runtime-statistics 
--input {input} 
--output {output}
"""


class JPLMRunner:
    def __init__(self, jplm_bin_path=None):
        if jplm_bin_path is not None:
            self.jplm_bin_path = jplm_bin_path
        elif "JPLM_BIN" in os.environ:
            self.jplm_bin_path = os.environ["JPLM_BIN"]
        else:
            raise ValueError(
                "JPLM binary folder not found.\n"
                "You can provide a path through the ambient variable JPLM_BIN"
            )
        
    def encode(self, input_path: str | Path, output_path: str | Path, config: Config):
        input_path = Path(input_path)
        output_path = Path(output_path)

        command = ENCODER_TEMPLATE.format(
            jplm_bin = self.jplm_bin_path,
            input = input_path,
            output = output_path,
        ).split()

        for name, val in config.items():
            command.append(str(name))
            command.append(str(val))

        res = subprocess.run(command, capture_output=True)
        if res.returncode != 0:
            raise Exception(res.stderr.decode())
        return res.stdout.decode()

    def decode(self, input_path: str | Path, output_path: str | Path, config: Config):
        input_path = Path(input_path)
        output_path = Path(output_path)

        command = DECODER_TEMPLATE.format(
            jplm_bin = self.jplm_bin_path,
            input = input_path,
            output = output_path,
        ).split()

        for name, val in config.items():
            command.append(str(name))
            command.append(str(val))
        
        res = subprocess.run(command, capture_output=True)
        if res.returncode != 0:
            raise Exception(res.stderr.decode())
        return res.stdout.decode()
