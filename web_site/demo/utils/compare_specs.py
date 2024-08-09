import fuzzywuzzy.fuzz as fuzz


def compare_specs(resume_results,inputs):
    score_dict={}
    for file_path in resume_results:
        score_dict[file_path]=0
        resume_result=resume_results[file_path]
        for input in inputs:
            for resume_part in resume_result:
                if resume_part["phrase"]==input:
                    similarity = fuzz.ratio(resume_part["text"],inputs[input] ) / 100
                    if similarity>0.8:
                        score_dict[file_path]+=inputs[f'{input} Score']
    return score_dict
    