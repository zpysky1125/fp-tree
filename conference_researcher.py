# -*- coding: utf-8 -*-

if __name__ == "__main__":
    conference_supporter = {'IJCAI': {}, 'AAAI': {}, 'COLT': {}, 'CVPR': {}, 'NIPS': {}, 'KR': {}, 'SIGIR': {}, 'KDD': {}}
    conference_year_supporter = {'IJCAI': {}, 'AAAI': {}, 'COLT': {}, 'CVPR': {}, 'NIPS': {}, 'KR': {}, 'SIGIR': {}, 'KDD': {}}

    with open('dblp') as dblp_input:
        while True:
            author_list, title, year, conference = [], '', '', ''
            line = dblp_input.readline()
            if not line:
                break
            author_list = line.strip().split("\t")[1:]
            title = dblp_input.readline().strip().split('\t')[1]
            year = int(dblp_input.readline().strip().split('\t')[1])
            conference = dblp_input.readline().strip().split('\t')[1]
            dblp_input.readline()
            for author in author_list:
                if conference_supporter[conference].has_key(author):
                    conference_supporter[conference][author].append(year)
                else:
                    conference_supporter[conference][author] = [year]
            if conference_year_supporter[conference].has_key(year):
                conference_year_supporter[conference][year].extend(author_list)
            else:
                conference_year_supporter[conference][year] = author_list
    with open('conference_researcher', 'w') as output:
        for key, conf in conference_supporter.items():
            output.write(key+"\n")
            for k, v in conf.items():
                output.write(k + "\t" + "\t".join([str(year) for year in sorted(v)])+"\n")
            output.write("\n")
    with open('conference_year_researcher', 'w') as output:
        for conf, year_supporter in conference_year_supporter.items():
            output.write(conf+"\n")
            for year, supporter_list in sorted(year_supporter.items()):
                output.write(str(year) + "\t" + "\t".join(set(supporter_list)) + "\n")
            output.write("\n")


