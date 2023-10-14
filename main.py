from bin.args import args
import subprocess
def main():
    run_args = []
    if(args.t == 1):
        run_args.append('api/python.exe')
        run_args.append('bin/highdefinition.py')
        run_args.append('--configjson')
        run_args.append(str(args.configjson))
        run_args.append('--redraw_methods')
        run_args.append(str(args.redraw_methods))
        run_args.append('--redrawcamplitude')
        run_args.append(str(args.redrawcamplitude))
        run_args.append('--fixcount')
        run_args.append(str(args.fixcount))
        run_args.append('--control_methods')
        run_args.append(str(args.control_methods))
        print('Launched: ' + ' '.join(run_args))
    subprocess.Popen(run_args)






if __name__ == '__main__':
    main()