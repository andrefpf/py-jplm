import array
from dataclasses import dataclass
from itertools import count
from pathlib import Path
from typing import Union

import numpy as np

from io import BufferedWriter, BufferedReader

@dataclass
class PGXHeader:
    width: int
    height: int
    depth: int
    byteorder: int


class PGXHanlder:
    def read(self, path: Union[str, Path]) -> np.ndarray:
        with open(path, "rb") as file:
            header = self._read_header(file)
            image = self._read_data(file, header)
        return image

    def write(self, path: Union[str, Path], data: np.ndarray):
        with open(path, "wb") as file:
            # self._write_header(file, data)
            self._write_data(file, data)

    def _read_header(self, file: BufferedReader) -> PGXHeader:
        header = file.readline().split()

        if len(header) != 5:
            raise ValueError("Invalid PGX Header")

        header_id = header[0].decode("utf-8")
        endianess = header[1].decode("utf-8")
        signal_depth = header[2].decode("utf-8")
        width = int(header[3])
        height = int(header[4])

        signal = signal_depth[0]
        depth = int(signal_depth[1:])

        if header_id != "PG":
            raise ValueError(f'Invalid header id "{header_id}"')

        if endianess == "ML":
            byteorder = "big"
        elif endianess == "LM":
            byteorder = "little"
        else:
            raise ValueError(f'Invalid endianess "{endianess}"')

        if signal not in ["+", "-"]:
            raise ValueError(f'Invalid signal "{signal}"')

        if depth <= 0:
            raise ValueError(f'Invalid depth "{depth}"')

        if width <= 0:
            raise ValueError(f'Invalid width "{width}"')

        if height <= 0:
            raise ValueError(f'Invalid height "{height}"')

        return PGXHeader(width, height, depth, byteorder)
    
    def _read_data(self, file: BufferedReader, header: PGXHeader) -> np.ndarray:
        raw_array = array.array("h", file.read())
        raw_array.byteswap()
        image_array = np.array(raw_array)
        shape = (header.height, header.width)
        image_array = image_array.reshape(shape)
        return image_array

    def _write_header(self, file: BufferedWriter, data: np.ndarray):
        byteorder = "big" # "little"
        signal = "+"
        depth = 10
        height, width = data.shape

        file.write(b"PG ")

        if byteorder == "big":
            file.write(b"ML ")
        else:
            file.write(b"LM ")

        file.write(bytes(signal, "utf8"))
        file.write(bytes(f"{depth} {width} {height} \n", "utf8"))

    def _write_data(self, file: BufferedWriter, data: np.ndarray):
        raw_array = array.array("h", data.flatten())
        bytes_data = raw_array.tobytes()
        file.write(bytes_data)
