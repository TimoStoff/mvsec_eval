import numpy as np

def events_to_image(xs, ys, ps, sensor_size=(180, 240), padding=False):
    """
    Place events into an image using numpy
    """
    img_size = sensor_size

    mask = np.where(xs>=sensor_size[1]-1, 0, 1)*np.where(ys>=sensor_size[0]-1, 0, 1)*np.where(xs<0, 0, 1)*np.where(ys<0, 0, 1)
    coords = np.stack((ys*mask, xs*mask))

    try:
        abs_coords = np.ravel_multi_index(coords, sensor_size)
    except ValueError:
        raise ValueError("Issue with input arrays! coords={}, min_x={}, min_y={}, max_x={}, max_y={}, coords.shape={}, sum(coords)={}, sensor_size={}".format(coords, min(xs), min(ys), max(xs), max(ys), coords.shape, np.sum(coords), sensor_size))
        
    img = np.bincount(abs_coords, weights=ps, minlength=sensor_size[0]*sensor_size[1])
    img = img.reshape(sensor_size)
    return img
