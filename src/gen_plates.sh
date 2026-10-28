#!/bin/bash
# Generate Ep002 plates as asset tests (z-ai image, 1344x768) — prompts from assets/prompts.md
set -e
RAW=/home/z/my-project/pluto-never-one-of-us/assets/raw
mkdir -p "$RAW"
cd "$RAW"

gen() {
  local name="$1"; shift
  local prompt="$1"; shift
  if [ -s "$name.png" ]; then echo "SKIP $name (exists)"; return 0; fi
  echo "== generating $name =="
  z-ai image -p "$prompt" -o "$name.png" -s 1344x768 || { echo "FAIL $name"; return 1; }
  echo "OK $name"
}

gen plate-a-pluto-hero "Vintage 19th-century natural history lithograph plate of the dwarf planet Pluto, antique astronomy illustration in flat printed inks: a small pale tan and cream sphere with subtle mottled surface patches and a faint lighter heart-shaped region, drawn with clean engraved contour lines and a visible halftone print dot pattern, soft painted drop shadow beneath the sphere as if it lies pinned on a museum sheet. The planet sits large in the right two-thirds of the image; generous quiet empty aged cream ledger paper fills the left third, top and bottom margins. Faint horizontal ledger rules and light foxing stains in the paper, warm ochre and pale ice-blue duotone with cream highlights. Wide landscape composition. No text, no letters, no numbers anywhere."

gen plate-b-lineup "Vintage 19th-century astronomy lithograph diagram plate of the solar system, antique scientific illustration in flat printed inks with a visible halftone dot pattern: nine small planets arranged in a loose vertical column along the right third of the image, each drawn as a small engraved sphere with subtle surface detail - banded Jupiter, ringed Saturn, blue Neptune, and tiny Pluto drawn last with a faint heart patch on it - with generous quiet empty aged cream ledger paper on the left third and in the margins. Faint horizontal ledger rules and light foxing stains in the paper, warm ochre duotone with muted planet colours. Wide landscape composition. No text, no letters, no numbers anywhere."

gen plate-c-observatory "Vintage 19th-century lithograph illustration of a small astronomical observatory dome with a long refracting telescope pointed into a corner of starry night sky, antique scientific illustration in flat printed inks with a visible halftone dot pattern: one small human figure silhouetted at the eyepiece, telescope and dome large in the right half of the image, generous quiet empty aged cream ledger paper on the left third. Faint horizontal ledger rules and light foxing stains in the paper, warm ochre and sepia duotone, deep indigo ink reserved for the sky corner only. Wide landscape composition. No text, no letters, no numbers anywhere."

gen plate-d-orbit-xray "Dark X-ray scientific plate of the outer solar system seen from directly above, on a near-black deep emerald-green ground: the Sun drawn as a small glowing dot far to the left, planetary orbits as thin luminous cream ellipse lines, and one eccentric stretched orbit tilted at a steep angle crossing inside a neighbouring orbit, drawn brighter than the rest, with a small pale dwarf planet dot sitting on it circled by one thin verdict-red targeting ring. A column of small film-sprocket rectangles runs down the right edge like a strip of film. Vintage specimen-file print aesthetic, halftone dot texture, restrained cream and red diagram accents on darkness. Wide landscape composition. No text, no letters, no numbers anywhere."

gen plate-e-eris "Vintage 19th-century natural history lithograph plate of a distant icy dwarf planet, antique astronomy illustration in flat printed inks: a small silver-white and pale blue mottled sphere with faint frost streaks, drawn with clean engraved contour lines and a visible halftone dot pattern, soft painted drop shadow beneath the sphere as if pinned on a museum sheet. The sphere sits in the right two-thirds of the image; generous quiet empty aged cream ledger paper fills the left third and margins. Faint horizontal ledger rules and light foxing stains, cold silver-blue duotone on warm cream paper. Wide landscape composition. No text, no letters, no numbers anywhere."

gen plate-f-kuiper-xray "Dark X-ray scientific plate of a vast belt of icy bodies seen from directly above, on a near-black deep emerald-green ground: hundreds of small glowing cream dots and tiny engraved ice chunks scattered in a wide diagonal band across the frame, like a crowded donut of frozen debris; one dot near the centre-right rendered slightly larger with a faint heart-shaped patch, circled by one thin verdict-red targeting ring. A column of small film-sprocket rectangles runs down the right edge like a strip of film. Vintage specimen-file print aesthetic, halftone dot texture, restrained cream and red accents on darkness. Wide landscape composition. No text, no letters, no numbers anywhere."

gen plate-g-heart-xray "Dark X-ray scientific plate of the dwarf planet Pluto seen from directly above, on a near-black deep emerald-green ground: the planet as a large pale translucent ghost sphere with faint mottled terrain patches, its heart-shaped region rendered as a glowing bright cream heart blazing through the surface with a soft radiant glow, nitrogen glacier texture hinted inside the glow. Thin crosshair hairlines cross the planet, a column of small film-sprocket rectangles runs down the right edge like a strip of film, and one thin verdict-red targeting ring circles the heart. Vintage specimen-file print aesthetic, halftone dot texture, restrained cream and red accents on darkness. Wide landscape composition, planet large in the right two-thirds, quiet dark ground on the left third. No text, no letters, no numbers anywhere."

echo "ALL PLATES DONE"
