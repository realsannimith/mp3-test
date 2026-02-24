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

# Mapping: English filename (without .mp3) → Khmer text to speak
NAMES = {
    "makara_sothea":           "មករា សុធា",
    "sopheap_vichea":          "សុភាព វិជ្ជា",
    "ratanak_dara":            "រតនៈ ដារា",
    "chenda_vann":             "ចន្ទា វ៉ាន់",
    "boknarith_sovan":         "បុកនរិទ្ធ សុវណ្ណ",
    "haha_chi_devit_mak_mok_yok": "ហាហាជីដេវីត ម៉ាក់មកយក",
}

# Khmer voices available in edge-tts:
#   km-KH-PisethNeural  (Male)
#   km-KH-SreymomNeural (Female)
# Change VOICE to any voice from `edge-tts --list-voices`
VOICE = "km-KH-PisethNeural"


async def generate_voice(filename_stem: str, text: str) -> None:
    filename = filename_stem + ".mp3"
    output_path = os.path.join(VOICES_DIR, filename)

    if os.path.exists(output_path):
        print(f"[SKIP]  {filename} already exists.")
        return

    print(f"[GEN]   Generating '{text}' → {filename}  (voice: {VOICE})")
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_path)
    print(f"[DONE]  Saved {output_path}")


async def main() -> None:
    os.makedirs(VOICES_DIR, exist_ok=True)

    tasks = [generate_voice(stem, text) for stem, text in NAMES.items()]
    await asyncio.gather(*tasks)

    print("\nAll done! Files in voices/:")
    for f in sorted(os.listdir(VOICES_DIR)):
        if f.endswith(".mp3"):
            size = os.path.getsize(os.path.join(VOICES_DIR, f))
            print(f"  {f}  ({size:,} bytes)")


if __name__ == "__main__":
    asyncio.run(main())
