import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import cm
from matplotlib.gridspec import GridSpec

def draw_synonym_graph(drug_id, df_synonyms):
    synonyms = df_synonyms[df_synonyms['drugbank_id'] == drug_id]['synonym'].tolist()

    G = nx.Graph()
    G.add_node(drug_id, color='#FF6B6B')
    for synonym in synonyms:
        G.add_node(synonym, color='#9FE2BF')
        G.add_edge(drug_id, synonym)

    pos = nx.spring_layout(G, k=0.8)
    node_colors = [d['color'] for _, d in G.nodes(data=True)]

    nx.draw(G, pos,
           with_labels=True,
           node_color=node_colors,
           node_size=1200,
           font_size=9,
           edge_color='#D3D3D3',
           width=1.5,
           font_weight='bold',
           )

    plt.title(f'Synonyms for {drug_id}', fontsize=12, pad=20)
    plt.show()


import matplotlib.pyplot as plt
import networkx as nx

def draw_pathway_drug_bipartite(df_pathways_to_drugs):
    B = nx.Graph()

    pathways = df_pathways_to_drugs['pathway_name'].unique()
    drugs = df_pathways_to_drugs['drugbank_id'].unique()

    # Add nodes with modified colors
    B.add_nodes_from(pathways, bipartite=0, color='#9FE2BF')  # Soft green
    B.add_nodes_from(drugs, bipartite=1, color='#FF6B6B')     # Coral

    # Add edges
    for _, row in df_pathways_to_drugs.iterrows():
        B.add_edge(row['pathway_name'], row['drugbank_id'])

    # Create manual layout
    pos = {}
    for i, pw in enumerate(pathways):
        # move the pathway nodes a bit to the left (x=0.8)
        pos[pw] = (0.8, i)
    for j, dr in enumerate(drugs):
        pos[dr] = (2, j)

    node_colors = [d['color'] for _, d in B.nodes(data=True)]

    # Make the figure bigger, then draw
    plt.figure(figsize=(10, 8))  # Increase width and height
    nx.draw(
        B, pos, 
        with_labels=True,
        node_color=node_colors,
        node_size=1000,
        font_size=8,
        edge_color='#808080',
        width=0.5
    )
    plt.title('Bipartite Graph of Pathways Interacting with Drugs')

    # This helps ensure axis labels / titles / nodes fit
    plt.tight_layout()
    plt.show()



def draw_histogram_pathways_per_drug(df_pathways_count_per_drug):
    sns.histplot(df_pathways_count_per_drug['num_pathways'], binwidth=1)
    plt.xlabel('number of pathways')
    plt.ylabel('count of drugs')
    plt.title('pathways count per drug')
    plt.show()


def draw_pie_cellular_locations(df_targets):
    counts = df_targets['cellular_location'].value_counts(dropna=True)

    fig, ax = plt.subplots(figsize=(10, 8))

    def autopct_func(pct):
        return f'{pct:.1f}%' if pct >= 2 else ''

    wedges, _, autotexts = ax.pie(
        counts,
        labels=None,
        autopct=autopct_func,
        startangle=140,
        textprops={'fontsize': 12}
    )

    ax.legend(
        wedges,
        counts.index,
        title='Cellular Location',
        loc='center left',
        bbox_to_anchor=(1, 0.5),
        fontsize=9
    )

    ax.set_title('Cellular locations of drug targets', fontsize=14)
    plt.axis('equal')

    plt.tight_layout()
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


def _build_gene_drug_product_graph(gene_name, df_targets, df_products):
    # Get all DrugBank IDs linked to the selected gene
    relevant_drug_ids = df_targets[df_targets['gene_name'] == gene_name]['drugbank_id'].unique()
    # Filter only products matching these DrugBank IDs
    relevant_products = df_products[df_products['drugbank_id'].isin(relevant_drug_ids)]
    
    # Create the graph
    G = nx.Graph()
    # Add the gene node (increased size)
    G.add_node(gene_name, type='gene', size=3500)
    
    product_mapping = {}
    drug_colors = {}
    product_number = 1
    
    # Prepare a color map for drugs
    cmap = cm.Blues
    num_drugs = len(relevant_drug_ids)
    for i, drug_id in enumerate(relevant_drug_ids):
        # Each drug will have a slightly different shade of blue
        drug_colors[drug_id] = cmap(0.2 + 0.7 * i / num_drugs)
    
    # Add nodes and edges for drugs and their products
    for drug_id in relevant_drug_ids:
        # Drug node (increased size)
        G.add_node(drug_id, type='drug', size=2500, color='#4ECDC4')
        G.add_edge(gene_name, drug_id)
        
        # Get unique product names for this drug
        product_names = relevant_products[relevant_products['drugbank_id'] == drug_id]['product_name'].unique()
        
        for product_name in product_names:
            # If this product hasn't been added yet, create a new node
            if product_name not in G.nodes:
                G.add_node(
                    product_name,
                    type='product',
                    size=1000,
                    color=drug_colors[drug_id],
                    number=product_number
                )
                # Add to the legend mapping only the first time we see it
                product_mapping[product_number] = product_name
                product_number += 1
            
            # Create an edge between the drug and this product
            G.add_edge(drug_id, product_name)
    
    return G, product_mapping, relevant_drug_ids


def _position_nodes(G, gene_name, relevant_drug_ids, drug_radius=2.5, product_spread=3.5):
    pos = {}
    pos[gene_name] = (0, 0)
    
    # Arrange drugs in a circle around the gene
    angles = np.linspace(0, 2 * np.pi, len(relevant_drug_ids), endpoint=False)
    for drug_id, angle in zip(relevant_drug_ids, angles):
        x = drug_radius * np.cos(angle)
        y = drug_radius * np.sin(angle)
        pos[drug_id] = (x, y)
    
    # Arrange products around each drug
    for drug_id in relevant_drug_ids:
        product_nodes = [n for n in G.neighbors(drug_id) if G.nodes[n]['type'] == 'product']
        base_x, base_y = pos[drug_id]
        
        for product in product_nodes:
            if product not in pos:  # position it only if not already set
                theta = 2 * np.pi * np.random.random()
                r = product_spread * (np.random.random() ** 0.7)
                dx = r * np.cos(theta)
                dy = r * np.sin(theta)
                
                # Offset from the drug node to avoid overlap
                direction = np.array([base_x, base_y])
                norm = np.linalg.norm(direction)
                if norm > 0:
                    direction /= norm
                offset = direction * 3
                
                pos[product] = (base_x + dx + offset[0], base_y + dy + offset[1])
    
    return pos


def _draw_network(G, pos, product_mapping, gene_name, 
                 figsize=(35, 18), width_ratios=(3, 1.5), 
                 main_font_size=17, legend_font_size=18):
    # Prepare node colors and labels
    colors = []
    labels = {}
    for node in G.nodes:
        node_type = G.nodes[node]['type']
        if node_type == 'gene':
            colors.append('#FF6B6B')   # gene color
            labels[node] = node
        elif node_type == 'drug':
            colors.append('#4ECDC4')  # drug color
            labels[node] = node
        else:  # product
            colors.append(G.nodes[node]['color'])
            labels[node] = str(G.nodes[node]['number'])  # display the product number only
    
    # Create the figure and gridspec
    fig = plt.figure(figsize=figsize)
    gs = GridSpec(1, 2, width_ratios=width_ratios)
    ax_main = fig.add_subplot(gs[0])
    ax_legend = fig.add_subplot(gs[1])
    ax_legend.axis('off')

    # Draw edges and nodes on the main axis
    nx.draw_networkx_edges(G, pos, ax=ax_main, edge_color='gray', alpha=0.3, width=0.8)
    nx.draw_networkx_nodes(
        G, pos, ax=ax_main,
        node_color=colors,
        node_size=[G.nodes[n]['size'] for n in G.nodes],
        edgecolors='white',
        linewidths=0.8
    )
    # Draw labels with a larger font size
    nx.draw_networkx_labels(
        G, pos, ax=ax_main,
        labels=labels,
        font_size=main_font_size,
        font_color='black',
        font_weight='bold'
    )

    # Build the legend (right panel)
    if product_mapping:
        sorted_products = sorted(product_mapping.items(), key=lambda x: x[0])
        legend_text = "Product Legend:\n\n"
        legend_text += "\n".join([f"{num}: {name}" for num, name in sorted_products])
        ax_legend.text(
            0.05, 0.5, 
            legend_text,
            va='center',
            ha='left',
            fontsize=legend_font_size,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray')
        )

    ax_main.set_title(f'Gene {gene_name} Interactions', fontsize=main_font_size + 1)
    ax_main.axis('off')
    plt.tight_layout()
    plt.show()


def draw_gene_drug_product_graph(gene_name, df_targets, df_products):
    # 1) Build the graph
    G, product_mapping, relevant_drug_ids = _build_gene_drug_product_graph(gene_name, df_targets, df_products)
    
    # 2) Position the nodes
    pos = _position_nodes(G, gene_name, relevant_drug_ids)
    
    # 3) Draw the resulting network
    _draw_network(G, pos, product_mapping, gene_name)
