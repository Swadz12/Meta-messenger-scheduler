import paths
import scheduler

def main():
    args = paths.parse_cli_args()
    paths.update_config_from_args(args)
    if args.run:
        scheduler.run_script()

if __name__ == "__main__":
    main()