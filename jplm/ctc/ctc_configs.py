from jplm.config import Config


CTC_LENSLET_CONFIG = Config({
    "--part": 2,
    "--type": 0,
    "--enum-cs": "YCbCr_2",
    "--border_policy": 1,
    "--number-of-colour-channels": 3,
    "--view_height": 434,
    "--view_width": 625,
    "--number_of_rows": 13,
    "--number_of_columns": 13,

    "--transform_size_maximum_intra_view_vertical": 31,
    "--transform_size_maximum_intra_view_horizontal": 25,
    "--transform_size_maximum_inter_view_vertical": 13,
    "--transform_size_maximum_inter_view_horizontal": 13,

    "--transform_size_minimum_intra_view_vertical": 4,
    "--transform_size_minimum_intra_view_horizontal": 4,
    "--transform_size_minimum_inter_view_vertical": 13,
    "--transform_size_minimum_inter_view_horizontal": 13,
})


CTC_SYNTHETIC_CONFIG = Config({
    "--part": 2,
    "--type": 0,
    "--enum-cs": "YCbCr_2",
    "--border_policy": 1,
    "--number-of-colour-channels": 3,
    "--view_height": 512,
    "--view_width": 512,
    "--number_of_rows": 9,
    "--number_of_columns": 9,

    "--transform_size_maximum_intra_view_vertical": 32,
    "--transform_size_maximum_intra_view_horizontal": 32,
    "--transform_size_maximum_inter_view_vertical": 9,
    "--transform_size_maximum_inter_view_horizontal": 9,

    "--transform_size_minimum_intra_view_vertical": 4,
    "--transform_size_minimum_intra_view_horizontal": 4,
    "--transform_size_minimum_inter_view_vertical": 9,
    "--transform_size_minimum_inter_view_horizontal": 9,
})


CTC_TAROT_CONFIG = Config({
    "--part": 2,
    "--type": 0,
    "--enum-cs": "YCbCr_2",
    "--border_policy": 1,
    "--number-of-colour-channels": 3,
    "--view_height": 1024,
    "--view_width": 1024,
    "--number_of_rows": 17,
    "--number_of_columns": 17,

    "--transform_size_maximum_intra_view_vertical": 32,
    "--transform_size_maximum_intra_view_horizontal": 32,
    "--transform_size_maximum_inter_view_vertical": 17,
    "--transform_size_maximum_inter_view_horizontal": 17,

    "--transform_size_minimum_intra_view_vertical": 4,
    "--transform_size_minimum_intra_view_horizontal": 4,
    "--transform_size_minimum_inter_view_vertical": 17,
    "--transform_size_minimum_inter_view_horizontal": 17,
})


CTC_SET2_CONFIG = Config({
    "--part": 2,
    "--type": 0,
    "--enum-cs": "YCbCr_2",
    "--border_policy": 1,
    "--number-of-colour-channels": 3,
    "--view_height": 1080,
    "--view_width": 1920,
    "--number_of_rows": 11,
    "--number_of_columns": 33,

    "--transform_size_maximum_intra_view_vertical": 36,
    "--transform_size_maximum_intra_view_horizontal": 32,
    "--transform_size_maximum_inter_view_vertical": 11,
    "--transform_size_maximum_inter_view_horizontal": 33,

    "--transform_size_minimum_intra_view_vertical": 4,
    "--transform_size_minimum_intra_view_horizontal": 4,
    "--transform_size_minimum_inter_view_vertical": 11,
    "--transform_size_minimum_inter_view_horizontal": 33,
})


CTC_POZNANLAB1_TAU_CONFIG = Config({
    "--part": 2,
    "--type": 0,
    "--enum-cs": "YCbCr_2",
    "--border_policy": 1,
    "--number-of-colour-channels": 3,
    "--view_height": 1288,
    "--view_width": 1936,
    "--number_of_rows": 31,
    "--number_of_columns": 31,

    "--transform_size_maximum_intra_view_vertical": 46,
    "--transform_size_maximum_intra_view_horizontal":44,
    "--transform_size_maximum_inter_view_vertical": 31,
    "--transform_size_maximum_inter_view_horizontal": 31,

    "--transform_size_minimum_intra_view_vertical": 4,
    "--transform_size_minimum_intra_view_horizontal": 4,
    "--transform_size_minimum_inter_view_vertical": 31,
    "--transform_size_minimum_inter_view_horizontal": 31,
})
