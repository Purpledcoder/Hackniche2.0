import docker
import json
import concurrent.futures
import time

def get_container_stats(container_id):
    try:
        container = client.containers.get(container_id)
        stats_stream = container.stats(stream=True)
        for stats in stats_stream:
            info = stats.decode('utf-8')
            data = json.loads(info)
            print(container.id)
            print(data['cpu_stats']['cpu_usage']['total_usage'])
    except docker.errors.NotFound as e:
        print(f"Container not found: {e}")
    except docker.errors.APIError as e:
        print(f"Error fetching container stats: {e}")

def monitor_containers():
    while True:
        # Get the list of all containers
        existing_containers = client.containers.list(all=True)
        existing_container_ids = [container.id for container in existing_containers]

        # Get the list of container IDs currently being monitored
        monitoring_container_ids = set(thread_container_ids)

        # Identify new containers by finding the difference
        new_container_ids = set(existing_container_ids) - monitoring_container_ids

        # Add new containers to the monitoring list
        thread_container_ids.extend(new_container_ids)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(get_container_stats, thread_container_ids)

        time.sleep(5)  # Adjust the sleep duration as needed

if __name__ == "__main__":
    client = docker.from_env()
    thread_container_ids = []  # List to store container IDs being monitored

    # Start monitoring containers in a separate thread
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(monitor_containers)

    # Your main program continues here
    # You may want to add a KeyboardInterrupt handler or other termination mechanism
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program terminated.")
