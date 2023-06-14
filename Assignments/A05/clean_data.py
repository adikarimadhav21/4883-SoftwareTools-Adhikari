import pandas as pd
import random


"""
Cleaning Data - Griffins data cleansing code
 This is profess Friffins code . I used for data cleaning 
 I will modify my own code later

"""




def genAgeChoices(oldOnly=False):
  """Creates a list of age choices based on a weighted averages. Meaning more 
     70+ and 80+ ages will be returned than 
  Params:
    oldOnly: if True, then only old ages will be returned
  Returns:
    ages: list of ages to choose from
  """
  ages = []
  # Define the age ranges and their corresponding weights
  # probably not totally accurate when compared to real life
  ageRanges = [(50, 59, 5), (60, 69, 9), (70, 79, 20),
               (80, 89, 32), (90, 99, 23), (100, 109, 5)]
  if not oldOnly:
    ageRanges += [(1, 5, 1), (20, 49, 5)]
    
  for ageTuple in ageRanges:
    for i in range(ageTuple[2]):
      ages.append(random.randint(ageTuple[0], ageTuple[1] + 1))

  random.shuffle(ages)

  return ages



age_choices = genAgeChoices(True)
months = list(range(1, 13))
days = list(range(1, 29))


class Names:
    def __init__(self):
        self.first_names = []
        self.last_names = []
        self.clan_names = []
        first_files = ['Assignments/A05/data/asian_first_names.csv', 'Assignments/A05/data/dnd_first_names.csv', 'Assignments/A05/data/mock_names.csv']
        last_files = ['Assignments/A05/data/asian_surnames.txt', 'Assignments/A05/data/dnd_last_names.txt']

        for first_file in first_files:
            df = pd.read_csv(first_file)
            self.first_names.extend(list(zip(df['first_name'], df['gender'])))
            if first_file == 'Assignments/A05/data/mock_names.csv':
                self.last_names.extend(list(df['last_name']))

        for last_file in last_files:
            with open(last_file) as f:
                rows = f.readlines()
                self.last_names.extend([row.strip().capitalize() for row in rows])

        with open("Assignments/A05/data/clan_names.txt") as f:
            rows = f.readlines()
            self.clan_names.extend([row.strip().capitalize() for row in rows])

        self.last_names = list(set(self.last_names))
        self.first_names = list(set(self.first_names))
        self.first_names = sorted(self.first_names)
        self.last_names = sorted(self.last_names)

    def get_random_last_name(self):
        return random.choice(self.last_names)

    def get_random_first_name_with_gender(self):
        return random.choice(self.first_names)

    def get_random_clan_name(self, id=None):
        if id:
            self.clan_names = sorted(self.clan_names)
            return self.clan_names[id]
        return random.choice(self.clan_names)


name_helper = Names()


def get_first_name_gender_last_name_clan_name(clan_id=None):
    global name_helper
    first_name, gender = name_helper.get_random_first_name_with_gender()
    return first_name, gender, name_helper.get_random_last_name(), name_helper.get_random_clan_name(clan_id)


def get_birth_death(year):
    global age_choices
    global months
    global days

    birth_year = int(year)
    rand_age = random.choice(age_choices)
    death_year = birth_year + rand_age

    birth_month, birth_day = random.choice(months), random.choice(days)
    birth_date = f"{birth_month}/{birth_day}/{birth_year}"

    death_month, death_day = random.choice(months), random.choice(days)
    death_date = f"{death_month}/{death_day}/{death_year}"

    return birth_date, death_date, rand_age


def fix_data():
    old_data = pd.read_csv('Assignments/A05/data/dwarf_family_tree.csv')
    new_data = pd.DataFrame()

    for idx, row in old_data.iterrows():
        birth_date, death_date, age = get_birth_death(row['byear'])
        first_name, gender, last_name, clan_name = get_first_name_gender_last_name_clan_name(int(row['clan']))

        new_row = {
            "id": row['pid'],
            "generation": row['generation'],
            "first_name": first_name,
            "last_name": last_name,
            "gender": gender,
            "birth_date": birth_date,
            "death_date": death_date,
            "age": age,
            "married_year": row['myear'],
            "married_age": row['mage'],
            "personality": row['ptype'],
            "clan_name": clan_name,
            "spouse_id": row['spouseId'],
            "father_id": row['parentId1'],
            "mother_id": row['parentId2'],
            "parent_node_id": row['parentNodeId']
        }

        new_data = pd.concat([new_data, pd.DataFrame(new_row, index=[0])], ignore_index=True)


    return new_data


def write_json(data):
    data.to_json('Assignments/A05/data/dwarf_family_tree.json', indent=4)


def write_csv(data):
    data.to_csv('Assignments/A05/data/family_tree_data.csv', index=False)


if __name__ == "__main__":
    n = Names()
    print(n.get_random_first_name_with_gender())
    print(n.get_random_last_name())
    print(n.get_random_clan_name())
    print(get_first_name_gender_last_name_clan_name())
    print(get_first_name_gender_last_name_clan_name())
    print(get_birth_death(1701))
    print(get_birth_death(1701))

    new_data = fix_data()
    print(new_data)
    write_json(new_data)
    write_csv(new_data)
