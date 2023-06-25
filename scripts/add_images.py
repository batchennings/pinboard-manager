
# les images sont posées dans /data/_new
# vérfier si le nom de l'image est déjà dans la base
# si une image portant le même nom est dans la base, on avertit et on la refuse
# ------
# proposer un ou plusieurs tags pour ces nouvelles images, séparés par des virgules
# les vignettes sont créées (copie, crop, renommage)
# les images acceptées sont rentrées dans la base

from os import listdir
from os.path import isfile, join

path='/Users/patjennings/Documents/pinboard_manager/data/_new'
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
print(onlyfiles)
