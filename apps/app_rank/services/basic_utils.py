import hashlib
import json
from typing import Dict, Any


class BasicUtils:
    @staticmethod
    def get_text_from_html_element(html_element):
        if html_element is None:
            return ''
        return html_element.text.replace('\\n', '').strip()

    @staticmethod
    def get_dict_hash(dictionary: Dict[str, Any]) -> str:
        """MD5 hash of a dictionary."""
        dhash = hashlib.md5()
        # We need to sort arguments so {'a': 1, 'b': 2} is
        # the same as {'b': 2, 'a': 1}
        encoded = json.dumps(dictionary, sort_keys=True).encode()
        dhash.update(encoded)
        return dhash.hexdigest()
