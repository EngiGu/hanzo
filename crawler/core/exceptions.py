# 2
class ApplyTask(Exception):
    pass

# 3
class ApplyActionError(ApplyTask):
    pass

class ApplySiteError(ApplyTask):
    pass


class ApplyTypeError(ApplyTask):
    pass

class ApplyRequestError(ApplyTask):
    pass


class SpiderDoNotExists(Exception):
    pass


class ListParseDoNotExists(Exception):
    pass

class DetailParseDoNotExists(Exception):
    pass

class SpiderError(Exception):
    pass

class ParseResultNone(Exception):
    pass

if __name__ == '__main__':
    # raise SpecNameDoNotExists
    pass
