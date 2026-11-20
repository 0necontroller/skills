"""Generate speech with Kitten TTS 2 Mini (KittenML/kitten-tts-2-mini).

Run with the dedicated environment (see SKILL.md):

    PY=~/kitten-tts/.venv/bin/python
    $PY speak.py "Hello there." -o hello.wav              # one clip (.wav or .mp3)
    $PY speak.py --file script.txt -o narration.mp3         # a text file, one clip
    $PY speak.py --segments segments.json -o clips/         # one clip per segment
    $PY speak.py --list-voices [--language en]

segments.json is {"key": "text", ...} (order kept). It writes clips/<key>.wav and
clips/durations.json ({"key": seconds}), for pacing a screen recording or mixing
narration onto a video at given offsets (see SKILL.md, "Narrating a video").
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

MODEL = "KittenML/kitten-tts-2-mini"
RATE = 24000


def load():
    from kittenml import KittenTTS

    return KittenTTS(MODEL)


def write(audio, path: Path) -> None:
    import soundfile as sf

    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() == ".wav":
        sf.write(path, audio, RATE)
        return
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg is needed for non-WAV output (brew install ffmpeg)")
    with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
        sf.write(tmp.name, audio, RATE)
        subprocess.run(
            ["ffmpeg", "-loglevel", "error", "-y", "-i", tmp.name, str(path)],
            check=True,
        )


def generate(model, text: str, args):
    kwargs = {"voice": args.voice, "speed": args.speed}
    if args.language:
        kwargs["language"] = args.language
    return model.generate(text, **kwargs)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("text", nargs="?", help="text to speak")
    parser.add_argument("--file", help="read the text from this file")
    parser.add_argument("--segments", help='JSON {"key": "text"}; -o is a directory')
    parser.add_argument("-o", "--out", help="output file (.wav/.mp3/...) or directory")
    parser.add_argument("--voice", default="Danny", help="voice name (default Danny)")
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--language", help="language code, e.g. de (optional)")
    parser.add_argument("--list-voices", action="store_true")
    args = parser.parse_args()

    model = load()

    if args.list_voices:
        langs = [args.language] if args.language else sorted(model.available_voices)
        for lang in langs:
            print(f"[{lang}]")
            for voice in model.voices(lang):
                print(f"  {voice['name']:<10} {voice['description']}")
        return

    if not args.out:
        parser.error("-o/--out is required")

    if args.segments:
        segments = json.loads(Path(args.segments).read_text())
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        durations = {}
        for key, text in segments.items():
            audio = generate(model, text, args)
            write(audio, out / f"{key}.wav")
            durations[key] = round(len(audio) / RATE, 3)
            print(f"{key}\t{durations[key]}s")
        (out / "durations.json").write_text(json.dumps(durations, indent=2))
        print(f"wrote {len(durations)} clips and durations.json to {out}")
        return

    text = Path(args.file).read_text() if args.file else args.text
    if not text:
        parser.error("give text, --file or --segments")
    audio = generate(model, text, args)
    write(audio, Path(args.out))
    print(f"wrote {args.out} ({len(audio) / RATE:.1f}s)")


if __name__ == "__main__":
    main()
