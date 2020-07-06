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
