#
# generate a vocab file for re-use
# -------------------------------
#

# usage:
# python matchmaker/preprocessing/generate_vocab.py --out-dir vocabDir --dataset-files list of all dataset files: format <id>\t<sequence text>'

import argparse
import os
import sys
sys.path.append(os.getcwd())
from collections import defaultdict

from matchmaker.dataloaders.ir_tuple_loader import *
from allennlp.data.vocabulary import Vocabulary
from allennlp.modules.token_embedders import Embedding
from allennlp.data.fields.text_field import Token
from allennlp.common import Params, Tqdm
Tqdm.default_mininterval = 1

#
# config
#
parser = argparse.ArgumentParser()

parser.add_argument('--out-dir', action='store', dest='out_dir',
                    help='vocab save directory', required=True)

#parser.add_argument('--out-dir2', action='store', dest='out_dir2',
#                    help='vocab save directory 2', required=True)

#parser.add_argument('--out-dir3', action='store', dest='out_dir3',
#                    help='vocab save directory 3', required=True)

parser.add_argument('--lowercase', action='store', dest='lowercase',type=bool,default=True,
                    help='bool ', required=False)


parser.add_argument('--dataset-files', nargs='+', action='store', dest='dataset_files',
                    help='list of all dataset files: format <id>\t<sequence text>', required=True)

args = parser.parse_args()


#
# load data & create vocab
# -------------------------------
#  

loader = IrTupleDatasetReader(lazy=True,lowercase=args.lowercase)


def getInstances():
    for file in args.dataset_files:
        instances = loader.read(file)
        for i in instances:
            yield Instance({"text":i["target_tokens"]})

namespace_token_counts: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
for instance in Tqdm.tqdm(getInstances()):
    instance.count_vocab_items(namespace_token_counts)

#with open(args.out_dir,"w",encoding="utf8") as out:
#    for n in namespace_token_counts:
#        #out.write("--"+n+"\n")
#        for w,i in namespace_token_counts[n].items():
#            out.write(w+"\t"+str(i)+"\n")

vocab = Vocabulary(namespace_token_counts, min_count={"tokens":100})
vocab.save_to_files(args.out_dir)

#vocab = Vocabulary(namespace_token_counts, min_count={"tokens":50})
#vocab.save_to_files(args.out_dir2)

#vocab = Vocabulary(namespace_token_counts, min_count={"tokens":10})
#vocab.save_to_files(args.out_dir3)

