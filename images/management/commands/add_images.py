
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
from os.path import isfile, join, getctime, getmtime, splitext
import shutil
# from django.db import models
from django.core.management.base import BaseCommand, CommandError
from images.models import Image
from PIL import Image as Img
from datetime import datetime
import subprocess
import ffmpeg

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

        ext_images = ['.jpg', '.jpeg', '.JPEG', '.JPG', '.png', '.PNG', '.gif', '.webp']
        ext_videos = ['.m4v', '.mp4', '.mov']

        add_list = []

        is_active = True # mettre sur True pour que le script écrive dans la base et copie les fichiers. sur False pour les tests

        def check_file(f, list):
            check_passed = True
            f_noext = splitext(f)[0]
            for g in list:
                if g == f_noext:
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
                u = f_tags[t]
                u_nospace = u.strip()
                result+='\''+u_nospace+'\''
                if t != len(f_tags)-1:
                    result+=','
                t+=1
            result+= ']'
            return result

        def generate_thumbnail_from_video(in_filename, out_filename):
            # print(in_filename)
            probe = ffmpeg.probe(in_filename)
            time = float(probe['streams'][0]['duration']) // 2
            v = 0
            width = 960
            while probe['streams']:
                print(probe['streams'][v])
                if 'width' in probe['streams'][v]:
                    width = probe['streams'][v]['width']
                    break
                v+=1
            try:
                (
                    ffmpeg
                    .input(in_filename, ss=time)
                    .filter('scale', width, -1)
                    .output(out_filename, vframes=1)
                    .overwrite_output()
                    .run(capture_stdout=True, capture_stderr=True)
                )
            except ffmpeg.Error as e:
                print(e.stderr.decode(), file=sys.stderr)
                sys.exit(1)

        for f in listdir(input_folder):
            if isfile(join(input_folder, f)):
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

            a_noext = splitext(a)[0]
            a_ext = splitext(a)[1]

            a_type = ''
            thumb_file = ''

            for t in ext_images:
                # print(t, ' vs ', a_ext)
                if a_ext == t:
                    a_type = 'image'

            for u in ext_videos:
                if a_ext == u:
                    a_type = 'video'

            if is_active:
                a_created = datetime.fromtimestamp(getmtime(join(input_folder, a))).strftime('%Y-%m-%d')
                shutil.copyfile(join(input_folder, a), join(data_folder, a)) #copie le fichier principal

                if a_type == 'image':
                    shutil.copyfile(join(input_folder, a), join(data_thumbnails_folder, a)) # copie le fichier principal pour créer la vignette
                    thumb_file = join(data_thumbnails_folder, a)
                elif a_type == 'video':
                    generate_thumbnail_from_video(join(input_folder, a), join(data_thumbnails_folder, a_noext+'.jpg')) # extrait une image de la vidéo
                    thumb_file = join(data_thumbnails_folder, a_noext+'.jpg')

                with Img.open (thumb_file) as img:
                    cur_w, cur_h = img.size

                    if cur_w > cur_h: # landscape
                        new_width = int(thumb_size*(cur_w/cur_h))
                        th_size = (new_width, thumb_size)
                        crop_box = ((new_width-thumb_size)/2, 0, thumb_size+((new_width-thumb_size)/2), thumb_size)
                        resized = img.resize(th_size).crop(crop_box)
                    elif cur_h > cur_w: # portrait
                        new_height = int(thumb_size*(cur_h/cur_w))
                        th_size = (thumb_size, new_height)
                        crop_box = (0, (new_height-thumb_size)/2, thumb_size, thumb_size+((new_height-thumb_size)/2))
                        resized = img.resize(th_size).crop(crop_box)
                    else: # square
                        th_size = (thumb_size,thumb_size)
                        resized = img.resize(th_size)

                    resized.convert("RGB").save(join(data_thumbnails_folder, a_noext+"_mini.jpg"), "JPEG")
                    remove(thumb_file)

                remove(join(input_folder, a))

                print(a+' créé le '+a_created)
                print(a+' copié dans data')
                print(a+' copié dans data/thumbnails')
                print(a+' : vignette créée')
                print(a+' supprimé de _new')
                print(a+' ajouté à la base, avec les tags : '+tags)

                new_record = Image(name=a_noext, file=a, tags=tags, thumb=a_noext+"_mini.jpg", date_created=a_created, type=a_type)
                new_record.save()
