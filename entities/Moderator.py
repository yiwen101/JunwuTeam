import numpy as np

class Moderator:
    def __init__(self, properties):
        self.properties = properties
        self.tasks = []
        self.tasksEstimatedTime = []
        self.totalTaskRemainTime = 0
        self.effectiveWorkTime = 0
        self.totalWorkTime = 0
        self.isWorking = True
        self.id = None

    def isIdle(self):
        return self.isWorking and len(self.tasks) == 0

    def assign(self, advertisement, estimatedTime):
        # if already exceeded work time, refuse task
        if self.totalWorkTime + estimatedTime > self.properties["Productivity"] * 4:
            return False
        advertisement.assign()
        self.tasks.append(advertisement)
        self.tasksEstimatedTime.append(estimatedTime)
        self.totalTaskRemainTime += np.ceil(estimatedTime)
        self.totalWorkTime += estimatedTime
        self.effectiveWorkTime += estimatedTime
        return True

    def work(self):
        if self.totalWorkTime > self.properties["Productivity"] * 4:
            self.isWorking = False
        if self.isIdle():
            self.totalWorkTime += 1
        elif self.isWorking:
            self.tasksEstimatedTime[0] -= 1
            self.totalTaskRemainTime -= 1
            if (self.tasksEstimatedTime[0] <= 0):
                self.tasks.pop(0).done()
                self.tasksEstimatedTime.pop(0)


def ModeratorTest():
    class fakeAd:
        def __init__(self):
            self.isDone = False
            self.isAssigned = False

        def assign(self):
            self.isAssigned = True

        def done(self):
            self.isDone = True

    md = Moderator(
        {"moderator": 1, "market": ["US", "CA"], "Productivity": 286.2176,
         "Utilisation": 0.8124, "handling time": 123549, "accuracy": 0.99})
    ok = md.isIdle() and md.totalTaskRemainTime == 0
    ad1, ad2, ad3 = fakeAd(), fakeAd(), fakeAd()
    ok = not ad1.isAssigned
    md.assign(ad1, 2)
    ok = ok and not md.isIdle() and md.totalTaskRemainTime == 2 and ad1.isAssigned and not ad1.isDone
    md.work()
    ok = ok and not md.isIdle() and md.totalTaskRemainTime == 1 and not ad1.isDone
    md.work()
    ok = ok and md.isIdle() and md.totalTaskRemainTime == 0 and ad1.isDone
    md.work()
    ok = ok and md.effectiveWorkTime == 2 and md.totalWorkTime == 3
    md.assign(ad2, 2)
    md.assign(ad3, 1)
    md.work()
    ok = ok and md.totalTaskRemainTime == 2 and ad2.isAssigned and ad3.isAssigned
    md.work()
    ok = ok and md.totalTaskRemainTime == 1 and ad2.isDone
    if ok:
        print("ModeratorTest passed")
    else:
        print("ModeratorTest failed")
