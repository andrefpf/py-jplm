import numpy as np
from dataclasses import dataclass
from itertools import count
from pathlib import Path
from typing import Union
import array


@dataclass
class PGXHeader:
    width: int
    height: int
    depth: int
    byteorder: int


class PGXReader:
    def read(self, path: Union[str, Path]) -> np.ndarray:
        with open(path, "rb") as file:
            header = self._read_header(file)
            image = self._read_data(file, header)
        return image

    def _read_data(self, file, header: PGXHeader) -> np.ndarray:
        raw_array = array.array("h", file.read())
        raw_array.byteswap()
        image_array = np.array(raw_array)
        shape = (header.height, header.width)
        image_array = image_array.reshape(shape)
        return image_array

    def _read_header(self, file) -> PGXHeader:
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
