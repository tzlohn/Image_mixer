import re

string = "After_alignment_X187_Y-597_4x_Left.raw_meta.txt"
ext = ".raw_meta.txt"
pattern = re.compile(r"(.*)(_\d+)?%s"%ext)
output = pattern.findall(string)
print(output)