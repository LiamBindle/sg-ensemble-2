import os.path
import sys
import pathlib

import yaml

if __name__ == '__main__':
    dirname = sys.argv[1]

    with open(os.path.join(dirname, 'simulations.yaml'), 'r') as f:
        sims = yaml.safe_load(f)

    queue = sys.argv[2]
    cores_per_node = 36 if queue == 'rvmartin' else 30

    cutoff = 122

    for sim in sims:
        short_name = sim.pop('short_name')
        rundir = os.path.join(dirname, short_name)

        if sim['cs_res'] > cutoff:
            continue

        pathlib.Path(rundir).mkdir(exist_ok=True)

        # Calculate nnodes
        res_factor = sim["cs_res"] / 48
        complexity = 2**(res_factor - 1)
        nnodes = int(4*complexity + 0.5)
        nnodes = max(nnodes, 1)

        # Put together conf
        conf = {
            'grid': sim,
            'job': {
                'cores_per_node': cores_per_node,
                'num_cores': cores_per_node*nnodes,
                'num_nodes': nnodes,
                'queue': queue
            },
            'paths': {'run_directory': os.path.abspath(rundir)},
            'templates': ['/scratch1/liam.bindle/sg-ensemble-2/rundir-template']
        }

        with open(os.path.join(rundir, 'conf.yml'), 'w') as f:
            yaml.safe_dump(conf, f)
