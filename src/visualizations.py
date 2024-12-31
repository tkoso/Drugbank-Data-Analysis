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


def draw_pie_cellular_locations(df_targets):
    cellular_locations = df_targets['cellular_location'].value_counts(dropna=True) # dropping NaN counts
    cellular_locations.plot.pie(autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Cellular locations of drug targets')
    plt.show()

def draw_pie_chart_groups(df_groups):
    group_sizes = df_groups['group'].value_counts()
    group_sizes.plot.pie(
        startangle=140,
        autopct = lambda p: f'{int(p * sum(group_sizes) / 100)}'
    )
    plt.axis('equal')
    plt.title('Distribution of drugs in groups')
    plt.show()

def draw_gene_drug_product_graph(gene_name, df_targets, df_products):
    relevant_drug_ids = df_targets[df_targets['gene_name'] == gene_name]['drugbank_id'].unique()
    relevant_products = df_products[df_products['drugbank_id'].isin(relevant_drug_ids)]

    G = nx.Graph()
    G.add_node(gene_name, color='red')
    for drug_id in relevant_drug_ids:
        G.add_node(drug_id, color='green')
        G.add_edge(gene_name, drug_id)

    
    for _, row in relevant_products.iterrows():
        G.add_node(row['product_name'], color='blue')
        G.add_edge(row['drugbank_id'], row['product_name'])

    pos = nx.spring_layout(G, k=0.8)
    node_colors = [d['color'] for _, d in G.nodes(data=True)]

    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1000, font_size=8)
    plt.title(f'Products of drugs targeting {gene_name}')
    plt.show()