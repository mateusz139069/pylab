# coding=utf-8
from shutil import copy
from time import sleep

from pathlib import Path
from invoke import run, task

@task
def tags(docs=False):
    if docs:
        run(u"Przygotuj tagi dla pliku pong.py w oparciu o wersje pliku w folderze zadania")

    targets = {}
    cwd = Path(".")
    exercises = Path("./zadania")
    for p in exercises.iterdir():
        name, tag = p.stem.rsplit("_", 1)
        targets.setdefault(tag, []).append(name)
    for tag in sorted(targets.keys()):
        for name in targets[tag]:
            src = exercises / (name + "_" + tag + ".py")
            dst = cwd / (name+".py")
            print "Kopiuje ", src, " do ", dst
            copy(unicode(src), unicode(dst))
        run('git commit -am '+tag, warn=True)
        run('git tag -f '+tag, warn=True)
        sleep(1)  # Git psuje ścieżki powiązań jeśli operacje są zbyt blisko siebie


@task
def push(docs=False):
    run("git push --tags")
