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

    def expand_domain(self, x):
        self._domain.add(x)

    def assign(self, value):
        self._aux_domain = self._domain - {value}
        self._domain = {value}
        self.value = value

    def unassign(self):
        self._domain = self._aux_domain.union({self.value})
        self.value = None
        del self._aux_domain
