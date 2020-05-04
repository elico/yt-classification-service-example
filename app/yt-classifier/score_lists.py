import tools
import os
import config
import glob

rate_lists = []

debug = int(config.BaseConfig.DEBUG)


def check_score(vid):
    global rate_lists
    matched_lists = dict()
    if debug > 0:
        print("CHECKING VID Score:", vid)
        print("RATE LISTS:", len(rate_lists))
    for rate_list in rate_lists:
        if debug > 0:
            print("Testing against:", rate_list.Name)

        if rate_list.has_vid(vid):
            if debug > 0:
                print("Found a match for VID:", vid)
            matched_lists[rate_list.Name] = rate_list.Score

    return matched_lists


class YTRateList(object):
    Score = int
    List = list()
    path = str
    Name = str
    Description = str

    def __init__(self, direcotry):
        self.path = direcotry
        self.Name = os.path.basename(direcotry)

        try:
            score_file = open(self.path + '/defaultscore', 'r')

            score_file_lines = score_file.readlines()
            score_file.close()
            valid_score, score = tools.is_valid_score(score_file_lines[0])
            if not valid_score:
                return
            self.Score = score
        except Exception as e:
            print("Score File", e)
            return

        try:
            description_file = open(self.path + '/description', 'r')

            description_file = score_file.readlines()
            description_file.close()
            valid_description = tools.is_string(description_file[0])
        except Exception as e:
            print("Description File", e)

        files = [f for f in glob.glob(self.path + "/*.list", recursive=False)]
        for file in files:
            try:
                score_file = open(file, 'r')
                count = 0
                valid_cout = 0
                for line in score_file:
                    count += 1
                    line = line.strip()
                    if tools.is_string(line):
                        if tools.is_valid_vid(line) is None:
                            continue

                    self.List.append(line)
                    if debug >0:
                        print("VALID VID line:", line)
                    valid_cout += 1
                    # Closing files
                if debug > 0:
                    print("Lines: {}  , In file: {}".format(count, file))
                    print("Valid IDs: {}  , In file: {}".format(valid_cout, file))
                score_file.close()
            except Exception as e:
                print(e)
                continue

    def has_vid(self, vid):
        if vid in self.List:
            return True
        else:
            return False


def read_lists():
    global rate_lists
    # r=root, d=directories, f = files
    print(config.BaseConfig.LISTS_PATH)
    for r, d, f in os.walk(config.BaseConfig.LISTS_PATH):
        print(d)
        for folder in d:
            new_list = YTRateList(config.BaseConfig.LISTS_PATH + "/" + d[0])
            if debug > 0:
                print("Adding list:", new_list.Name, new_list)
            rate_lists.append(new_list)

    if debug > 0:
        print("rate_lists RATE LISTS :", len(rate_lists) )
