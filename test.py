#!/usr/bin/env python
import os
import glob
from tqdm import tqdm
import time
import numpy as np

from eval_utils import *
from event_utils import events_to_image
from memmap_dataset import MemMapLoader

def load_pred_flow(data_root):
    flow_list = sorted(glob.glob(os.path.join(data_root, "*npy")))
    flow = [np.load(x) for x in tqdm(flow_list)]
    if flow[0].shape[0] == 2:
        flow = [x.transpose(1,2,0) for x in flow]
    return flow

def evaluate(data, gt, seq_name, events):

    data_ts = np.loadtxt(os.path.join(data, "timestamps.txt"))
    data_ts_end = np.append(data_ts[1:-1], data_ts[-2:])
    image_timestamps = np.stack((data_ts, data_ts_end)).transpose()[1:-1, :]
    print("Loading predictions...")
    flow_predictions = load_pred_flow(data)[1:-2]

    if source is 'ours':
        #our flow needs to be converted to displacement
        flow_predictions = [x*(ts[1]-ts[0]) for ts, x in zip(image_timestamps[:], flow_predictions)]

    gt = np.load(gt)
    gt_timestamps = gt['timestamps']
    U_gt_all = gt['x_flow_dist']
    V_gt_all = gt['y_flow_dist']

    aee, paee, npts = [], [], []
    print("Processing {}...".format(seq_name))
    for idx, pred_flow in enumerate(tqdm(flow_predictions)):
        img_ts = image_timestamps[idx]

        U_gt, V_gt = estimate_corresponding_gt_flow(U_gt_all, V_gt_all,
                                                    gt_timestamps,
                                                    img_ts[0],
                                                    img_ts[1])
        
        #Must be in format y, x, 2
        gt_flow = np.stack((U_gt, V_gt), axis=2)

        image_size = pred_flow.shape
        full_size = gt_flow.shape
        xsize = full_size[1]
        ysize = full_size[0]
        xcrop = image_size[1]
        ycrop = image_size[0]
        xoff = (xsize - xcrop) // 2
        yoff = (ysize - ycrop) // 2
        
        if xoff > 0 or yoff > 0:
            gt_flow = gt_flow[yoff:-yoff, xoff:-xoff, :]       
            #print("gt={}, x_off={}, y_off={}".format(gt_flow.shape, xoff, yoff))
        
        event_img = None
        event_set = events.get_by_frame_ts(img_ts[0], img_ts[1])
        event_img = events_to_image(event_set['xs'].int(), event_set['ys'].int(), event_set['ps'], sensor_size=(image_size[0], image_size[1]))

        # Calculate flow error.
        AEE, percent_AEE, n_points = flow_error_dense(gt_flow, 
                                                      pred_flow, 
                                                      event_img=event_img,
                                                      is_car='outdoor' in seq_name)
        aee.append(AEE)
        paee.append(percent_AEE)
        npts.append(n_points)
    return np.array(aee), np.array(paee), np.array(npts)

def evaluate_all(gt_root, data_root, savedir, eventsdir, source):
    gt_files = sorted(glob.glob(os.path.join(gt_root, "*npz")))
    data_files = sorted(glob.glob(os.path.join(data_root, "*")))
    event_files = []
    for ef in sorted(glob.glob(os.path.join(eventsdir, "*"))):
        if os.path.isdir(ef):
            event_files.append(ef)
    seqnames = [os.path.basename(x.strip("_gt_flow_dist.npz")) for x in gt_files]

    for seq, data, gt, events in zip(seqnames, data_files, gt_files, event_files):
        if not seq in data or not seq in gt:
            raise Exception("{} and {} do not match".format(data, gt))

        event_loader = MemMapLoader(events)
        err = evaluate(data, gt, seq, event_loader, source)
        print("AEE={}".format(np.mean(err[0])))
        print("%AEE={}".format(np.mean(err[1])))
        print("npts={}".format(np.mean(err[2])))
        fname = os.path.join(savedir, seq) 
        np.savez(fname, aee=err[0], paee=err[1], npts=err[2])

if __name__ == '__main__':
    import argparse
    args = argparse.ArgumentParser(description='PyTorch Template')
    args.add_argument('-d', '--data', default=None, type=str,
                      help='data root file path (default: None)')
    args.add_argument('-g', '--gt', default=None, type=str,
                      help='gt root path')
    args.add_argument('-s', '--savedir', default="/tmp", type=str,
                      help='savedir')
    args.add_argument('-e', '--eventsdir', default=None, type=str,
                      help='events dir')
    args.add_argument('-c', '--source', default="ours", type=str,
                      help='Is it "ours" or "evflownet"?')

    args = args.parse_args()
    evaluate_all(args.gt, args.data, args.savedir, args.eventsdir, args.source)
