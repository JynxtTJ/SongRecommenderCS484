import parse
import Preprocessing.FE_INTE as preproc
import Evaluater.KNN_Basic as eval

do_parse = True

def main():
    path_to_data = 'data/data.csv'

    if do_parse:
        parse.capture_feature_set()
        preproc.enest_terms_label_encoding(path_to_data)

    eval.display_similar(path_to_data)


if __name__ == "__main__":
    main()
