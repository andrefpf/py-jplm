class Config:
    def __init__(self, initial_params=None):
        self._parameters = list()

        if isinstance(initial_params, dict):
            for key, val in initial_params.items():
                self.add_parameter(key, val)

    def add_parameter(self, name, val):
        self._parameters.append((name, val))

    def pop(self, name):
        for i, (p_name, p_val) in self._parameters:
            if p_name == name:
                return self._parameters.pop(i)
        return None

    def keys(self):
        for name, val in self._parameters:
            yield name

    def values(self):
        for name, val in self._parameters:
            yield val

    def items(self):
        for name, val in self._parameters:
            yield (name, val)

    def copy(self):
        c = Config()
        for params in self.items():
            c.add_parameter(*params)
        return c

    def __getitem__(self, key):
        for name, val in self._parameters:
            if key == name:
                return val
        raise KeyError(f"{key}")

    def __setitem__(self, key, new_value):
        self.add_parameter(key, new_value)

    def __str__(self) -> str:
        items = ",\n".join([f"{key}={val}" for key, val in self.items()])
        return f"Config({items})"