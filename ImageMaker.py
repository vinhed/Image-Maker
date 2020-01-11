from PIL import Image
from time import time
from os import walk, makedirs, remove, path, system
from sys import exit, argv
from math import sqrt

start = time()

# ---------- Settings ---------- #

if(str(argv[1]) == "setup" or str(argv[1]) == "s" or str(argv[1]) == "-s"):
    if not path.exists("./TEMP"):
        makedirs("./TEMP")
    if not path.exists("./Output"):
        makedirs("./Output")
    if not path.exists("./Horizontal"):
        makedirs("./Horizontal")
    if not path.exists("./Collection"):
        makedirs("./Collection")
    print(f"Type -h for help")
    exit()

elif(str(argv[1]) == "h" or str(argv[1]) == "help" or str(argv[1]) == "-h"):
    print(f"Usage: \"ImageMaker.exe [Image Name] [Images in width] [Images in height] [Output width]\"")
    print(f"Image Name          - Name of primary image")
    print(f"Image in width      - Small images in width")
    print(f"Image in height     - Small images in height")
    print(f"Output width        - Width of output image")
    exit()

elif(len(argv) == 5):
    IMGNAME             = str(argv[1])
    IMAGE_IN_X          = int(argv[2])
    IMAGE_IN_Y          = int(argv[3])
    OUTCOME_WIDTH       = int(argv[4])

else:
    print(f"Syntax Error: Use \"ImageMaker.exe [Image Name] [Images in width] [Images in height] [Output width]\"\nType -h for usage")
'''
IMGNAME = "pdp.jpg"
IMAGE_IN_X = 200
IMAGE_IN_Y = 200
OUTCOME_WIDTH = 4000

'''# ---------- Setup ---------- #

try:
    image = Image.open(IMGNAME)
    pixel_layout = image.load()
    width, height = image.size
    aspect_ratio = height / width
except:
    print(f'[-] Error! Can\'t find image "{IMGNAME}"')

if not path.exists("./TEMP"):
    makedirs("./TEMP")
if not path.exists("./Output"):
    makedirs("./Output")
if not path.exists("./Horizontal"):
    makedirs("./Horizontal")
if not path.exists("./Collection"):
    makedirs("./Collection")

IMAGE_SIZE_W        = int(OUTCOME_WIDTH / IMAGE_IN_X)
IMAGE_SIZE_H        = int(OUTCOME_WIDTH / IMAGE_IN_Y * aspect_ratio)
IMAGE_IN_COL        = IMAGE_IN_X
IMAGE_IN_ROW        = IMAGE_IN_Y
PID                 = str(time())[::-4]
FILE_NAME           = f'{IMAGE_SIZE_W}x{IMAGE_SIZE_H}x{IMAGE_IN_ROW} -- {time()}.jpg'
PROCESS_NAME        = f'{IMGNAME.lower().replace(".jpg", "").replace(".png", "")}-{IMAGE_SIZE_W}x{IMAGE_SIZE_H}x{IMAGE_IN_ROW}-{PID}'
TEMP_LIST           = []
IMG_USED            = []

if(len(PROCESS_NAME) > 254):
    PROCESS_NAME = PROCESS_NAME[:-len(PROCESS_NAME) - 254]

if(len(FILE_NAME) > 254):
    FILE_NAME = FILE_NAME[:-len(FILE_NAME) - 254]

empty_folders = []
folders = next(walk('./Output'))[1]

if(len(empty_folders) > 0):
    for folder in empty_folders:
        try:
            remove(f"./Output/{folder}")
            remove(f"./TEMP/{folder}")
            remove(f"./Horizontal/{folder}")
        except:
            pass

try:
    makedirs(f'Horizontal/{PROCESS_NAME}')
    makedirs(f'Output/{PROCESS_NAME}')
    makedirs(f'TEMP/{PROCESS_NAME}')
except:
    pass


files = []
for (_, _, filenames) in walk(f"./Collection/"):
    files.extend(filenames)

for file in files:
    image = Image.open(f"Collection/{file}").convert("RGB")
    image = image.resize((IMAGE_SIZE_W, IMAGE_SIZE_H), Image.NEAREST)
    image.save(f"TEMP/{PROCESS_NAME}/{file}")


# ---------- Program ---------- #

def load_image(path, org):
    global width, height
    image = Image.open(path)
    pixel_layout = image.load()
    width, height = image.size

    if(org):
        global WIDTH, W_OFFSET, HEIGHT, H_OFFSET

        WIDTH = int(width / IMAGE_IN_ROW)
        W_OFFSET = width - (WIDTH * IMAGE_IN_ROW)
        HEIGHT = int(height / IMAGE_IN_COL)
        H_OFFSET = height - (HEIGHT * IMAGE_IN_COL)

    image_list = []

    for row in range(height):
        temp_list = []
        for col in range(width):
            if(len(list(pixel_layout[col, row])) == 4):
                temp_list.append(list(pixel_layout[col, row])[:-1])
            else:
                temp_list.append(list(pixel_layout[col, row]))
        image_list.append(temp_list)

    return image_list


def crop_image(x, y, right, down):

    image_list = []
    for row in range(y, down + y):
        temp_list = []
        for pix in range(x, right + x):
            temp_list.append(org_img[row][pix])
        image_list.append(temp_list)

    return image_list


def compare_images(image_list, crop_org):
    val_0_org = 0
    val_1_org = 0
    val_2_org = 0

    val_0 = 0
    val_1 = 0
    val_2 = 0

    val_0_c = 0
    val_1_c = 0
    val_2_c = 0

    for row in range(HEIGHT):
        for col in range(WIDTH):
            #print(crop_org[row][col], image_list[row][col])
            for val in range(3):
                #print(row, col, val)
                if(val == 0):
                    val_0_org += int(crop_org[row][col][val])
                    val_0 += int(image_list[row][col][val])
                    val_0_c += 1

                elif(val == 1):
                    val_1_org += int(crop_org[row][col][val])
                    val_1 += int(image_list[row][col][val])
                    val_1_c += 1

                elif(val == 2):
                    val_2_org += int(crop_org[row][col][val])
                    val_2 += int(image_list[row][col][val])
                    val_2_c += 1

    r, g, b = (int(val_0_org / val_0_c), int(val_1_org / val_1_c), int(val_2_org / val_2_c))
    cr, cg, cb = (int(val_0 / val_0_c), int(val_1 / val_1_c), int(val_2 / val_2_c))
    color_diff = sqrt(abs(r - cr) ** 2 + abs(g - cg) ** 2 + abs(b - cb) ** 2)

    return color_diff


def checkFolders():
    try:
        makedirs(f'Horizontal/{PROCESS_NAME}')
    except:
        pass
    try:
        makedirs(f'Output/{PROCESS_NAME}')
    except:
        pass
    try:
        makedirs(f'TEMP/{PROCESS_NAME}')
    except:
        pass

    temp_files = []
    for (_, _, filenames) in walk(f"./TEMP/{PROCESS_NAME}/"):
        temp_files.extend(filenames)

    missing_files = []
    for pic in files:
        if(pic not in temp_files):
            missing_files.append(pic)

    if(len(missing_files) > 0):
        print(f"{len(missing_files)} Missing Pictures - Adding...")

        for pic in missing_files:
            image = Image.open(f"./Collection/{pic}")
            image = image.resize((IMAGE_SIZE_W, IMAGE_SIZE_H), Image.NEAREST)
            image.save(f"TEMP/{PROCESS_NAME}/{pic}")


def main():
    global org_img

    inc_img_v = []
    inc_img_h = []
    ETA_list = []

    org_img = load_image(IMGNAME, True)
    #print(f"Width: {WIDTH} W_OFFSET: {W_OFFSET}\nHeight: {HEIGHT} H_OFFSET: {H_OFFSET}\n")

    for filename in files:
        try:
            load_image(f"TEMP/{PROCESS_NAME}/{filename}", False)
        except:
            remove(f"TEMP/{PROCESS_NAME}/{filename}")

    c = 0
    for grid_row in range(IMAGE_IN_ROW):
        for grid_col in range(IMAGE_IN_COL):
            checkFolders()

            image_values = {}
            for filename in files:
                diff = compare_images(load_image(f"TEMP/{PROCESS_NAME}/{filename}", False), crop_image(grid_col * WIDTH, grid_row * HEIGHT, WIDTH, HEIGHT))
                image_values[diff] = filename

            value = min(image_values, key=lambda x:abs(x-0))
            name = image_values[value]

            if(name not in IMG_USED):
                IMG_USED.append(name)

            pct = ((IMAGE_IN_COL * grid_row) + grid_col)*100 / (IMAGE_IN_COL * IMAGE_IN_ROW)
            time_spent = int(time() - start)

            try:
                ETA_list.append(int(time_spent / pct))
                ETA = sum(ETA_list) / len(ETA_list)
            except:
                continue

            if(len(ETA_list) > 9):
                ETA_list.pop(0)

            system('CLS')
            print(f"{round(pct, 2)}% Time Elapsed: {time_spent}s ETA: {int((ETA)/0.01 - time_spent)}s Grid: {grid_row+1} {grid_col+1} Process Name: {PROCESS_NAME} Image: {name}")
            inc_img_h.append(f"TEMP/{PROCESS_NAME}/{name}")



        images = [Image.open(x) for x in inc_img_h]
        widths, heights = zip(*(i.size for i in images))

        total_width = sum(widths)
        max_height = max(heights)

        new_im = Image.new('RGB', (total_width, max_height))

        x_offset = 0
        for im in images:
            new_im.paste(im, (x_offset, 0))
            x_offset += im.size[0]
        inc_img_v.append(f'Horizontal/{PROCESS_NAME}/vertical{len(inc_img_v) + 1}.jpg')
        new_im.save(f'Horizontal/{PROCESS_NAME}/vertical{len(inc_img_v)}.jpg')
        inc_img_h = []

        print(f"\nImages Used: {len(IMG_USED)}/{len(files)}\n")

        if (len(inc_img_v) > 1):
            images_list = inc_img_v
            imgs = [Image.open(i) for i in images_list]

            min_img_width = min(i.width for i in imgs)

            total_height = 0
            for i, img in enumerate(imgs):
                if img.width > min_img_width:
                    imgs[i] = img.resize((min_img_width, int(img.height / img.width * min_img_width)), Image.ANTIALIAS)
                total_height += imgs[i].height

            img_merge = Image.new(imgs[0].mode, (min_img_width, total_height))
            y = 0
            for img in imgs:
                img_merge.paste(img, (0, y))

                y += img.height

            img_merge.save(f"Output/{PROCESS_NAME}/" + FILE_NAME)


print(f"Setup Complete - Setup Took: {round(time() - start, 3)}\n")
start = time()
main()

