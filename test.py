from yaml import safe_load

def yaml_dict(file: str)-> dict:
    """Takes a string for the YAML file path and returns a dictionary"""
    with open(file, "r") as yml:
       return safe_load(yml)  # pass back to the caller python data

for k,v in Networks['Networks'].items():
    print("Your hosts are:", v['hosts'])
    print("Your IP is:", v['subnet'])
