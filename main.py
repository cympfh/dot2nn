import click

from dot2nn.parser import parse
from dot2nn.compile import compile


@click.command()
@click.option('-T', '--type', type=click.Choice(['dot', 'keras', 'pytorch']))
def main(type):
    print(compile(parse(' '.join(open('/dev/stdin', 'r').readlines())), type=type))


if __name__ == '__main__':
    main()
