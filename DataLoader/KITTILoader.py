import cv2
import glob
from tqdm import tqdm

from utils.tools import dict_update
from utils.PinholeCamera import PinholeCamera


class KITTILoader(object):
    default_config = {
        "root_path": '/mnt/data/datasets/public/KITTI/KITTI/odometry',
        "sequence": '00',
        "start": 0
    }

    def __init__(self, config=None):
        self.config = self.default_config
        self.config = dict_update(self.config, config)

        if self.config['sequence'] in ["00", "01", "02"]:
            self.cam = PinholeCamera(1241.0, 376.0, 718.8560, 718.8560, 607.1928, 185.2157)
        elif self.config['sequence'] in ["03"]:
            self.cam = PinholeCamera(1242.0, 375.0, 721.5377, 721.5377, 609.5593, 172.854)
        elif self.config['sequence'] in ["04", "05", "06", "07", "08", "09", "10"]:
            self.cam = PinholeCamera(1226.0, 370.0, 707.0912, 707.0912, 601.8873, 183.1104)
        else:
            assert (False), f"Unknown sequence number {self.config['sequence']}"

        # read ground truth pose
        self.pose_path = self.config['root_path'] + '/poses/' + self.config['sequence'] + '.txt'
        with open(self.pose_path) as f:
            self.pose_gt = f.readlines()

        # image id
        self.img_id = self.config['start']
        self.img_N = len(glob.glob(pathname=self.config['root_path'] + '/sequences/' \
                                            + self.config['sequence'] + '/image_0/*.png'))

    def __getitem__(self, item):
        file_name = self.config['root_path'] + '/sequences/' + self.config['sequence'] \
                    + '/image_0/' + str(item).zfill(6) + '.png'
        img = cv2.imread(file_name)
        return img

    def __iter__(self):
        return self

    def __next__(self):
        if self.img_id < self.img_N:
            file_name = self.config['root_path'] + '/sequences/' + self.config['sequence'] \
                        + '/image_0/' + str(self.img_id).zfill(6) + '.png'
            img = cv2.imread(file_name)

            self.img_id += 1

            return img
        raise StopIteration()

    def __len__(self):
        return self.img_N - self.config['start']


if __name__ == "__main__":
    loader = KITTILoader()

    for img in tqdm(loader):
        cv2.imshow('img', img)
        # press Esc to exit
        if cv2.waitKey(10) == 27:
            break