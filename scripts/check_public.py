#!/usr/bin/env python3
"""Review an explicit publish allowlist, not the parent workspace or user directories."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    "credential_like": re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{24,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)"),
    "email_like": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    "phone_like": re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"),
    "local_home_path": re.compile(r"/(?:Users|home)/[^\s/]+/|[A-Za-z]:\\Users\\"),
}
EXTENSIONS = {".py", ".md", ".json", ".html", ".yml", ".yaml", ".txt"}


def scan(manifest_path):
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    files = manifest.get("files")
    if not isinstance(files, list) or not files or len(set(files)) != len(files):
        raise ValueError("发布清单必须为非空、不重复的路径列表")
    findings, verified = [], []
    for name in files:
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts or ".git" in relative.parts:
            raise ValueError("清单不能包含绝对路径、上级目录或Git历史")
        path = ROOT / relative
        if path.is_symlink() or not path.resolve().is_relative_to(ROOT.resolve()):
            raise ValueError("不能发布符号链接或项目外文件")
        if path.suffix not in EXTENSIONS and path.name not in {"LICENSE", ".gitignore"}:
            raise ValueError("清单包含不允许的文件类型")
        payload = path.read_bytes()
        text = payload.decode("utf-8")
        for rule, pattern in PATTERNS.items():
            if pattern.search(text):
                findings.append({"path": name, "rule": rule})
        verified.append({"path": name, "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()})
    return {"passed": not findings, "file_count": len(verified), "findings": findings, "files": verified,
            "limits": "Regex checks do not establish confidentiality or ownership; manual review is still required."}


def main():
    parser = argparse.ArgumentParser(description="检查明确列入清单的公开文件，不扫描任何项目外内容")
    parser.add_argument("--manifest", type=Path, default=ROOT / "publication.json")
    args = parser.parse_args()
    try:
        result = scan(args.manifest)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["passed"] else 1
    except (OSError, ValueError, TypeError) as exc:
        print(f"发布检查失败：{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
