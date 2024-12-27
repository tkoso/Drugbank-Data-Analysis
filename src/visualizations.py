import networkx as nx
import matplotlib.pyplot as plt

def draw_synonym_graph(drug_id, df_synonyms):
    synonyms = df_synonyms[df_synonyms['drugbank_id'] == drug_id]['synonym'].tolist()

    G = nx.Graph()
    G.add_node(drug_id, color='red')
    for synonym in synonyms:
        G.add_node(synonym, color='green')
        G.add_edge(drug_id, synonym)

    pos = nx.spring_layout(G, k=0.8)
    node_colors = [d['color'] for _, d in G.nodes(data=True)]

    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1000, font_size=8)
    plt.title(f'Synonyms for {drug_id}')
    plt.show()