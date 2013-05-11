"""Provides factories, I guess."""

import Databases.google_factory as gf
import Databases.dummy_factory as df

def get_factory():
        """Give 'em a factory."""
        return gf.factory()
        #return df.factory()
    