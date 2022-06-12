from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler(timezone="Asia/Seoul")

if __name__ == "__main__":
    try:
        import work
        for target in work.__all__:
            try:
                getattr(getattr(work, target), "init")(scheduler)
            except AttributeError:
                print("warning", f"fail to init {target} worker")

        scheduler.start()
    except KeyboardInterrupt:
        print("exited!")
