class Incognita:
    def __init__(self, name, domain):
        self.name = name
        self.value = None
        if not isinstance(domain, set):
            self._domain = set(domain)
        else:
            self._domain = domain

    def domain(self):
        return list(self._domain)

    def rem_from_domain(self, x):
        if x in self._domain:
            self._domain.remove(x)
