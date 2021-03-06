import subprocess
import os
from wacacore.train.hyper import rand_product


def stringify(k, v):
    """Turn a key value into command line argument"""
    if v is True:
        return "--%s" % k
    elif v is False:
        return ""
    else:
        return "--%s=%s" % (k, v)


def make_batch_string(options):
    """Turn options into a string that can be passed on command line"""
    batch_string = [stringify(k, v) for k, v in options.items()]
    return batch_string


def run_sbatch(options, file_path, bash_run_path=None):
    """Execute sbatch with options"""
    if bash_run_path is None:
      dir_path = os.path.dirname(os.path.realpath(__file__))
      bash_run_path = os.path.join(dir_path, 'run.sh')
    run_str = ['sbatch', bash_run_path, file_path] + make_batch_string(options)
    print(run_str)
    subprocess.call(run_str)


def run_local_batch(options, file_path, bash_run_path=None):
    """Execute sbatch with options"""
    run_str = ["python", file_path] + make_batch_string(options)
    print("Subprocess call:", run_str)
    subprocess.Popen(run_str)


def rand_sbatch_hyper_search(options, file_path, var_options_keys, nsamples,
                             prefix, nrepeats):
    """Randomized hyper parameter search locally without slurm"""
    rand_product(lambda options: run_sbatch(options, file_path),
                 options, var_options_keys, nsamples, prefix, nrepeats)


def rand_local_hyper_search(options, file_path, var_options_keys, nsamples,
                            prefix, nrepeats):
    """Randomized hyper parameter search using slurm sbatch"""
    rand_product(lambda options: run_local_batch(options, file_path),
                 options, var_options_keys, nsamples, prefix, nrepeats)
