from tahweel import TahweelArgumentParser


def main() -> None:
  args = TahweelArgumentParser(underscores_to_dashes=True).parse_args()
