"""Edit decision list: beat -> shots. Shot = (source, in_seconds, weight, fx).
Sources: noaa_* / mk_* / wm_* footage files, 'G:<graphic>' rendered graphics, 'BLACK', 'SPLIT'.
fx keys: slow (factor), push (True), grade ('cool','dark','night','dusk','grey','warm'), zoom (crop factor),
         d (fixed seconds), p (graphic params), xfade (seconds, dissolve from previous shot).
Beat-level overlays in OVERLAYS: beat -> (graphic, params, start offset)."""
A = 'noaa_1092315332001'    # killer whales, Alaska (St Paul Is., Aleutians)
S = 'noaa_3629965805001'    # Southern Residents, Puget Sound
H = 'noaa_4264909079001'    # Northern Residents, hexacopter aerial
WC = 'noaa_4088998754001'   # winter killer whale cruise, Pacific coast
D = 'noaa_5998935565001'    # DTAG research, Southern Residents near vessels
TD = 'noaa_6011240148001'   # Type D killer whales, Cape Horn (underwater)
U1 = 'noaa_4569239085001'   # UAV reveals killer whales (aerial)
U2 = 'noaa_3812337968001'   # UAV new view of killer whales (aerial)
PAC = 'noaa_1105831255001'  # whales on the Pacific coast (humpbacks, Lynn Canal)
HUMP = 'noaa_3911325489001' # humpbacks underwater
SPIN = 'noaa_5211554378001' # spinner dolphins
BEARD = 'noaa_5530478985001'# bearded seals on ice
ARC = 'noaa_6214018299001'  # Arctic sea ice from a ship
SALM = 'noaa_5531008936001' # Atlantic salmon underwater
CHIN = 'noaa_5227164781001' # winter-run Chinook
SHK = 'noaa_4651707268001'  # sharks
HSEAL = 'noaa_4419966618001'# harbour seals
KELP = 'noaa_3863054329001' # kelp, PNW coast, industrial waterfront
CSL = 'noaa_4084857759001'  # California sea lions colony
NEWP = 'noaa_897671512001'  # Newport harbour, Oregon
TDZ = {'zoom': 1.12}        # crop the small partner logo in Type D underwater shots

EDL = {
 1: [('mk_4466', 1.0, 1, {'grade': 'dark'}), (A, 24.0, 1.2, {'grade': 'dark'}), (U1, 15.0, 1.2, {'grade': 'dark'})],
 2: [('wm_00', 12.5, 1, {'slow': 1.5})],
 3: [('wm_09', 152.0, 1, {}), ('wm_05', 84.0, 1, {}), (ARC, 44.0, 1, {}), (CSL, 14.0, 1, {})],
 4: [('wm_00', 31.0, 1, {'slow': 1.3})],
 5: [('BLACK', 0, 1, {})],
 6: [('G:zero', 0, 1, {})],
 7: [('wm_00', 16.0, 1, {'slow': 1.4, 'grade': 'dark'})],
 8: [(U1, 29.0, 1, {})],
 9: [('G:family', 0, 1, {})],
 10: [('G:size', 0, 1, {})],
 11: [('G:world', 0, 1, {})],
 12: [('mk_1163', 1.0, 1, {}), ('mk_38939', 1.0, 1, {}), (A, 126.0, 1.2, {})],
 13: [('mk_4291', 1.0, 1, {}), (HSEAL, 20.0, 1, {}), (CSL, 60.0, 1, {}), (SPIN, 20.0, 1, {}), (SHK, 74.0, 1, {}), (HUMP, 14.0, 1.2, {})],
 14: [('mk_48090', 1.0, 1, {'grade': 'dark'})],
 15: [(H, 20.0, 1, {})],
 16: [('wm_22', 30.0, 1, {}), ('wm_22', 138.0, 1.3, {})],
 17: [(WC, 198.0, 1, {}), ('G:wavewash', 0, 1, {'d': 10.0})],
 18: [('G:weddell', 0, 1, {})],
 19: [('wm_00', 34.0, 1, {'slow': 1.3})],
 20: [(CSL, 12.0, 1, {}), (A, 38.0, 1, {}), ('G:beach', 0, 1, {'d': 10.0})],
 21: [(S, 108.0, 1, {}), (U1, 224.0, 1, {}), (S, 11.0, 1, {})],
 22: [('wm_05', 92.0, 1, {}), (WC, 186.0, 1, {}), ('G:bluewhale', 0, 1, {'d': 11.2})],
 23: [('G:portstar', 0, 1, {})],
 24: [('mk_4214', 1.0, 1, {}), ('mk_26300', 1.0, 1, {}), ('wm_10', 14.0, 1, {}), ('wm_09', 60.0, 1, {}), ('mk_51502', 1.0, 1, {})],
 25: [(H, 35.0, 1, {})],
 26: [('mk_27826', 1.0, 1, {'grade': 'dark'}), ('wm_02', 20.5, 1, {'grade': 'dark'})],
 27: [('G:incidents', 0, 1, {})],
 28: [('mk_25153', 1.0, 1, {}), ('mk_1068', 1.0, 1.2, {}), ('mk_51460', 1.0, 1, {}), (CSL, 100.0, 1, {})],
 29: [('mk_29397', 1.0, 1, {'grade': 'grey'})],
 30: [('mk_50141', 1.0, 1, {}), ('mk_26300', 8.0, 1, {})],
 31: [(PAC, 40.0, 1, {}), (NEWP, 82.0, 1, {})],
 32: [('mk_50214', 1.0, 1, {}), ('wm_00', 0.2, 1, {'slow': 1.3})],
 33: [('G:incidents', 0, 1, {'p': {'all': True}})],
 34: [(ARC, 14.0, 1, {}), (ARC, 198.0, 1, {})],
 35: [('G:sharks', 0, 1, {})],
 36: [('SPLIT', 0, 1, {'left': ('wm_09', 178.0), 'right': ('wm_00', 38.0)})],
 37: [('mk_22378', 1.0, 1, {'grade': 'cool'})],
 38: [('mk_8161', 1.0, 1, {'grade': 'night'})],
 39: [('mk_28203', 1.0, 1, {'grade': 'night'})],
 40: [('mk_45612', 1.0, 1, {'push': True, 'grade': 'dark'})],
 41: [('G:range', 0, 1, {})],
 42: [('SPLIT', 0, 1, {'left': (U2, 58.0), 'right': ('mk_40109', 1.0), 'rgrade': 'night'})],
 43: [('wm_00', 44.0, 1, {}), ('wm_02', 15.5, 1, {})],
 44: [('wm_15', 40.0, 1, {})],
 45: [(KELP, 92.0, 1, {}), (S, 50.0, 1, {}), (D, 39.0, 1, {})],
 46: [(H, 42.0, 1, {}), (U1, 17.5, 1, {})],
 47: [(U2, 74.0, 1, {}), (SALM, 14.0, 1, {})],
 48: [(A, 204.0, 1, {}), (HSEAL, 40.0, 1, {})],
 49: [('G:tree', 0, 1, {})],
 50: [(U1, 196.0, 1, {}), (U1, 232.0, 1, {}), ('wm_00', 49.0, 1, {})],
 51: [(HSEAL, 194.0, 1, {}), (A, 41.0, 1, {})],
 52: [(WC, 214.0, 1, {})],
 53: [(U1, 242.0, 1, {})],
 54: [('G:porpoise1', 0, 1, {})],
 55: [('G:porpoise2', 0, 1, {})],
 56: [('G:g78', 0, 1, {})],
 57: [(WC, 224.0, 1, {})],
 58: [('G:three', 0, 1, {})],
 59: [('mk_43088', 1.0, 1, {'grade': 'dark'})],
 60: [('mk_1903', 1.0, 1, {}), ('mk_7899', 1.0, 1, {}), (A, 146.0, 1, {})],
 61: [(S, 59.0, 1, {'slow': 1.4}), (A, 64.0, 1, {})],
 62: [('G:life', 0, 1, {})],
 63: [(S, 66.0, 1, {}), (D, 46.0, 1, {})],
 64: [(H, 12.0, 1, {}), ('wm_15', 118.0, 1, {}), ('wm_17', 4.0, 1, {})],
 65: [('G:grand', 0, 1, {})],
 66: [(U2, 66.0, 1, {}), (U1, 168.0, 1, {})],
 67: [('wm_00', 62.0, 1, {})],
 68: [(WC, 230.0, 1, {'push': True})],
 69: [(S, 38.0, 1, {})],
 70: [('G:brain', 0, 1, {})],
 71: [('mk_8662', 1.0, 1, {'grade': 'grey'}), (A, 10.0, 1, {'grade': 'grey'}), (NEWP, 6.0, 1, {'grade': 'grey'})],
 72: [(A, 108.0, 1, {'slow': 1.3, 'grade': 'grey'})],
 73: [(WC, 74.0, 1, {'grade': 'grey'}), (WC, 94.0, 1, {'grade': 'grey'})],
 74: [(U1, 38.0, 1, {'slow': 1.4, 'grade': 'warm'})],
 75: [('wm_02', 33.0, 1, {})],
 76: [('wm_00', 26.0, 1, {'slow': 1.3})],
 77: [('mk_25068', 1.0, 1, {}), (KELP, 100.0, 1, {}), ('wm_25', 48.0, 1, {})],
 78: [('G:carving', 0, 1, {})],
 79: [('wm_00', 55.0, 1, {'xfade': 2.0})],
 80: [(WC, 204.0, 1, {'grade': 'dusk'}), (D, 41.0, 1, {'grade': 'dusk'})],
 81: [('mk_4680', 1.0, 1, {})],
 82: [('mk_51478', 1.0, 1, {}), ('G:rudder', 0, 1, {'d': 8.5})],
 83: [('G:iberia', 0, 1, {})],
 84: [('G:gibraltar', 0, 1, {})],
 85: [('G:rudder', 0, 1, {'p': {'short': True}})],
 86: [('mk_27539', 1.0, 1, {}), (TD, 30.0, 1, {})],
 87: [(D, 50.0, 1, {})],
 88: [('wm_15', 50.0, 1, {}), (U1, 245.0, 1, {}), ('wm_00', 36.5, 1, {}), ('G:rudder', 0, 1, {'p': {'short': True}, 'reuse': 85})],
 89: [(KELP, 186.0, 1, {}), ('mk_31019', 1.0, 1, {})],
 90: [(D, 56.0, 1, {}), (CHIN, 30.0, 1, {}), ('mk_43603', 1.0, 1, {})],
 91: [('G:srkw', 0, 1, {})],
 92: [('mk_17100', 1.0, 1, {})],
 93: [(WC, 240.0, 1, {'push': True, 'grade': 'dusk'})],
 94: [(S, 19.0, 1, {'slow': 1.5})],
 95: [('wm_09', 186.0, 1, {}), ('wm_05', 98.0, 1, {}), ('wm_22', 150.0, 1, {}), (WC, 210.0, 1, {})],
 96: [(TD, 40.0, 1, dict(slow=1.4))],
 97: [(U1, 20.5, 1, {'grade': 'dusk'})],
 98: [('G:endcard', 0, 1, {})],
}
OVERLAYS = {
 7: ('title', {}, 0.6),
 28: ('lower', {'big': '1972', 'small': 'POINT SUR, CALIFORNIA'}, 0.8),
 30: ('lower', {'big': '1989', 'small': 'PATAGONIA, ARGENTINA'}, 0.8),
 31: ('lower', {'big': '2005', 'small': 'KETCHIKAN, ALASKA'}, 0.8),
 32: ('lower', {'big': '2014', 'small': 'NEW ZEALAND'}, 0.8),
 34: ('statement', {'big': 'UNCONFIRMED', 'small': 'CANADIAN ARCTIC · 1950s', 'size': 120}, 5.0),
 39: ('statement', {'big': 'CAPTIVITY: 4 DEATHS', 'size': 110, 'color': '#eef4f8'}, 0.8),
 40: ('statement', {'big': 'TILIKUM — 3 DEATHS', 'size': 96, 'small': 'LAST: 2010'}, 0.6),
 72: ('day17', {}, 0.4),
}
CHAPTER_CARDS = {
 2: ('2', 'The perfect killer'), 3: ('3', 'What an orca can do'), 4: ('4', 'The record'), 5: ('5', 'The dark exception'),
 6: ('THEORY ONE', 'We are not on the menu'), 7: ('7', "A twist: killers that don't eat"), 8: ('THEORY TWO', 'The grandmothers'),
 9: ('THEORY THREE', 'An intelligent, careful animal'), 10: ('THEORY FOUR', 'A promise'), 11: ('11', 'The test case'),
 12: ('12', 'The real danger'), 13: ('13', 'Conclusion'),
}
