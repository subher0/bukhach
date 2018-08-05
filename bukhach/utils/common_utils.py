import uuid


def make_filepath(instance, filename):
    new_filename = "%s.%s" % (uuid.uuid4(),
                             filename.split('.')[-1])
    return '/'.join([instance.__class__.__name__.lower(), new_filename])

