import logging.handlers
import argparse
import os
from sklearn.metrics import f1_score, accuracy_score
from sklearn.metrics import classification_report
import pandas as pd
import sys
sys.path.append('.')
from subtaskA.format_checker.format_checker import check_format

"""
Scoring of SEMEVAL-Task-8--subtask-A-and-B  with the metrics f1-macro, f1-micro and accuracy. 
"""

def evaluate(pred_fpath, gold_fpath):
  """
    Evaluates the predicted classes w.r.t. a gold file.
    Metrics are: f1-macro, f1-micro and accuracy

    :param pred_fpath: a json file with predictions, 
    :param gold_fpath: the original annotated gold file.

    The submission of the result file should be in jsonl format. 
    It should be a lines of objects:
    {
      id     -> identifier of the test sample,
      labels -> labels (0 or 1 for subtask A and from 0 to 5 for subtask B),
    }
  """
  
  pred_labels = pd.read_json(pred_fpath, lines=True)[['id', 'label']]
  gold_labels = pd.read_json(gold_fpath, lines=True)[['id', 'label']]

  merged_df = pred_labels.merge(gold_labels, on='id', suffixes=('_pred', '_gold'))

  macro_f1 = f1_score(merged_df['label_gold'], merged_df['label_pred'], average="macro", zero_division=0)
  micro_f1 = f1_score(merged_df['label_gold'], merged_df['label_pred'], average="micro", zero_division=0)
  accuracy = accuracy_score(merged_df['label_gold'], merged_df['label_pred'])
  
  # Evaluate the classifier
  print(classification_report(merged_df['label_gold'], merged_df['label_pred']))
  return macro_f1, micro_f1, accuracy


def validate_files(pred_files):
  if not check_format(pred_files):
    logging.error('Bad format for pred file {}. Cannot score.'.format(pred_files))
    return False
  return True


def readArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument( "--gold_file_name", '-g', type=str, required=True, help="Paths to the file with gold annotations.")
    parser.add_argument("--pred_file_name", '-p', type=str, required=True, help="Path to the file with predictions")
    args = parser.parse_args()
    return args
  
if __name__ == '__main__':

  args = readArgs()  
  pred_file_name = args.pred_file_name
  gold_file_name = args.gold_file_name
  absolute_path = os.path.abspath('subtaskA/data')

  gold_file_path = absolute_path + '/' + gold_file_name
  pred_file_path = absolute_path + '/predictions/' + pred_file_name
  
  if validate_files(pred_file_path):
    logging.info('Prediction file format is correct')
    macro_f1, micro_f1, accuracy = evaluate(pred_file_path, gold_file_path)
    logging.info("macro-F1={:.5f}\tmicro-F1={:.5f}\taccuracy={:.5f}".format(macro_f1, micro_f1, accuracy))


