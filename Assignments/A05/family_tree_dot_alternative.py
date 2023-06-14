from graphviz import Digraph
import pandas as pd
import random
import secrets
import hashlib


"""
Followong steps to make family tree
- Read family_tree_data.csv  data using pandas which help to generate datframe of each row of csv
- sort the data by generation; find the oldest patriarch or matriarch  and its on the top of data  frane
- looping the data by generation and make the subgraph for spouse and subgraph for childs and connect them all togther 
- Shape of node according to gender: rectangular for Male and ellipse for female 
- Use HTML table tag to make table in the node to display information of person
- Differnt color of node accrding of clan name 
- Generated the dot files 
- Preview dot file in dot language IDE then download the image of family tree 

"""



# Read data file using pandas : df is dataframe
df = pd.read_csv('family_tree_data.csv')
#df.columns = df.columns.str.strip()


def nodeLabelName(fname, lname, birthDate, deathDate, age, clanName):
    """ make table as node lable using html table tag  
      Params:
        fname, lname, birthDate, deathDate, age, clanName
      Returns:
         nodelable: after formting tables 
      """
    name = "{} {}".format(fname, lname)
    born_died = "{}-{}".format(birthDate, deathDate) if not pd.isnull(deathDate) else str(birthDate)
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
                        >'''.format(name, born_died, age, clanName)
    return node_label


color_dict = {}
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


#sort the dataframe by generation
df.sort_values(by=["generation"])
# fill empty value if values have NaN
df.fillna('')

"""
Find first acchestor 
Logic: if the parentNodeId =-1 in data , this row contains oldest  patriarch or matriarch
"""
oldest_p_or_m = df.loc[df['parentNodeId'] == -1, 'fname'].iloc[0]
"""
Determine the person who is added on the graph or remaining to add in the graph
Logic: Insert record_identifier with 0 for all data and after add the person in the graph update record_identifier with 1
        that is 1 means already in the graph and 0 means reaming to add in graph
"""
df['record_identifier '] = 0  

# generation_identifier_list hold the previous  generation id which used to find current person's spouse id and parents id
generation_identifier_list = [df.loc[df['parentNodeId'] == -1, 'id'].iloc[0]]

# this holds generation_identifier_list as whole list after generation_identifier_list refreshing later
full_generation_identifier_list = []


#  initialize dot langauge  with  graph attribute
dot = Digraph(comment='Family Tree Using Python', graph_attr={'splines': 'ortho'})

#Collect all nodes of graph
node_nm = []

"""
Initializing first node for  oldest patriarch or matriarch
Extract all data from data frame using loc 
Make nodes with different attribute 
Color used according to clan name
Make shape of node according to gender : rectangular for Male and ellipse for female 
"""
gender = df.loc[df['fname'] == oldest_p_or_m, 'gender'][0]
birthDate = df.loc[df['fname'] == oldest_p_or_m, 'birthDate'][0]
deathDate = df.loc[df['fname'] == oldest_p_or_m, 'deathDate'][0]
clanName = df.loc[df['fname'] == oldest_p_or_m, 'clanName'][0]
age = df.loc[df['fname'] == oldest_p_or_m, 'age'][0]
lname = df.loc[df['fname'] == oldest_p_or_m, 'lname'][0]
sh = 'rect' if gender == 'M' else 'ellipse'
dot.node(oldest_p_or_m, nodeLabelName(oldest_p_or_m, lname, birthDate, deathDate, age, clanName), style="filled",
         fillcolor=clanColor(clanName), shape=sh)
node_nm.append(oldest_p_or_m)

# first node is added in graph so update the flag =1 for this record
df.loc[df['fname'] == oldest_p_or_m, 'record_identifier '] = 1

# this dictionary will use later to connect diamond shape node and respective child
connection_node_dic = {}

"""
make graph according to generation instead of looping data frame
so calculate the newest generation that is max of generation columns  
 and random number due to spouse relation also consider in generation loop
"""
#todo
#max_iteration = df['generation'].max() +1
max_iteration = 20
for i in range(0, max_iteration):
    # Retain only data which need to add in graph 
    remaining_df = df[df['record_identifier '] == 0]
    remaining_df.fillna('')
    # Exist loop after all individuals have been inserted in graph
    if len(remaining_df) == 0:  
        break
    else:
        """
        Find current generation according to previous generation (spouse or parents)
        Logic: Search parentNodeId of each row with previously inserted ids in graph that is generation_identifier_list
             and update the current_generation_indentifier column 
             Here 1 in current_generation_indentifier this current generation 0 means other generation
        """
        # search  parentNodeId in  generation_identifier_list each row by using lambda
        remaining_df['current_generation_indentifier'] = remaining_df.apply(lambda x: 1 if x['parentNodeId'] in generation_identifier_list else 0, axis=1)
        remaining_df.fillna('')

        """
        implementing the sub graph on the basis of spouse
        Logic : Retain only current generation with spouse relation that is spouseId is not null
            Add node with same rank level
            Add color according to clan name and size also according to gender 
                
        """ 
        current_generation = remaining_df[(remaining_df['current_generation_indentifier'] == 1) & (remaining_df['spouseId'].fillna('') != '')]
        if len(current_generation) > 0:
            for j in range(0, len(current_generation)):
                person = current_generation['fname'].iloc[j]
                lname = current_generation['lname'].iloc[j]
                relation_person = df.loc[df['id'] == current_generation['parentNodeId'].iloc[j], 'fname'].iloc[0]
                g = current_generation['gender'].iloc[j]
                birthDate = current_generation['birthDate'].iloc[j]
                deathDate = current_generation['deathDate'].iloc[j]
                clanName = current_generation['clanName'].iloc[j]
                age = current_generation['age'].iloc[j]

                sh = 'rect' if g == 'M' else 'ellipse'

                born_died = "{}-{}".format(current_generation['birthDate'].iloc[j],
                                           current_generation['deathDate'].iloc[j]) if not pd.isnull(
                    current_generation['deathDate'].iloc[j]) else str(
                    current_generation['birthDate'].iloc[j])

                ## properties prepate for making node with the required attribute
                with dot.subgraph() as subs:
                    subs.attr(rank='same')
                    #		a1 [shape=diamond,label="",height=0.25,width=0.25];
                    connection_node_dic[person] = "{}{}".format(j, person)

                    subs.node(str(j) + person, label=" ", shape="diamond", height="0.25", width="0.25", style="filled",
                              fillcolor="red")
                    subs.node(person, nodeLabelName(person, lname, birthDate, deathDate, age, clanName), shape=sh,
                              style="filled", fillcolor=clanColor(current_generation['clanName'].iloc[j]))
                    node_nm.append(person)
                    # subs.edge(per2, per1, arrowhead='none', color="black:invis:black")
                    subs.edge(relation_person, str(j) + person, arrowhead='none')
                    subs.edge(str(j) + person, person, arrowhead='none', label="Married")


        """
        implementing the sub graph on the basis of child 
        Logic : Retain only current generation with child relation that is spouseId is  null
            Add node with default that is top bottom
            Add color according to clan name and size also according to gender 
                
        """
        remaining_df.fillna('')
        current_generation = remaining_df[(remaining_df['current_generation_indentifier'] == 1) & (remaining_df['spouseId'].fillna('') == '')]
        if len(current_generation) > 0:
            for j in range(0, len(current_generation)):
                person = current_generation['fname'].iloc[j]
                lname = current_generation['lname'].iloc[j]
                relation_person = df.loc[df['id'] == current_generation['parentNodeId'].iloc[j], 'fname'].iloc[0]
                g = current_generation['gender'].iloc[j]
                birthDate = current_generation['birthDate'].iloc[j]
                deathDate = current_generation['deathDate'].iloc[j]
                clanName = current_generation['clanName'].iloc[j]
                age = current_generation['age'].iloc[j]
                sh = 'rect' if g == 'M' else 'ellipse'
                dot.node(person, nodeLabelName(person, lname, birthDate, deathDate, age, clanName), shape=sh,
                         style="filled", fillcolor=clanColor(current_generation['clanName'].iloc[j]))
                node_nm.append(person)
                dot.edge(connection_node_dic[relation_person], person)
        """
        Update the person who is added on the graph 
        Logic: Update full_generation_identifier_list and generation_identifier_list to tract next and current generation 
            Update record_identifier with 1 for each row of  data that are inserted in graph 
              
                
        """
        full_generation_identifier_list.extend(generation_identifier_list)
        generation_identifier_list = list(remaining_df.loc[remaining_df['current_generation_indentifier'] == 1, 'id'])
        df['record_identifier '] = remaining_df.apply(lambda x: 1 if (x['id'] in generation_identifier_list) | (x['id'] in full_generation_identifier_list) else 0,
                                        axis=1)

# Save the DOT file
dot.render('family_tree_alternative.dot', view=True)
