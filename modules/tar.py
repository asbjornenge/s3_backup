import tarfile

def compress(source):
    target = "%s.%s" % (source, 'tgz')
    with tarfile.open(target, "w:gz") as tgz:
        tgz.add(source, arcname=target)
    tgz.close()
    return target