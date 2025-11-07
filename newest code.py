# -*- coding: utf-8 -*-
"""
Created on Fri Nov  7 19:52:35 2025

@author: Viraj
"""

import os
import requests
import folium
from datetime import datetime
from flask import Flask, render_template_string

app = Flask(__name__)

def fetch_fill_level():
    try:
        channel_id = "3150955"
        read_api_key = "V17KH0UBYNHPAQQU"
        url = f"https://api.thingspeak.com/channels/{channel_id}/fields/1.json?api_key={read_api_key}&results=1"
        response = requests.get(url)
        data = response.json()
        value = data['feeds'][0]['field1']
        return int(float(value)) if value else 0
    except:
        return 0

def generate_map_html():
    base_station = [16.705, 74.243]
    locations = [
        "Mahalaxmi Temple", "Rankala Lake", "Govt. College of Engineering",
        "City Railway Station", "Chhatrapati Shahu Stadium", "New Palace"
    ]
    live_fill = fetch_fill_level()
    bins = [
        [16.6950, 74.2375, live_fill],
        [16.7045, 74.2425, live_fill],
        [16.7055, 74.2460, live_fill],
        [16.7100, 74.2600, live_fill],
        [16.7200, 74.2470, live_fill],
        [16.7050, 74.2550, live_fill]
    ]
    m = folium.Map(location=base_station, zoom_start=14)
    for b, name in zip(bins, locations):
        color = "red" if b[2] >= 80 else "green"
        folium.Marker(
            [b[0], b[1]],
            popup=f"{name}<br>Fill: {b[2]}%",
            icon=folium.Icon(color=color)
        ).add_to(m)
    folium.Marker(
        base_station,
        popup=f"🕒 Last updated: {datetime.now().strftime('%d %b %Y %H:%M:%S')}",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)
    return m._repr_html_()

@app.route('/')
def index():
    return render_template_string("""
    <html>
      <head>
        <title>Smart Dustbin Map</title>
      </head>
      <body>
        <h2>Kolhapur Smart Dustbin - Live Map</h2>
        {{ map_html|safe }}
      </body>
    </html>
    """, map_html=generate_map_html())

if __name__ == "__main__":
    app.run(debug=True)
