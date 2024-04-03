from invoke import task


@task
def start(ctx):
    ctx.run("python3 src/index.py", pty=True)

@task
def create_sample_data(ctx):
    ctx.run("python3 src/create_sample_data.py", pty=True)