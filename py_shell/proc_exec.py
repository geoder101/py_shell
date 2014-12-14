#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE


def proc_exec(cmd, pinput=None):
    """
    Execute `cmd` (['proc', 'arg1', ..., 'argN']),
    pipe `pinput`, if any, to `stdin`
    and return (`exit status`, `stdout`, `stderr`).

    Example:
    --------

    >>> proc_exec(['cat', '-n'], "yo")
    (True, '     1\\tyo', '')
    """
    p = Popen(cmd, stdin=PIPE if pinput else None, stdout=PIPE, stderr=PIPE)
    pout, perr = p.communicate(pinput)
    pstatus = p.wait() == 0
    return pstatus, pout, perr

def proc_pipe(cmds):
    """
    Execute `cmds` (['proc1', 'arg1', ..., 'argN'], ['proc2', 'arg1', ..., 'argN'])
    in such a way that the output of each command in the pipeline
    is supplied as the input of the next command.

    Example:
    --------

    >>> proc_pipe([['echo', 'yo'], ['cat']])
    (True, 'yo\\n', '')
    """
    return reduce(_pipe, cmds, (True, '', ''))

def _pipe((ok, pin, perr), cmd):
    if ok:
        pstatus, pout, perr = proc_exec(cmd, pin)
        return pstatus, pout, perr
    else:
        return False, '', perr


if __name__ == '__main__':
    import doctest
    doctest.testmod()
