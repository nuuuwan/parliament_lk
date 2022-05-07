from parliament_lk.scrape_and_store import store_mps


def main():
    store_mps.store_all(FORCE_SCRAPE=True)


if __name__ == '__main__':
    main()
