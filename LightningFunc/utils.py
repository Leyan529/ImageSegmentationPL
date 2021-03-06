import os
from torchinfo import summary
import torch
import numpy as np
import matplotlib.pyplot as plt

def saveDetail(self):
    model_stats = summary(self.cuda(), self.sample)
    # model_stats = self.summarize(mode='full')
    os.makedirs(self.dir, exist_ok=True)
    summary_str = str(model_stats)
    summaryfile = os.path.join(self.dir, 'summary.txt')
    summary_file = open(summaryfile, 'w', encoding="utf-8")
    summary_file.write(summary_str + '\n')
    summary_file.close()


# def writeCSV(self):    
#     self.target.to_csv(os.path.join(self.dir, 'pred.csv'), index=False)     
#     tensorboard_logs = {'Info': "Write Successed!!!"}
#     return tensorboard_logs

def write_Best_model_path(self):  
    best_model_path = self.checkpoint_callback.best_model_path
    if (best_model_path!=""):
        best_model_file = os.path.join(self.dir, 'best_model_path.txt')
        best_model_file = open(best_model_file, 'w', encoding="utf-8")
        print("\nWrite best_model_path : %s \n"% best_model_path)
        best_model_file.write(best_model_path + '\n')
        best_model_file.close()

def read_Best_model_path(self):  
    best_model_file = os.path.join(self.dir, 'best_model_path.txt')
    if os.path.exists(best_model_file):
        best_model_file = open(best_model_file, 'r', encoding="utf-8")
        best_model_path = best_model_file.readline().strip()
        print("\nLoad best_model_path : %s \n"% best_model_path)
        self.load_from_checkpoint(checkpoint_path=best_model_path, 
                                    num_classes=self.num_classes, 
                                    args=self.args,
                                    map_location='cpu')
        best_model_file.close()    
    else:
        print("No model can load \n")
        if not os.path.exists(best_model_file):
            self.saveDetail()


def makegrid(output,numrows):
    outer=(torch.Tensor.cpu(output).detach())
    plt.figure(figsize=(20,5))
    b=np.array([]).reshape(0,outer.shape[2])
    c=np.array([]).reshape(numrows*outer.shape[2],0)
    i=0
    j=0
    while(i < outer.shape[1]):
        img=outer[0][i]
        b=np.concatenate((img,b),axis=0)
        j+=1
        if(j==numrows):
            c=np.concatenate((c,b),axis=1)
            b=np.array([]).reshape(0,outer.shape[2])
            j=0            
        i+=1
    return c

def decode_seg_map_sequence(label_masks, dataset='pascal'):
    rgb_masks = []
    for label_mask in label_masks:
        rgb_mask = decode_segmap(label_mask, dataset)
        rgb_masks.append(rgb_mask)
    rgb_masks = torch.from_numpy(np.array(rgb_masks).transpose([0, 3, 1, 2]))
    return rgb_masks


def decode_segmap(label_mask, dataset, plot=False):
    """Decode segmentation class labels into a color image
    Args:
        label_mask (np.ndarray): an (M,N) array of integer values denoting
          the class label at each spatial location.
        plot (bool, optional): whether to show the resulting color image
          in a figure.
    Returns:
        (np.ndarray, optional): the resulting decoded color image.
    """
    if dataset == 'VOCModule' or dataset == 'COCOModule':
        n_classes = 21
        label_colours = get_pascal_labels()
    elif dataset == 'CityscapeModule':
        n_classes = 19
        label_colours = get_cityscapes_labels()
    elif dataset == 'BDD100KModule':
        n_classes = 41
        label_colours = get_bdd100k_labels()
    else:
        raise NotImplementedError

    r = label_mask.copy()
    g = label_mask.copy()
    b = label_mask.copy()
    for ll in range(0, n_classes):
        r[label_mask == ll] = label_colours[ll, 0]
        g[label_mask == ll] = label_colours[ll, 1]
        b[label_mask == ll] = label_colours[ll, 2]
    rgb = np.zeros((label_mask.shape[0], label_mask.shape[1], 3))
    rgb[:, :, 0] = r / 255.0
    rgb[:, :, 1] = g / 255.0
    rgb[:, :, 2] = b / 255.0
    if plot:
        plt.imshow(rgb)
        plt.show()
    else:
        return rgb


def encode_segmap(mask):
    """Encode segmentation label images as pascal classes
    Args:
        mask (np.ndarray): raw segmentation label image of dimension
          (M, N, 3), in which the Pascal classes are encoded as colours.
    Returns:
        (np.ndarray): class map with dimensions (M,N), where the value at
        a given location is the integer denoting the class index.
    """
    mask = mask.astype(int)
    label_mask = np.zeros((mask.shape[0], mask.shape[1]), dtype=np.int16)
    for ii, label in enumerate(get_pascal_labels()):
        label_mask[np.where(np.all(mask == label, axis=-1))[:2]] = ii
    label_mask = label_mask.astype(int)
    return label_mask


def get_cityscapes_labels():
    return np.array([
        [128, 64, 128],
        [244, 35, 232],
        [70, 70, 70],
        [102, 102, 156],
        [190, 153, 153],
        [153, 153, 153],
        [250, 170, 30],
        [220, 220, 0],
        [107, 142, 35],
        [152, 251, 152],
        [0, 130, 180],
        [220, 20, 60],
        [255, 0, 0],
        [0, 0, 142],
        [0, 0, 70],
        [0, 60, 100],
        [0, 80, 100],
        [0, 0, 230],
        [119, 11, 32]])


def get_pascal_labels():
    """Load the mapping that associates pascal classes with label colors
    Returns:
        np.ndarray with dimensions (21, 3)
    """
    return np.asarray([[0, 0, 0], [128, 0, 0], [0, 128, 0], [128, 128, 0],
                       [0, 0, 128], [128, 0, 128], [0, 128, 128], [128, 128, 128],
                       [64, 0, 0], [192, 0, 0], [64, 128, 0], [192, 128, 0],
                       [64, 0, 128], [192, 0, 128], [64, 128, 128], [192, 128, 128],
                       [0, 64, 0], [128, 64, 0], [0, 192, 0], [128, 192, 0],
                       [0, 64, 128]])    

def get_bdd100k_labels():
    """BDD100K Dataset for Segmentation
    https://github.com/ucbdrive/bdd-data
    """
    unlabeled = [0, 0, 0]
    dynamic = [111, 74, 0]
    ego_vehicle = [0, 0, 0]
    ground = [81, 0, 81]
    static = [0, 0, 0]
    parking = [250, 170, 160]
    rail_track = [230, 150, 140]
    road = [128, 64, 128]
    sidewalk = [244, 35, 232]
    bridge = [150, 100, 100]
    building = [70, 70, 70]
    fence = [190, 153, 153]
    garage = [180, 100, 180]
    guard_rail = [180, 165, 180]
    tunnel = [150, 120, 90]
    wall = [102, 102, 156]
    banner = [250, 170, 100]
    billboard = [220, 220, 250]
    lane_divider = [255, 165, 0]
    parking_sign = [220, 20, 60]
    pole = [153, 153, 153]
    polegroup = [153, 153, 153]
    street_light = [220, 220, 100]
    traffic_cone = [255, 70, 0]
    traffic_device = [220, 220, 220]
    traffic_light = [250, 170, 30]
    traffic_sign = [220, 220, 0]
    traffic_sign_frame = [250, 170, 250]
    terrain = [152, 251, 152]
    vegetation = [107, 152, 35]
    sky = [70, 130, 180]
    person = [220, 20, 60]
    rider = [255, 0, 0]
    bicycle = [119, 11, 32]
    bus = [0, 60, 100]
    car = [0, 0, 142]
    caravan = [0, 0, 90]
    motorcycle = [0, 0, 230]
    trailer = [0, 0, 110]
    train = [0, 80, 100]
    truck = [0, 0, 70]

    return np.array([
        unlabeled, dynamic, ego_vehicle, ground, static, parking, rail_track, road, sidewalk, bridge,
        building, fence, garage, guard_rail, tunnel, wall, banner, billboard, lane_divider, parking_sign,
        pole, polegroup, street_light, traffic_cone, traffic_device, traffic_light, traffic_sign,
        traffic_sign_frame, terrain, vegetation, sky, person, rider, bicycle, bus, car, caravan,
        motorcycle, trailer, train, truck])