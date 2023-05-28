from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor,CellExecutionError
from datetime import datetime

dt = datetime.now().strftime('%d%m%H%M')
parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-n", "--notebook", default="None", help="Name of notebook to run")
parser.add_argument("-o", "--out_notebook", default=None, help="Name notebook for saving results")
args = vars(parser.parse_args())


#notebook_filename = "dqe_python_pandas_task1_aliaksandr_shkuratau.ipynb"
notebook_filename = args["notebook"]
notebook_filename_out = '{}_executed_{}.ipynb'.format(notebook_filename.split('.')[0],dt,) if args["out_notebook"] is None else args["out_notebook"]


with open(notebook_filename) as ff:
    nb_in = nbformat.read(ff, nbformat.NO_CONVERT)

ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

try:
    nb_out = ep.preprocess(nb_in)
except CellExecutionError:
    out = None
    msg = 'Error executing the notebook "%s".\n\n' % notebook_filename
    msg += 'See notebook "%s" for the traceback.' % notebook_filename_out
    print(msg)
    raise
finally:
    with open('executed_{}'.format(notebook_filename_out), 'w', encoding='UTF-8') as f:
        nbformat.write(nb_in, f)
        print('Executed notebook saved as {}'.format(notebook_filename_out))
