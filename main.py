import json
import time
import urllib.request
from os import cpu_count
from threading import Thread
from urllib.error import HTTPError

finished_count: int = 0


def count_letters(url: str, frequency: dict[str, int]) -> None:
    """
    Count the frequency of letters in the content obtained from a URL and update the provided frequency dictionary.
    
    :param url:
    :type url: str
    :param frequency: 
    :type frequency: dict[str, int]
    :return:
    :rtype: None
    """

    global finished_count

    try: 
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/120.0.0.0 Safari/537.36'
        }

        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        txt = str(response.read())

        for charter in txt:
            letter = charter.lower()
            if letter in frequency:
                frequency[letter] += 1
            else:
                frequency[letter] = 1
            finished_count += 1

    except HTTPError:
        return


def main(times: list[float], frequencies: list[dict[str, int]]) -> None:
    """
    Main function to initiate threads for counting letters in multiple RFCs.

    :param times: A list storing the times taken by each execution.
    :type times: list[float]
    :param frequencies: A list storing the dictionaries of letter frequencies obtained from each execution.
    :type frequencies: list[dict[str, int]]
    :return:
    :rtype: None
    """

    workers: list[Thread] = []
    main_frequency: dict[str, int] = {}

    for c in 'abcdefghijklmnopqrstuvwxyz':
        main_frequency[c] = 0

    print('Starting threads...')
    start: float = time.time()
    for i in range(1000, 1020):
        t: Thread = Thread(target=count_letters, args=(f'https://www.rfc-editor.org/rfc/rfc{i}.txt',
                                                       main_frequency))
        workers.append(t)
        t.start()

    for worker in workers:
        worker.join()

    end: float = time.time()
    times.append(end - start)

    global finished_count
    for key in main_frequency:
        main_frequency[key] /= finished_count
        main_frequency[key] *= 100

    frequencies.append(main_frequency)
    print(json.dumps(main_frequency, indent=4))
    print('Done, time taken', end - start)


def main_2(times: list[float], frequencies: list[dict[str, int]]) -> None:
    """
    Alternative version of the main function that organizes work into threads based on the number of CPU cores available

    :param times: A list storing the times taken by each execution.
    :type times: list[float]
    :param frequencies: A list storing the dictionaries of letter frequencies obtained from each execution.
    :type frequencies: list[dict[str, int]]
    :return:
    :rtype: None
    """

    rfc_start: int = 1000
    workers_times: list[int] = [cpu_count() for _ in range(20 // cpu_count())]
    workers_times.append(20 % cpu_count())

    workers: list[Thread] = []
    main_frequency: dict[str, int] = {}

    for c in 'abcdefghijklmnopqrstuvwxyz':
        main_frequency[c] = 0

    print('Starting threads...')
    start: float = time.time()

    for w in workers_times:

        for i in range(rfc_start, rfc_start+w):
            t: Thread = Thread(target=count_letters, args=(f'https://www.rfc-editor.org/rfc/rfc{i}.txt',
                                                           main_frequency))
            workers.append(t)
            t.start()
        for worker in workers:
            worker.join()

        rfc_start += w
        workers = []

    end: float = time.time()
    times.append(end - start)

    global finished_count
    for key in main_frequency:
        main_frequency[key] /= finished_count
        main_frequency[key] *= 100

    frequencies.append(main_frequency)
    print('Done, time taken', end - start)


def without_threads(times: list[float], frequencies: list[dict[str, int]]):
    main_frequency: dict[str, int] = {}

    for c in 'abcdefghijklmnopqrstuvwxyz':
        main_frequency[c] = 0

    print("Starting threads...")
    start: float = time.time()
    for i in range(1000, 1020):
        count_letters(f'https://www.rfc-editor.org/rfc/rfc{i}.txt', main_frequency)

    end: float = time.time()
    times.append(end - start)

    global finished_count
    for key in main_frequency:
        main_frequency[key] /= finished_count
        main_frequency[key] *= 100

    frequencies.append(main_frequency)
    print(json.dumps(main_frequency, indent=4))
    print('Done, time taken', end - start)


def are_different(dic1: dict[str, int], expected_frequency: dict[str, int]):
    """
    Compare two dictionaries of letter frequencies to check if they are different.

    :param dic1: First dictionary to compare.
    :type dic1: dict
    :param expected_frequency: Second dictionary to compare.
    :type expected_frequency: dict
    :return: True if the dictionaries are different, False otherwise.
    :rtype: bool
    """

    global finished_count
    for c in 'abcdefghijklmnopqrstuvwxyz':
        if dic1[c] != (expected_frequency[c] / finished_count)*100:
            print('Something went wrong')
            print(f'dict1["{c}"] = {dic1[c]} is not equal to '
                  f'expected_frequency["{c}"] = {expected_frequency[c] / finished_count * 100}')
            return True
    return False


if __name__ == "__main__":
    expected_freq = {
        "a": 80014,
        "b": 16998,
        "c": 48003,
        "d": 40501,
        "e": 140093,
        "f": 26074,
        "g": 19010,
        "h": 36316,
        "i": 79913,
        "j": 2170,
        "k": 6614,
        "l": 38305,
        "m": 31176,
        "n": 135371,
        "o": 84258,
        "p": 32270,
        "q": 2835,
        "r": 75326,
        "s": 79790,
        "t": 103557,
        "u": 27572,
        "v": 10580,
        "w": 14195,
        "x": 4719,
        "y": 13914,
        "z": 1115,
    }

    time_list: list[float] = []
    frequencies_list: list[dict[str, int]] = []

    count: int = 0
    for _ in range(6):
        main(time_list, frequencies_list)
        if _ == 0:
            count = finished_count
        finished_count = 0

    finished_count = count

    is_ok: bool = True
    for freq in frequencies_list:
        if are_different(freq, expected_freq):
            is_ok = False
            break

    if is_ok:
        print("Everything is ok")
