import subprocess
import csv
import sys
from flask_login import login_required, current_user
from flask import Flask, Blueprint, flash, render_template, request
from house.auth import login


main = Blueprint('main', __name__)

@main.route("/")
@login_required
def index():
    with open('house/data/scan.csv', "w+", newline='') as scanfile, open('house/data/known.csv', newline='') as knownfile, open("house/data/blacklist.csv", newline='') as blackfile:
        # excute scan 1 round, to csv file in house/data/..
        subprocess.Popen("fing -r 1 -o log,csv,house/data/scan.csv",
                         shell=True, stdout=subprocess.PIPE).stdout.read()
        scan_file = csv.reader(scanfile, delimiter=';')
        known_file = csv.reader(knownfile, delimiter=';')
        black_file = csv.reader(blackfile, delimiter=";")

        black = []
        # add mac to blaclist
        for i in black_file:
            black.append(i[0])

        bekend = []
        scan = []
        # add macs from scan
        for i in scan_file:
            zin = i[5] + ";" + i[4] + ";" + i[6]
            scan.append(zin)
            bekend.append(i[5])
            # naam+mac

        bek = []
        known = []
       # add macs to known
        for i in known_file:
            zin = i[0] + ";" + i[3]
            bek.append(i[0])
            known.append(zin)


        online = []
        # online list
        for mac in known:
            if mac[:17] not in black:
                if mac[:17] in bekend:
                    online.append(mac)

        offline = []
        # offline list
        for mac_add in known:
            if mac_add[:17] not in black:
                if mac_add[:17] not in bekend:
                    offline.append(mac_add)

        new = []
        # new mac list
        for macc in scan:
            if macc[:17] not in black:
                if macc[:17] not in bek:
                    new.append(macc)

    scanfile.close()
    knownfile.close()
    blackfile.close()
    return render_template('index.html', header='House', mac_list=online, offline=offline, new_mac=new)

@main.route('/', methods=['POST'])
@login_required
def my_form_post():
    text = request.form['name']
    mac = request.form['mac_val']
    print((text, mac), file=sys.stderr)
    processed_text = mac + ";" + text
    with open('house/data/known.csv', "a") as csvfile1:
        csvfile1.write(processed_text + "\n")
        csvfile1.close()
    return index()

@main.route("/known")
@login_required
def known():
    macs = []
    with open('house/data/known.csv', "r", newline='') as csvfile3:
        known = csv.reader(csvfile3)

        # known mac addressen
        for mac_known in known:
            macs.append(str(mac_known).strip("[").strip("]").replace("'",""))
    csvfile3.close()
    return render_template('known.html', header='Known Macs', known_mac=macs)


@main.route("/blacklist")
@login_required
def blacklisted():
    macs = []
    with open('house/data/blacklist.csv', "r", newline='') as csvfile3:
        reader3 = csv.reader(csvfile3, delimiter=';')

        # blacklisted mac addressen
        for mac_black in reader3:
            l = str(mac_black).strip("[").strip("]").strip("'")
            macs.append(l)

    csvfile3.close()
    return render_template('blacklist.html', header='Blacklist', blacklist_mac=macs)

@main.route("/blacklist/<mac>", methods=['POST'])
@login_required
# add MAC to blacklist
def blacklist(mac):
    with open("house/data/blacklist.csv", "a") as csvfile2:
        csvfile2.write(mac[:17] + "\n")
        csvfile2.close()
    return index()


@main.route("/remblack/<mac>", methods=['POST'])
@login_required
# remove mac out of the blacklist
def remove(mac):
    r = []
    with open("house/data/blacklist.csv", "r") as csvfile5:
        for row in csv.reader(csvfile5):
            r.append(str(row).replace("'","").strip("[").strip("]"))
    with open("house/data/blacklist.csv", "w") as csvfile8:
        for i in r:
            if i != mac:
                csvfile8.write(i + "\n")
    csvfile8.close()
    csvfile5.close()
    return blacklist()

@main.route("/remknown/<mac>", methods=['POST'])
@login_required
# remove known mac in known table
def remove_known(mac):
    r = []
    with open("house/data/known.csv", "r") as csvfile9:
        for row in csv.reader(csvfile9):
            r.append(str(row).replace("'","").strip("[").strip("]"))
    with open("house/data/known.csv", "w") as csvfile10:
        for i in r:
            if i != mac:
                csvfile10.write(i + "\n")
    csvfile9.close()
    csvfile10.close()
    return known()