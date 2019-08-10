import hashlib
import os
import queue
import sys
import subprocess

import git
import click

from .helpers import GitConfig


@click.group(
    help="All options can be set with `git config --global git-oras.OPTION value`"
)
@click.option(
    "--registry",
    prompt=False,
    default=lambda: GitConfig.get("git-oras.registry"),
    help="OCI compatible registry URL",
    required=True,
)
@click.pass_context
def cli(ctx, registry):
    ctx.ensure_object(dict)
    ctx.obj["registry"] = registry
    ctx.obj["files"] = {}
    if not os.path.isdir(".git"):
        print("This is not a git repository!")
        sys.exit(-1)
    if os.path.isfile(".git-oras"):
        with open(".git-oras", "r") as f:
            for line in f.readlines():
                sha, filename = line.split()
                ctx.obj["files"][filename] = sha


@cli.command()
@click.pass_context
def init(ctx):
    if not os.path.isfile(".git-oras"):
        open(".git-oras", "a").close()
    pass


@cli.command()
@click.pass_context
def status(ctx):
    print(ctx.obj["files"], ctx.obj["registry"])
    pass


@cli.command()
@click.argument("files", nargs=-1)
@click.pass_context
def add(ctx, files):
    for file in files:
        with open(file, "rb") as f:
            b = f.read()
            hash = hashlib.sha256(b).hexdigest()
            ctx.obj["files"][file] = hash
    with open(".git-oras", "w") as f:
        for key in sorted(ctx.obj["files"].keys()):
            f.write("{} {}\n".format(ctx.obj["files"][key], key))
    pass


@cli.command()
@click.pass_context
def push(ctx):
    todo = queue.Queue()
    work = queue.Queue()
    for file in ctx.obj["files"].keys():
        todo.put(file)
    while todo.qsize() > 0:
        if work.qsize() < 32:
            file = todo.get()
            p = subprocess.Popen(
                [
                    "oras",
                    "push",
                    "{}/blob/{}:{}".format(ctx.obj["registry"], file.split("/")[1], ctx.obj["files"][file]),
                    "{}:application/octet-stream".format(file),
                ],
                stdout=subprocess.PIPE,
            )
            work.put(p)
        else:
            print(work.get().communicate()[0].decode("utf-8"))
    while work.qsize() > 0:
        print(work.get().communicate()[0].decode("utf-8"))


@cli.command()
@click.pass_context
def pull(ctx):
    todo = queue.Queue()
    work = queue.Queue()
    for file in ctx.obj['files'].keys():
        todo.put(file)
    while todo.qsize() > 0:
        if work.qsize() < 32:

            file = todo.get()
            p = subprocess.Popen(
                [
                    "oras",
                    "pull",
                    "{}/blob/{}:{}".format(ctx.obj["registry"], file.split("/")[1], ctx.obj["files"][file]),
                    "-a",

                ],
                stdout = subprocess.PIPE,
            )
            work.put(p)
        else:
            print(work.get().communicate()[0].decode("utf-8"))
    while work.qsize() > 0:
        print(work.get().communicate()[0].decode("utf-8"))

    pass

@cli.command()
def verify():
    p = subprocess.Popen(
        [
            "sha256sum",
            "--check",
            "--quiet",
            "--status",
            ".git-oras"

        ]
    )