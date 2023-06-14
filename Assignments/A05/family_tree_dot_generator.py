from graphviz import Digraph
import pandas as pd
import random
import secrets
import hashlib




# Read data file using pandas: df is a dataframe
df = pd.read_csv('family_tree_data.csv')

def nodeLabelName(person):
    """Make table as node label using HTML table tag
    Params:
        person: dictionary containing person information
    Returns:
        node_label: after formatting tables
    """
    name = "{} {}".format(person['fname'], person['lname'])
    born_died = "{}-{}".format(person['birthDate'], person['deathDate']) if not pd.isnull(person['deathDate']) else str(person['birthDate'])
    node_label = '''<
                    <table border="1" cellborder="1" cellspacing="0" cellpadding="4" style="font-size: 10pt">
                    <tr>
                    <td><b>Name</b></td>
                    <td>{}</td>
                    </tr>
                    <tr>
                    <td><b>Born-Died</b></td>
                    <td>{}</td>
                    </tr>
                    <tr>
                    <td><b>Age</b></td>
                    <td>{}</td>
                    </tr>
                    <tr>
                    <td><b>Clan</b></td>
                    <td>{}</td>
                    </tr>
                    </table>
                    >'''.format(name, born_died, person['age'], person['clanName'])
    return node_label


color_dict = {} # key: clan name and value =color code
def clanColor(clanName):
    """ Generate hash value of color according to clanName
        If already have color hash for  clanName then get and return
        otherwise add new random color expect black , white and already assigned color
          Params:
            clanName
          Returns:
             color hash value
    """
    if clanName in color_dict:
        return color_dict[clanName]
    else:
        color = ''
        while not color or color in ['FFFFFF', '000000'] or color in list(color_dict.values()):
            color = hashlib.sha256(secrets.token_bytes(16)).hexdigest()[:6]

        color_dict[clanName] = '#' + color
        return '#' + color

# Sort the dataframe by generation and within same generation sort by id
df = df.sort_values(by=["generation", "id"])
#df= df.astype(str)

# Initialize dot language with graph attribute
dot = Digraph(comment='Family Tree Using Python', graph_attr={'splines': 'ortho'})

# Collect all nodes of the graph : It will use to track whether nodes is already in graph or not
node_names = []

df=df.fillna("") # Replace all nan values to empty str

connection_node_dic = {} # used to apply logic to connect spouse by diamond shape and respective child to diamond shape

# Iterate through individuals
for _, person in df.iterrows():
    node_id = person['id']
    parent_node_id = person['parentNodeId']
    spouse_id = person['spouseId']
    clan_name = person['clanName']
    gender = person['gender']
    fname = person['fname']
    #Make shape of node according to gender : rectangular for Male and ellipse for female
    sh = 'rect' if gender == 'M' else 'ellipse'
    # Check if the current person has already been added to the graph
    if node_id not in node_names:

        if (spouse_id or spouse_id==0.0)and (parent_node_id in node_names):
            """
                   implementing the sub graph on the basis of spouse
                   Logic : Check Spouse id is not noll and parent_node_id (here same as spouse id in data) in already added nodes that is node_names 
                           if yes then 
                           Add node with same rank level for spouse 
                           Link Spouse by diamond shape with red color edge 
                           Add color according to clan name for node  
                           size also according to gender for node
                           append this node to list of node_names as flag added to graph
                   """
            with dot.subgraph() as s:
                s.attr(rank='same')
                connection_node_dic[node_id] = "{}{}".format(node_id, fname)

                s.node(str(node_id) + fname, label=" ", shape="diamond", height="0.25", width="0.25", style="filled",
                          fillcolor="red")

                s.node(str(node_id), label=nodeLabelName(person.to_dict()), shape=sh,style="filled", fillcolor=clanColor(clan_name))
                s.edge(str(parent_node_id), str(node_id) + fname, arrowhead='none',label="Spouse")
                s.edge(str(node_id) + fname, str(node_id), color='red')
                node_names.append(node_id)
        else:
            """
                   implementing the  graph on the basis of child
                   Logic : If spouse id is null then they should be child so 
                           Add node without same rank so by default top to bottom 
                           Link child  with respective parents  
                           Add color according to clan name for node  
                           size also according to gender for node
                           append this node to list of node_names as flag added to graph 
                   """
            dot.node(str(node_id), label=nodeLabelName(person.to_dict()), shape=sh,style="filled", fillcolor=clanColor(clan_name))
            node_names.append(node_id)
            # Check if the parent node has already been added to the graph
            if parent_node_id in node_names:
                # Connect the current individual to the parent node
                dot.edge(connection_node_dic[parent_node_id], str(node_id),label="Child")



# Save the DOT file
dot.render('family_tree.dot', view=True)