"""
Hash Chain Logger — tamper-evident audit trail for the entire pipeline.
Each entry stores prev_hash + SHA-256(prev_hash + entry_data), forming a chain.
Any edit to a past entry breaks the chain from that point forward.
"""
import hashlib, json, os, time

GENESIS_HASH = "0" * 64


class HashChainLogger:
    def __init__(self, path="audit_log.jsonl"):
        self.path = path

    def _last_hash(self):
        if not os.path.exists(self.path):
            return GENESIS_HASH
        last_line = None
        with open(self.path, "r") as f:
            for line in f:
                if line.strip():
                    last_line = line
        if not last_line:
            return GENESIS_HASH
        return json.loads(last_line)["hash"]

    def append(self, stage, data):
        prev_hash = self._last_hash()
        entry = {
            "timestamp": time.time(),
            "stage": stage,
            "data": data,
            "prev_hash": prev_hash,
        }
        raw = json.dumps(entry, sort_keys=True, default=str).encode()
        entry_hash = hashlib.sha256(prev_hash.encode() + raw).hexdigest()
        entry["hash"] = entry_hash
        with open(self.path, "a") as f:
            f.write(json.dumps(entry, default=str) + "\n")
        return entry

    def verify_chain(self):
        if not os.path.exists(self.path):
            return True, []
        prev = GENESIS_HASH
        problems = []
        with open(self.path) as f:
            for i, line in enumerate(f):
                if not line.strip():
                    continue
                e = json.loads(line)
                if e.get("prev_hash") != prev:
                    problems.append(f"Entry #{i} ({e.get('stage')}): broken chain link")
                check = {k: v for k, v in e.items() if k != "hash"}
                raw = json.dumps(check, sort_keys=True, default=str).encode()
                expected = hashlib.sha256(e.get("prev_hash", "").encode() + raw).hexdigest()
                if expected != e.get("hash"):
                    problems.append(f"Entry #{i} ({e.get('stage')}): hash mismatch — TAMPERED")
                prev = e.get("hash")
        return len(problems) == 0, problems

    def read_all(self):
        entries = []
        if os.path.exists(self.path):
            with open(self.path) as f:
                for line in f:
                    if line.strip():
                        entries.append(json.loads(line))
        return entries

    def reset(self):
        if os.path.exists(self.path):
            os.remove(self.path)
