# (C) Copyright IBM Corporation 2020-2022
# LICENSE: Apache License 2.0 (Apache-2.0)
# http://www.apache.org/licenses/LICENSE-2.0

import logging

from debater_python_api.api.clients.keypoints_client import KpAnalysisTaskFuture, \
    KpaIllegalInputException, KpAnalysisUtils, KpAnalysisClient
import pandas as pd

def write_sentences_to_csv(sentences, out_file):
    if len(sentences) == 0:
        logging.info('there are no sentences, not saving file')
        return

    cols = list(sentences[0].keys())
    rows = [[s[col] for col in cols] for s in sentences]
    df = pd.DataFrame(rows, columns=cols)
    df.to_csv(out_file, index=False)


def run_on_sentences_two_stances(domain, stance_to_future):
    keypoints_client.wait_till_all_comments_are_processed(domain=domain)
    run_params['stances_to_run'] = ['pos']
    run_params['stances_threshold'] = 0.5
    stance_to_future['pro'] = keypoints_client.start_kp_analysis_job(domain=domain,
                                                                     run_params=run_params)

    run_params['stances_to_run'] = ['neg', 'sug']
    run_params['stances_threshold'] = 0.5
    stance_to_future['con'] = keypoints_client.start_kp_analysis_job(domain=domain,
                                                                     run_params=run_params)

def get_merge_and_save_results(stance_to_future, file):
    stance_to_result = {}
    for stance in stance_to_future:
        future = stance_to_future[stance]
        try:
            kpa_result = future.get_result(high_verbosity=True, polling_timout_secs=60)
            stance_to_result[stance] = kpa_result
        except Exception as e:
            if 'maybe the input size is too small' not in e.args[0]:
                raise e
            else:
                print(f'job: {future.get_job_id()} don\'t have enough data for extracting key points')
                kpa_result = {'keypoint_matchings': []}
                stance_to_result[stance] = kpa_result

    if 'pro' in stance_to_result and 'con' in stance_to_result:
        pro_result = KpAnalysisUtils.set_stance_to_result(stance_to_result['pro'], 'pro')
        KpAnalysisUtils.write_result_to_csv(pro_result, file.replace('.csv', '_pro_kpa_results.csv'))
        con_result = KpAnalysisUtils.set_stance_to_result(stance_to_result['con'], 'con')
        KpAnalysisUtils.write_result_to_csv(con_result, file.replace('.csv', '_con_kpa_results.csv'))
        merged_result = KpAnalysisUtils.merge_two_results(pro_result, con_result)
        KpAnalysisUtils.write_result_to_csv(merged_result, file.replace('.csv', '_merged_kpa_results.csv'))
    else:
        print('a stance is missing: %s' % str(list(stance_to_result.keys())))


def get_comments_ids_and_texts(file, comment_ids_column, comment_text_column):
    df = pd.read_csv(file)
    id_text = sorted(list(zip(df[comment_ids_column], df[comment_text_column])))
    id_text = [t for t in id_text if len(t[1]) < 1000]  # comments must have at most 1000 chars
    comments_ids = [str(t[0]) for t in id_text]
    comments_texts = [str(t[1]) for t in id_text]
    return comments_ids, comments_texts


if __name__ == '__main__':
    KpAnalysisUtils.init_logger()

    # ======================= update params =======================
    api_key = '<api_key>'
    file = '<input_csv>'
    comment_ids_column = '<ids_column_in_csv>'
    comment_text_column = '<text_column_in_csv>'
    domain = '<domain_name>'
    host = '<kpa_backend_host_url>'
    # ======================= update params =======================

    keypoints_client = KpAnalysisClient(apikey=api_key, host=host)

    # what to run
    delete_all_domains = False  # deletes-all! cannot be undone
    restart = False
    delete_domain = restart
    create_domain = restart
    upload_comments = restart
    run_kpa_both_stances = False
    download_sentences = False
    get_report = False
    connect_to_running_job = False
    cancel_all_running_jobs_in_the_domain = False

    # how to run
    domain_params = {'do_stance_analysis': True}
    run_params = {'sentence_to_multiple_kps': True}

    if delete_all_domains:
        answer = input("Are you sure you want to delete ALL domains (cannot be undone)? yes/no:")
        if answer == 'yes':
            keypoints_client.delete_all_domains_cannot_be_undone()

    if get_report:
        KpAnalysisUtils.print_report(keypoints_client.get_full_report())

    if delete_domain:
        answer = input(f'Are you sure you want to delete domain: {domain} (cannot be undone)? yes/no:')
        if answer == 'yes':
            KpAnalysisUtils.delete_domain_ignore_doesnt_exist(keypoints_client, domain)

    if create_domain:
        KpAnalysisUtils.create_domain_ignore_exists(keypoints_client, domain, domain_params)

    if upload_comments:
        comments_ids, comments_texts = get_comments_ids_and_texts(file, comment_ids_column, comment_text_column)

        keypoints_client.upload_comments(domain=domain,
                                         comments_ids=comments_ids,
                                         comments_texts=comments_texts)

        keypoints_client.wait_till_all_comments_are_processed(domain=domain)

    if download_sentences:
        sentences = keypoints_client.get_sentences_for_domain(domain)
        write_sentences_to_csv(sentences, file.replace('.csv', '_sentences.csv'))

    stance_to_future = {}
    if run_kpa_both_stances:
        run_on_sentences_two_stances(domain, stance_to_future)

    if connect_to_running_job:
        stance_to_future['pro'] = KpAnalysisTaskFuture(keypoints_client, '<pro_job_id>')
        stance_to_future['con'] = KpAnalysisTaskFuture(keypoints_client, '<con_job_id>')

    if len(stance_to_future.keys()) > 0:
        get_merge_and_save_results(stance_to_future, file)

    if cancel_all_running_jobs_in_the_domain:
        keypoints_client.cancel_all_extraction_jobs_for_domain(domain=domain)