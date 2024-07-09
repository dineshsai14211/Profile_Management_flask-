import logging as log

log.basicConfig(filename="../log/app.log", filemode="a", level=log.DEBUG,
                format="%(asctime)s - %(levelname)s - %(message)s")