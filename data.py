import h5py
from util.event_util import binary_search_h5_dset

class HDF5EventLoader():

    def get_by_frame_ts(self, t_start, t_end=None, num_events=20000):

        idx0 = np.searchsorted(self.ts, t_start)

        if t_end is not None:
            idx1 = self.find_ts_index(t_end)
            num_events = max(2, idx1-idx0)
            if num_events == 2:
                print("WARNING: minimal events for this frame")
        else:
            idx1 = min(len(self.ts), idx0+num_events)

        return self.get_events(idx0, idx1)

    def get_frame(self, index):
        return self.h5_file['images']['image{:09d}'.format(index)][:]

    def get_flow(self, index):
        return self.h5_file['flow']['flow{:09d}'.format(index)][:]

    def get_events(self, idx0, idx1):
        xs = self.h5_file['events/xs'][idx0:idx1]
        ys = self.h5_file['events/ys'][idx0:idx1]
        ts = self.h5_file['events/ts'][idx0:idx1]
        ps = self.h5_file['events/ps'][idx0:idx1] * 2.0 - 1.0
        return xs, ys, ts, ps

    def load_data(self, data_path):
        try:
            self.h5_file = h5py.File(data_path, 'r')
        except OSError as err:
            print("Couldn't open {}: {}".format(data_path, err))

        if self.sensor_resolution is None:
            self.sensor_resolution = self.h5_file.attrs['sensor_resolution'][0:2]
        else:
            self.sensor_resolution = self.sensor_resolution[0:2]
        print("sensor resolution = {}".format(self.sensor_resolution))
        self.has_flow = 'flow' in self.h5_file.keys() and len(self.h5_file['flow']) > 0
        self.t0 = self.h5_file['events/ts'][0]
        self.tk = self.h5_file['events/ts'][-1]
        self.num_events = self.h5_file.attrs["num_events"]
        self.num_frames = self.h5_file.attrs["num_imgs"]

        self.frame_ts = []
        for img_name in self.h5_file['images']:
            self.frame_ts.append(self.h5_file['images/{}'.format(img_name)].attrs['timestamp'])

        data_source = self.h5_file.attrs.get('source', 'unknown')
        try:
            self.data_source_idx = data_sources.index(data_source)
        except ValueError:
            self.data_source_idx = -1

    def find_ts_index(self, timestamp):
        idx = binary_search_h5_dset(self.h5_file['events/ts'], timestamp)
        return idx

    @staticmethod
    def binary_search_h5_dset(dset, x, l=None, r=None, side='left'):
        l = 0 if l is None else l
        r = len(dset)-1 if r is None else r
        while l <= r:
            mid = l + (r - l)//2;
            midval = dset[mid]
            if midval == x:
                return mid
            elif midval < x:
                l = mid + 1
            else:
                r = mid - 1
        if side == 'left':
            return l
        return r

