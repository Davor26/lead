"""DRAFT script for 'Why Humpback Whales Save Other Animals From Orcas'. Generates narration_en.txt and shot_plan.json
from one beat list so the two always match word for word. For review/approval before production."""
import json, re
from pathlib import Path
P = Path(__file__).resolve().parents[1]
CH = [
 ('1 — The rescue', [
  ("Antarctica, 2009. A Weddell seal lies on a small raft of ice. Around it, the water is moving.", "AI illustration hb_ai_01 (seal on ice floe, orca fins around) if supplied, otherwise diagram: floe, seal, fins. Slow Ken Burns. Low drone."),
  ("A group of killer whales swims side by side towards the floe. At the last moment, they dive together, and a wave rolls across the ice.", "Animated diagram: orcas line up, dive, wave washes over the floe."),
  ("The seal slides into the sea. It should be the end of the story.", "Diagram continues: seal in the water. [1 s — pause]"),
  ("But a few metres away, a humpback whale rolls onto its back. The seal is swept up onto its huge chest, between its two long flippers.", "AI illustration hb_ai_02 (seal on humpback chest) if supplied, otherwise diagram: humpback belly-up, seal on its chest."),
  ("When the seal begins to slip, the whale lifts it back with a flipper. A few moments later, the seal swims to another floe, out of reach.", "Diagram continues: flipper nudge, seal escapes to a floe."),
  ("Two scientists in a small boat watched the whole scene. They could hardly believe what they had seen.", "Research boat on the open ocean (NOAA)."),
  ("Because it makes no sense.", "Black screen. Music stops. [2 s — pause]"),
  ("A humpback whale does not eat seals. It does not need them, and it does not know them. Yet it had just put itself between a pack of killer whales and their prey.", "Humpback whale underwater (NOAA)."),
  ("And it was not the only one.", "Title card: WHY HUMPBACK WHALES SAVE OTHER ANIMALS FROM ORCAS. [2 s — pause]"),
 ]),
 ('2 — The giant with wings', [
  ("To understand this story, start with the whale itself.", "Humpbacks surfacing, aerial (Commons, Adam Fish)."),
  ("An adult humpback can be around fifteen metres long and weigh thirty tonnes or more. That is heavier than five adult orcas put together.", "Size graphic: humpback / orca / human."),
  ("Its scientific name, Megaptera, means big wings. Its flippers can be up to five metres long, almost a third of its body. No other whale has flippers like them.", "Diagram: humpback silhouette, flipper length highlighted."),
  ("The edges of those flippers are covered in bumps, and often in sharp barnacles. A blow from one of them can cut skin.", "Humpback flipper slapping the surface (NOAA)."),
  ("Its tail, the fluke, can be five metres wide. Each tail has its own pattern of black and white, like a fingerprint.", "Humpback tail lifted out of the water (Commons, tail sailing)."),
  ("Humpbacks eat small fish and krill. They spend their summers feeding in cold waters, then travel thousands of kilometres to warm seas to give birth.", "Whales on the Pacific coast (NOAA)."),
  ("In the breeding season, males sing. Their songs can last for twenty minutes, and be repeated for hours, carrying for kilometres through the water.", "Humpback underwater (NOAA). Music thins."),
  ("They are gentle giants, slow and patient. But they are not defenceless.", "Humpback mother and calf from the air (Commons). [1 s — pause]"),
 ]),
 ('3 — The wolves of the sea', [
  ("On the other side of this story is the most successful predator in the ocean.", "Orcas surfacing together (NOAA)."),
  ("The killer whale, or orca, is not really a whale but the largest member of the dolphin family. A big male can reach eight or nine metres and weigh several tonnes.", "Orca from the air, drone view (NOAA)."),
  ("Orcas live in family groups called pods, led by older females. They hunt together, and they plan together.", "Orca pod travelling, aerial (NOAA)."),
  ("Their tactics are passed from mother to calf, generation after generation, like a culture.", "Orca mother and young surfacing (NOAA)."),
  ("They see well, hear even better, and use echolocation, clicks that bounce off objects, to find their way and their prey in dark water.", "Diagram: echolocation clicks from an orca's head."),
  ("Different pods have their own sounds, like accents. Some hunt fish, others hunt seals, others chase sharks or even large whales.", "Orcas surfacing near a research ship (NOAA)."),
  ("No animal in the sea hunts them. That is why they are called the wolves of the sea.", "Orca dorsal fins cutting the surface (NOAA)."),
  ("But not all orcas hunt the same thing. And that detail is the key to the whole mystery.", "Orcas surfacing, slow motion (NOAA). [2 s — pause]"),
 ]),
 ('4 — Two kinds of hunters', [
  ("In the North Pacific, scientists recognise different types of killer whales. They share the same waters, but they almost never mix.", "Map: North Pacific coast, two orca types."),
  ("Some eat only fish, mostly salmon. They travel in large, noisy family groups and call to each other all day long.", "Orcas surfacing near a research ship (NOAA)."),
  ("Others hunt only mammals: seals, sea lions, porpoises, and the calves of large whales. They are often called Bigg's killer whales, or transients.", "Orcas in Alaska (NOAA)."),
  ("Mammal hunters move in small groups, and they hunt in silence. Their prey can hear them, so they say nothing until the attack begins.", "Diagram: two orca types side by side, prey icons."),
  ("And here is the first surprise. Humpbacks largely ignore the fish-eating orcas, even when they swim right past them.", "Humpbacks and orcas in the same water, wide (NOAA)."),
  ("But when mammal-eating orcas start a hunt, humpbacks often come towards them, sometimes from far away.", "Diagram: humpbacks converging on an orca hunt. [1 s — pause]"),
 ]),
 ('5 — Antarctica, 2009', [
  ("The scientists in that boat in 2009 were Robert Pitman and John Durban. They were studying killer whales off the Antarctic Peninsula.", "Text card: ANTARCTIC PENINSULA, 2009."),
  ("Here, at the bottom of the world, the sea is full of floating ice. Seals haul out on the floes to rest, safe from leopard seals and orcas in the water. At least, that is the idea.", "Text card over grey sea: SOUTHERN OCEAN."),
  ("The orcas they followed specialise in seals resting on ice floes. They find a seal, look at it, then work as a team to make a wave that washes it off.", "Map: Antarctic Peninsula."),
  ("That day, two humpback whales were swimming nearby. Each time the orcas closed in, the humpbacks came between them and the seal.", "Diagram: floe, seal, two humpbacks, orca pod."),
  ("When the seal ended up on the humpback's chest, the whale stayed on its back, with its belly above the water, holding the seal out of the sea.", "AI illustration hb_ai_02, closer framing, if supplied, otherwise diagram."),
  ("The humpbacks were bellowing and slapping the water with their flippers and tails. The killer whales gave up and swam away.", "Humpback slapping the water with its flipper (NOAA)."),
  ("Pitman later wrote that it looked like a rescue. But one strange event proves nothing. He wanted to know if it happened again.", "Research ship at sea (NOAA). [2 s — pause]"),
 ]),
 ('6 — Monterey Bay, 2012', [
  ("Three years later, and half a world away, it happened again.", "Map: Monterey Bay, California."),
  ("Every spring, gray whale mothers swim north along the coast of California with their calves, from the lagoons of Mexico to the feeding grounds of the Arctic.", "Gray whales off the coast (NOAA)."),
  ("Monterey Bay is a dangerous place for them. Its deep underwater canyon comes close to shore, and mammal-eating orcas know it.", "Diagram: Monterey Bay canyon and the migration route."),
  ("In May 2012, in Monterey Bay, California, a group of mammal-eating orcas separated a gray whale calf from its mother.", "Gray whales at the surface, wide (NOAA)."),
  ("The calf did not survive. We will not show that moment.", "Grey sea, distant blows (NOAA). Music low."),
  ("But what happened next amazed the people watching. Humpback whales arrived, first a pair, then more.", "AI illustration hb_ai_03 (humpbacks gathering near orcas) if supplied, otherwise diagram."),
  ("They placed themselves around the place where the calf had died. They trumpeted, a loud call blown through the blowhole, and slapped the water with their tails.", "Humpback tail slapping (NOAA)."),
  ("For more than six hours, they stayed. And for all that time, the orcas had trouble feeding.", "Humpbacks surfacing together, aerial (Commons)."),
  ("The humpbacks could not save the calf. Yet they did not leave. To the observer, Alisa Schulman-Janiger, it looked like they were standing guard.", "Humpback at the surface, slow push. [2 s — pause]"),
 ]),
 ('7 — One hundred and fifteen encounters', [
  ("Stories like these are hard to trust on their own. So Robert Pitman and his colleagues began to collect them.", "Researchers on a ship with binoculars (NOAA)."),
  ("They gathered reports from scientists, whale-watching crews and photographers. Some went back more than sixty years.", "Diagram: map of the world filling with report points."),
  ("In 2017, they published their results. They had found one hundred and fifteen interactions between humpback whales and killer whales.", "Text card: 115 ENCOUNTERS — PITMAN ET AL., 2017."),
  ("In most of them, it was the humpbacks that approached the orcas, not the other way round.", "Diagram: arrows, humpbacks moving towards orcas."),
  ("And in almost every case where the type of orca was known, they were mammal hunters. The humpbacks were not reacting to orcas in general. They were reacting to hunts.", "Diagram: bar, mammal hunters vs fish eaters."),
  ("Some of these encounters lasted minutes. Some lasted for hours.", "Humpback blowing at the surface (NOAA). [1 s — pause]"),
 ]),
 ('8 — Who gets saved', [
  ("The study listed at least ten different prey species that humpbacks appeared to defend, across the Pacific, the Atlantic and the Southern Ocean.", "Map: three oceans, report points."),
  ("Then came the most surprising result of all. The scientists looked at what the orcas had been hunting each time.", "Graphic: prey species counter."),
  ("Sometimes it was a humpback calf. But that was rare.", "Humpback mother and calf (Commons)."),
  ("In about nine cases out of ten where the prey could be identified, it was another species.", "Graphic: 9 / 10 — ANOTHER SPECIES."),
  ("Harbour seals.", "Harbour seals on the Pacific coast (NOAA)."),
  ("California sea lions.", "California sea lions (NOAA)."),
  ("Steller sea lions, gray whale calves, porpoises, and even an ocean sunfish.", "Graphic: silhouettes of the prey species appear one by one."),
  ("A sea lion brings the humpback nothing. A sunfish brings it nothing. Yet the whales came anyway, and sometimes they stayed long after the prey had escaped.", "Seal swimming underwater (NOAA, monk seal). [2 s — pause]"),
 ]),
 ('9 — Scars on the tail', [
  ("To understand why, look closely at the underside of a humpback's tail.", "Humpback fluke lifted, slow motion (NOAA)."),
  ("Many of them carry parallel white lines. These are rake marks, left by the teeth of killer whales.", "Diagram: fluke with parallel rake marks."),
  ("In some populations, up to about a third of adult humpbacks carry these scars.", "Graphic: 1 IN 3 (some populations)."),
  ("Most of the scars seem to be made when the whales are young, often during their first long migration.", "Humpback mother and calf swimming (Commons)."),
  ("A humpback calf is small, slow, and far from home. For mammal-eating orcas, it is one of the most valuable prey in the ocean.", "AI illustration hb_ai_04 (mother shielding calf from orcas) if supplied, otherwise diagram."),
  ("Off the coast of Western Australia, scientists have watched mammal-eating orcas follow humpback mothers and calves for hours along their migration route.", "Map: Western Australia migration route."),
  ("A mother defends her calf by keeping it close, often above her own back or tucked beside her flipper, and turning her tail towards the attackers.", "Humpback mother and calf from the air (Commons)."),
  ("So every adult humpback alive today has survived a world full of killer whales. Many of them have met orcas up close, and remember it.", "Humpback underwater (NOAA). [1 s — pause]"),
 ]),
 ('10 — How a humpback fights', [
  ("A humpback has no teeth. It cannot bite. So how does it fight a predator built to kill?", "Humpback surfacing beside a boat (NOAA)."),
  ("Watch a humpback at the surface for a while, and you will see the tools it uses.", "Humpback flipper slapping the surface (NOAA)."),
  ("Its first weapon is its flippers. Swung through the water, these five-metre wings hit with enormous force, and the barnacles on their edges cut.", "Diagram: flipper swing arc, barnacle close-up."),
  ("Its second weapon is its tail. One stroke can lift the whole fluke out of the sea and bring it down with a crash.", "Humpback tail sailing and slapping (Commons)."),
  ("Its third weapon is noise. Humpbacks trumpet and bellow, and those calls may bring other humpbacks to the scene.", "Diagram: sound rings spreading from a humpback."),
  ("And its last weapon is numbers. Several humpbacks working together can surround the prey and keep the orcas away.", "Humpbacks together at the surface (Commons, aerial)."),
  ("Sometimes an adult male joins a mother and calf during an attack, as an escort. Sometimes several unrelated adults arrive at once.", "Diagram: escort humpback beside mother and calf, orcas circling."),
  ("Orcas are fast and clever. But a hunt costs them energy, and a blow from a humpback could injure them. Often, they simply give up.", "Orcas moving away, wide (NOAA). [2 s — pause]"),
 ]),
 ('11 — Why do they do it?', [
  ("So we come back to the big question. Why would a humpback risk its safety for a seal?", "Seal resting on a beach (NOAA)."),
  ("The first answer is simple: protecting their own. Humpbacks protect their calves, and sometimes the calves of other humpbacks, which may be relatives.", "Humpback mother and calf (Commons)."),
  ("The second answer is more surprising. Mammal-eating orcas are silent until the attack starts. Then they become loud.", "Diagram: orcas silent, then sound rings at the attack."),
  ("A humpback hearing those sounds from far away cannot know what is being attacked. It could be a seal. Or it could be a humpback calf.", "Humpback underwater, listening (NOAA)."),
  ("Pitman and his colleagues suggested that the safest rule is to go and interfere every time. If you go too often, you lose a little energy. If you stay away when it is your own kind, you lose a calf.", "Diagram: decision tree — go / stay away."),
  ("By this logic, the seal is saved almost by accident. The humpback is not thinking of the seal at all. It is fighting the killer whale.", "Seal swimming underwater (NOAA, monk seal). [2 s — pause]"),
 ]),
 ('12 — Kindness or instinct?', [
  ("But not everyone is satisfied with that answer.", "Humpback at the surface, slow push (NOAA)."),
  ("Other animals help different species too, sometimes. Dolphins have been seen staying close to injured or stranded animals. But such stories are rare, and hard to prove.", "Open ocean, wide (NOAA)."),
  ("Remember the whale in Antarctica, lying on its back, lifting the seal with its flipper. Remember the humpbacks in Monterey Bay, staying for hours beside a calf they could no longer save.", "AI illustration hb_ai_02, wide framing, if supplied, otherwise diagram."),
  ("Humpbacks have large and complex brains. Male humpbacks sing long songs that change from year to year and spread from one population to another.", "Diagram: song spectrogram scrolling."),
  ("Some researchers think it is possible that humpbacks feel something when they hear an animal in distress.", "Humpback underwater, close (NOAA)."),
  ("Pitman himself was careful. He wrote that when a human protects another species, we call it compassion. A humpback might be doing something similar, even if it is not thinking about it.", "Text card: 'COMPASSION?' (quote paraphrased)."),
  ("For now, the honest answer is that we do not know. Kindness, instinct, or a mix of both, the result for the seal is the same.", "Seal resting safely on a beach (NOAA). [2 s — pause]"),
 ]),
 ('13 — The return of the giants', [
  ("There is another reason we see this behaviour more often today. For most of the twentieth century, there were very few humpbacks left to see it.", "Old-style text card: COMMERCIAL WHALING, 20TH CENTURY."),
  ("Commercial whaling killed hundreds of thousands of humpbacks. In some regions, only a few percent of the original population survived.", "Graphic: population curve falling."),
  ("In 1966, humpbacks were protected worldwide. Slowly, they began to come back.", "Text card: 1966 — PROTECTED WORLDWIDE."),
  ("Today, many populations have recovered strongly, and the species is listed as Least Concern by the IUCN.", "Graphic: population curve rising; card IUCN — LEAST CONCERN."),
  ("Scientists can now recognise thousands of individual humpbacks from photos of their tails, and follow them across oceans and decades.", "Humpback fluke and photo-ID catalogue graphic."),
  ("More humpbacks means more encounters with killer whales, and more people on the water to see them.", "Whale-watching boat and humpbacks (NOAA)."),
  ("Since the 2017 study, new reports have kept coming, from Alaska, from Canada, from Mexico, and from the Southern Ocean. The list of rescued species keeps getting longer.", "Map: new report points appear."),
  ("Mammal-eating orcas are doing well too, in some regions. The two giants now meet more often than they have for a century.", "Orcas surfacing, aerial (NOAA). [2 s — pause]"),
 ]),
 ('14 — Conclusion', [
  ("We often imagine the ocean as a place where every animal fights only for itself.", "Open blue ocean (NOAA)."),
  ("The humpback shows us a different picture.", "Humpback underwater (NOAA)."),
  ("Not every whale joins in. Not every hunt is stopped. Many seals and sea lions are still caught every year, because that is how the ocean works.", "Sea lions on rocks (NOAA)."),
  ("Here, a giant that eats only krill and small fish swims towards the most dangerous predator in the sea, to break up a hunt that has nothing to do with its own meal.", "Montage: floe and seal diagram, humpbacks, orcas moving away."),
  ("Maybe it is protecting its own kind. Maybe it simply cannot stand the sound of a killer whale hunting. Maybe it is something we do not yet have a word for.", "Humpback tail lifting out of the water (Commons)."),
  ("Whatever the reason, somewhere in the Antarctic, a seal is alive because a whale decided to get involved.", "Seal on a beach, slow push (NOAA). [3 s — pause]"),
  ("If you enjoyed this film, subscribe to Naturexplore for a new documentary every week. And tell us in the comments: do you think the humpbacks know what they are doing?", "End card with two suggested videos."),
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
