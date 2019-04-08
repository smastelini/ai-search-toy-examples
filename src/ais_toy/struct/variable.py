class Variable:
    def __init__(self, name, domain):
        self.value = None
        self.name = name
        if not isinstance(domain, set):
            self._domain = set(domain)
        else:
            self._domain = domain

    def domain(self):
        return self._domain.tolist()

    def rem_from_domain(self, x):
        if x in self._domain:
            self._domain.remove(x)
