from pathlib import Path
from typing import Union

import numpy as np

from jplm import PGXHandler
from jplm.utils import nested_dict, view_position_from_name


class LightField:
    def __init__(self) -> None:
        self.data: np.ndarray = np.array([])

    @property
    def t(self):
        pass

    @property
    def s(self):
        pass

    @property
    def v(self):
        pass

    @property
    def u(self):
        pass

    def get_view(self, channel, t, s) -> np.ndarray:
        return self.data[t, s, :, :, channel]

    @classmethod
    def from_pgx(cls, path: Union[str, Path]) -> "LightField":
        # TODO: maybe it should not load all views at once.

        path = Path(path)
        reader = PGXHandler()

        n_channels = 0
        t_size = 0
        s_size = 0
        v_size = 0
        u_size = 0

        max_channel = max(path.glob("*"))        
        max_view_path = max(max_channel.glob("*"))
        with open(max_view_path, "rb") as file:
            max_view_header = reader._read_header(file)

        n_channels = int(max_channel.name) + 1
        t_size, s_size = view_position_from_name(max_view_path.stem)
        v_size = max_view_header.height
        u_size = max_view_header.width
        t_size += 1
        s_size += 1

        data = np.empty((t_size, s_size, v_size, u_size, n_channels))
        for c in range(n_channels):
            for t in range(t_size):
                for s in range(s_size):
                    view = reader.read(path / f"{c}/{t:03}_{s:03}.pgx")
                    data[t, s, :, :, c] = view

        obj = cls()
        obj.data = data
        return obj
