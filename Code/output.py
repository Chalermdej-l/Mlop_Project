import json

def main():
    json_data_raw = open('output.json')
    json_data = json.load(json_data_raw)
    env_dict = {
    'ecr_registry_url' : json_data['ecr_registry_url']['value'],
    'ecr_repo_url' : json_data['ecr_repo_url']['value'],
    'instance_dns_name' : json_data['instance_dns_name']['value'],
    'rds_endpoint_ml' : json_data['rds_endpoint_ml']['value'][:-5],
    'rds_endpoint_moni' : json_data['rds_endpoint_moni']['value'][:-5]
    }
    env_list = list(env_dict.keys())
    new_file = []
    with open('.env','r') as con_env:
        env_file = con_env.read().split('\n')
        for val in env_file:
            key = val[:val.find('=')-1].strip()
            if  key in env_list:
                new_val = env_dict[key]
                new_val = key + f" = '{new_val}'"
                new_file.append(new_val)
            else:
                new_file.append(val)
    new_file = '\n'.join(new_file)
    with open('.env','w')as f:
        f.write(new_file)

if __name__ == '__main__':
    main()
