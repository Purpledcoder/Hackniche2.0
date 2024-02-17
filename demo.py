import docker
import json

def get_container_stats(container_id):
    client = docker.from_env()

    try:
        container = client.containers.get(container_id)
        stats_stream = container.stats(stream=True)
        # memory_stats = stats_stream['memory_stats']
        # print(memory_stats)
        # print("\n")
        # Print the stats (you can modify this part based on your requirements)
        for stats in stats_stream:
            info = stats.decode('utf-8')
            data = json.loads(info)
            print(container.id)
            print(data['cpu_stats']['cpu_usage']['total_usage'])
            

    except docker.errors.NotFound as e:
        print(f"Container not found: {e}")
    except docker.errors.APIError as e:
        print(f"Error fetching container stats: {e}")

if __name__ == "__main__":
    # Replace 'your_container_id' with the actual container ID
    container_id = '1ffba5dfbca83563e5e92e04098ba4693718efdeb7934461b90853e53cef1e1a'
    get_container_stats(container_id)
