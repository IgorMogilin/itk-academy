import random
import json
import time
import math
from concurrent import futures
import multiprocessing as mp
from functools import wraps


def timer_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"⏱️  {func.__name__} выполнен за {execution_time:.4f} секунд")
        return result
    return wrapper


def generate_data(n):
    return [random.randint(1, 50) for _ in range(n)]


def process_number(number):
    n = min(number, 30)
    result = math.factorial(n)
    return {
        "input_number": number,
        "factorial_of": n,
        "digits_count": len(str(result))
    }


def worker(input_queue, output_queue):
    while True:
        number = input_queue.get()
        if number is None:
            break
        result = process_number(number)
        output_queue.put(result)


@timer_decorator
def sequential_processing(numbers):
    return [process_number(num) for num in numbers]


@timer_decorator
def parallel_with_threads(numbers):
    with futures.ThreadPoolExecutor() as executor:
        return list(executor.map(process_number, numbers))


@timer_decorator
def parallel_with_process_pool(numbers):
    with mp.Pool(processes=mp.cpu_count()) as pool:
        return pool.map(process_number, numbers)


@timer_decorator
def parallel_with_manual_processes(numbers):
    input_queue = mp.Queue()
    output_queue = mp.Queue()
    num_processes = min(mp.cpu_count(), 4)
    processes = []
    results = []

    for _ in range(num_processes):
        p = mp.Process(target=worker, args=(input_queue, output_queue))
        p.start()
        processes.append(p)

    for number in numbers:
        input_queue.put(number)

    for _ in range(num_processes):
        input_queue.put(None)

    for _ in range(len(numbers)):
        results.append(output_queue.get())

    for p in processes:
        p.join()

    return results


def save_results(results, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


def main():
    print("🚀 Запуск программы...")
    numbers = generate_data(10000)
    print(f"📊 Сгенерировано {len(numbers)} чисел")
    approaches = {
        "Sequential": sequential_processing,
        "ThreadPool": parallel_with_threads,
        "ProcessPool": parallel_with_process_pool,
        "ManualProcesses": parallel_with_manual_processes
    }
    results_saved = False
    for approach_name, approach_func in approaches.items():
        print(f"\n{'='*40}")
        print(f"🧪 Тестируем {approach_name}")

        try:
            results = approach_func(numbers)
            print(f"✅ Успешно - {len(results)} результатов")
            if not results_saved:
                save_results(results, "processing_results.json")
                print("💾 Результаты сохранены в 'processing_results.json'")
                results_saved = True
        except Exception as e:
            print(f"❌ Ошибка: {e}")

    print(f"\n{'='*40}")
    print("🎉 Программа завершена!")


if __name__ == "__main__":
    main()
