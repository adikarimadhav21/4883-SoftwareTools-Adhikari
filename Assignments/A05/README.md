
## A05 - Binary Searh Tree using Graphviz
### Madhav Adhikari
### Description:
We used a tool like the following: http://mcdemarco.net/tools/family-tree-generator/lineage.html to generate our own unique family tree and clean it by using random names and ages.Then I  will do followong steps to make family tree of this data ( Thanks to help from ChatCPT and [Family tree](https://medium.com/@ahsenparwez/building-a-family-tree-with-python-and-graphviz-e4afb8367316)
 I learned from there as well )

- Read family_tree_data.csv  data using pandas which help to generate datframe of each row of csv
- sort the data by generation; find the oldest patriarch or matriarch  and its on the top of data  frane
- looping the data by generation and make the subgraph for spouse and subgraph for childs and connect them all togther 
- Shape of node according to gender: rectangular for Male and ellipse for female 
- Use HTML table tag to make table in the node to display information of person
- Differnt color of node accrding of clan name 
- Generated the dot files 
- Preview dot file in dot language IDE then download the image of family tree 

 

### Files

|   #   | File            | Description                                        |
| :---: | --------------- | -------------------------------------------------- |
|   1   | family_tree_data.csv       | file that data for family tree   |
|   2  | family_tree_dot_generator.py      | file that holds python code to generate dot files    |
|   3  | family_tree.dot      | file that holds dot files of family tree    |
|   4   | family_tree.svg      | file that holds image of family tree    |
|   5   | requirements.txt      | file that holds  list of dependencies    |




### Instructions

- Make sure you install requirements.txt compontes
- Run family_tree_dot_generator.py
- Place dot files in online dot editor or install Graphviz preview Extension in your IDE


### Example Command:
- python family_tree_dot_generator.py

