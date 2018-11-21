Disclaimer: this is only a proof-of-concept (and a joke), please don't actually use this.


# bin2fasta

Store any file as a fasta file!


## Installation

```bash
$ pip install bin2fasta
```


## Usage

```bash
$ file foo.webm
foo.webm: WebM
$ bin2fasta foo.webm > bar.fasta
1343440it [00:01, 1132297.03it/s]
$ head -c50 bar.fasta
>Sequence_master
AGTTGAGGCGCCTTACTGCCGAATTAGTTAAGA
$ bin2fasta --decode bar.fasta > baz.webm
671720it [00:01, 452470.18it/s]
$ file baz.webm
baz.webm: WebM
$ diff foo.webm baz.webm
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
