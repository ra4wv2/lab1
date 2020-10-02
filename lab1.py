from xml.dom import minidom
import re

filename = 'processed.conllu'
global word_tags


def load_dependency_tree(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.read().split('\n')
    for j in range(7):
        del lines[0]
    words = [l.split('\t') for l in lines[:-1]]
    del words[-1]
    tags = [word[3] + ', ' + ', '.join(word[5].split('|')) for word in words]
    tokens = [w[0] + '. ' + w[2] for w in words]
    global word_tags
    word_tags = {}
    for i in range(len(tokens)):
        word_tags[tokens[i]] = tags[i]
    nodes = [('0. root', [])]
    nodes.extend([(t, []) for t in tokens])
    for i, word in enumerate(words):
        nodes[int(word[6])][1].append(nodes[i + 1])

    return nodes[0]


def xml_maker(node, word):
    pattern = '\d+\.\s'
    word_wo_number = re.sub(pattern, '', node[0])
    global word_tags
    daughter = doc.createElement('daughters')
    words = doc.createElement('word')
    words.setAttribute('tags', word_tags[node[0]])
    words.setAttribute('text', word_wo_number)
    daughter.appendChild(words)
    word.appendChild(daughter)
    xml_str = doc.toprettyxml(indent="  ")
    with open("sentence.xml", "w", encoding='windows-1251') as f:
        f.write(xml_str)
    if node[1]:
        for k in range(len(node[1])):
            xml_maker(node[1][k], words)


node = load_dependency_tree(filename)


doc = minidom.Document()
root = doc.createElement('root')
root.setAttribute('text', 'ROOT')
doc.appendChild(root)


xml_maker(node[1][0], root)
