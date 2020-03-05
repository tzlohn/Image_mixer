import re

string = "After_alignment_X187_Y-597_4x_Left.raw_meta.txt"
ext = ".raw_meta.txt"
side = "_Left"
pattern = re.compile(r"(.*)%s(_\d+)?%s"%(side,ext))
output = pattern.findall(string)
print(output)