"""Produces datasources."""

class factory:
    """Produces datasource data objects."""

    def produce(self, type):
        if "type" == "mendeley":
            import Datasources.mendeley
            return Datasources.mendeley.data()
        if "type" == "bibtex":
            import Datasources.bibtex
            return Datasources.bibtex.data()
        if "type" == "wos":
            import Datasources.wos
            import Datasources.wos.data()