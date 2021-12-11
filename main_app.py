import parse
import Preprocessing.FE_INTE as preproc
import Evaluater.KNN_Basic as eval

# If you incorporate new data or are running for the first time this must be set to True
# Otherwise if you have already generated the csv and done the preprocessing can be set to False
# Just saves you a some time by caching values
do_parse = True


def main():
    # How to run ->
    # Can be anywhere so long as this application has access to it.

    path_to_data = 'data/data.csv'
    path_to_mss = 'millionsongsubset'

    if do_parse:
        parse.capture_feature_set(path_to_csv=path_to_data, path_to_msd_subset=path_to_mss)
        preproc.enest_terms_label_encoding(path_to_data)

    # Title and artist must be within the dataset
    eval.display_similar(path_to_data, title="Panama (Remastered Album Version)", artist="Van Halen")


if __name__ == "__main__":
    main()
