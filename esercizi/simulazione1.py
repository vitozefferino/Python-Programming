class ExamException(Exception):
    pass

class MovingAverage:
    def __init__(self, window_size):
        if window_size is None or not isinstance(window_size, int) or window_size < 1:
            raise ExamException("Invalid window size")
        self.window_size = window_size

    def compute(self, values):
        if not isinstance(values, list):
            raise ExamException("Values should be a list")
        if not values:
            raise ExamException("Values list is empty")
        if len(values) < self.window_size:
            raise ExamException("Window size is larger than the number of values")
        if any(not isinstance(i, (int, float)) for i in values):
            raise ExamException("Value list should contain only numeric")
        result = []
        for i in range(len(values) - self.window_size + 1):
            window = values[i:i+self.window_size]
            avg = sum(window) / len(window)
            result.append(avg)
        return result

moving_average = MovingAverage(2)
result = moving_average.compute([2,4,8,16])
print(result)