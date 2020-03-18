import pandas as pd
import os

def parse_mr(data_mr):
    ret = []
    for mr in data_mr:
        instance_list = []
        mr_instances = mr.split(',')
        for i in mr_instances:
            splitted = i.split('[')
            instance_list.append((splitted[0].strip(), splitted[1].replace(']', '').strip()))
        ret.append(instance_list)
    return ret

def that_or_and(order):
    if order > 0:
        return ' and '
    else:
        return ' that '

def generate_nl(mr_instance):
    nl = ''
    order_0 = 0
    order_1 = 0
    for mr_type, mr_val in mr_instance:
        if mr_type == 'name':
            nl += mr_val
        elif mr_type == 'eatType':
            nl += (' is a ' + mr_val)
            order_1 += 1
        elif mr_type == 'food':
            if(order_1 > 0):
                nl += ' that'
            nl += ' serves '
            if 'food' in mr_val:
                nl += mr_val
            else:
                nl += (mr_val + ' food')
        elif mr_type == 'priceRange':
            if len(mr_val.split()) > 1:
                nl += (' with a price range of ' + mr_val)
            else:
                nl += (' with a ' + mr_val + ' price range')
        elif mr_type == 'customer rating':
            nl += (' with a ' + mr_val + ' customer rating')
        elif mr_type == 'familyFriendly':
            nl += that_or_and(order_0) + 'is '
            if mr_val == 'no':
                nl += 'not '
            nl += 'family friendly'
            order_0 += 1
        elif mr_type == 'near':
            nl += that_or_and(order_0) + 'is near ' + mr_val
            order_0 += 1
        elif mr_type == 'area':
            nl += that_or_and(order_0) + 'is located in ' + mr_val
            order_0 += 1
    nl += '.'
    return nl


if __name__ == '__main__':
    dataset_dir = 'e2e-dataset'
    result_dir = 'results'
    for split in ['train', 'dev', 'test']:
        data_csv = pd.read_csv(os.path.join(dataset_dir, split + 'set.csv'))
        data_mr = None
        if(split == 'test'):
            data_mr = data_csv['MR']
        else:
            data_mr = data_csv['mr']
        parsed_mr = parse_mr(data_mr)
        nls = []
        for i in parsed_mr:
            nls.append(generate_nl(i))
        result_file = open(os.path.join(result_dir, split + '_rb_gen.txt'), 'w', encoding='utf-8')
        for nl in nls:
            result_file.write(nl + '\n')