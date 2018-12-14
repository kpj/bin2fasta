import sys

import click
from tqdm import tqdm


class FileStreamer:
    """Generic file opener context"""
    def __init__(self, fname, mode):
        self.fname = fname
        self.mode = mode

        self.fd = None

    def __enter__(self):
        if self.fname == '-':
            self.fd = sys.stdin.buffer if 'b' in self.mode else sys.stdin
        else:
            self.fd = open(self.fname, self.mode)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fd.close()


class BitReader(FileStreamer):
    """Read individual bits of file"""
    def read(self):
        while True:
            byte = self.fd.read(1)
            if len(byte) == 0:
                return

            b = ord(byte)
            for i in range(7, -1, -1):
                yield (b >> i) & 1


class SequenceReader(FileStreamer):
    """Read only bases from FASTA file"""
    def read(self):
        ignore = True
        while True:
            char = self.fd.read(1)
            if len(char) == 0:
                return

            if char == '>':
                ignore = True
                continue
            elif char == '\n':
                ignore = False
                continue

            if not ignore:
                yield char


TABLE_BIN2FASTA = {0: {0: 'A', 1: 'G'}, 1: {0: 'T', 1: 'C'}}
TABLE_FASTA2BIN = {'A': '00', 'G': '01', 'T': '10', 'C': '11'}


@click.command()
@click.argument('filename', type=click.Path(exists=True, allow_dash=True))
@click.option(
    '-D', '--decode', is_flag=True, default=False,
    help='Enable conversion from FASTA to binary.')
@click.option(
    '-o', '--output', type=click.File('w'), default='-',
    help='File to write to.')
def main(filename, decode, output):
    """Store any file as a fasta file"""
    if decode:
        with SequenceReader(filename, mode='r') as fd:
            data = ''
            for base in tqdm(fd.read()):
                out = TABLE_FASTA2BIN[base]
                data += out

                if len(data) == 8:
                    int_ = 0
                    for bit in data:
                        int_ = (int_ << 1) | int(bit)
                    data = ''

                    byte = int_.to_bytes(1, byteorder=sys.byteorder)
                    output.buffer.write(byte)
    else:
        section_length = 250

        output.write('>Sequence_master\n')
        with BitReader(filename, mode='rb') as fd:
            last = None
            for i, bit in enumerate(tqdm(fd.read())):
                if (i+1) % section_length == 0:
                    output.write(f'\n>Sequence_{hex(i)}\n')

                if last is None:
                    last = bit
                else:
                    out = TABLE_BIN2FASTA[last][bit]
                    last = None
                    output.write(out)


if __name__ == '__main__':
    main()
