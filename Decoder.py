import os

# -----------------------
# CHARACTER MAP
# -----------------------

rev_char = {i: chr(i+65) for i in range(26)}
rev_char[26] = " "
rev_char[27] = "."

# -----------------------
# SYSTEM 1 (32 TOKENS)
# -----------------------

sys1=[
"THE","OF","AND","TO","IN","IS","YOU","THAT",
"IT","HE","WAS","FOR","ON","ARE","AS","WITH",
"HIS","THEY","I","AT","BE","THIS","HAVE","FROM",
"OR","ONE","HAD","BY","WORD","BUT","NOT","WHAT"
]

# -----------------------
# SYSTEM 2 (64 TOKENS)
# -----------------------

sys2=[
"ALL","WERE","WHEN","YOUR","CAN","SAID","THERE","USE",
"AN","EACH","WHICH","SHE","DO","HOW","THEIR","IF",
"WILL","UP","OTHER","ABOUT","OUT","MANY","THEN","THEM",
"THESE","SO","SOME","HER","WOULD","MAKE","LIKE","HIM",
"INTO","TIME","HAS","LOOK","TWO","MORE","WRITE","GO",
"SEE","NUMBER","NO","WAY","COULD","PEOPLE","MY","THAN",
"FIRST","WATER","BEEN","CALL","WHO","OIL","ITS","NOW",
"FIND","LONG","DOWN","DAY","DID","GET","COME","MADE"
]

# -----------------------
# SYSTEM 3 (128 TOKENS)
# -----------------------

sys3=[
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

# -----------------------
# SYSTEM 4 (256 TOKENS)
# -----------------------

sys4=[
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
"FUNCTION","DATABASE","SERVER","CLIENT","STORAGE","DEVICE",
"DRIVER","ENGINE","SERVICE","MODULE","PACKAGE","OBJECTS",
"METHODS","VALUES","SYSTEMS","THREADS","FILESYS","NETWORKING",
"COMPRESSION","CONFIGURATION","IMPLEMENTATION","INFORMATION",
"DEVELOPMENT","APPLICATION","COMMUNICATION","IDENTIFICATION",
"ORGANIZATION","REPRESENTATION","TRANSFORMATION","ADMINISTRATION",
"ENVIRONMENT","MANAGEMENT","RELATIONSHIP","INTEGRATION",
"OPERATION","INSTRUCTION","AUTHENTICATION","AUTHORIZATION",
"DOCUMENTATION","INITIALIZATION","SYNCHRONIZATION",
"MULTITHREADING","INTERACTION","VISUALIZATION","OPTIMIZATION",
"TRANSACTION","INTERFACE","ARCHITECTURE","DISTRIBUTION",
"PERFORMANCE","COMPATIBILITY","FUNCTIONALITY","DEPENDENCY",
"PROFESSIONAL","EDUCATIONAL","ENGINEERING","COMPUTATIONAL",
"MATHEMATICAL","SCIENTIFIC","TECHNOLOGY","PROGRAMMING",
"AUTOMATION","SIMULATION","CALCULATION","STRUCTURAL",
"MECHANISM","ANALYTICAL","STATISTICAL","DEMONSTRATION",
"EXPERIMENTAL","COMPARISON","EVALUATION","INTERPRETATION",
"MODIFICATION"
]

# -----------------------
# READ FILE
# -----------------------

path="/storage/emulated/0/Download/text.bin"

with open(path,"rb") as f:
    data=f.read()

bits="".join(format(b,"08b") for b in data)

# -----------------------
# DECODE
# -----------------------

i=0
output=""

while True:

    if i+2 > len(bits):
        break

    prefix = bits[i:i+2]
    i += 2

    # literal
    if prefix == "00":

        if i+5 > len(bits):
            break

        val = int(bits[i:i+5],2)
        i += 5
        output += rev_char.get(val,"")

    # token
    elif prefix == "01":

        if i+2 > len(bits):
            break

        sysid = bits[i:i+2]
        i += 2

        if sysid == "00":

            if i+5 > len(bits):
                break

            idx = int(bits[i:i+5],2)
            i += 5
            output += sys1[idx]

        elif sysid == "01":

            if i+6 > len(bits):
                break

            idx = int(bits[i:i+6],2)
            i += 6
            output += sys2[idx]

        elif sysid == "10":

            if i+7 > len(bits):
                break

            idx = int(bits[i:i+7],2)
            i += 7
            output += sys3[idx]

        elif sysid == "11":

            if i+8 > len(bits):
                break

            idx = int(bits[i:i+8],2)
            i += 8
            output += sys4[idx]

    # LZ77
    elif prefix == "10":

        if i+18 > len(bits):
            break

        dist = int(bits[i:i+12],2)
        i += 12

        length = int(bits[i:i+6],2)
        i += 6

        start = len(output) - dist

        for j in range(length):
            output += output[start+j]

    else:
        break

print(output)