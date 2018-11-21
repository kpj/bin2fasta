from click.testing import CliRunner

from ..main import main


def test_integration():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # setup environment
        content = 'Hello World!'

        fname = 'test.dat'
        with open(fname, 'w') as fd:
            fd.write(content)

        # run conversions
        result_b2f = runner.invoke(
            main, [fname, '-o', 'tmp.fasta'])
        result_f2b = runner.invoke(
            main, ['--decode', '-o', 'out.dat', 'tmp.fasta'])

        assert result_b2f.exit_code == 0
        assert result_f2b.exit_code == 0

        # check result
        with open('out.dat') as fd:
            conv_content = fd.read()

        assert content == conv_content
