def fibonacci(n):
    nums = [0, 1]
    for i in range(2, n):
        nums.append(nums[i-1] + nums[i-2])
    return nums[n-1]

print(fibonacci(1))