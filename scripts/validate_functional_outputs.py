from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


VERDICTS = {
    BLOCK_PUBLIC_LAUNCH,
    PRIVATE_BETA_ONLY,
    CONDITIONAL_LAUNCH,
    PUBLIC_LAUNCH_READY,
}

GATE_ALIASES = [
    [SMS/email
