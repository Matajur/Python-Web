from multiprocessing import Pool, cpu_count, current_process
from time import time


def factorize_sync(number):
    print(f"Starting syncronous calculation: {current_process().name}")
    results = []
    for num in number:
        result = []
        for i in range(1, num + 1):
            if num % i == 0:
                result.append(i)
        results.append(result)
    print(f"Syncronous calculation is finished: {current_process().name}")
    return results


def factorize_async(number):
    print(f"Starting asyncronous calculation: {current_process().name}")
    result = []
    for i in range(1, number + 1):
        if number % i == 0:
            result.append(i)
    print(f"{current_process().name} is finished")
    return result


if __name__ == "__main__":
    numbers = (
        128,
        255,
        99999,
        10651060,
        54657876,
        12443508,
        86785637,
        72467590,
    )

    timer1 = time()

    a, b, c, d, e, f, g, h = factorize_sync(numbers)

    print(f"Synchronous calculation has taken {round(time() - timer1, 4)}s")  # 13.1734s

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]

    print(f"CPU count: {cpu_count()}")  # 8
    timer2 = time()

    with Pool(cpu_count()) as pool:
        s, t, u, v, w, x, y, z = pool.map(factorize_async, numbers)
        pool.close()
        pool.join()

    print(f"Asynchronous calculation has taken {round(time() - timer2, 4)}s")  # 6.8109s

    assert s == [1, 2, 4, 8, 16, 32, 64, 128]
    assert t == [1, 3, 5, 15, 17, 51, 85, 255]
    assert u == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
