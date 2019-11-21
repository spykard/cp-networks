import networkx
import matplotlib.pyplot as plt

# There are only 3 existing repos
# https://github.com/potassco/asprin (Python)
# https://github.com/FabienLab/CPnets-McDiarmid (Python)
# https://github.com/nmattei/GenCPnet (C++)
# https://github.com/KathrynLaing/DQ-Pruning (R)

# Theory
# https://arxiv.org/pdf/1107.0023.pdf
# https://ourspace.uregina.ca/bitstream/handle/10294/7676/Alanazi_Eisa_200277152_PHD_CS_Spring2017.pdf

# Preferences
preference_node_1 = "Fish soup"  # strictly prefered over Vegetable Soup
preference_node_2_a = "Red Wine"  # depends on the soup, it is prefered if Vegetable Soup
preference_node_2_b = "White Wine"  # depends on the soup, it is prefered if Fish Soup

G = networkx.Graph()
G.add_edges_from([(1, 2), (1, 3)])
G.add_node(1)
G.add_edge(1, 2)
G.add_node("spam")        # adds node "spam"
G.add_nodes_from("spam")  # adds 4 nodes: 's', 'p', 'a', 'm'
G.add_edge(3, 'm')
print(G.degree(1))

lollipop = networkx.lollipop_graph(10, 20)

print(lollipop.degree())

networkx.draw_circular(lollipop, with_labels=True, font_weight='bold')
plt.show()