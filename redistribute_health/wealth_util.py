# (C) Copyright IBM Corp. 2020.

import csv
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report


def sign(n):
    if n < 0:
        return -1
    return 1


def calculate_statistics(labels_file, pro_con_scores):
    with open(labels_file, encoding='utf8') as csv_file:
        reader = csv.DictReader(csv_file)
        examples = list(reader)

    for i, example in enumerate(examples):
        example['score'] = pro_con_scores[i]

    examples = sorted(examples, key=lambda k: abs(k['score']))
    for i, example in enumerate(examples):
        example['coverage'] = (len(examples) - i) / len(examples)
        predicted_classes = [sign(example['score']) for example in examples[i:]]
        labels = [int(example['label']) for example in examples[i:]]
        labels_set = list(set(predicted_classes))
        if len(labels_set) > 1:
            example['classification_report'] = classification_report(labels, predicted_classes, digits=4, zero_division=0,
                                                           labels=labels_set, output_dict=True)
        else:
            example['classification_report'] = classification_report(labels, predicted_classes, digits=4, zero_division=0,
                                                           output_dict=True)
        # generate unclassified predictions
        if i > 0:
            labels = [int(example['label']) for example in examples[:i]]
            predicted_classes = [0 for example in examples[:i]]
            classification_report_ = classification_report(labels, predicted_classes, digits=4, zero_division=0,
                                                           output_dict=True)
            example['classification_report']['0'] = {}
            example['classification_report']['0']['precision'] = classification_report_['0']['precision']

    return examples


def add_line(examples, label, stance):
    stance_2_class_label = {'pro': '1', 'con': '-1', 'neutral': '0'}
    class_label = stance_2_class_label[stance]
    plt.plot([example['coverage'] for example in examples],
             [example['classification_report'][class_label]['precision']
              if class_label in example['classification_report'] else 1.0
              for example in examples]
             , label='{}_{}'.format(label, stance))


def plot_stance(stance, examples_list, labels):
    for examples, label in zip(examples_list, labels):
        add_line(examples, label, stance)
    plt.title('precision / coverage - SBC data {}'.format(stance))
    plt.xlabel('coverage')
    plt.ylabel('precision')
    plt.legend(loc='best')


def plot_graph(examples_list, labels):
    plt.figure(figsize=(12, 8))
    plt.subplot(1, 3, 1)
    plot_stance('pro',  examples_list, labels)
    plt.subplot(1, 3, 2)
    plot_stance('con',  examples_list, labels)
    plt.subplot(1, 3, 3)
    plot_stance('neutral',  examples_list, labels)
    plt.show()
