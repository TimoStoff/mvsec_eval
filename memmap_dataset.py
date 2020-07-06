import os.path
import numpy as np
import torch

class MemMapLoader():

    def __init__(self, 
                 root):

        self.filehandle = self.load_files(root)
        self.root = root

        self.timestamps = None

    def load_files(self, rootdir):
        assert os.path.isdir(rootdir), '%s is not a valid rootdirectory' % rootdir

        data = {}
        self.has_flow = False
        for subroot, _, fnames in sorted(os.walk(rootdir)):
            for fname in sorted(fnames):
                path = os.path.join(subroot, fname)

                if fname.endswith(".npy"):
                    if fname.endswith("index.npy"):  # index mapping image index to event idx
                        indices = np.load(path)  # N x 2
                        assert len(indices.shape) == 2 and indices.shape[1] == 2
                        indices = indices.astype("int64")  # ignore event indices which are 0 (before first image)
                        data["index"] = indices.T
                        data["length"] = len(data["index"])
                    elif fname.endswith("timestamps.npy"):
                        frame_stamps = np.load(path)
                        data["frame_stamps"] = frame_stamps
                    elif fname.endswith("images.npy"):
                        data["images"] = np.load(path, mmap_mode="r")
                    elif fname.endswith("optic_flow.npy"):
                        data["optic_flow"] = np.load(path, mmap_mode="r")
                        self.has_flow = True
                    elif fname.endswith("optic_flow_timestamps.npy"):
                        optic_flow_stamps = np.load(path)
                        data["optic_flow_stamps"] = optic_flow_stamps


                    handle = np.load(path, mmap_mode="r")
                    if fname.endswith("t.npy"):  # timestamps
                        data["t"] = handle
                        self.ts = data["t"][:].squeeze()
                    elif fname.endswith("xy.npy"): # coordinates
                        data["xy"] = handle
                    elif fname.endswith("p.npy"): # polarity
                        data["p"] = handle

            if len(data) > 0:
                data['path'] = subroot

                if "t" not in data:
                    print(f"Ignoring rootdirectory {subroot} since no events")
                    continue
                assert(len(data['p']) == len(data['xy']) and len(data['p']) == len(data['t']))
                data["num_events"] = len(data['p'])

        return data

    def get_by_frame_ts(self, t_start, t_end=None, num_events=None, eachside=True):

        index = np.searchsorted(self.ts, t_start)
        if t_end is None and num_events is None:
            num_events = 20000
        elif num_events is None:
            end_index = np.searchsorted(self.ts, t_end)
            num_events = max(2, end_index-index)
            if num_events == 2:
                print("WARNING: minimal events for this frame")

        if eachside:
            idx0 = max(0, index-(num_events//2))
        else:
            idx0 = index
        idx1 = min(len(self.ts), idx0 + num_events)

        xy = self.filehandle["xy"][idx0:idx1]
        events = {
                'xs': torch.from_numpy(xy[:,0].squeeze()).int(),
                'ys': torch.from_numpy(xy[:,1].squeeze()).float(),
                'ts': torch.from_numpy((self.filehandle["t"][idx0:idx1]-t_start).squeeze()),
                'ps': torch.from_numpy(self.filehandle["p"][idx0:idx1].squeeze()).float()
                }
        return events
