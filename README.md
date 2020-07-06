# mvsec_eval
Code for getting MVSEC numbers for optic flow from events. 
Most of this code is from [EV-FlowNet](https://github.com/daniilidis-group/EV-FlowNet), with modifications to aid compatiability with [Stoffregen et al., ECCV 2020](https://github.com/TimoStoff/event_cnn_minimal).

## Usage
To get numbers for optic flow estimated from the MVSEC dataset, you must provide the ground truth optic flow from the [MVSEC project page](https://daniilidis-group.github.io/mvsec/).
Then you may run:
```
python test.py --data /root/dir/of/flow --gt /root/dir/of/gt --savedir /where/to/save/numbers --eventsdir /path/to/events/hdf5
```
`--data` must point to a directory containing directories containing the `.npy` files with the optic flow as well as a file 'timestamps.txt` with the timestamps for each flow frame.
Running inference from [Stoffregen et al., ECCV 2020](https://github.com/TimoStoff/event_cnn_minimal) should get you the data in the correct format.

`--gt`is the root directory of the ground truth optic flow from the MVSEC project page.

`--savedir` is the location to which the resulting numbers will be saved

`--eventsdir` is a directory containing the events from MVSEC in HDF5 file format (see [Stoffregen et al., ECCV 2020](https://github.com/TimoStoff/event_cnn_minimal) for tools to convert to this format).
This is necessary, as the MVSEC metrics always mask the flow by the event image and the events are used to create these masks.

`--source` this flag can be left out if running inference on [Stoffregen et al., ECCV 2020](https://github.com/TimoStoff/event_cnn_minimal) only.
To get numbers for the original EVFlowNet, you must set this flag to `evflownet` since the flow is saved in displacement by default in their code and requires conversion.

You should get an output like this:
```
Loading predictions...
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1871/1871 [00:02<00:00, 862.31it/s]
Processing indoor_flying1...
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1868/1868 [00:05<00:00, 328.71it/s]
AEE=0.5582177941755221
%AEE=0.9984800419413141
npts=3684.917023554604
Loading predictions...
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1881/1881 [00:01<00:00, 949.52it/s]
Processing indoor_flying2...
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1878/1878 [00:06<00:00, 299.12it/s]
AEE=0.6633795138420633
%AEE=0.9987678292418837
npts=6559.0346112886045
Loading predictions...
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1881/1881 [00:02<00:00, 907.90it/s]
Processing indoor_flying3...
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1878/1878 [00:05<00:00, 319.53it/s]
AEE=0.5881189025692585
%AEE=0.9981815867668927
npts=4891.375931842385
Loading predictions...
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 284/284 [00:00<00:00, 933.49it/s]
Processing indoor_flying4...
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 281/281 [00:01<00:00, 274.57it/s]
AEE=1.518712010403692
%AEE=0.8978006138345855
npts=7376.886120996442
Loading predictions...
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7283/7283 [00:08<00:00, 851.88it/s]
Processing outdoor_day1...
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7280/7280 [00:17<00:00, 426.90it/s]
AEE=0.6810412810035561
%AEE=0.9919788577379473
npts=1651.6111263736263
Loading predictions...
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 6996/6996 [00:08<00:00, 804.18it/s]
Processing outdoor_day2...
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 6993/6993 [00:19<00:00, 360.92it/s]
AEE=0.8241772373938709
%AEE=0.9628368668207049
npts=3651.1783211783213
```
(Don't forget to respect the sequence cuts described in the paper).
