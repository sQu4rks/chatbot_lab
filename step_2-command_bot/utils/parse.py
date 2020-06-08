import shlex

def parse(cmd_string):
    split = shlex.split(cmd_string)

    cmd = split[0]

    arguments = {}
    for argument_pair in split[1:]:
        arg_split = argument_pair.split("=")
        arg = arg_split[0]

        if len(arg_split) == 1:
            val = None
        else:
            val = arg_split[1]

        arguments[arg] = val

    return cmd, arguments

