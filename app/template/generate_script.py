def generate_script_for_image(script_content) -> str:
    start = """ 
    from sys import addaudithook
    def block_mischief(event,arg):
    if 'WRITE_LOCK' in globals() and ((event=='open' and arg[1]!='r') or event.split('.')[0] in ['subprocess', 'os', 'shutil', 'winreg']):
        raise IOError('file write forbidden')
        
    addaudithook(block_mischief)
    
    def not_available(*args, **kwargs):
        return 'Not allowed'
    eval = not_available
    exec = not_available
    print = not_available
    compile = not_available
    exit = not_available
    breakpoint = breakpoint
    input = breakpoint
    import builtins
    builtins.eval = not_available
    builtins.exec = not_available
    builtins.print = not_available
    builtins.compile = not_available
    builtins.breakpoint = not_available
    builtins.input = not_available
    
    """
    end = """"""
    return f"def run_script(user_id: str, script_name: str):\n" \
           f"    {start} \n " \
           f"    {script_content}" \
           f"    {end}\n" \
           f"\n"


def generate_script_for_live_coding(script_content, user_id: str, ) -> str:
    start = """ 
    from sys import addaudithook
    def block_mischief(event,arg):
    if 'WRITE_LOCK' in globals() and ((event=='open' and arg[1]!='r') or event.split('.')[0] in ['subprocess', 'os', 'shutil', 'winreg']):
        raise IOError('file write forbidden')

    addaudithook(block_mischief)

    def not_available(*args, **kwargs):
        return 'Not allowed'
    eval = not_available
    exec = not_available
    print = not_available
    compile = not_available
    exit = not_available
    breakpoint = breakpoint
    input = breakpoint
    import builtins
    builtins.eval = not_available
    builtins.exec = not_available
    builtins.print = not_available
    builtins.compile = not_available
    builtins.breakpoint = not_available
    builtins.input = not_available

    """
    end = """"""
    return f"{start} \n" \
           f"{script_content}\n" \
           f" {end}\n" \
           f"\n"
