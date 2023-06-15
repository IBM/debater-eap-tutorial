# (C) Copyright IBM Corporation 2020-2022
# LICENSE: Apache License 2.0 (Apache-2.0)
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import os
from debater_python_api.api.clients.keypoints_client import KpsClient
import pandas as pd


def get_comments_ids_and_texts(file, comment_ids_column, comment_text_column):
    df = pd.read_csv(file)
    id_text = sorted(list(zip(df[comment_ids_column], df[comment_text_column])))
    id_text = [t for t in id_text if len(t[1]) < 3000]  # comments must have at most 1000 chars
    comments_ids = [str(t[0]) for t in id_text]
    comments_texts = [str(t[1]) for t in id_text]
    return comments_ids, comments_texts


if __name__ == '__main__':
    KpsClient.init_logger()

    # ======================= update params =======================
    api_key = '<api_key>'
    host = 'https://keypoint-matching-backend.debater.res.ibm.com'
    input_file = '<input_csv>'
    comment_ids_column = '<ids_column_in_csv>'
    comment_text_column = '<text_column_in_csv>'
    output_dir = '<output_dir>'  # existing output directory
    job_name = '<job name>'  # job mane to appear in output files names
    domain = '<domain_name>'
    # ======================= update params =======================

    # what to run
    restart = False  # set to True for recreating the domain and uploading comments
    delete_domain = restart
    create_domain = restart
    upload_comments = restart  # set to True for uploading more comments to an existing domain
    download_sentences = True
    get_report = False
    run_kps_job = True
    both_stances = True

    # how to run
    domain_params = {}
    run_params = {}
    if run_kps_job and both_stances:
            run_params_pro = run_params  # change for customized pro run
            run_params_con = run_params  # change for customized con run

    #########################

    keypoints_client = KpsClient(apikey=api_key, host=host)

    if get_report:
        KpsClient.print_report(keypoints_client.get_full_report())

    if delete_domain:
        answer = input(f'Are you sure you want to delete domain: {domain} (cannot be undone)? yes/no:')
        if answer == 'yes':
            keypoints_client.delete_domain_cannot_be_undone(domain)

    if create_domain:
        keypoints_client.create_domain(domain, domain_params)

    if upload_comments:
        comments_ids, comments_texts = get_comments_ids_and_texts(input_file, comment_ids_column, comment_text_column)
        keypoints_client.upload_comments(domain=domain, comments_ids=comments_ids, comments_texts=comments_texts)

    if download_sentences:
        sentences_df = keypoints_client.get_sentences_for_domain(domain)
        sentences_df.to_csv(os.path.join(output_dir, f'{job_name}_sentences.csv'))

    kps_result = None
    if run_kps_job:
        if both_stances:
            kps_result = keypoints_client.run_kps_job_both_stances(
                        domain, run_params_con=run_params_con, run_params_pro=run_params_pro)
        else:
            kps_result = keypoints_client.run_kps_job(domain=domain, run_params=run_params)

    if kps_result:
        kps_result.save(os.path.join(output_dir, f'{job_name}.json'))
        kps_result.export_to_all_outputs(output_dir=output_dir, result_name=job_name)
