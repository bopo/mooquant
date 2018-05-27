from mooquant import bar
from mooquant.tools import resample, mootdx


def main():
    import coloredlogs
    coloredlogs.install(level='DEBUG', fmt='[%(asctime)s] %(levelname)s %(message)s')

    instrument = "600036"
    feeds = mootdx.build_feed([instrument], 2003, 2018, "histdata/mootdx")
    resample.resample_to_csv(feeds, bar.Frequency.MINUTE * 30, "30min-bitstampUSD.csv")


if __name__ == "__main__":
    main()
