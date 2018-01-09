# -*- coding: utf-8 -*-


def read_file():
    res, res_dict, author_papers, paper_year = [], {}, {}, {}
    with open('dblp') as dblp_input:
        while True:
            author_list = dblp_input.readline().strip().split("\t")[1:]
            title = dblp_input.readline().strip().split("\t")[1]
            year = int(dblp_input.readline().strip().split("\t")[1])
            conference = dblp_input.readline().strip().split("\t")[1]
            for author in author_list:
                if res_dict.has_key(author):
                    res_dict[author] += 1
                else:
                    res_dict[author] = 1
            res.append(author_list)
            for author in author_list:
                if author_papers.has_key(author):
                    author_papers[author].append(title)
                else:
                    author_papers[author] = [title]
            paper_year[title] = year
            line = dblp_input.readline()
            if not line:
                break
    return res, res_dict, author_papers, paper_year


# 得到从大到小排序的数组
def array_sort(author_lists, person_num):
    res = []
    for item in author_lists:
        item = [v for v in item if person_num.has_key(v)]
        item = sorted(item, key=lambda x:(-person_num[x], x), reverse=False)
        res.append(item)
    return res


# 递归构造 conditional fp-tree，并得到 frequent items
def get_frequent_items(base_author, sorted_authors, support):
    res = [base_author]
    author_num = {}
    for author_list in sorted_authors:
        for author in author_list:
            if author_num.has_key(author):
                author_num[author] += 1
            else:
                author_num[author] = 1
    filtered_authors = [k for k, v in author_num.items() if v >= support]
    for author in filtered_authors:
        res = res + get_frequent_items(base_author + [author], [author_list[:author_list.index(author)] for author_list in sorted_authors if author in author_list], support)
    return res


def get_paper_keyword():
    paper_keywords = {}
    with open('topic_keywords') as input_file:
        while True:
            title = input_file.readline()
            if not title:
                break
            keywords = input_file.readline().strip().split("\t")
            paper_keywords[title.strip()] = keywords
    return paper_keywords


def get_team_papers(author_topics, frequent_items_with_support_3):
    res = []
    for team in frequent_items_with_support_3:
        inter_topics = set(author_topics[team[0]])
        for team_member in team[1:]:
            inter_topics.intersection_update(set(author_topics[team_member]))
        res.append(inter_topics)
    return res


def get_teams(frequent_items_with_support_3, item_topics):
    res, res_topics = [], []
    mask = [1] * len(frequent_items_with_support_3)
    for index1, team1 in enumerate(frequent_items_with_support_3):
        for index2, team2 in enumerate(frequent_items_with_support_3):
            if index1 != index2 and mask[index1] == 1 and len(set(team1) & set(team2) ^ set(team1)) == 0 and item_topics[index1] == item_topics[index2]:
                mask[index1] = 0
                break
    for index1, team1 in enumerate(frequent_items_with_support_3):
        if mask[index1]:
            res.append(team1), res_topics.append(item_topics[index1])
    return res, res_topics


if __name__ == '__main__':
    support = 3
    author_lists, person_num, author_papers, paper_year = read_file()
    sorted_author_lists = array_sort(author_lists, person_num)
    frequent_items = get_frequent_items([], sorted_author_lists, support)
    frequent_items_with_support_3 = [frequent_item for frequent_item in frequent_items if len(frequent_item) > 3]
    frequent_items_papers = get_team_papers(author_papers, frequent_items_with_support_3)
    # close patterns with support >= threshold are teams
    teams, team_papers = get_teams(frequent_items_with_support_3, frequent_items_papers)
    paper_keywords = get_paper_keyword()

    with open('team_papers', 'w') as output:
        for index, team in enumerate(teams):
            output.write("\t".join(team) + '\n')
            for paper in sorted(team_papers[index], key=lambda x: paper_year[x]):
                output.write("\t".join(['', paper, str(paper_year[paper]), "\t".join(paper_keywords[paper])]) + '\n')
            output.write('\n')



