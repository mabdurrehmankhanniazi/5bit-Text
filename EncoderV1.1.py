import os
import re

# -----------------------
# CHARACTER MAP
# -----------------------

chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ."
char_map = {c: i for i, c in enumerate(chars)}

# -----------------------
# TOKEN SYSTEMS
# -----------------------

sys1 = [
"THE","OF","AND","TO","IN","IS","YOU","THAT",
"IT","HE","WAS","FOR","ON","ARE","AS","WITH",
"HIS","THEY","I","AT","BE","THIS","HAVE","FROM",
"OR","ONE","HAD","BY","WORD","BUT","NOT","WHAT"
]

sys2 = [
"ALL","WERE","WHEN","YOUR","CAN","SAID","THERE","USE",
"AN","EACH","WHICH","SHE","DO","HOW","THEIR","IF",
"WILL","UP","OTHER","ABOUT","OUT","MANY","THEN","THEM",
"THESE","SO","SOME","HER","WOULD","MAKE","LIKE","HIM",
"INTO","TIME","HAS","LOOK","TWO","MORE","WRITE","GO",
"SEE","NUMBER","NO","WAY","COULD","PEOPLE","MY","THAN",
"FIRST","WATER","BEEN","CALL","WHO","OIL","ITS","NOW",
"FIND","LONG","DOWN","DAY","DID","GET","COME","MADE"
]

sys3 = [
"WORK","PART","TAKE","YEAR","PLACE","LIVE","BACK","GIVE",
"MOST","VERY","AFTER","THING","OUR","JUST","NAME","GOOD",
"SENTENCE","MAN","THINK","SAY","GREAT","WHERE","HELP",
"THROUGH","MUCH","BEFORE","LINE","RIGHT","TOO","MEAN",
"OLD","ANY","SAME","TELL","BOY","FOLLOW","CAME","WANT",
"SHOW","ALSO","AROUND","FORM","THREE","SMALL","SET",
"PUT","END","DOES","ANOTHER","WELL","LARGE","MUST",
"BIG","EVEN","SUCH","BECAUSE","TURN","HERE","WHY",
"ASK","WENT","MEN","READ","NEED","LAND","DIFFERENT",
"HOME","US","MOVE","TRY","KIND","HAND","PICTURE",
"AGAIN","CHANGE","OFF","PLAY","SPELL","AIR","AWAY",
"ANIMAL","HOUSE","POINT","PAGE","LETTER","MOTHER",
"ANSWER","FOUND","STUDY","STILL","LEARN","SHOULD",
"AMERICA","WORLD","HIGH","EVERY","NEAR","ADD","FOOD",
"BETWEEN","OWN","BELOW","COUNTRY","PLANT","LAST",
"SCHOOL","FATHER","KEEP","TREE","NEVER","START",
"CITY","EARTH","EYE","LIGHT","THOUGHT","HEAD","UNDER",
"STORY","LEFT","DON","FEW","WHILE","ALONG","MIGHT"
]

sys4 = [
"SYSTEM","NUMBER","PROGRAM","PROCESS","CONTROL","NETWORK","MEMORY",
"METHOD","OBJECT","RESULT","STRING","VALUE","STATE","MODEL","ARRAY",
"STACK","QUEUE","CACHE","DEBUG","BUILD","FILES","INDEX","LEVEL",
"POINT","GROUP","CLASS","STRUCT","VECTOR","THREAD","PUBLIC",
"PRIVATE","GLOBAL","LOCAL","RETURN","IMPORT","EXPORT","FORMAT",
"PARSE","COMPILE","EXECUTE","STATUS","OPTION","CONFIG","DEFINE",
"UPDATE","DELETE","INSERT","SELECT","SEARCH","FILTER","CREATE",
"REMOVE","CHANGE","CHECK","PRINT","WRITE","READ","TEST","CASE",
"USER","ADMIN","LOGIN","LOGOUT","ACCESS","SECURE","VALID","SUCCESS",
"FAILED","WARNING","DEFAULT","CUSTOM","EMAIL","PHONE","ADDRESS",
"COUNTRY","CITY","STREET","FIELD","TABLE","ROW","COLUMN","ENTRY",
"RECORD","REQUEST","RESPONSE","HEADER","BODY","SESSION","COOKIE",
"TOKEN","PROFILE","BINARY","DECIMAL","FLOAT","DOUBLE","BOOLEAN",
"INTEGER","CHAR","VARIABLE","CONSTANT","PARAMETER","ARGUMENT",
"FUNCTION","DATABASE","SERVER","CLIENT","STORAGE","DEVICE"
]

# dictionaries
d1 = {w: i for i, w in enumerate(sys1)}
d2 = {w: i for i, w in enumerate(sys2)}
d3 = {w: i for i, w in enumerate(sys3)}
d4 = {w: i for i, w in enumerate(sys4)}

# -----------------------
# LZ77 COPY
# -----------------------

def find_match(text, pos, max_dist=4095, max_len=63):
    best_len = 0
    best_dist = 0

    for dist in range(1, min(pos, max_dist) + 1):
        length = 0
        while (
            pos + length < len(text)
            and text[pos + length] == text[pos + length - dist]
            and length < max_len
        ):
            length += 1

        if length > best_len:
            best_len = length
            best_dist = dist

    return best_dist, best_len

# -----------------------
# INPUT TEXT
# -----------------------

text = """HELLO WORLD."""

text = text.upper()
text = text.replace("\n", " ")
text = re.sub(r"[^A-Z .]", " ", text)

# -----------------------
# ENCODING
# -----------------------

bits = ""
i = 0

while i < len(text):

    if text[i].isalpha():

        j = i
        word = ""

        while j < len(text) and text[j].isalpha():
            word += text[j]
            j += 1

        if word in d1:
            bits += "01" + "00" + format(d1[word], "05b")
            i = j
            continue

        if word in d2:
            bits += "01" + "01" + format(d2[word], "06b")
            i = j
            continue

        if word in d3:
            bits += "01" + "10" + format(d3[word], "07b")
            i = j
            continue

        if word in d4:
            bits += "01" + "11" + format(d4[word], "08b")
            i = j
            continue

    dist, length = find_match(text, i)

    literal_cost = length * 7
    copy_cost = 20

    if length >= 4 and copy_cost < literal_cost:
        bits += "10"
        bits += format(dist, "012b")
        bits += format(length, "06b")
        i += length
        continue

    bits += "00" + format(char_map[text[i]], "05b")
    i += 1

# -----------------------
# PACK BITS
# -----------------------

while len(bits) % 8 != 0:
    bits += "0"

data = bytearray()

for i in range(0, len(bits), 8):
    data.append(int(bits[i:i+8], 2))

# -----------------------
# SAVE FILE
# -----------------------

path = "/storage/emulated/0/Download/text.bin"

with open(path, "wb") as f:
    f.write(data)

print("Saved:", path)
print("Size:", len(data), "bytes")
