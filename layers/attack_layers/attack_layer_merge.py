import json
import argparse
import sys
import traceback
# TODO: Scores merging by weights. Currently only average is supported and all
# properties of first layer is imported

if __name__ == "__main__":
    # handle arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", nargs='+',
                        dest="input_fn", default="../data/samples/APT1.json ../data/samples/APT12.json",
                        help="input ATT&CK layer json file ex: APT1.json APT12.json")
    parser.add_argument("-c", "--comments",
                        dest="delimiter", action="store_true",
                        default=True,
                        help="input delimiter to seperate comments by")
    parser.add_argument("-d", "--delimiter",
                        dest="delimiter", default="\n",
                        help="input delimiter to seperate comments by")
    args = parser.parse_args()
    if isinstance(args.input_fn, str):
        file_input_list = args.input_fn.split(' ')
        # print(file_input_list)
    elif isinstance(args.input_fn, list):
        file_input_list = args.input_fn
        if len(file_input_list) < 2:
            print('Error: Please input 2 files to merge')
            sys.exit(1)
    else:
        print('Error in input please check file names')
        sys.exit
    try:
        with open(file_input_list[0], 'r') as f:
            final_layer = json.load(f)
        final_layer['name'] = ""
        final_layer['techniques'] = []
        final_techniques = {}
        for i in file_input_list:
            # print('Loading '+i)
            with open(i, 'r') as f:
                temp_layer = json.load(f)
            final_layer['name'] += temp_layer.get('name', 'Layer')
            temp_techniques = temp_layer.get('techniques', [])
            for z in temp_techniques:
                if z['techniqueID'] + z['tactic'] not in final_techniques.keys():
                    final_techniques[z['techniqueID'] + z['tactic']] = {}
                    final_techniques[z['techniqueID'] + z['tactic']]['count'] = 1
                    final_techniques[z['techniqueID'] + z['tactic']]['result'] = z
                else:
                    final_techniques[z['techniqueID'] + z['tactic']]['count'] += 1
                    temp_score = final_techniques[z['techniqueID'] + z['tactic']]['result']['score']
                    temp_score = (temp_score+z['score'])/final_techniques[z['techniqueID']]['count']                        # print(temp_score)
                    final_techniques[z['techniqueID'] + z['tactic']]['result']['comment'] += args.delimiter
                    final_techniques[z['techniqueID'] + z['tactic']]['result']['comment'] += z['comment']
        for z in final_techniques:
            # import ipdb; ipdb.set_trace()
            if final_techniques[z]['count'] == 1:
                final_techniques[z]['result']['score'] = final_techniques[z]['result']['score']/len(file_input_list)
                final_layer['techniques'].append(final_techniques[z]['result'])
            else:
                final_layer['techniques'].append(final_techniques[z]['result'])
        print(json.dumps(final_layer, indent=4))
    except Exception as e:
        traceback.print_exc()
        print(e)
