""" Module for moving assets from nb_dir to site_dir/assets """

def copy_assets():
    """ Copy assets (images, etc) from notebooks folder to docs/assets folder """

    #TODO update so it doesn't overwrite by default --or asks first

    dest = os.path.join(os.path.dirname(__file__), '..', 'docs/assets/')
    print("Preparing to copy asset files...")

    for subdir in inp:
        print("Looking in: {}".format(subdir))
        files = glob.glob(conf.INPUT_NB_DIR + subdir + '/*')
        print("Found files: {}".format(files))
        for src in files:
            if os.path.isfile(src):
                fname = src.split("/")[-1]
                print("Copying file: {}...".format(fname))
                fdest = dest + subdir
                if not os.path.exists(fdest):
                    os.makedirs(fdest)
                copyfile(src, fdest + '/' + fname)

if __name__ == '__main__':
    move()