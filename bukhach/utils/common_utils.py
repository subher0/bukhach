import uuid


def make_filepath(instance, filename):
    new_filename = "%s.%s" % (uuid.uuid4(),
                             filename.split('.')[-1])
    return '/'.join([instance.__class__.__name__.lower(), new_filename])

def transform_time(dt):
    if dt.minute >= 30:
        dt = dt.replace(hour=dt.hour + 1)
    dt = dt.replace(minute=0, second=0)
    return dt