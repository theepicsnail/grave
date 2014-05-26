import threading, time, sys, traceback
def proc():
    time.sleep(10)
    dump(file("procdump", "w"))
    #while True:
    #    time.sleep(10)
    #    with file("procdump", "w") as out:
    #        dump(out)

def dump(out= sys.stderr):
    print >> out, "\n*** STACKTRACE - START ***\n"
    code = []
    for threadId, stack in sys._current_frames().items():
        code.append("\n# ThreadID: %s" % threadId)
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename,
                                                        lineno, name))
            if line:
                code.append("  %s" % (line.strip()))

    for line in code:
        print >> out, line
    print >> out, "\n*** STACKTRACE - END ***\n"


threading.Thread(target = proc).start()

