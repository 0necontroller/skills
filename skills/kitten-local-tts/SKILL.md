---
name: kitten-local-tts
description: >-
  Generate speech audio locally and offline with Kitten TTS 2 Mini (KittenML, 82M
  params, 16 languages, CPU/ONNX, no API key). Use when the user asks to turn text
  into speech or audio, make a voiceover or narration, read a script aloud, add a
  voice to a screen recording, demo or walkthrough video, or mentions "kitten tts",
  "kittenml", "local tts" or "text to speech". Covers setup (including Intel Macs),
  the one-clip CLI, per-segment clips with durations for syncing to video, mixing
  narration onto a video with ffmpeg, voices, and writing text that sounds right.
---

# Kitten Local TTS

Model: [KittenML/kitten-tts-2-mini](https://huggingface.co/KittenML/kitten-tts-2-mini),
24 kHz mono. Runs offline on CPU once the model is cached (~85 MB, in
`~/.cache/huggingface`). The first generation in a process takes ~10 s; later
sentences take ~1 s each.

## Setup check

Use a dedicated environment, never the project's Python or a bare `pip install`.
`$SKILL` is the directory that contains this `SKILL.md` (for example
`.agents/skills/kitten-local-tts` or `~/.claude/skills/kitten-local-tts`).

```bash
PY=~/kitten-tts/.venv/bin/python
SKILL=<directory of this SKILL.md>
$PY -W ignore -c "import kittenml" && echo ready   # check before use
```

If that fails, follow [Install](#install) first. Non-WAV output and video mixing
also need `ffmpeg` on the PATH.

## One clip

```bash
$PY $SKILL/scripts/speak.py "Hello there." -o hello.wav
$PY $SKILL/scripts/speak.py --file script.txt -o narration.mp3 --voice Martha
$PY $SKILL/scripts/speak.py "Guten Morgen." -o de.wav --voice Felix --speed 1.1
$PY $SKILL/scripts/speak.py --list-voices --language en
```

The output format follows the extension (`.wav` natively; `.mp3`, `.m4a` and
others through ffmpeg). The default voice is **Danny** (cheerful podcast host).

English voices:
- Female: Eleanor (somber historian), Martha (radio journalist), Serena (yoga
  instructor), Iris (museum guide), Grace (nurse), Edith (grandmother), Diana
  (military officer).
- Male: Otis (blues musician), Vincent (museum guide), Max (sports announcer),
  Danny (podcast host).

English voices also speak de/es/it/pt/ru with `--language`. Each other language
has its own voices (`--list-voices`).

## Writing text that sounds right

- Spell out acronyms you want read as letters, with spaces: `P A`, `T B D`,
  `E H R`. Leave ones that are spoken as words (`NASA`).
- Write numbers and dates the way they are said when it matters ("September
  thirtieth", "three hundred dollars").
- Short sentences, one idea each. Commas give pauses.
- Code identifiers, paths and URLs read badly; describe them instead.
- The agent cannot hear the output. Tell the user which words might be
  mispronounced so they can check before shipping.

## Narrating a video

Keep picture and voice in sync by generating the narration **first**, pacing
the recording to the clip lengths, then mixing at the recorded offsets:

1. Write `segments.json`, one entry per step, in order:
   `{"intro": "This is the settings page.", "row_1": "Carter is on hold."}`
2. `$PY $SKILL/scripts/speak.py --segments segments.json -o clips/`
   writes `clips/<key>.wav` and `clips/durations.json` (seconds).
3. Record the video (for example Playwright `record_video_dir`). At each step,
   note the offset since the page was created and wait for that segment's
   duration (+0.3 s gap) while the on-screen action happens. Save the offsets as
   `cues.json`: `[["intro", 1.5], ["row_1", 37.5], ...]`.
4. `python3 $SKILL/scripts/mix_narration.py video.webm clips/ cues.json out.mp4`
   (H.264 + AAC, loudness-normalised; plain python3, no Kitten TTS needed).
5. Check: `ffprobe` shows a video and an audio stream; grab a frame at a cue
   offset (`ffmpeg -ss <t> -i out.mp4 -frames:v 1 f.png`) and confirm the screen
   matches what is being said.

To narrate an existing video with no cue log, estimate offsets from frames, or
just concatenate:
`ffmpeg -i video.mp4 -i narration.wav -map 0:v -map 1:a -c:v copy -c:a aac -shortest out.mp4`.

Playwright headless recordings show no mouse pointer. Inject a fixed-position
cursor element that follows `mousemove`, and move with
`page.mouse.move(x, y, steps=30)` so the motion is visible.

## Python API

```python
from kittenml import KittenTTS
import soundfile as sf

m = KittenTTS("KittenML/kitten-tts-2-mini")             # backend="onnx" (default)
audio = m.generate("Hello.", voice="Danny", speed=1.0)  # numpy float array
sf.write("out.wav", audio, 24000)
```

Load the model once and reuse it for many sentences.

## Install

Check the machine first: `uname -sm`.

### Apple Silicon, Linux, Windows

```bash
mkdir -p ~/kitten-tts && cd ~/kitten-tts
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python kittenml soundfile
```

(On Windows the interpreter is `.venv\Scripts\python.exe`.)

### Intel Mac (`Darwin x86_64`)

kittenml ≥0.9 declares `torch>=2.6`, which has no Intel-Mac wheels, so a normal
install silently falls back to the ancient kittenml 0.1.0. The ONNX speech model
needs no torch; only the English pronunciation fallback (a small BART model)
does, and torch 2.2.2 (the last Intel-Mac release) runs it. Working recipe:

```bash
mkdir -p ~/kitten-tts && cd ~/kitten-tts
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python soundfile huggingface_hub brotli einops \
  safetensors pyloudnorm "kitten-text-processing>=0.1.0" espeakng_loader phonemizer \
  onnxruntime "misaki>=0.9.4" "spacy>=3.8" num2words \
  "torch==2.2.2" "transformers<4.50" "numpy<2" "scipy<1.15"
uv pip install --python .venv/bin/python --no-deps "kittenml==0.9.8"
```

Left out on purpose: `librosa` (numba/llvmlite won't build there), `torchaudio`,
`diffusers` and friends. Only the torch backend needs them, so
`backend="torch"` does not work; the default ONNX backend does. Never run
`pip install -U kittenml` in this env: it would pull the incompatible
dependency set.

### First run

The first generation downloads the model and spaCy's `en_core_web_sm`
(~1-2 min). After that everything runs offline.
