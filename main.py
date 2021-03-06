import csv
import svgwrite
from lxml import etree
import matplotlib.pyplot as plt
import networkx as nx
c=0
d =0
MIN_LATITUDE = 0
MIN_LONGITUDE = 0
MAX_LATITUDE = 0
MAX_LONGITUDE = 0
insert_highways = {"motorway", "trunk", "primary", "secondary","tertiary", "unclassified", "residential","living_street"} 
SCALE = 4000


def checktag(tagsA,tagsB):
    a = False
    b= False

    for x in tagsA:
        if 'oneway' in x: 
            a = True
    for y in tagsB:
        if 'yes' in y:
            b = True
            return a and b




def parsing(filename):
    "берем границы  XML "
    global MIN_LATITUDE, MIN_LONGITUDE, MAX_LATITUDE, MAX_LONGITUDE,c, insert_highways, d
    parsed_graph = etree.parse(filename + ".osm")
    bounds = parsed_graph.find('/bounds')
    MIN_LATITUDE = float(bounds.get('minlat'))
    MIN_LONGITUDE = float(bounds.get('minlon'))
    MAX_LATITUDE = float(bounds.get('maxlat'))
    MAX_LONGITUDE = float(bounds.get('maxlon'))
     

    adjacency_list = {}
    coordinates = {}
    tagsV = {}
    tagsK= {}
    adj2 = {}


    for node in parsed_graph.iterfind('/node'):
        coordinates[node.get('id')] = [float(node.get('lon')), float(node.get('lat'))]
    for all_highways in parsed_graph.iterfind('/way/tag[@k="highway"]'):
        if all_highways.get("v") in insert_highways:
            prev_node = None
            d = d+1
            for all_higway_nds in all_highways.iterfind('../nd'):
                
                    if prev_node is None:
                        prev_node = all_higway_nds
                    else:

                        for all_tags in all_highways.iterfind('../tag'):
                            
                            if all_tags.get('k') == 'oneway' and \
                                all_tags.get('v') == 'yes':
                                c = c+1
                                if prev_node.get('ref') not in adjacency_list:
                                    adjacency_list[prev_node.get('ref')] = set()
                                adjacency_list[prev_node.get('ref')].add(
                                all_higway_nds.get('ref'))
                                prev_node = all_higway_nds
                            else:
                                if prev_node.get('ref') not in adjacency_list:
                                    adjacency_list[prev_node.get('ref')] = set()
                                if all_higway_nds.get('ref') not in adjacency_list:
                                    adjacency_list[all_higway_nds.get('ref')] = set()

                                adjacency_list[prev_node.get('ref')].add(
                                    all_higway_nds.get('ref'))
                                adjacency_list[all_higway_nds.get('ref')].add(
                                    prev_node.get('ref'))
                                prev_node = all_higway_nds

    return adjacency_list, coordinates

   
def Tasks(adj_list,filename1,filename2):
    #список смежности
    with open(filename1 + ".csv", 'w') as file:
        csv.writer(file).writerows(adj_list.items())
    # матрица смежности
    with open(filename2 + ".csv", 'w') as file:
        output = csv.writer(file)
        output.writerow([''] + list(adj_list.keys()))

        for first_vertex in adj_list:
            matrix_row = []
            for second_vertex in adj_list:
                if second_vertex in adj_list[first_vertex]:
                    matrix_row.append(1)
                else:
                    matrix_row.append(0)
            output.writerow([first_vertex] + list(matrix_row))





def plotGraphDDD(adjaa_list, locs):
    llpp = []
    tt=0
    ff = ''
    for i in adjaa_list:
        llpp.append(i+' ')
        for h in adjaa_list[i]:     
            ff = str( llpp[tt] )
            ff=ff+h+' '
            llpp[tt]=ff

        tt=tt+1

    thefile = open('test.txt', 'w')
    for item in llpp:
     thefile.write("%s\n" % item)


def plotGraph(filename, locs):
    G = nx.read_adjlist(filename) 
    nx.draw(G, pos=locs, node_size = 0, width = 0.05) 
    plt.axis('off') 
    plt.savefig("graphSvg.svg", dpi=3000, figsize=(10,15)) 
   # plt.savefig('graphPdf.pdf')


adja_list, coord = parsing(input())
Tasks(adja_list,"adj_list","adj_matrix")
plotGraphDDD(adja_list,coord)
plotGraph("test.txt",coord)
print(c)
print(d)
