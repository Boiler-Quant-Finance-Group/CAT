import re
def get_pairs_kraken(pair_tups = True):
    pattern_pair = "[A-Z0-9]{2,5}/[A-Z]{2,5}"
    file=open("krakenpairs.txt","r")
    string = file.read()
    pairs = (re.findall(pattern_pair, string))
    updated_pairs = []
    for pair in pairs:
        updated_pairs.append(tuple(pair.split("/")))
    
    volume_pattern = "[0-9]+[.]*[0-9]+[KM]"
    volumes = (re.findall(volume_pattern, string))
    updated_volumes = []
    for vol in volumes:
        if "K" in vol:
            updated_volumes.append(float(vol.replace("K", ""))*1000)
        else:
            updated_volumes.append(float(vol.replace("M", "")) * 1_000_000)

#     print("updated pairs:",updated_pairs)
#     print("updated pairs size", len(updated_pairs))
#     print("updated_volumes:", updated_volumes)
#     print("updated_volumes size:", len(updated_volumes))
#     print((volumes))
    merged_list = list(tuple(zip(updated_pairs, updated_volumes)))

    top_400_sorted = sorted(merged_list, key=lambda tup: tup[1], reverse=True)

    if pair_tups:
        return [x[0] for x in top_400_sorted]
    else:
        return[(x[0][0] + x[0][1]) for x in top_400_sorted]
        

