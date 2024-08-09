import sys
import time
import os
import cv2
import numpy as np
from segmentation import ImageSegmentation
from algorithms.ford_fulkerson import ford_fulkerson
from algorithms.edmonds_karp import edmonds_karp
from algorithms.dinic import dinic
from algorithms.push_relabel import push_relabel

def measure_performance(algo, image_path):
    print(f"Processing image: {image_path} using {algo.__name__}...")
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error reading image: {image_path}")
        return None

    bg_threshold = np.mean(image)
    img_name = os.path.splitext(os.path.basename(image_path))[0]
    segmentation = ImageSegmentation(image, "res", img_name)

    start_time = time.time()
    try:
        segmentation.segment(bg_threshold, algo)
    except Exception as e:
        print(f"Error during segmentation: {e}")
        return None
    end_time = time.time()

    return end_time - start_time

def run_tests(image_paths, algorithms):
    results = []
    for image_path in image_paths:
        print(f"Running tests for {image_path}")
        for algo_name, algo_func in algorithms.items():
            exec_time = measure_performance(algo_func, image_path)
            if exec_time is not None:
                img_name = os.path.splitext(os.path.basename(image_path))[0]
                results.append((img_name, algo_name, exec_time))
    return results

def print_results(results):
    print(f"{'Image':<20}{'Algorithm':<20}{'Time (s)':<10}")
    print("-" * 50)
    for img_name, algo_name, exec_time in results:
        print(f"{img_name:<20}{algo_name:<20}{exec_time:<10.5f}")

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <image_path1> <image_path2> ...")
        return

    image_paths = sys.argv[1:]
    algorithms = {
        "Ford-Fulkerson": ford_fulkerson,
        "Edmonds-Karp": edmonds_karp,
        "Dinic": dinic,
        "Push-Relabel": push_relabel
    }

    print("Starting performance tests...")
    results = run_tests(image_paths, algorithms)
    print_results(results)

if __name__ == "__main__":
    main()
