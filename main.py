import json
import time
import urllib.request
from os import cpu_count
from threading import Thread
from urllib.error import HTTPError

finished_count: int = 0


def count_letters(url: str, frequency: dict[str, int]) -> None:
    """
    :param url:
    :type url: str
    :param frequency: 
    :type frequency: dict[str, int]
    :return:
    :rtype None
    """

    global finished_count

    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"}

    try:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        txt = str(response.read())
        for charter in txt:
            letter = charter.lower()
            if letter in frequency:
                frequency[letter] += 1
    except HTTPError:
        return


def main(times: list[float], frequencies: list[dict[str, int]]) -> None:
    workers: list[Thread] = []
    main_frequency: dict[str, int] = {}

    for c in "abcdefghijklmnopqrstuvwxyz":
        main_frequency[c] = 0

    print("Starting threads...")
    start: float = time.time()
    for i in range(1000, 1020):
        t: Thread = Thread(target=count_letters, args=(f"https://www.rfc-editor.org/rfc/rfc{i}.txt",
                                                       main_frequency))
        workers.append(t)
        t.start()

    for worker in workers:
        worker.join()

    end: float = time.time()
    times.append(end - start)
    frequencies.append(main_frequency)
    print(json.dumps(main_frequency, indent=4))
    print("Done, time taken", end - start)


def main_2(times: list[float], frequencies: list[dict[str, int]]) -> None:
    rfc_start: int = 1000
    workers_times: list[int] = [cpu_count() for _ in range(20 // cpu_count())]
    workers_times.append(20 % cpu_count())
    
    workers: list[Thread] = []
    main_frequency: dict[str, int] = {}

    for c in "abcdefghijklmnopqrstuvwxyz":
        main_frequency[c] = 0

    print("Starting threads...")
    start: float = time.time()
    
    for w in workers_times:
        
        for i in range(rfc_start, rfc_start+w):
            t: Thread = Thread(target=count_letters, args=(f"https://www.rfc-editor.org/rfc/rfc{i}.txt",
                                                           main_frequency))
            workers.append(t)
            t.start()
        for worker in workers:
            worker.join()

        rfc_start += w
        workers = []
   
    end: float = time.time()

    print(rfc_start)
    times.append(end - start)
    frequencies.append(main_frequency)
    print(json.dumps(main_frequency, indent=4))
    print("Done, time taken", end - start)


def without_threads(times: list[float], frequencies: list[dict[str, int]]):
    main_frequency: dict[str, int] = {}

    for c in "abcdefghijklmnopqrstuvwxyz":
        main_frequency[c] = 0

    print("Starting threads...")
    start: float = time.time()
    for i in range(1000, 1020):
        count_letters(f"https://www.rfc-editor.org/rfc/rfc{i}.txt", main_frequency)

    end: float = time.time()
    times.append(end - start)
    frequencies.append(main_frequency)
    print(json.dumps(main_frequency, indent=4))
    print("Done, time taken", end - start)


def are_different(dic1, dic2):
    if len(dic1) != len(dic2):
        return True

    for clave in dic1:
        if clave not in dic2:
            return True

    for clave, valor in dic1.items():
        if valor != dic2[clave]:
            return True

    return False


if __name__ == "__main__":
    a = {
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

    for _ in range(1):
        main(time_list, frequencies_list)

    for freq in frequencies_list:
        if are_different(freq, a):
            print("Error")
            print(freq)
            print(a)
