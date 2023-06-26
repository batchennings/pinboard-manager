
# les images sont posées dans /data/_new
# vérfier si le nom de l'image est déjà dans la base
# si une image portant le même nom est dans la base, on avertit et on la refuse
# ------
# proposer un ou plusieurs tags pour ces nouvelles images, séparés par des virgules
# les vignettes sont créées (copie, crop, renommage)
# les images acceptées sont rentrées dans la base

# run script within django
# python manage.py shell < scripts/add_images.py
import sys
from os import listdir, remove
from os.path import isfile, join, getctime, getmtime
import shutil
# from django.db import models
from django.core.management.base import BaseCommand, CommandError
from images.models import Image
from PIL import Image as Img
from datetime import datetime

class Command(BaseCommand):
    help = 'Update database with new images'

    def handle(self, *args, **options):
        exclusion_list = ['.DS_Store']
        presence_list = []
        images = Image.objects.all().values('name')
        thumb_size = 480

        for i in images:
            presence_list.append(i['name'])

        input_folder='/Users/patjennings/Documents/pinboard_manager/data/_new'
        data_folder='/Users/patjennings/Documents/pinboard_manager/data'
        data_thumbnails_folder='/Users/patjennings/Documents/pinboard_manager/data/thumbnails'

        add_list = []

        def check_file(f, list):
            check_passed = True
            for g in list:
                if g == f:
                    check_passed = False
            if check_passed:
                return True
            else:
                return False

        def format_tags(tags):
            f_tags = tags_in.split(",")
            result = '['
            t=0
            while t < len(f_tags):
                result+='\''+f_tags[t]+'\''
                if t != len(f_tags)-1:
                    result+=','
                t+=1
            result+= ']'
            return result

        for f in listdir(input_folder):
            if isfile(join(input_folder, f)):
                # print(getctime(join(input_folder, f)))
                check_db = check_file(f, presence_list)
                check_exclusion = check_file(f, exclusion_list)
                if check_db and check_exclusion:
                    add_list.append(f)
                    print(f+' accepté')
                else:
                    print(f+' rejeté')
                # shutil.copyfile(join(input_folder, f), join(data_folder, f))

        tags_in = input("étiquettes, séparées par des virgules: ")
        tags = format_tags(tags_in)

        for a in add_list:

            a_created = datetime.fromtimestamp(getmtime(join(input_folder, a))).strftime('%Y-%m-%d')
            print(a+' créé le '+a_created)

            shutil.copyfile(join(input_folder, a), join(data_folder, a))
            print(a+' copié dans data')

            shutil.copyfile(join(input_folder, a), join(data_thumbnails_folder, a))
            print(a+' copié dans data/thumbnails')

            with Img.open (join(data_thumbnails_folder, a)) as img:
                # img.thumbnail(thumb_size, Img.Resampling.LANCZOS)
                cur_w, cur_h = img.size

                if cur_w > cur_h: 
                    print('landscape')
                    new_width = int(thumb_size*(cur_w/cur_h))
                    th_size = (new_width, thumb_size)
                    crop_box = ((new_width-thumb_size)/2, 0, thumb_size+((new_width-thumb_size)/2), thumb_size)
                    # crop_box = (0, 0, 480, 480)
                    # resized = img.resize(th_size)
                    resized = img.resize(th_size).crop(crop_box)
                elif cur_h > cur_w:
                    print('portrait')
                    new_height = int(thumb_size*(cur_h/cur_w))
                    th_size = (thumb_size, new_height)
                    crop_box = (0, (new_height-thumb_size)/2, thumb_size, thumb_size+((new_height-thumb_size)/2))
                    # crop_box = (0, 0, 480, 480)
                    # resized = img.resize(th_size)
                    resized = img.resize(th_size).crop(crop_box)
                else:
                    print('square')
                    th_size = (thumb_size,thumb_size)
                    resized = img.resize(th_size)

                print(th_size)
                resized.convert("RGB").save(join(data_thumbnails_folder, a), "JPEG")

                # resized = img.resize((320,320))
            print(a+' : thumbnail traité')

            remove(join(input_folder, a))
            print(a+' supprimé de _new')

            # a_tags = '['+tags+']'
            print(a+' ajouté à la base, avec les tags : '+tags)

            new_record = Image(name=a, file=a, tags=tags, thumb=a, date_created=a_created)
            new_record.save()
