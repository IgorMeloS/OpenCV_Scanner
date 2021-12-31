# =============================================================================
# Scanner engine with OpenCV
# =============================================================================

from transform import points_transform
from skimage.filters import threshold_local
from imutils import paths
import numpy as np
import cv2 as cv
import imutils
import img2pdf
import argparse as arg
import os
import shutil
import datetime

ap = arg.ArgumentParser()
ap.add_argument("-mlt", "--multiple", type = bool, default = False,
                help = "Multiple scan mode, by default False, with you want more than one scan, pass True.")
ap.add_argument("-m", "--mode", type = str, default="c",
                help = "Mode of the scan, by default color (c). Options black and white (bw) or both (cbw)")
ap.add_argument("-s", "--save", type = str, default = "pdf",
                help = "Save mode, by default pdf. You can pass jpg or b to save your with both formats")
ap.add_argument("-op", "--one_pdf",type = bool,  default = True,
                 help = "One pdf by default True. Must be passed when using multiple scan and pdf save mode. If False, each scanned image will be saved in a different pdf.")

args = vars(ap.parse_args())
 #grabing date and hour to create a new folder
date = datetime.datetime.now().strftime("%d_%m_%Y_%H:%M:%S")
nfolder = 'scan_' + date
savin = nfolder + "/"

#list of arguments
mode_list = [True, False]
color_list = ['c', 'bw', 'cbw']
save_list = ['pdf', 'jpg', 'b']
pdf_list = [True, False]

##checking the argmuments for a better scanner
#Multiple mode
if args["multiple"] in mode_list:
    pass
else:
    print("WARNING: You passed '{}' as argument --multiple.".format(args["multiple"]))
    print("The required values are True or False, in this case the multiple page scan is considered")

#Color mode
if args["mode"] in color_list:
    pass
else:
    raise Exception('--mode (-m) must be c, bw or cbw. The value of -m was: {}'.format(args["mode"]))

#save mode
if args["save"] in save_list:
    pass
else:
    raise Exception('--save (-s) must be pdf, jpg or b. The value of -s was: {}'.format(args["save"]))

#One pdf function
if args["one_pdf"] in pdf_list:
    pass
else:
    raise Exception('--one_pdf (-op) must be True or False. The value of -op was: {}'.format(args["one_pdf"]))

print("[INFO] Scanning...")
if args["multiple"] == False:

    dataset = 'input'
    pathImages = list(paths.list_images(dataset))
    if len(pathImages) > 1:
        print("The folder input contains more than one file.\n The scan will consider the file {}".format(pathImages[0]))
    os.makedirs(nfolder)
    image = cv.imread(pathImages[0])
    ratio_h = image.shape[0]/500.
    orig = image.copy()
    image = imutils.resize(image, height=500)

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    gray = cv.GaussianBlur(gray, (5,5), 0)

    edg = cv.Canny(gray, 75, 200)

    cnts = cv.findContours(edg.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv.contourArea, reverse=True)[:5]

    for c in cnts:
        prmt = cv.arcLength(c, True)
        apprx = cv.approxPolyDP(c, 0.01*prmt, True)
        if len(apprx) == 4:
            pts = apprx
            break
    cv.drawContours(image, [pts], -1, (0, 255, 0), 2)



    pts = pts.reshape(4, 2)

    wraped = points_transform(orig, pts*ratio_h)

    g_w = cv.cvtColor(wraped, cv.COLOR_BGR2GRAY)
    T = threshold_local(g_w, 11, offset=10)
    g_w = (g_w > T).astype('uint8')*255

    ## color mode
    #checking the arguments for the color mode
    if args["mode"] == 'c':

        if args["save"] == 'pdf':

            cv.imwrite(savin + 'scan.jpg', wraped)#saving jpg
            with open(savin + "scan.pdf", "wb") as f: #saving pdf
                f.write(img2pdf.convert(savin + 'scan.jpg'))
            f.close()
            paths = list(paths.list_images(savin))
            for img in paths:
                os.remove(img)#removing jpg

        elif args["save"] == 'jpg':
            cv.imwrite(savin + 'scan.jpg', wraped)#saving jpg
        elif args["save"] == 'b':
            cv.imwrite(savin + 'scan.jpg', wraped)#saving jpg
            with open(savin + "scan.pdf", "wb") as f: #saving pdf
                f.write(img2pdf.convert(savin + 'scan.jpg'))
            f.close()


    ## mode black and white
    if args["mode"] == 'bw':

        if args["save"] == 'pdf':

            cv.imwrite(savin + 'scan_bw.jpg', g_w)
            with open(savin + "scan_bw.pdf", "wb") as f:
                f.write(img2pdf.convert(savin + 'scan_bw.jpg'))
            f.close()
            paths = list(paths.list_images(savin))
            for img in paths:
                os.remove(img)

        elif args["save"] == 'jpg':
            cv.imwrite(savin + 'scan_bw.jpg', g_w)

        elif args["save"] == 'b':
            cv.imwrite(savin + 'scan_bw.jpg', g_w)
            with open(savin + "scan_bw.pdf", "wb") as f:
                f.write(img2pdf.convert(savin + 'scan_bw.jpg'))
            f.close()

    ### Mode color and black and white
    if args["mode"] == 'cbw':

        if args["save"] == 'pdf':

            cv.imwrite(savin + 'scan_bw.jpg', g_w)
            with open(savin + "scan_bw.pdf", "wb") as f:
                f.write(img2pdf.convert(savin + 'scan_bw.jpg'))
            f.close()
            paths = list(paths.list_images(savin))
            for img in paths:
                os.remove(img)

            cv.imwrite(savin + 'scan.jpg', wraped)
            with open(savin + "scan.pdf", "wb") as f:
                f.write(img2pdf.convert(savin + 'scan.jpg'))
            f.close()
            paths = list(paths.list_images(savin))
            for img in paths:
                os.remove(img)

        elif args["save"] == 'jpg':

            cv.imwrite(savin + 'scan_bw.jpg', g_w)
            cv.imwrite(savin + 'scan.jpg', wraped)

        elif args["save"] == 'b':

            cv.imwrite(savin + 'scan_bw.jpg', g_w)
            with open(savin + "scan_bw.pdf", "wb") as f:
                f.write(img2pdf.convert(savin + 'scan_bw.jpg'))
            f.close()

            cv.imwrite(savin + 'scan.jpg', wraped)
            with open(savin + "scan.pdf", "wb") as f:
                f.write(img2pdf.convert(savin + 'scan_color.jpg'))
            f.close()


    cwd = os.getcwd()
    dest = cwd + '/' + savin + '/' + 'originals'
    os.makedirs(dest)
    for i in pathImages:
        shutil.copy(i, dest)
    imagePath = os.listdir(dataset)
    for org in imagePath:
        os.remove(dataset + '/' + org)
    print("[INFO] Done!")




elif args['multiple']:

    os.makedirs(nfolder)
    dataset = 'input'
    pathImages = list(paths.list_images(dataset))

    color = []
    bwhite = []
    for i in pathImages:

        image = cv.imread(i)
        ratio_h = image.shape[0]/500.
        orig = image.copy()
        image = imutils.resize(image, height=500)

        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        gray = cv.GaussianBlur(gray, (5,5), 0)

        edg = cv.Canny(gray, 75, 200)

        cnts = cv.findContours(edg.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key = cv.contourArea, reverse=True)[:5]

        for c in cnts:
            prmt = cv.arcLength(c, True)
            apprx = cv.approxPolyDP(c, 0.01*prmt, True)
            if len(apprx) == 4:
                pts = apprx
                break
        cv.drawContours(image, [pts], -1, (0, 255, 0), 2)

        pts = pts.reshape(4, 2)

        wraped = points_transform(orig, pts*ratio_h)

        g_w = cv.cvtColor(wraped, cv.COLOR_BGR2GRAY)
        T = threshold_local(g_w, 11, offset=10)
        g_w = (g_w > T).astype('uint8')*255
        color.append(wraped)
        bwhite.append(g_w)

    ##Saving options
    if args['mode'] == 'c':

        if args['save'] == 'pdf':

            if args['one_pdf'] is True:
                count = 1
                for i in color:
                    cv.imwrite(savin + 'scan_' + str(count) + '.jpg', i)
                    count += 1
                paths_scan = list(paths.list_images(savin))
                with open(savin + "scan.pdf", "wb") as f:
                    f.write(img2pdf.convert(paths_scan))
                f.close()
                for scan in paths_scan:
                    os.remove(scan)
            if args['one_pdf'] is not True:
                count = 1
                for i in color:
                    cv.imwrite(savin + 'scan_' + str(count) + '.jpg', i)
                    count += 1
                paths_scan = list(paths.list_images(savin))
                count = 1
                for i in paths_scan:
                    with open(savin + "scan_" + str(count) + '.pdf', "wb") as f:
                        f.write(img2pdf.convert(i))
                    f.close()
                    count += 1
                for scan in paths_scan:
                    os.remove(scan)

        if args['save'] == 'jpg':

            count = 1
            for i in color:
                cv.imwrite(savin + 'scan_' + str(count) + '.jpg', i)
                count += 1

        if args['save'] == 'b':
            count = 1
            for i in color:
                cv.imwrite(savin + 'scan_' + str(count) + '.jpg', i)
                count += 1
            if args['one_pdf'] is True:
                count = 1
                for i in color:
                    cv.imwrite(savin + 'scan_' + str(count) + '.jpg', i)
                    count += 1
                paths_scan = list(paths.list_images(savin))
                with open(savin + "scan.pdf", "wb") as f:
                    f.write(img2pdf.convert(paths_scan))
                f.close()
            if args['one_pdf'] is not True:
                count = 1
                for i in color:
                    cv.imwrite(savin + 'scan_' + str(count) + '.jpg', i)
                    count += 1
                paths_scan = list(paths.list_images(savin))
                count = 1
                for i in paths_scan:
                    with open(savin + "scan_" + str(count) + '.pdf', "wb") as f:
                        f.write(img2pdf.convert(i))
                    f.close()
                    count += 1
     #black white mode
    if args['mode'] == 'bw':
        if args['save'] == 'pdf':

            if args['one_pdf'] is True:
                count = 1
                for i in bwhite:
                    cv.imwrite(savin + 'scan_bw_' + str(count) + '.jpg', i)
                    count += 1
                paths_scan = list(paths.list_images(savin))
                with open(savin + "scan_bw.pdf", "wb") as f:
                    f.write(img2pdf.convert(paths_scan))
                f.close()
                for scan in paths_scan:
                    os.remove(scan)
            if args['one_pdf'] is not True:
                count = 1
                for i in bwhite:
                    cv.imwrite(savin + 'scan_bw_' + str(count) + '.jpg', i)
                    count += 1
                paths_scan = list(paths.list_images(savin))
                count = 1
                for i in paths_scan:
                    with open(savin + "scan_bw_" + str(count) + '.pdf', "wb") as f:
                        f.write(img2pdf.convert(i))
                    f.close()
                    count += 1
                for scan in paths_scan:
                    os.remove(scan)

        if args['save'] == 'jpg':

            count = 1
            for i in bwhite:
                cv.imwrite(savin + 'scan_bw_' + str(count) + '.jpg', i)
                count += 1

        if args['save'] == 'b':
            ###jpg
            count = 1
            for i in bwhite:
                cv.imwrite(savin + 'scan_bw_' + str(count) + '.jpg', i)
                count += 1
            ###pdf###
            paths_scan = list(paths.list_images(savin))
            if args['one_pdf'] is True:
                with open(savin + "scan_bw.pdf", "wb") as f:
                    f.write(img2pdf.convert(paths_scan))
                f.close()
            if args['one_pdf'] is not True:
                count = 1
                for i in paths_scan:
                    with open(savin + "scan_bw_" + str(count) + '.pdf', "wb") as f:
                        f.write(img2pdf.convert(i))
                    f.close()
                    count += 1


    # mode color black white
    if args['mode'] == 'cbw':

        #pdf
        if args['save'] == 'pdf':
            #one pdf
            if args['one_pdf'] is True:
                #bw
                count = 1
                for i in bwhite:
                    cv.imwrite(savin + 'scan_bw_' + str(count) + '.jpg', i)
                    count += 1
                paths_scan = list(paths.list_images(savin))
                with open(savin + "scan_bw.pdf", "wb") as f:
                    f.write(img2pdf.convert(paths_scan))
                f.close()
                for scan in paths_scan:
                    os.remove(scan)
                #c
                count = 1
                for i in color:
                    cv.imwrite(savin + 'scan_' + str(count) + '.jpg', i)
                    count += 1
                paths_scan = list(paths.list_images(savin))
                with open(savin + "scan.pdf", "wb") as f:
                    f.write(img2pdf.convert(paths_scan))
                f.close()
                for scan in paths_scan:
                    os.remove(scan)
            # multiple pdf
            if args['one_pdf'] is not True:
                #bw
                count = 1
                for i in bwhite:
                    cv.imwrite(savin + 'scan_bw_' + str(count) + '.jpg', i)
                    count += 1
                paths_scan = list(paths.list_images(savin))
                count = 1
                for i in paths_scan:
                    with open(savin + "scan_bw_" + str(count) + '.pdf', "wb") as f:
                        f.write(img2pdf.convert(i))
                    f.close()
                    count += 1
                for scan in paths_scan:
                    os.remove(scan)
                #c
                count = 1
                for i in color:
                    cv.imwrite(savin + 'scan_' + str(count) + '.jpg', i)
                    count += 1
                paths_scan = list(paths.list_images(savin))
                count = 1
                for i in paths_scan:
                    with open(savin + "scan_" + str(count) + '.pdf', "wb") as f:
                        f.write(img2pdf.convert(i))
                    f.close()
                    count += 1
                for scan in paths_scan:
                    os.remove(scan)

        #jpg
        if args['save'] == 'jpg':
            #bw
            count = 1
            for i in bwhite:
                cv.imwrite(savin + 'scan_bw_' + str(count) + '.jpg', i)
                count += 1
            #c
            count = 1
            for i in color:
                cv.imwrite(savin + 'scan_' + str(count) + '.jpg', i)
                count += 1

        if args['save'] == 'b':
            #bw
            ##jpg
            count = 1
            for i in bwhite:
                cv.imwrite(savin + 'scan_bw_' + str(count) + '.jpg', i)
                count += 1
            ###pdf###
            ##One
            paths_scan = list(paths.list_images(savin))
            if args['one_pdf'] is True:
                with open(savin + "scan_bw.pdf", "wb") as f:
                    f.write(img2pdf.convert(paths_scan))
                f.close()

            if args['one_pdf'] is not True:
                count = 1
                for i in paths_scan:
                    with open(savin + "scan_bw_" + str(count) + '.pdf', "wb") as f:
                        f.write(img2pdf.convert(i))
                    f.close()
                    count += 1
            #c
            ##jpg
            count = 1
            for i in color:
                cv.imwrite(savin + 'scan_' + str(count) + '.jpg', i)
                count += 1
            ###pdf###

            paths_scan = list(paths.list_images(savin))
            paths_scan1 = []
            for idx in range(len(paths_scan)):

                if 'bw' in paths_scan[idx]:
                    pass
                else:
                    paths_scan1.append(paths_scan[idx])
            if args['one_pdf'] is True:
                with open(savin + "scan.pdf", "wb") as f:
                    f.write(img2pdf.convert(paths_scan1))
                f.close()
            if args['one_pdf'] is not True:
                count = 1
                for i in paths_scan1:
                    with open(savin + "scan_" + str(count) + '.pdf', "wb") as f:
                        f.write(img2pdf.convert(i))
                    f.close()
                    count += 1
    cwd = os.getcwd()
    dest = cwd + '/' + savin + '/' + 'originals'
    os.makedirs(dest)
    for i in pathImages:
        shutil.copy(i, dest)
    imagePath = os.listdir(dataset)

    for org in imagePath:
        os.remove(dataset + '/' + org)
    print("[INFO] Done!")
