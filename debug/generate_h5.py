import h5py
import numpy as np
import os
from progressbar import *

def generate_h5_file(n, dir):

    BATCH_SIZE=1000

    labels = []
    energies = []
    positions = []
    angles = []

    batch_ends = [i for i in range(0,n,BATCH_SIZE)]
    batch_ends.append(n)

    for i in range(n):
        labels.append(np.random.rand(1))
        angles.append(np.random.rand(2))
        energies.append(np.squeeze(np.random.rand(1)))
        positions.append(np.random.rand(1,3))

    f = h5py.File(os.path.join(dir, 'dummy_dataset.h5'), 'w')

    f.create_dataset('event_data',(n,40,40,38),dtype='float64')
    f.create_dataset('labels',data=labels)
    f.create_dataset('energies',data=energies)
    f.create_dataset('positions',data=positions)
    f.create_dataset('angles',data=angles)

    pbar = ProgressBar(widgets=['Generating Event Data: ', Percentage(), ' ', Bar(marker='0',left='[',right=']'),
            ' ', ETA()], maxval=n)
    pbar.start()
    for idx, batch_start in enumerate(batch_ends[:-1]):
        event_data=[]
        for i in range(BATCH_SIZE):
            pbar.update(idx*BATCH_SIZE+i)
            event_data.append(np.random.rand(40,40,38))
        f['event_data'][batch_start:batch_ends[idx+1]]=event_data
        del event_data
    pbar.finish()

    f.close()

def generate_indices(n_train,n_val,n, dir):
    a = [i for i in range(n)]
    np.random.shuffle(a)
    train_idxs=a[:n_train]
    val_idxs = np.delete(a, train_idxs)[:n_val]
    np.savez(os.path.join(dir,'dummy_trainval_idxs.npz'), train_idxs=train_idxs, val_idxs=val_idxs)