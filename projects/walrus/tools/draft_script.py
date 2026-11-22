"""DRAFT script for 'Why Polar Bears Throw Rocks at Walruses'. Generates narration_en.txt and shot_plan.json
from one beat list so the two always match word for word. For review/approval before production."""
import json, re
from pathlib import Path
P = Path(__file__).resolve().parents[1]
CH = [
 ('1 — The paradox', [
  ("A polar bear stands on a ridge of ice above the shore. Below it, a walrus lies asleep on the stones.", "AI illustration: walrus_ai_01_bear_ridge_ice (slow Ken Burns). Low drone."),
  ("The bear lifts a heavy block of ice in its front paws.", "AI illustration: walrus_ai_06_bear_lifts_ice (slow push in)."),
  ("It takes aim, and throws it at the walrus's head. Then it waits to see whether the giant below will move again.", "Animated diagram: ice block arc from ridge to walrus head. [1 s — pause]"),
  ("For more than a century, Inuit hunters in Greenland and the Canadian Arctic have described scenes like this one. Hunters who knew the ice better than anyone said they had seen it with their own eyes.", "Wide Arctic coast, sea ice and snow."),
  ("And for just as long, many scientists treated those stories as legends. Nobody had filmed it, and nobody had measured it.", "Pack ice from a ship's bow, grey light."),
  ("Because it makes no sense.", "Black screen. Music stops. [2 s — pause]"),
  ("The polar bear is the largest predator that lives on land. It can kill a seal with a single blow. Its paws are as wide as dinner plates, and its sense of smell can find a seal under a metre of snow.", "Polar bear walking on sea ice (USGS)."),
  ("So why would the most powerful hunter in the Arctic ever need a weapon?", "Polar bear collar-cam POV on the ice (USGS). [2 s — pause]"),
  ("The answer is lying on that beach. And it weighs more than a tonne.", "Title card: WHY POLAR BEARS THROW ROCKS AT WALRUSES. [2 s — pause]"),
 ]),
 ('2 — A fortress with tusks', [
  ("To understand the problem, look at the two animals side by side. On paper, the bear should win every time.", "Walrus herd close (USGS haul-out)."),
  ("A large male polar bear can weigh around six hundred kilograms. A large male walrus can weigh more than twice as much.", "Size graphic: walrus / polar bear / human."),
  ("A walrus is not a seal. It is closer to a fortress. Even its body is built for conflict.", "Walruses resting on a beach, tusks visible (USGS)."),
  ("Its skin can be several centimetres thick on the neck and shoulders. Under the skin lies a deep layer of blubber, and under that, heavy muscle.", "Diagram: skin, blubber, muscle cutaway."),
  ("Claws and teeth that open a seal in seconds barely get through. The thickest skin covers exactly the places where rival males strike each other with their tusks during the breeding season.", "Diagram continues: claw marks stopping in the blubber."),
  ("And then there are the tusks. They are canine teeth that never stop growing, and in a big male they can approach a metre in length.", "Diagram: walrus skull with tusks."),
  ("A walrus uses them to haul itself out of the water, to fight its rivals, and to defend itself.", "Walrus hauling out with its tusks (USGS tracking footage)."),
  ("For a bear, attacking an adult walrus head on is not hunting. It is a gamble with its own life.", "Polar bear watching from the ice. [1 s — pause]"),
 ]),
 ('3 — Life on the ice', [
  ("Pacific walruses spend much of the year on the drifting sea ice of the Bering and Chukchi seas. They follow the ice as it grows in winter and shrinks in summer.", "Map: Chukchi Sea, Wrangel Island, Alaska."),
  ("The ice is their raft. They rest on it between dives, give birth on it, and ride it north as it melts each summer.", "Aerial ice floes (Mixkit)."),
  ("Below the ice lies one of the richest seafloors on Earth: a shallow continental shelf covered with clams, worms and snails.", "Icy water, light from above; seals swimming among ice."),
  ("There, walruses gather by the thousands, pressed together, tusks resting on each other's backs. On a single floe, hundreds of animals can lie side by side, steaming in the cold air.", "Dense walrus haul-out (USGS)."),
  ("For a walrus, a crowd means safety. Every animal is another pair of eyes, and another pair of tusks.", "Walrus herd, slow pan."),
  ("For a polar bear, a crowd is a wall. And yet, every year, some bears try to break through it.", "Polar bear at the edge of the ice, looking out. [2 s — pause]"),
  ("Most of the time, polar bears hunt seals, waiting beside a breathing hole in the ice for hours until one comes up for air. Walruses are something else entirely: bigger, rarer, and far more dangerous.", "Polar bear waiting on sea ice (USGS collar footage)."),
 ]),
 ('4 — Svalbard, 2015', [
  ("In July 2015, on a beach in Svalbard, a photographer filmed a hungry polar bear and her cub approaching a herd of sleeping walruses.", "AI illustration: walrus_ai_02_bear_sniffs_walrus (slow Ken Burns)."),
  ("The bear did not charge. She walked slowly among them, sniffing one walrus after another. Most of the walruses barely moved.", "Animated diagram: bear path weaving through a sleeping herd (top view)."),
  ("Scientists who studied the footage suggested she was testing them, looking for one that was weak, sick, or already dead. A healthy adult walrus was simply too dangerous to attack.", "AI illustration: walrus_ai_02_bear_sniffs_walrus, closer framing."),
  ("Then she touched one with her paw.", "Diagram: paw touch, walrus head lifting."),
  ("The walrus woke up. And it was the bear that backed away. A predator weighing hundreds of kilograms had retreated from an animal that had only lifted its head.", "Generic walrus raising its head (USGS). [2 s — pause]"),
  ("Without a meal, experts feared that the cub would not survive for long.", "Polar bear walking away over broken ice (USGS). [1 s — pause]"),
 ]),
 ('5 — Wrangel Island, 1990', [
  ("To see what really happens between the two species, scientists went to Wrangel Island, in the Russian Arctic. The island is a nature reserve, sometimes called the maternity ward of the polar bear, because so many females dig their dens there.", "Map: Wrangel Island, haul-out beach marked."),
  ("In the autumn of 1990, the Russian biologists Nikita Ovsyanikov and Anatoly Kochnev watched the island's walrus haul-outs, day after day.", "Grey Arctic coast, wind and snow."),
  ("Thousands of walruses crowded onto the beaches. And the bears came too, sometimes dozens of them. When the sea ice drifted away in autumn, many bears were left on the island with little else to eat.", "AI illustration: walrus_ai_04_wrangel_beach (slow Ken Burns)."),
  ("The bears did not attack the herd from the front. They walked along its edge, watching. Some lay down near the walruses for hours, as if they were waiting for a signal.", "Polar bear walking along a shoreline (USGS)."),
  ("They were waiting for one thing: the moment the herd would panic.", "Slow push on the crowded beach. [2 s — pause]"),
 ]),
 ('6 — When the walrus fights back', [
  ("When a bear comes too close, an adult walrus does not run. It turns to face it. Its size, which makes it slow on land, suddenly becomes its greatest strength.", "AI illustration: walrus_ai_03_walrus_lunges (slow Ken Burns)."),
  ("It raises its head, opens its mouth, and swings its tusks.", "AI illustration: walrus_ai_03_walrus_lunges, closer framing."),
  ("A single strike can drive a tusk deep into a bear's neck or shoulder. And unlike a bear, the walrus does not need to win the fight. It only needs to make the attacker give up.", "Diagram: bear wound zones (neck, shoulder, chest)."),
  ("Polar bears have been seriously injured, and even killed, by walruses defending themselves.", "Polar bear resting on the ice (USGS)."),
  ("On Wrangel Island, the observers counted the attacks. Every approach, every charge, every retreat.", "Walrus herd on the beach (USGS)."),
  ("Eleven of them were attacks on adult walruses. Bears charged, circled and tested them, sometimes again and again.", "Text card: ADULTS: 0 / 11."),
  ("Not one of those adults was killed.", "Text card holds. [2 s — pause]"),
  ("The bears seemed to know it. Most of them avoided adult walruses altogether, and turned their attention to something smaller.", "Polar bear walking away along the shore (USGS)."),
 ]),
 ('7 — The stampede', [
  ("So the bears use another strategy. They do not attack the walrus. They attack the crowd.", "Polar bear approaching over the ice (USGS)."),
  ("A bear runs toward the herd. Panic spreads, and thousands of animals rush for the water at the same time. Walruses that weigh more than a tonne climb over each other to reach the sea.", "AI illustration: walrus_ai_05_stampede, cropped to the herd (slow Ken Burns). Tense music."),
  ("In the chaos, the smallest animals are knocked over, pinned and crushed. Young walruses, separated from their mothers, are caught under animals many times their weight.", "Wide shot: crowded haul-out moving toward the sea (USGS). No close-ups."),
  ("That is when the bears move in. Not on the giants, but on the calves.", "AI illustration: walrus_ai_05_stampede, second framing."),
  ("In one season of observations, the scientists recorded about twenty-five hunting attempts. Only two ended in a kill. Both were calves.", "Text card: 25 ATTEMPTS → 2 KILLS → BOTH CALVES."),
  ("Far more walruses died in the stampedes themselves.", "Empty grey beach, waves (wide)."),
  ("Of the walrus carcasses examined on the island's beaches, around forty-three percent were calves.", "Text card: ~43% OF CARCASSES = CALVES."),
  ("For the bear, the stampede is a weapon of its own. But it is not the only one.", "Slow push on the waves. [2 s — pause]"),
 ]),
 ('8 — The weapon', [
  ("But some stories describe something stranger.", "AI illustration: walrus_ai_01_bear_ridge_ice, different framing."),
  ("In 2021, three of the most experienced polar bear scientists in the world, Ian Stirling, Kristin Laidre and Erik Born, published a study in the journal Arctic.", "Text card: STIRLING, LAIDRE & BORN — ARCTIC, 2021."),
  ("They gathered Inuit accounts and historical reports from Greenland and the Canadian Arctic, going back more than a century. Some came from hunters, some from explorers, some from naturalists who had spent their lives on the ice.", "Greenland-style coast, ice and cliffs."),
  ("Again and again, the stories described the same scene: a bear picking up a block of ice or a stone, and throwing it at the head of a walrus.", "AI illustration: walrus_ai_06_bear_lifts_ice (slow Ken Burns)."),
  ("The target is always the same. The head. It is where a stunned walrus can no longer fight back. Elsewhere, the walrus is protected by skin, blubber and muscle. The skull is the one place where a heavy blow can do real damage.", "Animated diagram: thrown stone aimed at the head."),
  ("The scientists also pointed to a young male polar bear named GoGo, at a zoo in Osaka, Japan.", "Animated diagram: zoo enclosure, food hanging out of reach."),
  ("Faced with food hung out of his reach, GoGo threw sticks and other objects at it until it fell.", "Diagram continues: stick thrown, food drops."),
  ("Using a tool is rare in the animal world. Chimpanzees fish for termites with sticks, sea otters crack shells on stones, and some crows bend twigs into hooks. Among large predators, it is almost unheard of.", "Animated diagram: icons of tool-using animals."),
  ("The authors concluded that tool use by wild polar bears is probably rare. But it is likely real, and it seems to appear in one situation above all: when the prey is a walrus.", "Polar bear on sea ice, slow push (USGS)."),
  ("Not every scientist agrees. Some argue that stories, however many, are not enough evidence.", "Ice and snow, grey light."),
  ("But if the accounts are right, the polar bear is one of very few mammals that uses a tool to hunt.", "Polar bear collar-cam on the ice (USGS). [2 s — pause]"),
 ]),
 ('9 — Whiskers and clams', [
  ("To understand why a walrus is worth that risk, follow it to the bottom of the sea.", "Seals swimming in icy water (Mixkit). Lighter, curious music."),
  ("A walrus feeds in the dark, in mud and silt, often dozens of metres down. It can stay underwater for up to half an hour, searching the bottom with its face.", "Underwater light, particles in green water."),
  ("It finds its food by touch. Its snout carries hundreds of thick, sensitive whiskers, able to feel the shape of a clam buried in the mud.", "AI illustration: walrus_ai_07_whiskers_clams (slow Ken Burns)."),
  ("Then it uses its tongue like a piston. It pulls it back sharply, creating a powerful suction that pulls the clam right out of its shell.", "Diagram: tongue as a piston, clam sucked out."),
  ("A walrus can also blow jets of water into the seafloor to uncover its prey.", "AI illustration: walrus_ai_07_whiskers_clams, closer framing."),
  ("In a single feeding trip, one walrus can eat three thousand to six thousand clams. It does not crush the shells. It leaves them almost untouched on the seafloor, emptied.", "Text card: 3,000–6,000 CLAMS IN ONE MEAL."),
  ("All that food becomes blubber. And blubber is exactly what a polar bear needs.", "Polar bear on the ice (USGS). [1 s — pause]"),
 ]),
 ('10 — Mothers', [
  ("A walrus calf is born on the ice in spring, and it stays with its mother for about two years. It drinks her milk for more than a year, long after it has learned to swim.", "AI illustration: walrus_ai_08_mother_calf (slow Ken Burns). Warmer music."),
  ("When danger comes, the mother dives with her calf, holds it against her body, or carries it on her back in the water.", "AI illustration: walrus_ai_08_mother_calf, closer framing."),
  ("Walrus mothers have been seen placing themselves between their calf and a bear. Other females in the herd sometimes help, forming a living barrier of bodies and tusks.", "Walrus herd at the water's edge (USGS)."),
  ("And that is why a stampede is so dangerous. In the panic, a mother can lose her calf, and the calf can be trampled by its own herd.", "Wide crowded haul-out (USGS). [2 s — pause]"),
 ]),
 ('11 — Songs under the ice', [
  ("Walruses are not only fighters. They are also surprisingly musical. Much of their life happens in sound.", "Icy water surface, soft light. Lighter music."),
  ("In winter, males sing underwater for hours, with knocks, taps and long, bell-like tones. The sound can carry far through the cold water.", "Underwater light through ice."),
  ("Each male's song is his own, repeated again and again to attract females and to warn rivals.", "Seals swimming in a frozen sea (Mixkit), generic marine life."),
  ("On land, walruses snort, roar and grumble. A mother and her calf can recognise each other's voices.", "Walrus herd close, heads moving (USGS)."),
  ("It is a society built on sound and touch, packed tightly together on the ice.", "Walrus herd from above (USGS). [1 s — pause]"),
 ]),
 ('12 — The lost ice', [
  ("For thousands of years, this system worked.", "Aerial ice floes (Mixkit). Sober music."),
  ("In summer, the ice edge retreated north, but it stayed above the shallow shelf, where walruses could rest on the ice and dive straight down to their food.", "Diagram: ice edge over the shallow shelf."),
  ("Now, in many summers, the ice melts back past the edge of the shelf, over water that is thousands of metres deep.", "Diagram continues: ice edge retreating past the shelf break."),
  ("A walrus cannot feed that deep. It has to choose: stay on the ice and go hungry, or swim to the coast. Every trip between the coast and the feeding grounds costs energy, and calves pay the highest price.", "Melting ice in the sea (Mixkit)."),
  ("Since 2007, the summer ice has retreated beyond the shelf in most years. What was once rare has become normal.", "Glacier ice melting into the ocean (Mixkit)."),
  ("And so tens of thousands of walruses now come ashore in Alaska and Russia, often far from where they feed.", "Walrus haul-out on a beach (USGS). [2 s — pause]"),
 ]),
 ('13 — The crowded beaches', [
  ("In September 2014, near the village of Point Lay, Alaska, about thirty-five thousand walruses crowded onto a single beach.", "Map and card: POINT LAY, ALASKA — ~35,000 WALRUSES."),
  ("Crowds like this are exactly what the bears of Wrangel Island learned to exploit.", "AI illustration: walrus_ai_04_wrangel_beach, different framing."),
  ("In 1991, a single stampede on Wrangel Island left one hundred and four walruses trampled to death. Most of them were young.", "Text card: WRANGEL 1991 — 104 TRAMPLED. Tense music."),
  ("Today, a stampede can be started by a bear, by a low-flying aircraft, by a boat, or even by a person walking on the beach.", "Wide crowded haul-out (USGS), no close-ups."),
  ("In 2009, at Icy Cape in Alaska, scientists found more than one hundred young walruses crushed after a single stampede.", "Empty Alaskan coast, grey sea (wide)."),
  ("Villages near the haul-outs now ask pilots to fly high, and visitors to keep their distance. Some communities even close their beaches during the haul-out season.", "Aerial coast with ice (Mixkit)."),
  ("And the bears are still there. Pushed ashore by the same melting ice, they walk the beaches, hungry.", "Polar bear walking on land and ice (USGS)."),
  ("Some of them may still pick up a block of ice.", "AI illustration: walrus_ai_06_bear_lifts_ice, closer framing. [2 s — pause]"),
 ]),
 ('14 — Conclusion', [
  ("Today there are an estimated two hundred and fifty thousand Pacific walruses.", "Text card: PACIFIC WALRUS ~250,000."),
  ("The species is listed as Vulnerable by the IUCN.", "Text card: IUCN — VULNERABLE."),
  ("Scientists now count walruses from the air with drones and aircraft, and follow them with satellite tags, to understand how they are adapting to a changing sea.", "USGS walrus tracking footage (tagging, aerial survey)."),
  ("Their future depends on the sea ice, and on how much of it is left over the shallow seas where they feed. The polar bear depends on that ice too. Without it, both animals are pushed onto the same narrow strip of land.", "Ice floes drifting (Mixkit)."),
  ("We often imagine the Arctic as a place of simple strength, where the biggest animal always wins.", "Polar bear on the ice, wide (USGS)."),
  ("But the walrus shows us a different picture.", "Walrus herd at rest (USGS)."),
  ("Here, the largest predator on land sometimes needs patience, a crowd in panic, or a block of ice. It needs a plan.", "Montage: bear on ridge, stampede, ice block (AI and footage)."),
  ("Not because the bear is weak. But because the walrus is that strong.", "Slow push on a walrus at rest. [3 s — pause]"),
  ("If you enjoyed this film, subscribe to Naturexplore for a new documentary every week. And tell us in the comments: would you have guessed the rock?", "End card with two suggested videos."),
 ]),
]
beats, lines, t = [], [], 0.0
WPS = 2.25  # ~135 words per minute
for ch, bl in CH:
    lines.append(f'## {ch}\n')
    for vo, vis in bl:
        m = re.search(r'\[(\d+) s — pause\]', vis)
        beats.append({'chapter': ch, 'time': f'{int(t // 60)}:{int(t % 60):02d}', 'voice_over': vo, 'visual': vis})
        t += len(vo.split()) / WPS + 0.5 + (int(m.group(1)) if m else 0)
        lines.append(vo)
    lines.append('')
(P/'narration_en.txt').write_text('\n'.join(lines), encoding='utf-8')
json.dump(beats, open(P/'shot_plan.json', 'w'), indent=1, ensure_ascii=False)
words = sum(len(b['voice_over'].split()) for b in beats)
print(len(CH), 'chapters,', len(beats), 'beats,', words, 'words, est.', f'{int(t // 60)}:{int(t % 60):02d}')
