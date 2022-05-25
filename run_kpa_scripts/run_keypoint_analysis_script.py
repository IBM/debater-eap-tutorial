# (c) Copyright IBM Corporation 2020-2022

import logging

from debater_python_api.api.clients.keypoints_client import KpAnalysisTaskFuture, \
    KpaIllegalInputException, KpAnalysisUtils, KpAnalysisClient
from debater_python_api.api.debater_api import DebaterApi
import pandas as pd


def write_sentences_to_csv(sentences, out_file):
    if len(sentences) == 0:
        logging.info('there are no sentences, not saving file')
        return

    cols = list(sentences[0].keys())
    rows = [[s[col] for col in cols] for s in sentences]
    df = pd.DataFrame(rows, columns=cols)
    df.to_csv(out_file, index=False)


def get_comments_ids_and_texts(file, ids_column, comment_text_column):
    df = pd.read_csv(file)
    id_text = sorted(list(zip(df[ids_column], df[comment_text_column])))
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

    debater_api = DebaterApi(apikey=api_key)
    keypoints_client = KpAnalysisClient(apikey=api_key, host=host)
    keypoints_client.delete_all_domains_cannot_be_undone()

    # what to run
    delete_all_domains = False  # deletes-all! cannot be undone
    restart = False
    delete_domain = restart
    create_domain = restart
    upload_comments = restart
    run_kpa = False
    download_sentences = False
    get_report = True
    connect_to_running_job = False
    cancel_all_running_jobs_in_the_domain = False

    # how to run
    domain_params = {}
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
            keypoints_client.delete_domain_cannot_be_undone(domain)

    if create_domain:
        try:
            keypoints_client.create_domain(domain, {})
            print('domain was created')
        except KpaIllegalInputException as e:
            print('domain already exist')

    if upload_comments:
        comments_ids, comments_texts = get_comments_ids_and_texts(file, comment_ids_column, comment_text_column)

        keypoints_client.upload_comments(domain=domain,
                                         comments_ids=comments_ids,
                                         comments_texts=comments_texts)

        keypoints_client.wait_till_all_comments_are_processed(domain=domain)

    if download_sentences:
        sentences = keypoints_client.get_sentences_for_domain(domain)
        write_sentences_to_csv(sentences, file.replace('.csv', '_sentences.csv'))

    future = None
    if run_kpa:
        keypoints_client.wait_till_all_comments_are_processed(domain=domain)
        future = keypoints_client.start_kp_analysis_job(domain=domain, run_params=run_params)

    if connect_to_running_job:
        future = KpAnalysisTaskFuture(keypoints_client, '<job_id>')

    if future is not None:
        kpa_result = future.get_result(high_verbosity=True, polling_timout_secs=30)
        KpAnalysisUtils.write_result_to_csv(kpa_result, file.replace('.csv', '_kpa_results.csv'))

    if cancel_all_running_jobs_in_the_domain:
        keypoints_client.cancel_all_extraction_jobs_for_domain(domain=domain)
