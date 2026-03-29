import re

# -----------------------
# CHARACTER MAP (REVERSE)
# -----------------------

chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ."
rev_char_map = {i: c for i, c in enumerate(chars)}

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

# -----------------------
# LOAD FILE
# -----------------------

path = "/storage/emulated/0/Download/text.bin"

with open(path, "rb") as f:
    data = f.read()

# -----------------------
# UNPACK BITS
# -----------------------

bits = ""
for b in data:
    bits += format(b, "08b")

# -----------------------
# DECODING
# -----------------------

i = 0
output = []

def read(n):
    global i
    val = bits[i:i+n]
    i += n
    return val

while i < len(bits):

    # prevent reading padding garbage
    if len(bits) - i < 2:
        break

    prefix = read(2)

    # -----------------------
    # LITERAL
    # -----------------------
    if prefix == "00":
        if len(bits) - i < 5:
            break
        idx = int(read(5), 2)
        output.append(rev_char_map.get(idx, ""))

    # -----------------------
    # TOKEN
    # -----------------------
    elif prefix == "01":
        if len(bits) - i < 2:
            break

        system = read(2)

        if system == "00":
            idx = int(read(5), 2)
            output.append(sys1[idx])

        elif system == "01":
            idx = int(read(6), 2)
            output.append(sys2[idx])

        elif system == "10":
            idx = int(read(7), 2)
            output.append(sys3[idx])

        elif system == "11":
            idx = int(read(8), 2)
            output.append(sys4[idx])

    # -----------------------
    # LZ77 COPY
    # -----------------------
    elif prefix == "10":
        if len(bits) - i < 18:
            break

        dist = int(read(12), 2)
        length = int(read(6), 2)

        start = len(output) - dist

        for j in range(length):
            if start + j < 0 or start + j >= len(output):
                break
            output.append(output[start + j])

    else:
        break  # "11" unused → stop safely

# -----------------------
# FINAL TEXT
# -----------------------

decoded = "".join(output)

print("Decoded text:\n")
print(decoded)