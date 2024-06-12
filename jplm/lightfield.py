from pathlib import Path
from typing import Union

import numpy as np

from jplm import PGXReader
from jplm.utils import nested_dict, view_position_from_name


class LightField:
    def __init__(self) -> None:
        self.data = np.array([])

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
        return self.data[channel, t, s]

    @classmethod
    def from_pgx(cls, path: Union[str, Path]):
        # TODO: maybe it should not load all views at once.

        path = Path(path)
        reader = PGXReader()

        lf_dict = nested_dict()
        for channel_path in path.glob("*"):
            if not channel_path.name.isnumeric():
                continue

            c = int(channel_path.name)
            for view_path in channel_path.glob("*"):
                view = reader.read(view_path)
                t, s = view_position_from_name(view_path.stem)
                lf_dict[c, t, s] = view

        n_channels = len({c for c, t, s in lf_dict.keys()})
        t_size = len({t for c, t, s in lf_dict.keys()})
        s_size = len({s for c, t, s in lf_dict.keys()})

        v_size = None
        u_size = None

        for view in lf_dict.values():
            v, u = view.shape

            if v_size is None:
                v_size = v

            if u_size is None:
                u_size = u

            if (v != v_size) or (u != u_size):
                raise ValueError("Invalid light field shape")

        data = np.empty((n_channels, t_size, s_size, v_size, u_size))
        for (c, t, s), view in lf_dict.items():
            data[c, t, s, :, :] = view

        obj = cls()
        obj.data = data
        return obj
