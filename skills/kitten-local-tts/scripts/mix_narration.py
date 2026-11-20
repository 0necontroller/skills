"""Mix narration clips onto a video at given offsets (needs ffmpeg).

    python3 mix_narration.py VIDEO CLIPS_DIR CUES_JSON OUT.mp4

CUES_JSON is [["key", seconds_from_video_start], ...]; each CLIPS_DIR/<key>.wav
starts at its offset. The video is re-encoded to H.264 + AAC (plays everywhere)
and the narration is loudness-normalised. Plain python3, no Kitten TTS needed.
"""

import json
import subprocess
import sys
from pathlib import Path


def main(video: str, clips: str, cues_path: str, out: str) -> None:
    cues = json.loads(Path(cues_path).read_text())
    args = ["ffmpeg", "-loglevel", "error", "-y", "-i", video]
    filters = []
    for index, (key, offset) in enumerate(cues, 1):
        args += ["-i", str(Path(clips) / f"{key}.wav")]
        ms = int(float(offset) * 1000)
        filters.append(f"[{index}:a]adelay={ms}|{ms},aresample=48000[a{index}]")
    labels = "".join(f"[a{i}]" for i in range(1, len(cues) + 1))
    filters.append(
        f"{labels}amix=inputs={len(cues)}:normalize=0,"
        "loudnorm=I=-16:TP=-1.5,apad[aout]"
    )
    args += [
        "-filter_complex", ";".join(filters),
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "160k",
        "-movflags", "+faststart", "-shortest", out,
    ]  # fmt: skip
    subprocess.run(args, check=True)
    print(f"wrote {out}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    main(*sys.argv[1:])
