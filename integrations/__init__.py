import sys
import os

from .petpooja import PetPoojaAdapter

# Registry of available POS adapters
adapters = {
    "petpooja": PetPoojaAdapter()
}

def get_pos_adapter(name: str):
    return adapters.get(name.lower())
