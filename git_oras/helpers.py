import subprocess


class GitConfig:
    @staticmethod
    def get(key):
        p = subprocess.Popen(
            ["git", "config", "--get", key],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        out, err = p.communicate()
        return out.decode("utf-8").strip() if out else None
