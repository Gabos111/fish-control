"""
Reads cfg.yaml every time you call get_cfg().
If you edit the file over SSH, the next loop cycle picks it up.
"""

import yaml, os, time
_CFG_PATH = os.path.join(os.path.dirname(__file__), "..", "cfg.yaml")
_cache = None
_mtime  = 0

def get_cfg() -> dict:
    global _cache, _mtime
    m = os.path.getmtime(_CFG_PATH)
    if _cache is None or m != _mtime:
        _cache = yaml.safe_load(open(_CFG_PATH))
        _mtime = m
    return _cache