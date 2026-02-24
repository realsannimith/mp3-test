"""
generate_voices.py
------------------
Uses edge-tts to generate MP3 files for each name in NAMES
and saves them to the voices/ directory.

Install dependency first:
    pip install edge-tts

Run:
    python generate_voices.py
"""

import asyncio
import os
import edge_tts

VOICES_DIR = "voices"

# Names to generate
NAMES = [
    "មករា សុធា",
    "សុភាព វិជ្ជា",
    "រតនៈ ដារា",
    "ចន្ទា វ៉ាន់",
    "បុកនរិទ្ធ សុវណ្ណ",
    "ហាហាជីដេវីត ម៉ាក់មកយក",
]

# Khmer voices available in edge-tts:
#   km-KH-PisethNeural  (Male)
#   km-KH-SreymomNeural (Female)
# Change VOICE to any voice from `edge-tts --list-voices`
VOICE = "km-KH-PisethNeural"


def name_to_filename(name: str) -> str:
    """Convert 'Makara Sothea' → 'makara_sothea.mp3'"""
    return name.lower().replace(" ", "_") + ".mp3"


async def generate_voice(name: str) -> None:
    filename = name_to_filename(name)
    output_path = os.path.join(VOICES_DIR, filename)

    if os.path.exists(output_path):
        print(f"[SKIP]  {filename} already exists.")
        return

    print(f"[GEN]   Generating '{name}' → {filename}  (voice: {VOICE})")
    communicate = edge_tts.Communicate(name, VOICE)
    await communicate.save(output_path)
    print(f"[DONE]  Saved {output_path}")


async def main() -> None:
    os.makedirs(VOICES_DIR, exist_ok=True)

    tasks = [generate_voice(name) for name in NAMES]
    await asyncio.gather(*tasks)

    print("\nAll done! Files in voices/:")
    for f in sorted(os.listdir(VOICES_DIR)):
        if f.endswith(".mp3"):
            size = os.path.getsize(os.path.join(VOICES_DIR, f))
            print(f"  {f}  ({size:,} bytes)")


if __name__ == "__main__":
    asyncio.run(main())
