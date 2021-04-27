import math

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


def print_results(result, n_sentences_per_kp, title, one_line_sentences_only=False):
    total_sentences = 0
    matched_sentences = 0
    lines = []
    for i, keypoint_matching in enumerate(result['keypoint_matchings']):
        kp = keypoint_matching['keypoint']
        matches = keypoint_matching['matching']
        total_sentences += len(matches)
        if keypoint_matching['keypoint'] == 'none':  # skip cluster of all unmatched sentences
            continue

        matched_sentences += len(matches)
        if len(matches) <= 1:
            continue

        lines.append('{} - {}'.format(len(matches), kp))

        sentences = [match['sentence_text'] for match in matches]
        if one_line_sentences_only:
            sentences = [sentence for sentence in sentences if len(sentence) <= MAX_LINE_LENGTH]
        sentences = sentences[1:(n_sentences_per_kp + 1)]  # first sentence is the kp itself
        lines.extend(split_sentences_to_lines(sentences, 1))
    print(title + ' coverage: %.2f' % ((float(matched_sentences) / float(total_sentences)) * 100.0))
    print(title + ' key points:')
    print('\n'.join(lines))

def split_sentences_to_lines(sentences, n_tabs):
    lines = []
    for sentence in sentences:
        lines.extend(split_sentence_to_lines(sentence, MAX_LINE_LENGTH))
    return [('\t' * n_tabs) + line for line in lines]

def print_top_and_bottom_matches_for_kp(result, kp_to_print, top_k, bottom_k):
    for i, keypoint_matching in enumerate(result['keypoint_matchings']):
        kp = keypoint_matching['keypoint']
        if kp != kp_to_print:
            continue

        matches = keypoint_matching['matching']
        top_k_matches = matches[:top_k]
        bottom_k_matches = matches[-bottom_k:]

        print('Top %d matches:' % top_k)
        sentences = [match['sentence_text'] for match in top_k_matches]
        print('\n'.join(split_sentences_to_lines(sentences, 1)))

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