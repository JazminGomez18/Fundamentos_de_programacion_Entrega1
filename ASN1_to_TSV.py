"""code to obtain tsv file from asn1 file"""

#  create lists for the file columns
protein_title = []                                                      # list for protein name column
protein_length = []                                                     # list for protein length
protein_id = []                                                         # list for protein accession code
translation = []                                                        # list for aminoacid sequence

asn1_file_name = ['PYVV.asn1', 'ToCV_2.asn1']                           # list with .asn1 file names

for asn1_file in asn1_file_name:

    # clear lists every time you read a new file
    protein_title = []
    protein_length = []
    protein_id = []
    translation = []

    # open files
    with open(asn1_file) as file:
        seq = ""

        # bring virus name
        for tit in file:
            if 'name virus' in tit:
                tit = tit.strip()
                tit = tit.replace('name virus "', '')
                tit = tit.split('"')[0]
                print(tit.upper())                                      # name in capital letters
                break
        # to be able to perform a second task with the same file
        file.seek(0)

        # print column titles
        print(f"{'Protein name'}\t{'Protein accession code'}\t{'Length (aa)'}\t{'Protein sequence'}")

        # fill columns
        for line in file:

            # bring protein name
            if 'title' in line:
                line = line.strip()
                line = line.replace('title "', '')
                line = line.split('[')[0]
                protein_title.append(line)
                # print(line)

            # bring protein length (aa)
            elif 'mol aa' in line:
                next_line = next(file, '').strip()
                # print(next_line)
                next_line = next_line.strip()
                next_line = next_line.replace('length ', '')
                next_line = next_line.split(',')[0]
                protein_length.append(next_line)
                # print(line)

            # bring accession code
            elif 'accession' in line:
                line = line.strip()
                line = line.replace('accession "', '')
                line = line.split('"')[0]
                protein_id.append(line)
                # print(line)

            # bring complete protein sequence
            elif 'seq-data ncbieaa' in line:
                seq = line.split('"', 1)[1]
                if '"'in seq:
                    translation.append(seq.split('"')[0].strip())
                    seq = ""
                else:
                    seq = seq.strip()

            elif seq:
                if '"' in line:
                    seq += line.split('"')[0].strip()
                    translation.append(seq.replace("\n", ""))
                    seq = ""
                else:
                    seq += line.split('"')[0]

        protein_id = protein_id[1:]  # Save the list from the second element, the first is the GenBank access number

        # print all columns
        for p_name, p_id, p_len, p_seq in zip(protein_title, protein_id, protein_length, translation):
            print(f"{p_name}\t{p_id}\t{p_len}\t{p_seq}")

    # prints a separator between files
    print('-' * 50)


