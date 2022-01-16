from main import Permutation_counter
import sys
import pyperclip

if __name__ == '__main__':
    textes = []
    perm = Permutation_counter()
    names_file = open('text.txt', 'r')
    params = names_file.readline()
    lens = params.split()
    i = 0    
    for l in lens:
        perm.add_sign(int(l))
        textes.append(list())
        for j in range(int(l)):
            textes[i].append(names_file.readline()[:-1])
        i += 1

    counter = 0

    try:
        print(f'skipping {sys.argv[1]}')
        perm.skip(int(sys.argv[1]))
        counter = int(sys.argv[1])
    except:
        print('no skip')
        pass 

    while 1:
        indexes = perm.get()
        desc = ''
        if indexes:
            i = 0
            for index in indexes:
                element = textes[i][index]
                desc += element + ' '
                i += 1
        else:
            break
        print(desc + str(counter))
        pyperclip.copy(desc)
        input()
        counter += 1