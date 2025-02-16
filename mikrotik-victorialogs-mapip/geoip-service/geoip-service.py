import geoip2.database
import json
import requests
from flask import Flask, jsonify, request
from collections import defaultdict
# wget https://git.io/GeoLite2-City.mmdb

# Configuration
GEOIP_DB_PATH = "/data/GeoLite2-City.mmdb"  # Path to GeoLite2 database
API_URL = "http://victoria-logs:9428/select/logsql/query"  # URL to fetch IP data
API_QUERY_COMMON = "!NAT !ICMP | extract ', proto <proto>, <src-ip>:<src-port>-><dst-ip>:<dst-port>, len' from _msg | stats by (dst-ip) count() dst-ip-count | sort (dst-ip-count) desc limit 1000"

app = Flask(__name__)

# Load GeoIP database
reader = geoip2.database.Reader(GEOIP_DB_PATH)

def fetch_ips(ip='*', time='1d'):
    """Fetch IP data from the given API."""
    try:
        response = requests.post(API_URL, data={"query": f"{ip} _time:{time} {API_QUERY_COMMON}"})
        response.raise_for_status()  # Raise an error for bad responses
        lines = response.text.strip().split("\n")  # Parse line-separated JSON

        ip_data = [json.loads(line) for line in lines]  # Convert each line to JSON
        return [entry["dst-ip"] for entry in ip_data if "dst-ip" in entry]  # Extract IPs

    except Exception as e:
        print(f"Error fetching IPs: {e}")
        return []

def get_geo_data(ip, time):
    """Resolve IPs to geographical locations."""
    ip_addresses = fetch_ips(ip, time)
    locations = []

    for ip in ip_addresses:
        try:
            response = reader.city(ip)
            locations.append({
                "ip": ip,
                "latitude": response.location.latitude,
                "longitude": response.location.longitude,
                "city": response.city.name or "Unknown",
                "country": response.country.name or "Unknown"
            })
        except Exception as e:
            print(f"Error processing {ip}: {e}")

    return locations

def get_country_counts(ip, time):
    """Count occurrences of each country from resolved IPs."""
    ip_addresses = fetch_ips(ip, time)
    country_counts = defaultdict(int)

    for ip in ip_addresses:
        try:
            response = reader.city(ip)
            country = response.country.name or "Unknown"
            country_counts[country] += 1
        except Exception as e:
            print(f"Error processing {ip}: {e}")

    return [{"country": country, "count": count} for country, count in country_counts.items()]

def get_city_counts(ip, time):
    """Count occurrences of each city from resolved IPs."""
    ip_addresses = fetch_ips(ip, time)
    city_counts = defaultdict(int)

    for ip in ip_addresses:
        try:
            response = reader.city(ip)
            if response.city.name:
                city = response.city.name
                city_counts[city] += 1
        except Exception as e:
            print(f"Error processing {ip}: {e}")

    return [{"city": city, "count": count} for city, count in city_counts.items()]


@app.route("/city_data")
def city_data():
    ip = request.args.get("ip")
    time = request.args.get("time")
    return jsonify(get_city_counts(ip, time))


@app.route("/country_data")
def country_data():
    ip = request.args.get("ip")
    time = request.args.get("time")
    return jsonify(get_country_counts(ip, time))

@app.route("/geo_data")
def geo_data():
    ip = request.args.get("ip")
    time = request.args.get("time")
    return jsonify(get_geo_data(ip, time))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555)
