from lingpy import align

with open("list_seq.fasta", 'r') as file_seq:
    list_seq, list_pdb = [], []
    for line in file_seq:
        if line[0] == ">":
            list_pdb.append(line[:-5].upper())
        else:
            list_seq.append(line[:-1])
        

m = align.multiple.mult_align(list_seq, pprint=False)


for i in range(len(m[0])):
    list_char = []
    tot = 0

    for j in range(len(m)):
        list_char.append(m[j][i])
        if len(m[j][i]) > tot:
            tot = len(m[j][i])

    for k in range(len(m)):
        if len(list_char[k]) < tot:

            for l in range(0, tot - len(list_char[k])):
                m[k][i] += "-"


with open("seq_align.fasta", 'w') as file_align:

    for n in range(len(m)):
        final_seq = ""
        for char in m[n]:
            final_seq += char
            
        file_align.write(list_pdb[n] + "\n" + final_seq + "\n")