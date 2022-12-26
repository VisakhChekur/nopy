import nox


@nox.session(name="Tests", python=["3.9", "3.10", "3.11"], reuse_venv=True)
def tests(session: nox.Session):
    """Running the tests."""

    session.install("poetry")
    session.run("poetry", "install")
    session.run("pytest")
