Disclaimer: this is only a proof-of-concept (and a joke), please don't actually use this.


# bin2fasta

Store any file as a fasta file!


## Installation

```bash
$ pip install bin2fasta
```


## Usage

```bash
$ file foo.png
foo.png: PNG image data, 618 x 257, 8-bit/color RGBA, non-interlaced
$ bin2fasta -o bar.fasta foo.png
319400it [00:00, 683649.99it/s]
$ head -c50 bar.fasta
>Sequence_master
AGTTGAGGCGCCTTACTGCCGAATTAGTTAAGA
$ bin2fasta --decode -o baz.png bar.fasta
159700it [00:00, 455825.67it/s]
$ file baz.png
baz.png: PNG image data, 618 x 257, 8-bit/color RGBA, non-interlaced
$ diff foo.png baz.png
$
```

Note that you can easily chain multiple commands by piping their respective outputs and using `-`:
```bash
$ cat foo.png | xz | gpg -c | bin2fasta - > bar.fasta
$ cat bar.fasta | bin2fasta -D - | gpg -d | xz --decompress > baz.png
$ diff foo.png baz.png
$
```


## Poetry workflow

Only relevant for [developers](https://poetry.eustace.io/docs/):

Run executable:
```bash
$ poetry run bin2fasta
```

Publish to PyPi:
```bash
$ poetry --build publish
```
