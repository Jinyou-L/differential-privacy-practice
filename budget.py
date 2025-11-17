from client import avg, count, count0, _pretty_print

# 每次 query 消耗 epsilon = 0.5
EPSILON = 0.5

class BudgetTracker:
    def __init__(self, budget):
        # 初始化时传入总预算，比如 2.0
        self.budget = budget

    def check_and_update_budget(self):
        # 检查当前预算是否足够
        if self.budget < EPSILON:
            raise ValueError(f"Out of budget! Remaining: {self.budget:.2f}")
        # 如果够，就减去 0.5
        self.budget -= EPSILON
        print(f"✅ Query approved. Remaining budget: {self.budget:.2f}")
        return True

    def avg(self, group_by, averaged_column):
        self.check_and_update_budget()
        return avg(group_by, averaged_column, True)

    def count(self, group_by):
        self.check_and_update_budget()
        return count(group_by, True)

    def count0(self, group_by):
        self.check_and_update_budget()
        return count0(group_by, True)


if __name__ == "__main__":
    # 初始化隐私预算为 2.0
    tracker = BudgetTracker(2.0)

    # 前 4 个查询会成功
    _pretty_print(*tracker.avg(["programming"], "age"))
    _pretty_print(*tracker.count(["age", "music"]))
    _pretty_print(*tracker.count0(["programming"]))
    _pretty_print(*tracker.count(["programming"]))

    # 第 5 个查询会报错
    _pretty_print(*tracker.avg(["sport"], "age"))
