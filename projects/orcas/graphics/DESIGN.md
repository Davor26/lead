# Orcas: The Ocean's Wolf Packs — graphics design

## Style Prompt
Calm, cinematic nature-documentary graphics for the Naturexplore channel. Deep cold-ocean
backgrounds with a soft radial light from above, as if seen from below the surface. Simple
flat silhouettes (orca, seal, shark, whale) in ice-white, one warm amber accent that marks
the single thing the narration is pointing at. Diagrams are sparse: one idea per beat,
large numbers, few words, slow confident motion. Nothing graphic or violent: predation is
shown as positions and arrows, never wounds or blood.

## Colors
- `--deep`   #0A1C24 — background (deep water), used on every graphic
- `--mid`    #12313D — secondary surfaces, map seas, shallow-water glow
- `--ice`    #EEF2EC — foreground text and silhouettes (ice-white, tinted)
- `--mist`   #93ABB1 — secondary labels, inactive elements
- `--amber`  #E9A23B — the one accent: the highlighted value, the chosen prey, the key fin

## Typography
- **Fraunces** (serif) — statements, titles, chapter cards. 900 for titles, 300 for subtitles.
  Tracking -0.03em on display sizes.
- **IBM Plex Mono** — data, numbers, labels, dates, scientific names' annotations.
  The tension: the warm human voice of the story vs. the cool measured voice of the science.

## Motion
- Slow and sure: entrances 0.6–1.2 s, eases `power3.out`, `expo.out`, `sine.inOut`.
- Numbers count up with `tabular-nums`. Lines draw on. Silhouettes glide in from the water.
- Ambient: radial light breathes slowly (scale 1 → 1.06), faint caustic drift.
- Each graphic is a single scene: fade in from black over 0.4 s, hold, fade to black over
  0.4 s at the end (it is cut into the film like a shot).

## What NOT to Do
- No blood, wounds, bite marks or carcasses — the blue-whale and shark beats stay abstract.
- No cyan neon, no purple/blue gradients, no gradient text, no full-screen linear gradients.
- No logos or branding of BBC, National Geographic, Netflix, OceanX, Project ORCA, TV channels.
- No invented figures: every number on screen is spoken in the narration.
- No chart furniture: no gridlines, ticks, legends, pie charts.
