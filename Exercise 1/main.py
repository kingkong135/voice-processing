import os
from nltk.tokenize import sent_tokenize

folder_path = 'Data'

dirs = os.listdir(folder_path)
for path in dirs:
    # filename = dir + '.txt'
    file_path = path + '.txt'
    with open(os.path.join(folder_path, path, file_path), 'r') as f:
        lines = f.readlines()
        lines = ' '.join(lines)
    lines = sent_tokenize(lines)

    out_path = path + 'out.txt'
    with open(os.path.join(folder_path, path, out_path), 'w') as f:
        for line in lines:
            f.write(line + '\n')
