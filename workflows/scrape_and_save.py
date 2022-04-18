from parliament_lk import scrape_mem_dir, scrape_mem

if __name__ == '__main__':
    # mem_dir_info_list = scrape.scrape_mem_dir()
    mem = scrape_mem.scrape_mem(1244)
    print(mem)
