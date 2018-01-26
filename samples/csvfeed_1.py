from mooquant.feed import csvfeed

feed = csvfeed.Feed("Date", "%Y-%m-%d")
feed.addValuesFromCSV("../tests/data/quandl_gold_2.csv")

for dateTime, value in feed:
    print(dateTime, value)
