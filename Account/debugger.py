# debugger.py

def initialize_debugger():
    if initialize_debugger.has_run:
        return

    initialize_debugger.has_run = True

    import multiprocessing
    import logging

    debug_log = logging.getLogger("debug")
    logging.basicConfig()
    debug_log.setLevel(logging.DEBUG)

    pid =  multiprocessing.current_process().pid
    debug_log.info("pid = " + str(pid))
 
    if pid < 10:
        import debugpy
 
        debugpy.listen(("0.0.0.0", 5678))
        debug_log.info("wait_for_client on port 5678")
        debugpy.wait_for_client()

initialize_debugger.has_run = False
