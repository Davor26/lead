"""Hand-drawn flat silhouettes (side view, facing right). viewBox units given per shape."""
# Orca: 1000 x 340, nose at right
ORCA_BODY = ("M 12 168 C 40 160 80 158 120 160 "                                   # fluke tip (horizontal fluke seen edge-on)
             "C 170 150 230 135 300 118 C 380 100 450 90 515 86 "                       # tail stock rising to back
             "C 530 50 548 18 570 2 C 572 40 585 70 615 88 "                            # dorsal fin
             "C 700 92 790 100 860 116 C 920 130 965 148 985 168 "                     # back to melon
             "C 996 180 990 192 970 198 C 930 210 880 218 820 224 "                    # snout and lower jaw
             "C 790 236 770 262 735 300 C 712 322 690 330 668 328 C 680 300 690 272 695 246 " # paddle pectoral
             "C 620 252 520 250 430 238 C 330 224 240 200 170 186 "                    # belly to tail stock
             "C 130 180 70 182 12 168 Z")
ORCA_EYEPATCH = "M 800 150 C 830 138 868 138 888 148 C 872 162 834 166 806 160 Z"
ORCA_SADDLE = "M 470 98 C 540 92 620 94 680 104 C 630 120 540 122 470 112 Z"
ORCA_BELLY = ("M 960 196 C 900 214 830 222 760 226 C 700 230 640 234 560 232 "
              "C 520 231 480 234 450 240 C 520 248 620 252 700 246 C 790 236 880 222 960 196 Z")
ORCA_FLANK = "M 420 214 C 470 196 520 194 560 204 C 520 222 470 232 430 236 Z"
# Seal (Weddell-like, lying), 600 x 200
SEAL_OLD = ("M 20 150 C 10 140 15 125 35 128 C 60 132 80 135 110 132 C 200 110 300 95 400 92 "
        "C 470 90 530 95 560 112 C 585 125 592 145 580 158 C 560 170 520 172 470 170 "
        "C 380 172 260 175 160 172 C 120 171 90 168 70 165 C 55 178 30 185 12 182 C 20 172 25 160 20 150 Z")
SEAL = ("M 14 150 C 30 132 52 128 78 134 C 140 116 240 98 340 92 C 400 88 440 88 470 92 "
        "C 500 76 540 72 568 84 C 592 96 598 118 588 134 C 576 150 548 156 520 154 "
        "C 480 168 400 176 300 176 C 220 176 140 172 90 166 C 70 176 40 184 10 182 C 24 172 26 160 14 150 Z")
# Great white shark, 1000 x 360
SHARK = ("M 30 200 C 50 170 60 120 50 60 C 90 110 120 160 150 180 "
         "C 260 165 380 150 480 140 L 520 138 C 545 90 575 45 600 25 C 605 70 615 110 640 140 "
         "C 760 145 880 160 960 185 C 985 195 995 205 985 212 C 950 228 880 236 800 240 "
         "L 720 244 C 690 280 650 320 610 335 C 625 300 640 270 650 246 "
         "C 520 248 380 240 260 228 C 220 226 180 222 150 220 "
         "C 120 250 80 290 40 320 C 55 280 60 240 30 200 Z")
SHARK_LIVER = "M 560 175 C 640 165 760 172 820 192 C 790 215 700 228 620 226 C 580 222 555 205 560 175 Z"
# Blue whale, 2000 x 300 (long and slender)
BLUEWHALE = ("M 40 150 C 20 120 15 95 25 70 C 50 110 90 135 140 145 "
             "C 400 120 800 100 1200 92 L 1340 90 C 1360 80 1375 72 1390 70 C 1388 80 1392 88 1400 92 "
             "C 1600 95 1800 105 1930 125 C 1975 135 1995 150 1985 165 C 1940 185 1800 200 1600 205 "
             "C 1300 212 900 210 500 200 C 300 196 200 185 140 175 C 95 190 50 215 20 235 C 25 205 35 175 40 150 Z")
# Human diver (stylised, horizontal), 400 x 120
PERSON = ("M 60 0 C 80 0 92 14 92 32 C 92 50 80 62 60 62 C 40 62 28 50 28 32 C 28 14 40 0 60 0 Z "
          "M 30 72 L 90 72 C 108 72 118 84 118 100 L 118 210 L 98 210 L 98 340 L 66 340 L 66 230 L 54 230 L 54 340 "
          "L 22 340 L 22 210 L 2 210 L 2 100 C 2 84 12 72 30 72 Z")
# Bus (side), 1200 x 320
BUS = ("M 20 60 C 20 35 40 20 70 20 L 1130 20 C 1165 20 1185 40 1185 75 L 1185 250 C 1185 270 1170 280 1150 280 "
       "L 1050 280 C 1045 240 1000 215 960 215 C 920 215 880 240 875 280 L 340 280 C 335 240 295 215 255 215 "
       "C 215 215 175 240 170 280 L 50 280 C 32 280 20 268 20 250 Z")
def svg(path, vb, fill="var(--ice)", extra="", cls="", style=""):
    return f'<svg class="{cls}" viewBox="{vb}" style="{style}" xmlns="http://www.w3.org/2000/svg"><path d="{path}" fill="{fill}"/>{extra}</svg>'
def orca(cls="", style="", body="#04090C", white="var(--ice)", stroke="rgba(238,242,236,.55)"):
    """Orca in its real colours: black body, white eye patch, belly and flank, grey saddle."""
    return (f'<svg class="{cls}" viewBox="0 0 1000 340" style="{style}" xmlns="http://www.w3.org/2000/svg">'
            f'<path d="{ORCA_BODY}" fill="{body}" stroke="{stroke}" stroke-width="3"/>'
            f'<path d="{ORCA_BELLY}" fill="{white}"/><path d="{ORCA_FLANK}" fill="{white}"/>'
            f'<path d="{ORCA_EYEPATCH}" fill="{white}"/><path d="{ORCA_SADDLE}" fill="#93ABB1" opacity=".55"/></svg>')
