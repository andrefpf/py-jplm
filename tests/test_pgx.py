import jplm


def test_read_bikes():
    reader = jplm.PGXHandler()
    image = reader.read("tests/pgx_files/bikes.pgx")
    # test stuff


def test_read_greek():
    reader = jplm.PGXHandler()
    image = reader.read("tests/pgx_files/greek.pgx")
    # test stuff
