if __name__ == "__main__":
    conference_supporter = ['IJCAI', 'KDD', 'AAAI', 'COLT', 'CVPR', 'NIPS', 'KR', "SIGIR"]
    output = open("dblp", 'w')
    with open('FilteredDBLP.txt') as dblp_input:
        while True:
            line = dblp_input.readline()
            if not line:
                break
            author_list, title, year, conference = [], '', '', ''
            while not line.startswith("###") and line:
                if line.startswith("author"):
                    author_list.append(line.strip().split("\t")[1])
                elif line.startswith("title"):
                    title = line
                elif line.startswith("year"):
                    year = line
                else:
                    conference = line.strip().split("\t")[1]
                line = dblp_input.readline()
            for conf in conference_supporter:
                if conf.lower() in conference.lower():
                    conference = conf
                    output.write("author" + '\t' + '\t'.join(author_list) + '\n')
                    output.write(title if title != '' else 'title' + '\t' + '\n')
                    output.write(year if year != '' else 'year' + '\t' + '\n')
                    output.write("conference" + '\t' + conference + '\n' if conference != '' else 'conference' + '\t' + '\n')
                    output.write("\n")
    output.close()







