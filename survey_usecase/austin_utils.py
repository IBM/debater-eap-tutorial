import math
from collections import defaultdict

from prettytable import PrettyTable

MAX_LINE_LENGTH = 90


def split_sentence_to_lines(sentence, max_len):
    if len(sentence) <= max_len:
        return ['- ' + sentence]

    lines = []
    line = None
    tokens = sentence.split(' ')
    for token in tokens:
        if line is None:
            line = '- ' + token
        else:
            if len(line + ' ' + token) <= max_len:
                line += ' ' + token
            else:
                lines.append(line)
                line = '  ' + token
    if line is not None:
        lines.append(line)
    return lines


def print_results_in_a_table(result, n_sentences_per_kp, title, one_line_sentences_only=False):
    table = PrettyTable()
    table.field_names = ['#', 'key point', 'size', 'example']
    total_sentences = 0
    matched_sentences = 0
    for i, keypoint_matching in enumerate(result['keypoint_matchings']):
        kp = keypoint_matching['keypoint']
        matches = keypoint_matching['matching']
        total_sentences += len(matches)
        if keypoint_matching['keypoint'] == 'none':  # skip cluster of all unmatched sentences
            continue
        matched_sentences += len(matches)
        if len(matches) <= 1:
            continue
        table.add_row([i, kp, len(matches), ''])
        sentences = [match['sentence_text'] for match in matches]
        if one_line_sentences_only:
            sentences = [sentence for sentence in sentences if len(sentence) <= MAX_LINE_LENGTH]
        sentences = sentences[1:(n_sentences_per_kp+1)]  # first sentence is the kp itself
        for sentence in sentences:
            lines = split_sentence_to_lines(sentence, MAX_LINE_LENGTH)
            for line in lines:
                table.add_row(['', '', '', line])
    print(title + ' coverage: %.2f' % ((float(matched_sentences) / float(total_sentences)) * 100.0))
    print(title + ' key points:')
    print(table)


def print_results(result, n_sentences_per_kp, title):
    '''
    Prints the key point analysis result to console.
    :param result: the result, returned by method get_result in KpAnalysisTaskFuture.
    '''
    def print_kp(kp, n_matches, n_matches_subtree, depth, keypoint_matching, n_sentences_per_kp):
        has_n_matches_subtree = n_matches_subtree is not None
        print('%s%d%s - %s' % (('\t' * depth), n_matches_subtree if has_n_matches_subtree else n_matches,
                                   (' - %d' % n_matches) if has_n_matches_subtree else '', kp))
        sentences = [match['sentence_text'] for match in keypoint_matching['matching']]
        sentences = sentences[1:(n_sentences_per_kp + 1)]  # first sentence is the kp itself
        lines = split_sentences_to_lines(sentences, depth)
        for line in lines:
            print('\t%s' % line)

    kp_to_n_matches_subtree = defaultdict(int)
    parents = list()
    parent_to_kids = defaultdict(list)
    for keypoint_matching in result['keypoint_matchings']:
        kp = keypoint_matching['keypoint']
        kp_to_n_matches_subtree[kp] += len(keypoint_matching['matching'])
        parent = keypoint_matching.get("parent", None)
        if parent is None or parent == 'root':
            parents.append(keypoint_matching)
        else:
            parent_to_kids[parent].append(keypoint_matching)
            kp_to_n_matches_subtree[parent] += len(keypoint_matching['matching'])

    parents.sort(key=lambda x: kp_to_n_matches_subtree[x['keypoint']], reverse=True)

    total_sentences = 0
    matched_sentences = 0
    for i, keypoint_matching in enumerate(result['keypoint_matchings']):
        matches = keypoint_matching['matching']
        total_sentences += len(matches)
        if keypoint_matching['keypoint'] != 'none':  # skip cluster of all unmatched sentences
            matched_sentences += len(matches)

    print(title + ' coverage: %.2f' % ((float(matched_sentences) / float(total_sentences)) * 100.0))
    print(title + ' key points:')
    for parent in parents:
        kp = parent['keypoint']
        if kp == 'none':
            continue
        print_kp(kp, len(parent['matching']), None if len(parent_to_kids[kp]) == 0 else kp_to_n_matches_subtree[kp], 0, parent, n_sentences_per_kp)
        for kid in parent_to_kids[kp]:
            kid_kp = kid['keypoint']
            print_kp(kid_kp, len(kid['matching']), None, 1, kid, n_sentences_per_kp)


def split_sentences_to_lines(sentences, n_tabs):
    lines = []
    for sentence in sentences:
        lines.extend(split_sentence_to_lines(sentence, MAX_LINE_LENGTH))
    return [('\t' * n_tabs) + line for line in lines]


def print_bottom_matches_for_kp(result, kp_to_print, bottom_k):
    for keypoint_matching in result['keypoint_matchings']:
        kp = keypoint_matching['keypoint']
        if kp != kp_to_print:
            continue

        matches = keypoint_matching['matching']
        bottom_k_matches = matches[-bottom_k:]

        print('\nBottom %d matches:' % bottom_k)
        sentences = [match['sentence_text'] for match in bottom_k_matches]
        print('\n'.join(split_sentences_to_lines(sentences, 1)))
        break


def compare_results(result_1, title_1, result_2, title_2):
    kps1 = set([kp['keypoint'] for kp in result_1['keypoint_matchings'] if kp['keypoint'] != 'none'])
    kps1_n_args = {kp['keypoint']: len(kp['matching']) for kp in result_1['keypoint_matchings']
                   if kp['keypoint'] != 'none'}
    kps2 = set([kp['keypoint'] for kp in result_2['keypoint_matchings'] if kp['keypoint'] != 'none'])
    kps2_n_args = {kp['keypoint']: len(kp['matching']) for kp in result_2['keypoint_matchings']
                   if kp['keypoint'] != 'none'}
    kps_in_both = kps1.intersection(kps2)
    kps_in_both = sorted(list(kps_in_both), key=lambda kp: kps1_n_args[kp], reverse=True)
    table = PrettyTable()
    table.field_names = ['key point', title_1, title_2, 'change']
    for kp in kps_in_both:
        table.add_row([kp, kps1_n_args[kp], kps2_n_args[kp], str(math.floor((kps2_n_args[kp] - kps1_n_args[kp]) / kps1_n_args[kp] * 100.0)) + '%'])
    kps1_not_in_2 = kps1 - kps2
    kps1_not_in_2 = sorted(list(kps1_not_in_2), key=lambda kp: kps1_n_args[kp], reverse=True)
    for kp in kps1_not_in_2:
        table.add_row([kp, kps1_n_args[kp], '---', '---'])
    kps2_not_in_1 = kps2 - kps1
    kps2_not_in_1 = sorted(list(kps2_not_in_1), key=lambda kp: kps2_n_args[kp], reverse=True)
    for kp in kps2_not_in_1:
        table.add_row([kp, '---', kps2_n_args[kp], '---'])
    print('%s - %s comparison:' % (title_1, title_2))
    print(table)


def init_logger():
    from logging import getLogger, getLevelName, Formatter, StreamHandler
    log = getLogger()
    log.setLevel(getLevelName('INFO'))
    log_formatter = Formatter("%(asctime)s [%(levelname)s] %(filename)s %(lineno)d: %(message)s")

    console_handler = StreamHandler()
    console_handler.setFormatter(log_formatter)
    log.handlers = []
    log.addHandler(console_handler)


def print_top_and_bottom_k_sentences(sentences, k):
    top_sentences = sentences[:k]
    top_sentences = [sentence['text'] for sentence in top_sentences]
    print('Top %d quality sentences: ' % k)
    print('\n'.join(split_sentences_to_lines(top_sentences, 1)))

    bottom_sentences = sentences[-k:]
    bottom_sentences = [sentence['text'] for sentence in bottom_sentences]
    print('\n\nBottom %d quality sentences: ' % k)
    print('\n'.join(split_sentences_to_lines(bottom_sentences, 1)))
