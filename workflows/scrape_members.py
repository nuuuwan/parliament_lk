from utils import Parallel

from parliament_lk import MemberDirectoryPage, MemberPage

if __name__ == "__main__":
    member_short_info_list = MemberDirectoryPage.list_all()

    workers = []
    for member_short_info in member_short_info_list:

        def worker(member_short_info=member_short_info):
            MemberPage(member_short_info).member

        workers.append(worker)

    Parallel.run(workers, max_threads=8)
