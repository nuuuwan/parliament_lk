import json

from parliament_lk import scrape_mem

if __name__ == '__main__':
    # mem_dir_info_list = scrape.scrape_mem_dir()
    mem = scrape_mem.scrape_mem(3325)
    print(json.dumps(mem, indent=2))
